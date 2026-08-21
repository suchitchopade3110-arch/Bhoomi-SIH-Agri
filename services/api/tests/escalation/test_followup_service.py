"""Tests for FollowupService: closes the loop on POST
/followups/{problem_id}/respond (contract §2.12), reusing the Phase 1 health
engine unchanged. Reproduces PRD §7.4's own baseline(82) -> diagnosed(68) ->
got_worse(59) walk through real service calls, so the got_worse -> escalate
path is exercised against the exact fixture, not a synthetic one.
"""

import pytest

from app.core.enums import FollowupResponse, HealthBand, ProblemSeverity
from app.domain.health.inputs import CropIdealConditions
from app.repositories.health_context import (
    FarmHealthContext,
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
    OpenProblemRecord,
)
from app.repositories.in_memory import InMemoryFarmRepository, InMemoryUserRepository
from app.services.health_service import HealthService
from tests.escalation._helpers import build_escalation_service, build_followup_service

FARM_ID = "f_1"
PROBLEM_ID = "p_7"

_IDEAL = CropIdealConditions(
    temp_min_c=25.0, temp_max_c=35.0, humidity_min_pct=60.0, humidity_max_pct=80.0, soil_moisture_min_pct=65.0
)


class _FakeWeatherAdapter:
    """Mutable so the test can walk the PRD §7.4 fixture's weather changes
    between steps, same as the domain-level acceptance test does directly."""

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
async def test_got_worse_promotes_severity_recomputes_and_auto_escalates_with_case_id():
    farm_repo = InMemoryFarmRepository()
    user_repo = InMemoryUserRepository()
    await farm_repo.save({"id": FARM_ID, "district": "Madurai", "primary_crop": "Paddy"})

    problem_reader = InMemoryProblemLoadReader()
    treatment_reader = InMemoryTreatmentTrendReader()
    context_reader = InMemoryFarmHealthContextReader()
    weather = _FakeWeatherAdapter(temp_c=30.0, relative_humidity_pct=92.0)  # PRD §7.4's "diagnosed" reading

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
    # One open, EARLY-severity problem — PRD §7.4's "diagnosed" state (score 68, band watch).
    problem_reader.set_open_problems(FARM_ID, [OpenProblemRecord(problem_id=PROBLEM_ID, severity=ProblemSeverity.EARLY)])

    health_service = HealthService(
        snapshot_repo=_FakeHealthSnapshotRepo(),
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=treatment_reader,
        weather_port=weather,
    )
    baseline = await health_service.recompute(FARM_ID, reason="diagnosis")
    assert baseline.score == 68
    assert baseline.band == HealthBand.WATCH.value

    escalation_service = build_escalation_service(farm_repo, user_repo, health_service, problem_reader, treatment_reader)
    followup_service = build_followup_service(
        problem_reader, treatment_reader, context_reader, health_service, escalation_service
    )

    outcome = await followup_service.respond(problem_id=PROBLEM_ID, response=FollowupResponse.GOT_WORSE)

    # PRD §7.4's exact "got worse" number: severity promotes early -> moderate,
    # and the recomputed score crosses below Watch.
    assert outcome.health_to == 59
    assert outcome.health_band == HealthBand.POOR
    assert outcome.severity_from == ProblemSeverity.EARLY
    assert outcome.severity_to == ProblemSeverity.MODERATE
    assert outcome.escalated is True
    assert outcome.case_id is not None

    open_problems = await problem_reader.get_open_problems(FARM_ID)
    assert open_problems[0].severity == ProblemSeverity.MODERATE

    # The created case is real and fetchable.
    case_summary = await escalation_service.get_case(outcome.case_id)
    assert case_summary.case_id == outcome.case_id
    assert case_summary.problem.severity == ProblemSeverity.MODERATE


@pytest.mark.asyncio
async def test_improved_response_does_not_escalate():
    farm_repo = InMemoryFarmRepository()
    user_repo = InMemoryUserRepository()
    await farm_repo.save({"id": FARM_ID})

    problem_reader = InMemoryProblemLoadReader()
    treatment_reader = InMemoryTreatmentTrendReader()
    context_reader = InMemoryFarmHealthContextReader()
    context_reader.set_context(
        FARM_ID,
        FarmHealthContext(
            latitude=11.0,
            longitude=77.0,
            crop_ideal=_IDEAL,
            soil_moisture_pct=60.0,
            irrigation_delivered_mm=40.0,
            irrigation_required_mm=40.0,
            days_since_planting=30,
            expected_stage_day=30,
            days_since_last_scan=1,
        ),
    )
    problem_reader.set_open_problems(FARM_ID, [OpenProblemRecord(problem_id=PROBLEM_ID, severity=ProblemSeverity.EARLY)])

    health_service = HealthService(
        snapshot_repo=_FakeHealthSnapshotRepo(),
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=treatment_reader,
        weather_port=_FakeWeatherAdapter(temp_c=30.0, relative_humidity_pct=70.0),
    )
    escalation_service = build_escalation_service(farm_repo, user_repo, health_service, problem_reader, treatment_reader)
    followup_service = build_followup_service(
        problem_reader, treatment_reader, context_reader, health_service, escalation_service
    )

    outcome = await followup_service.respond(problem_id=PROBLEM_ID, response=FollowupResponse.IMPROVED)

    assert outcome.escalated is False
    assert outcome.case_id is None
    assert outcome.severity_from is None
    assert outcome.severity_to is None
    # Severity is untouched by a non-worsening response.
    open_problems = await problem_reader.get_open_problems(FARM_ID)
    assert open_problems[0].severity == ProblemSeverity.EARLY


@pytest.mark.asyncio
async def test_respond_to_unknown_problem_raises_not_found():
    from app.core.errors import NotFoundError

    farm_repo = InMemoryFarmRepository()
    user_repo = InMemoryUserRepository()
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
    escalation_service = build_escalation_service(farm_repo, user_repo, health_service, problem_reader, treatment_reader)
    followup_service = build_followup_service(
        problem_reader, treatment_reader, context_reader, health_service, escalation_service
    )

    with pytest.raises(NotFoundError):
        await followup_service.respond(problem_id="no_such_problem", response=FollowupResponse.NO_CHANGE)
