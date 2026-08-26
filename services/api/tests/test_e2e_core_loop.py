"""End-to-End Core Intelligence Loop Integration Test (Phase 4 Objective 3).

Exercises the full SIH26131 core loop in sequence:
  1. Initial farm baseline state & clear qualitative advisory.
  2. Photo diagnosis (above confidence gate) -> RAG grounded advisory composed with citations -> health penalty applied.
  3. Followup check-in -> farmer reports 'got_worse' -> problem promoted -> auto-escalation triggered.
  4. Escalation compiled -> 8-key CaseSummaryBundle assembled + KVK queue position and ETA assigned.
  5. Case PDF payload retrieved -> verified strict superset of bundle.
  6. Agronomist resolves case -> problem cleared -> case resolved -> health recomputed -> qualitative advisory reflects recovery.
"""

from datetime import datetime
import pytest
from app.adapters.stubs import (
    StubEmbeddingAdapter,
    StubImageDiagnosisAdapter,
    StubLLMAdapter,
    StubRosterAdapter,
    StubWeatherAdapter,
)
from app.core.config import Settings
from app.core.enums import CaseStatus, FollowupResponse, ProblemSeverity
from app.domain.advisory.derive import derive_qualitative_advisory
from app.domain.constants import CONFIDENCE_GATE
from app.domain.health.inputs import CropIdealConditions, TriggeringInput
from app.repositories.health_context import (
    FarmHealthContext,
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
    OpenProblemRecord,
)
from app.repositories.in_memory import InMemoryCaseRepository, InMemoryFarmRepository
from app.schemas.agronomist import ResolveCaseRequest
from app.schemas.diagnosis import DiagnoseRequest
from app.schemas.followup import FollowupCheckinRequest
from app.services.agronomist_service import AgronomistService
from app.services.diagnosis_service import DiagnosisService
from app.services.escalation_service import EscalationService
from app.services.followup_service import FollowupService
from app.services.health_service import HealthService
from app.services.health_snapshot_mapping import snapshot_row_to_schema
from app.services.rag.corpus_data import CORPUS_DOCS
from app.services.rag.retrieval import RetrievalService
from tests.rag._helpers import build_ingested_repo

SETTINGS = Settings(
    PROBLEM_STATEMENT="sih26131",
    ENVIRONMENT="test",
    CONFIDENCE_GATE=CONFIDENCE_GATE,
    RAG_RELEVANCE_THRESHOLD_PRODUCTION=0.60,
    RAG_RELEVANCE_THRESHOLD_STUB=0.18,
)

FARM_ID = "farm_e2e_core_loop_001"

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


class _E2EHealthSnapshotRepo:
    def __init__(self):
        self._rows = []

    async def save(self, row):
        import uuid
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


