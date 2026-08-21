"""Tests for ResolveService: POST /cases/{case_id}/resolve (contract §2.13)
lifts the score above baseline by reusing the Phase 1 engine unchanged.
Continues PRD §7.4's fixture from the "got worse" state (59, poor) through
resolution to exactly 86, good — the same number the domain-level
acceptance test (tests/domain/test_health_score.py) reaches directly.
"""

import pytest

from app.core.enums import CaseStatus, FollowupResponse, HealthBand, ProblemSeverity
from app.domain.health.inputs import CropIdealConditions
from app.repositories.health_context import (
    FarmHealthContext,
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
    OpenProblemRecord,
    TreatmentTrend,
)
from app.repositories.in_memory import InMemoryFarmRepository, InMemoryUserRepository
from app.services.health_service import HealthService
from tests.escalation._helpers import FakeCaseRepository, build_escalation_service, build_resolve_service

FARM_ID = "f_1"
PROBLEM_ID = "p_7"

_IDEAL = CropIdealConditions(
    temp_min_c=25.0, temp_max_c=35.0, humidity_min_pct=60.0, humidity_max_pct=80.0, soil_moisture_min_pct=65.0
)


class _FakeWeatherAdapter:
    def __init__(self, temp_c: float, relative_humidity_pct: float) -> None:
        self.temp_c = temp_c
        self.relative_humidity_pct = relative_humidity_pct

    async def get_current_weather(self, latitude, longitude):
        return {"temperature_c": self.temp_c, "relative_humidity_pct": self.relative_humidity_pct}

    async def get_daily_et0(self, latitude, longitude, target_date):
        return 4.8

    async def get_forecast(self, latitude, longitude, days=7):
        return []


class _FakeHealthSnapshotRepo:
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


@pytest.mark.asyncio
async def test_resolve_lifts_score_to_86_above_baseline_reusing_phase1_engine():
    farm_repo = InMemoryFarmRepository()
    user_repo = InMemoryUserRepository()
    await farm_repo.save({"id": FARM_ID})

    problem_reader = InMemoryProblemLoadReader()
    treatment_reader = InMemoryTreatmentTrendReader()
    context_reader = InMemoryFarmHealthContextReader()
    weather = _FakeWeatherAdapter(temp_c=30.0, relative_humidity_pct=92.0)  # PRD §7.4's "worse" reading

    # PRD §7.4's exact "got worse" (59, poor) state, seeded directly so this
    # test isolates the resolve step (the got_worse -> escalate step is
    # covered by test_followup_service.py).
    context_reader.set_context(
        FARM_ID,
        FarmHealthContext(
            latitude=11.0,
            longitude=77.0,
            crop_ideal=_IDEAL,
            soil_moisture_pct=55.0,
            irrigation_delivered_mm=24.0,
            irrigation_required_mm=40.0,
            days_since_planting=10,
            expected_stage_day=30,
            days_since_last_scan=6,
        ),
    )
    problem_reader.set_open_problems(FARM_ID, [OpenProblemRecord(problem_id=PROBLEM_ID, severity=ProblemSeverity.MODERATE)])
    treatment_reader.set_trend(
        FARM_ID,
        TreatmentTrend(
            latest_followup_response=FollowupResponse.GOT_WORSE,
            consecutive_got_worse_count=1,
            problem_resolved_with_confirmed_treatment=False,
        ),
    )

    health_service = HealthService(
        snapshot_repo=_FakeHealthSnapshotRepo(),
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=treatment_reader,
        weather_port=weather,
    )
    worse = await health_service.recompute(FARM_ID, reason="followup")
    assert worse.score == 59
    assert worse.band == HealthBand.POOR.value

    case_repo = FakeCaseRepository()
    escalation_service = build_escalation_service(
        farm_repo, user_repo, health_service, problem_reader, treatment_reader, case_repo=case_repo
    )
    created = await escalation_service.create_escalation(
        farm_id=FARM_ID,
        trigger_type="got_worse_followup",
        reason="follow-up got worse",
        severity=ProblemSeverity.MODERATE,
        problem_id=PROBLEM_ID,
    )

    # Conditions at the moment of the agronomist's visit — PRD §7.4's
    # "resolved" reading (weather/soil improve alongside the treatment;
    # ResolveService itself only clears the problem, confirms treatment, and
    # touches monitoring recency — see resolve_service.py's docstring).
    weather.temp_c, weather.relative_humidity_pct = 30.0, 80.0
    context_reader.set_context(
        FARM_ID,
        FarmHealthContext(
            latitude=11.0,
            longitude=77.0,
            crop_ideal=_IDEAL,
            soil_moisture_pct=60.0,
            irrigation_delivered_mm=24.0,
            irrigation_required_mm=40.0,
            days_since_planting=10,
            expected_stage_day=30,
            days_since_last_scan=6,  # ResolveService resets this to 0 itself
        ),
    )

    resolve_service = build_resolve_service(case_repo, problem_reader, treatment_reader, context_reader, health_service)
    resolution = await resolve_service.resolve(
        case_id=created.case_id,
        diagnosis="Bacterial leaf blight, moderate — confirmed and treated",
        treatment="Apply recommended bactericide; drain standing water.",
        notes="Recheck in 5 days.",
    )

    assert resolution.status == CaseStatus.RESOLVED
    assert resolution.problem_status.value == "resolved"
    assert resolution.health_to == 86
    assert resolution.health_band == HealthBand.GOOD
    assert resolution.health_from == worse.score
    assert resolution.health_to > 82  # above the original baseline (PRD §7.4)

    # The problem is cleared, the trend is a confirmed resolution, and
    # monitoring recency was touched — active_problem_load is back to 100.
    assert await problem_reader.get_open_problems(FARM_ID) == []
    trend = await treatment_reader.get_treatment_trend(FARM_ID)
    assert trend.problem_resolved_with_confirmed_treatment is True

    case = await case_repo.get_by_id(created.case_id)
    assert case.status == CaseStatus.RESOLVED.value
    assert case.resolution["diagnosis"].startswith("Bacterial leaf blight")


@pytest.mark.asyncio
async def test_resolve_unknown_case_raises_not_found():
    from app.core.errors import NotFoundError

    problem_reader = InMemoryProblemLoadReader()
    treatment_reader = InMemoryTreatmentTrendReader()
    context_reader = InMemoryFarmHealthContextReader()
    health_service = HealthService(
        snapshot_repo=_FakeHealthSnapshotRepo(),
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=treatment_reader,
        weather_port=_FakeWeatherAdapter(temp_c=30.0, relative_humidity_pct=70.0),
    )
    resolve_service = build_resolve_service(
        FakeCaseRepository(), problem_reader, treatment_reader, context_reader, health_service
    )

    with pytest.raises(NotFoundError):
        await resolve_service.resolve(case_id="no_such_case", diagnosis="x", treatment="y")
