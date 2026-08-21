"""Shared offline test doubles for the full case-lifecycle stack: health
engine (Phase 1) + gate (Phase 2) + RAG (Phase 3) + escalation (Phase 4).

Everything here is in-memory or a stub adapter — no Postgres, no network —
so the whole diagnose -> followup -> resolve loop can be exercised
end-to-end, deterministically, offline.
"""

import uuid

from app.adapters.stubs import StubStorageAdapter
from app.core.config import Settings
from app.domain.health.inputs import CropIdealConditions
from app.repositories.health_context import (
    FarmHealthContext,
    InMemoryFarmHealthContextReader,
    InMemoryTreatmentTrendReader,
)
from app.repositories.in_memory import InMemoryFarmRepository
from app.repositories.problem_registry import ProblemRegistry
from app.services.escalation.case_summary_service import CaseSummaryService
from app.services.escalation.escalation_service import EscalationService
from app.services.escalation.followup_service import FollowUpService
from app.services.escalation.resolve_service import ResolveService
from app.services.escalation.routing_service import RoutingService
from app.services.health_service import HealthService

FARM_ID = "f_1"

# Reproduces Phase 1's exact baseline fixture (score 82, no open problems).
IDEAL = CropIdealConditions(
    temp_min_c=25.0, temp_max_c=35.0, humidity_min_pct=60.0, humidity_max_pct=80.0, soil_moisture_min_pct=65.0
)


def baseline_context(**overrides) -> FarmHealthContext:
    base = dict(
        latitude=11.0,
        longitude=77.0,
        crop_ideal=IDEAL,
        soil_moisture_pct=55.0,
        irrigation_delivered_mm=24.0,
        irrigation_required_mm=40.0,
        days_since_planting=10,
        expected_stage_day=30,
        days_since_last_scan=2,
    )
    base.update(overrides)
    return FarmHealthContext(**base)


class FakeWeatherAdapter:
    """Settable weather so a test can walk through Phase 1's exact
    baseline -> diagnosed -> got_worse -> resolved humidity/temp sequence."""

    def __init__(self, temp_c: float = 30.0, relative_humidity_pct: float = 80.0) -> None:
        self.temp_c = temp_c
        self.relative_humidity_pct = relative_humidity_pct

    async def get_current_weather(self, latitude, longitude):
        return {"temperature_c": self.temp_c, "relative_humidity_pct": self.relative_humidity_pct}

    async def get_daily_et0(self, latitude, longitude, target_date):
        return 4.8

    async def get_forecast(self, latitude, longitude, days=7):
        return []


class FakeHealthSnapshotRepo:
    """In-memory stand-in for the SQLAlchemy-backed HealthSnapshotRepository
    (which requires a live Postgres session) — same async method surface."""

    def __init__(self) -> None:
        self._rows: list = []

    async def save(self, row):
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


class FakeEscalationCaseRepo:
    """In-memory stand-in for the SQLAlchemy-backed EscalationCaseRepository."""

    def __init__(self) -> None:
        self._rows: dict[str, _FakeCase] = {}
        self._order: list[str] = []

    async def create(self, farm_id, problem_id, reason, trigger, assigned_to, summary, status="open"):
        case_id = str(uuid.uuid4())
        row = _FakeCase(
            id=case_id,
            farm_id=farm_id,
            problem_id=problem_id,
            status=status,
            reason=reason,
            trigger=trigger,
            assigned_to=assigned_to,
            summary=summary,
        )
        self._rows[case_id] = row
        self._order.insert(0, case_id)
        return row

    async def get_by_id(self, case_id):
        return self._rows.get(case_id)

    async def update_summary(self, case_id, summary):
        row = self._rows.get(case_id)
        if row is not None:
            row.summary = summary
        return row

    async def list_queue(self, assigned_to=None, limit=20, cursor=None):
        rows = [self._rows[cid] for cid in self._order]
        if assigned_to:
            rows = [r for r in rows if r.assigned_to == assigned_to]
        return rows[:limit], None

    async def resolve(self, case_id, diagnosis, treatment, notes):
        row = self._rows.get(case_id)
        if row is None:
            return None
        row.status = "resolved"
        row.diagnosis = diagnosis
        row.treatment = treatment
        row.notes = notes
        return row

    async def update_assignment(self, case_id, assigned_to, status="assigned"):
        row = self._rows.get(case_id)
        if row is not None:
            row.assigned_to = assigned_to
            row.status = status
        return row


class _FakeCase:
    def __init__(self, id, farm_id, problem_id, status, reason, trigger, assigned_to, summary):
        self.id = id
        self.farm_id = farm_id
        self.problem_id = problem_id
        self.status = status
        self.reason = reason
        self.trigger = trigger
        self.assigned_to = assigned_to
        self.summary = summary
        self.diagnosis = None
        self.treatment = None
        self.notes = None


class Stack:
    """A fully-wired, offline case-lifecycle stack."""

    def __init__(self, farm_id: str = FARM_ID, context: FarmHealthContext | None = None) -> None:
        self.settings = Settings(CONFIDENCE_GATE=0.70, RAG_RELEVANCE_THRESHOLD=0.18, ROUTING_MODE="demo_fixed")

        self.problem_registry = ProblemRegistry()
        self.treatment_trend = InMemoryTreatmentTrendReader()
        self.context_reader = InMemoryFarmHealthContextReader()
        self.context_reader.set_context(farm_id, context or baseline_context())
        self.weather = FakeWeatherAdapter()
        self.snapshot_repo = FakeHealthSnapshotRepo()

        self.health_service = HealthService(
            snapshot_repo=self.snapshot_repo,
            context_reader=self.context_reader,
            problem_reader=self.problem_registry,
            treatment_reader=self.treatment_trend,
            weather_port=self.weather,
        )

        self.farm_repo = InMemoryFarmRepository()
        self.storage = StubStorageAdapter()
        self.case_repo = FakeEscalationCaseRepo()
        self.routing = RoutingService(agronomist_repo=None, settings=self.settings)  # demo_fixed never touches it
        self.case_summary_service = CaseSummaryService(
            farm_repo=self.farm_repo,
            problem_registry=self.problem_registry,
            health_service=self.health_service,
            storage_port=self.storage,
            treatment_trend_reader=self.treatment_trend,
        )
        self.escalation_service = EscalationService(
            case_repo=self.case_repo, routing=self.routing, case_summary=self.case_summary_service
        )
        self.followup_service = FollowUpService(
            problem_registry=self.problem_registry,
            health_service=self.health_service,
            treatment_trend_writer=self.treatment_trend,
            escalation_service=self.escalation_service,
        )
        self.resolve_service = ResolveService(
            case_repo=self.case_repo,
            problem_registry=self.problem_registry,
            health_service=self.health_service,
            treatment_trend_writer=self.treatment_trend,
            routing=self.routing,
        )
