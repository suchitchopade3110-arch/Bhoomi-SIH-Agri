"""Tests for Escalation Triggers and Case Resolution (Phase 3 Objective 2).

Verifies:
  1. Trigger: Below-confidence-gate diagnosis auto-escalates to CaseRepository.
  2. Trigger: Out-of-scope diagnosis label auto-escalates to CaseRepository.
  3. Trigger: Followup 'got_worse' response past threshold auto-escalates to CaseRepository.
  4. Trigger: No-retrieval on diagnosis (empty corpus / low relevance) auto-escalates to CaseRepository.
  5. Resolve Path: Resolving a case clears the problem and updates qualitative advisory to reflect resolution.
"""

import pytest
from app.adapters.stubs import (
    StubEmbeddingAdapter,
    StubImageDiagnosisAdapter,
    StubLLMAdapter,
    StubRosterAdapter,
)
from app.core.config import Settings
from app.core.enums import CaseStatus, FollowupResponse, ProblemSeverity
from app.domain.advisory.derive import derive_qualitative_advisory, AdvisoryTrend
from app.domain.health.inputs import CropIdealConditions
from app.repositories.health_context import (
    FarmHealthContext,
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
    OpenProblemRecord,
)
from app.repositories.in_memory import InMemoryCaseRepository, InMemoryFarmRepository
from app.schemas.agronomist import ResolveCaseRequest
from app.schemas.followup import FollowupCheckinRequest
from app.services.agronomist_service import AgronomistService
from app.services.diagnosis_service import DiagnosisService
from app.services.escalation_service import EscalationService
from app.services.followup_service import FollowupService
from app.services.health_service import HealthService
from app.services.rag.retrieval import RetrievalService
from tests.rag._helpers import build_ingested_repo

SETTINGS = Settings(CONFIDENCE_GATE=0.70, EMBEDDING_PROVIDER="stub")
FARM_ID = "farm_esc_test_1"

_IDEAL = CropIdealConditions(
    temp_min_c=25.0, temp_max_c=35.0, humidity_min_pct=60.0, humidity_max_pct=80.0, soil_moisture_min_pct=65.0
)
_BASELINE_CONTEXT = FarmHealthContext(
    latitude=11.0,
    longitude=77.0,
    crop_ideal=_IDEAL,
    soil_moisture_pct=55.0,
    irrigation_delivered_mm=32.0,
    irrigation_required_mm=40.0,
    days_since_planting=20,
    expected_stage_day=30,
    days_since_last_scan=3,
)


class _FakeWeatherAdapter:
    async def get_current_weather(self, lat, lon):
        return {"temperature_c": 30.0, "relative_humidity_pct": 80.0}

    async def get_daily_et0(self, lat, lon, target_date):
        return 4.8

    async def get_forecast(self, lat, lon, days=7):
        return []


class _FakeHealthSnapshotRepo:
    def __init__(self):
        self._rows = []

    async def save(self, row):
        import uuid
        from datetime import datetime
        row.id = row.id or str(uuid.uuid4())
        if not getattr(row, "computed_at", None):
            row.computed_at = datetime.utcnow()
        self._rows.append(row)
        return row

    async def get_latest(self, farm_id: str):
        for r in reversed(self._rows):
            if r.farm_id == farm_id:
                return r
        return None

    async def get_history(self, farm_id: str, limit: int, cursor=None):
        return [r for r in reversed(self._rows) if r.farm_id == farm_id][:limit], None


async def _setup_harness(image_label="bacterial_leaf_blight", image_confidence=0.85, empty_corpus=False):
    repo = await build_ingested_repo(docs=[]) if empty_corpus else await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    image_port = StubImageDiagnosisAdapter(label=image_label, confidence=image_confidence)
    problem_reader = InMemoryProblemLoadReader()
    followup_writer = InMemoryTreatmentTrendReader()
    context_reader = InMemoryFarmHealthContextReader()
    context_reader.set_context(FARM_ID, _BASELINE_CONTEXT)
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    await farm_repo.save({
        "id": FARM_ID,
        "farm_name": "Kavitha Farm",
        "primary_crop": "Rice",
        "district": "Madurai",
        "village": "Alanganallur",
        "growth_stage": "tillering",
        "land_status": "verified",
    })
    roster = StubRosterAdapter()

    health_service = HealthService(
        snapshot_repo=_FakeHealthSnapshotRepo(),
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=followup_writer,
        weather_port=_FakeWeatherAdapter(),
    )
    escalation_service = EscalationService(case_repo, farm_repo, roster)
    diagnosis_service = DiagnosisService(
        image_port=image_port,
        retrieval=retrieval,
        llm_port=StubLLMAdapter(),
        health_service=health_service,
        problem_writer=problem_reader,
        case_repo=case_repo,
        farm_repo=farm_repo,
        settings=SETTINGS,
        roster=roster,
    )
    followup_service = FollowupService(
        problem_writer=problem_reader,
        followup_writer=followup_writer,
        farm_repo=farm_repo,
        health_service=health_service,
        escalation_service=escalation_service,
    )
    agronomist_service = AgronomistService(
        case_repo=case_repo,
        farm_repo=farm_repo,
        problem_writer=problem_reader,
        health_service=health_service,
    )
    return {
        "diagnosis_service": diagnosis_service,
        "followup_service": followup_service,
        "escalation_service": escalation_service,
        "agronomist_service": agronomist_service,
        "case_repo": case_repo,
        "problem_reader": problem_reader,
        "farm_repo": farm_repo,
    }


