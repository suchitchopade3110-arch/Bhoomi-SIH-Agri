"""Tests for DiagnosisService — POST /farms/{id}/diagnose's orchestration
(contract §2.10): image confidence + retrieval combined into the gate, then
compose (with health_delta) or escalate. All offline and deterministic.
"""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter, StubImageDiagnosisAdapter, StubLLMAdapter
from app.core.config import Settings
from app.domain.health.inputs import CropIdealConditions
from app.repositories.health_context import (
    FarmHealthContext,
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
)
from app.repositories.in_memory import InMemoryCaseRepository, InMemoryFarmRepository
from app.services.diagnosis_service import DiagnosisService
from app.services.health_service import HealthService
from app.services.rag.retrieval import RetrievalService
from tests.rag._helpers import build_ingested_repo

SETTINGS = Settings(CONFIDENCE_GATE=0.70, RAG_RELEVANCE_THRESHOLD=0.18)

FARM_ID = "f_1"

# Reproduces Phase 1's baseline fixture (score 82, no open problems) so
# health_delta has a real, non-trivial before/after to assert on.
_IDEAL = CropIdealConditions(
    temp_min_c=25.0, temp_max_c=35.0, humidity_min_pct=60.0, humidity_max_pct=80.0, soil_moisture_min_pct=65.0
)
_BASELINE_CONTEXT = FarmHealthContext(
    latitude=11.0,
    longitude=77.0,
    crop_ideal=_IDEAL,
    soil_moisture_pct=53.0,
    irrigation_delivered_mm=32.0,
    irrigation_required_mm=40.0,
    days_since_planting=17,
    expected_stage_day=30,
    days_since_last_scan=6,
)


class _FakeWeatherAdapter:
    """Matches the fixture's baseline WeatherReading via WeatherPort.get_current_weather."""

    async def get_current_weather(self, latitude, longitude):
        return {"temperature_c": 30.0, "relative_humidity_pct": 80.0}

    async def get_daily_et0(self, latitude, longitude, target_date):
        return 4.8

    async def get_forecast(self, latitude, longitude, days=7):
        return []


class _FakeHealthSnapshotRepo:
    """In-memory stand-in for the SQLAlchemy-backed HealthSnapshotRepository
    (which requires a live Postgres session) — same async method surface."""

    def __init__(self) -> None:
        self._rows: list = []

    async def save(self, row):
        import uuid

        row.id = row.id or str(uuid.uuid4())
        self._rows.append(row)
        return row

    async def get_latest(self, farm_id: str):
        for row in reversed(self._rows):
            if row.farm_id == farm_id:
                return row
        return None

    async def get_history(self, farm_id: str, limit: int, cursor=None):
        rows = [r for r in reversed(self._rows) if r.farm_id == farm_id]
        return rows[:limit], None


def _make_health_service(problem_reader: InMemoryProblemLoadReader) -> HealthService:
    context_reader = InMemoryFarmHealthContextReader()
    context_reader.set_context(FARM_ID, _BASELINE_CONTEXT)
    return HealthService(
        snapshot_repo=_FakeHealthSnapshotRepo(),
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=InMemoryTreatmentTrendReader(),
        weather_port=_FakeWeatherAdapter(),
    )


async def _make_service(image_confidence: float = 0.87, image_label: str = "bacterial_leaf_blight", repo=None):
    repo = repo if repo is not None else await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    image_port = StubImageDiagnosisAdapter(label=image_label, confidence=image_confidence)
    problem_reader = InMemoryProblemLoadReader()
    health_service = _make_health_service(problem_reader)
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    await farm_repo.save({"id": FARM_ID, "farmer_id": "u_1", "soil_moisture_pct": 55.0})
    return DiagnosisService(
        image_port=image_port,
        retrieval=retrieval,
        llm_port=StubLLMAdapter(),
        health_service=health_service,
        problem_writer=problem_reader,
        case_repo=case_repo,
        farm_repo=farm_repo,
        settings=SETTINGS,
    )


@pytest.mark.asyncio
async def test_above_gate_composes_advisory_with_citation_and_health_delta():
    service = await _make_service(image_confidence=0.87, image_label="bacterial_leaf_blight")
    outcome = await service.diagnose(FARM_ID, "a_9", description_text="yellow water soaked lesions")

    assert outcome.above_gate is True
    assert outcome.reason is None
    assert outcome.escalation is None
    assert outcome.problem_id is not None
    assert outcome.label == "bacterial_leaf_blight"
    assert outcome.stage == "early"
    assert outcome.advisory is not None
    assert len(outcome.citations) >= 1
    assert outcome.health_delta_from == 82  # the baseline fixture's known score
    assert outcome.health_delta_to is not None
    assert outcome.health_delta_to < outcome.health_delta_from  # a new problem must lower the score


@pytest.mark.asyncio
async def test_below_image_confidence_escalates_without_advisory_or_problem():
    service = await _make_service(image_confidence=0.10, image_label="bacterial_leaf_blight")
    outcome = await service.diagnose(FARM_ID, "a_9")

    assert outcome.above_gate is False
    assert outcome.advisory is None
    assert outcome.citations == []
    assert outcome.problem_id is None
    assert outcome.health_delta_from is None
    assert outcome.health_delta_to is None
    assert "0.10" in outcome.reason
    assert outcome.escalation is not None
    assert outcome.escalation.case_id
    assert outcome.escalation.assigned_to


@pytest.mark.asyncio
async def test_out_of_scope_label_escalates_even_with_high_confidence():
    service = await _make_service(image_confidence=0.99, image_label="tomato_yellow_leaf_curl")
    outcome = await service.diagnose(FARM_ID, "a_9")

    assert outcome.above_gate is False
    assert outcome.advisory is None
    assert "supported set" in outcome.reason


@pytest.mark.asyncio
async def test_empty_corpus_escalates_even_with_confident_in_scope_diagnosis():
    empty_repo = await build_ingested_repo(docs=[])
    service = await _make_service(image_confidence=0.95, image_label="bacterial_leaf_blight", repo=empty_repo)
    outcome = await service.diagnose(FARM_ID, "a_9")

    assert outcome.above_gate is False
    assert outcome.advisory is None
    assert outcome.citations == []


@pytest.mark.asyncio
async def test_escalation_never_carries_advisory_and_compose_never_carries_reason():
    """Structural invariant: exactly one branch populated, never a mix."""
    composed = await (await _make_service(image_confidence=0.90)).diagnose(FARM_ID, "a_9")
    assert composed.above_gate and composed.advisory is not None and composed.reason is None and composed.escalation is None

    escalated = await (await _make_service(image_confidence=0.10)).diagnose(FARM_ID, "a_9")
    assert not escalated.above_gate and escalated.advisory is None and escalated.reason is not None and escalated.escalation is not None