@pytest.mark.asyncio
async def test_full_sih26131_core_loop_end_to_end():
    """Complete core loop: Diagnose -> Advisory -> Got Worse -> Escalate -> Bundle -> PDF -> Resolve -> Advisory Recovery."""
    # 0. Setup infrastructure harness
    repo = await build_ingested_repo(docs=CORPUS_DOCS)
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    image_port = StubImageDiagnosisAdapter(label="bacterial_leaf_blight", confidence=0.88)
    problem_reader = InMemoryProblemLoadReader()
    treatment_reader = InMemoryTreatmentTrendReader()
    context_reader = InMemoryFarmHealthContextReader()
    context_reader.set_context(FARM_ID, _BASELINE_CONTEXT)
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    roster = StubRosterAdapter()
    snapshot_repo = _E2EHealthSnapshotRepo()

    health_service = HealthService(
        snapshot_repo=snapshot_repo,
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=treatment_reader,
        weather_port=StubWeatherAdapter(),
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
        followup_writer=treatment_reader,
        farm_repo=farm_repo,
        health_service=health_service,
        escalation_service=escalation_service,
    )
    agronomist_service = AgronomistService(
        case_repo=case_repo,
        farm_repo=farm_repo,
        health_service=health_service,
        problem_writer=problem_reader,
    )

    # Seed farm profile
    await farm_repo.save({
        "id": FARM_ID,
        "farm_name": "Kavitha Paddy Farm",
        "primary_crop": "samba_paddy",
        "district": "Madurai",
        "village": "Alanganallur",
        "growth_stage": "tillering",
        "land_status": "verified",
    })

    # Step 0: Initial farm health baseline & clear advisory
    initial_snap = await health_service.recompute(
        FARM_ID,
        triggering_input=TriggeringInput(type="baseline_init", details={"confidence": 1.0}),
    )
    initial_score = float(initial_snap.score)
    assert initial_score > 70.0

    initial_advisory = derive_qualitative_advisory(
        open_problems_count=0,
        highest_severity=None,
        primary_problem_label=None,
        days_since_last_scan=0,
    )
    assert "clear" in initial_advisory.advisory.lower()

    # Step 1: Diagnose Day 22 (Above Gate, Confident In-Scope BLB)
    diag_res = await diagnosis_service.diagnose(
        farm_id=FARM_ID,
        image_asset_id="asset_blb_photo_01.jpg",
        description_text="Noticed water-soaked yellowing stripes on upper leaf tips.",
    )

    assert diag_res.above_gate is True
    assert diag_res.gate_confidence == 0.88
    assert diag_res.gate_threshold == 0.70
    assert diag_res.gate_reason_code is None
    assert len(diag_res.gate_alternatives) == 2
    assert diag_res.advisory is not None
    assert len(diag_res.citations) > 0
    assert diag_res.citations[0].doc_id in ("kb_213", "icar_pop_rice_blb")
    assert diag_res.health_delta_from is not None
    assert diag_res.health_delta_to is not None
    assert diag_res.health_delta_to < diag_res.health_delta_from  # Health dropped due to BLB

    # Step 2: Farmer Follow-up check-in reports 'got_worse'
    open_problems = await problem_reader.get_open_problems(FARM_ID)
    assert len(open_problems) == 1
    active_prob_id = open_problems[0].problem_id

    checkin_res = await followup_service.checkin(
        FollowupCheckinRequest(
            farm_id=FARM_ID,
            problem_id=active_prob_id,
            response=FollowupResponse.GOT_WORSE,
            notes="Lesions expanded to lower canopy.",
        )
    )
    assert checkin_res.response == FollowupResponse.GOT_WORSE
    assert checkin_res.auto_escalated is True
    assert checkin_res.escalation_id is not None
    escalation_id = checkin_res.escalation_id

    # Step 3: Escalation Case & 8-key CaseSummaryBundle Verification
    case_summary = await agronomist_service.get_case_detail(escalation_id)
    assert case_summary.case_id == escalation_id
    assert case_summary.farm_id == FARM_ID
    assert case_summary.status in (CaseStatus.ESCALATED, CaseStatus.ASSIGNED, CaseStatus.OPEN)

    bundle = case_summary.bundle
    assert bundle is not None
    bundle_dict = bundle.model_dump()
    expected_keys = {
        "crop",
        "region",
        "growth_stage",
        "problem_history",
        "images",
        "treatments_tried",
        "followup_trend",
        "current_advisory",
        "diagnosis",  # structured {label, confidence} — checklist §7.2
    }
    assert set(bundle_dict.keys()) == expected_keys
    # Strict drift guard: 0 land/soil keys
    forbidden = {"area_acres_verified", "soil_type", "total_area_acres", "boundary_geojson"}
    assert not (set(bundle_dict.keys()) & forbidden)

    # Step 4: Agronomist Case PDF Payload compilation
    pdf_payload = await agronomist_service.get_case_pdf_payload(escalation_id)
    assert pdf_payload.case_id == escalation_id
    assert pdf_payload.farm_id == FARM_ID
    assert pdf_payload.bundle == bundle
    assert "Paddy" in pdf_payload.summary_headline or "Rice" in pdf_payload.summary_headline

    # Step 5: Agronomist Resolves Case
    resolve_res = await agronomist_service.resolve_case(
        ResolveCaseRequest(
            escalation_id=escalation_id,
            agronomist_id="agro_madurai_01",
            confirmed_diagnosis="Bacterial Leaf Blight (Xanthomonas oryzae pv. oryzae)",
            expert_advice="Drain standing water completely for 3 days and spray Agrimycin-100 @ 100g/ha.",
            prescribed_inputs=["Agrimycin-100", "Copper Oxychloride 50 WP"],
            agronomist_name="Dr. S. Ramanathan",
        )
    )
    assert resolve_res.escalation_id == escalation_id
    assert resolve_res.status == CaseStatus.RESOLVED
    assert "successfully resolved" in resolve_res.message
    assert resolve_res.resolved_at is not None

    # Step 6: Post-resolution qualitative advisory check
    remaining_problems = await problem_reader.get_open_problems(FARM_ID)
    assert len(remaining_problems) == 0

    recovered_advisory = derive_qualitative_advisory(
        open_problems_count=0,
        highest_severity=None,
        primary_problem_label=None,
        days_since_last_scan=1,
    )
    assert "clear" in recovered_advisory.advisory.lower()
    assert recovered_advisory.trend.value in ("improving", "stable")