@pytest.mark.asyncio
async def test_trigger_1_below_confidence_gate_creates_case():
    """Trigger 1: Below confidence gate produces an escalation case."""
    harness = await _setup_harness(image_confidence=0.15)
    diag = harness["diagnosis_service"]
    case_repo = harness["case_repo"]

    outcome = await diag.diagnose(FARM_ID, "img_low_conf")
    assert outcome.above_gate is False
    assert outcome.escalation is not None
    assert outcome.escalation.case_id

    # Verify persisted in case repository
    saved_case = await case_repo.get_by_id(outcome.escalation.case_id)
    assert saved_case is not None
    assert saved_case["farm_id"] == FARM_ID
    assert "0.15" in saved_case["reason"]


@pytest.mark.asyncio
async def test_trigger_2_out_of_scope_label_creates_case():
    """Trigger 2: Out of scope crop/disease produces an escalation case."""
    harness = await _setup_harness(image_label="tomato_yellow_leaf_curl", image_confidence=0.98)
    diag = harness["diagnosis_service"]
    case_repo = harness["case_repo"]

    outcome = await diag.diagnose(FARM_ID, "img_oos")
    assert outcome.above_gate is False
    assert outcome.escalation is not None

    saved_case = await case_repo.get_by_id(outcome.escalation.case_id)
    assert saved_case is not None
    assert "supported set" in saved_case["reason"]


@pytest.mark.asyncio
async def test_trigger_3_got_worse_followup_creates_case():
    """Trigger 3: Followup 'got_worse' response promotes severity and produces escalation case."""
    harness = await _setup_harness()
    problem_reader = harness["problem_reader"]
    followup_service = harness["followup_service"]
    case_repo = harness["case_repo"]

    # Register an open early problem
    prob_id = "prob_blb_001"
    await problem_reader.add_open_problem(
        FARM_ID, OpenProblemRecord(problem_id=prob_id, severity=ProblemSeverity.EARLY, label="bacterial_leaf_blight")
    )

    # Farmer check-in: got worse
    checkin_res = await followup_service.checkin(
        FollowupCheckinRequest(farm_id=FARM_ID, problem_id=prob_id, response=FollowupResponse.GOT_WORSE)
    )

    assert checkin_res.auto_escalated is True
    assert checkin_res.escalation_id is not None

    saved_case = await case_repo.get_by_id(checkin_res.escalation_id)
    assert saved_case is not None
    assert saved_case["severity"] == ProblemSeverity.MODERATE.value
    assert "got worse" in saved_case["reason"]


@pytest.mark.asyncio
async def test_trigger_4_no_retrieval_creates_case():
    """Trigger 4: No retrieval above threshold produces an escalation case without LLM fabrication."""
    harness = await _setup_harness(empty_corpus=True)
    diag = harness["diagnosis_service"]
    case_repo = harness["case_repo"]

    outcome = await diag.diagnose(FARM_ID, "img_no_rag")
    assert outcome.above_gate is False
    assert outcome.advisory is None
    assert outcome.escalation is not None

    saved_case = await case_repo.get_by_id(outcome.escalation.case_id)
    assert saved_case is not None


@pytest.mark.asyncio
async def test_case_resolution_clears_problem_and_updates_qualitative_advisory():
    """Case resolution path: clears problem, marks case resolved, and qualitative advisory reflects recovery."""
    harness = await _setup_harness()
    agronomist_service = harness["agronomist_service"]
    problem_reader = harness["problem_reader"]
    case_repo = harness["case_repo"]

    prob_id = "prob_to_resolve_100"
    await problem_reader.add_open_problem(
        FARM_ID, OpenProblemRecord(problem_id=prob_id, severity=ProblemSeverity.MODERATE, label="bacterial_leaf_blight")
    )

    # Escalated case in repo
    saved = await case_repo.save({
        "farm_id": FARM_ID,
        "problem_id": prob_id,
        "reason": "Farmer reported worsening symptoms",
        "severity": ProblemSeverity.MODERATE.value,
        "status": CaseStatus.ESCALATED.value,
        "assigned_to": "TNAU KVK - Madurai",
    })
    case_id = saved["id"]

    # Before resolution: open problem exists -> qualitative advisory reflects active problem
    before_advisory = derive_qualitative_advisory(
        open_problems_count=1,
        highest_severity="moderate",
        primary_problem_label="bacterial_leaf_blight",
        days_since_last_scan=2,
    )
    assert before_advisory.trend in (AdvisoryTrend.STABLE, AdvisoryTrend.WORSENING)

    # Agronomist resolves case
    resolve_res = await agronomist_service.resolve_case(
        ResolveCaseRequest(
            escalation_id=case_id,
            agronomist_id="agr_001",
            confirmed_diagnosis="Bacterial Leaf Blight (confirmed)",
            expert_advice="Drain excess field water and spray Agrimycin-100 at 100g/ha.",
            prescribed_inputs=["Agrimycin-100", "Copper Oxychloride 50 WP"],
            agronomist_name="Dr. S. Ramanathan",
        )
    )
    assert resolve_res.status == CaseStatus.RESOLVED

    # Problem is now resolved in repository
    open_problems = await problem_reader.get_open_problems(FARM_ID)
    assert len(open_problems) == 0

    # Qualitative advisory now reflects clear condition
    after_advisory = derive_qualitative_advisory(
        open_problems_count=0,
        days_since_last_scan=2,
        latest_followup_response=None,
    )
    assert "clear" in after_advisory.advisory.lower()
    assert after_advisory.trend == AdvisoryTrend.STABLE
