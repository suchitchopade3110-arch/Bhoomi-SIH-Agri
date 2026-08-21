"""Tests for EscalationService: every trigger yields a complete, non-empty
CaseSummary with every contract §2.13 field populated, and routing behaves
per PRD §5.11 (nearest available, OFFICER_UNAVAILABLE otherwise). All offline
and deterministic.
"""

import pytest

from app.core.config import Settings
from app.core.enums import CaseStatus, ProblemSeverity
from app.core.errors import OfficerUnavailableError
from app.domain.health.inputs import CropIdealConditions
from app.repositories.agronomist_repository import AgronomistRecord
from app.repositories.health_context import (
    FarmHealthContext,
    InMemoryFarmHealthContextReader,
    InMemoryProblemLoadReader,
    InMemoryTreatmentTrendReader,
)
from app.repositories.in_memory import InMemoryFarmRepository, InMemoryUserRepository
from app.services.health_service import HealthService
from tests.escalation._helpers import DEMO_AGRONOMIST, FakeAgronomistDirectory, build_escalation_service

FARM_ID = "f_1"

_IDEAL = CropIdealConditions(
    temp_min_c=25.0, temp_max_c=35.0, humidity_min_pct=60.0, humidity_max_pct=80.0, soil_moisture_min_pct=65.0
)


class _FakeWeatherAdapter:
    async def get_current_weather(self, latitude, longitude):
        return {"temperature_c": 30.0, "relative_humidity_pct": 80.0}

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


async def _setup(farm_repo=None, user_repo=None):
    farm_repo = farm_repo if farm_repo is not None else InMemoryFarmRepository()
    user_repo = user_repo if user_repo is not None else InMemoryUserRepository()
    problem_reader = InMemoryProblemLoadReader()
    treatment_reader = InMemoryTreatmentTrendReader()
    context_reader = InMemoryFarmHealthContextReader()
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
            days_since_last_scan=2,
        ),
    )
    health_service = HealthService(
        snapshot_repo=_FakeHealthSnapshotRepo(),
        context_reader=context_reader,
        problem_reader=problem_reader,
        treatment_reader=treatment_reader,
        weather_port=_FakeWeatherAdapter(),
    )
    return farm_repo, user_repo, problem_reader, treatment_reader, health_service


@pytest.mark.asyncio
async def test_create_escalation_yields_complete_non_empty_case_summary():
    farm_repo, user_repo, problem_reader, treatment_reader, health_service = await _setup()
    await user_repo.save({"id": "u_1", "full_name": "Murugan", "phone_number": "9000000000"})
    await farm_repo.save(
        {
            "id": FARM_ID,
            "farmer_id": "u_1",
            "village": "Thottipalayam",
            "district": "Madurai",
            "primary_crop": "Paddy",
            "growth_stage": "vegetative",
            "land_status": "verified",
        }
    )
    service = build_escalation_service(farm_repo, user_repo, health_service, problem_reader, treatment_reader)

    result = await service.create_escalation(
        farm_id=FARM_ID, trigger_type="below_confidence_gate", reason="confidence 0.41 < gate 0.70"
    )

    assert result.case_id
    assert result.status == CaseStatus.ESCALATED
    assert result.assigned_to == DEMO_AGRONOMIST.name
    assert result.assigned_kvk_center == DEMO_AGRONOMIST.kvk_center

    summary = result.case_summary
    assert summary.case_id == result.case_id
    assert summary.farm_id == FARM_ID
    assert summary.farmer_name == "Murugan"
    assert summary.village == "Thottipalayam"
    assert summary.district == "Madurai"
    assert summary.crop == "Paddy"
    assert summary.growth_stage == "vegetative"
    assert summary.health_score is not None
    assert summary.land_verified is True
    assert summary.problem_summary
    assert summary.severity == ProblemSeverity.EARLY
    assert summary.status == CaseStatus.ESCALATED
    assert summary.escalated_to == DEMO_AGRONOMIST.name
    assert summary.spoken_summary

    # Fetched back by id, it's the identical case summary.
    fetched = await service.get_case(result.case_id)
    assert fetched.case_id == result.case_id
    assert fetched.farmer_name == "Murugan"


@pytest.mark.asyncio
async def test_create_escalation_completes_even_with_no_farm_or_user_on_record():
    """Every trigger — including one for a farm/user this repository doesn't
    know about yet — still yields a complete, non-empty CaseSummary rather
    than failing (PRD's 'never fabricate, but never silently drop the case'
    balance: unknown fields fall back to explicit placeholders)."""
    farm_repo, user_repo, problem_reader, treatment_reader, health_service = await _setup()
    service = build_escalation_service(farm_repo, user_repo, health_service, problem_reader, treatment_reader)

    result = await service.create_escalation(farm_id=FARM_ID, trigger_type="no_relevant_source", reason="no source")

    summary = result.case_summary
    assert summary.case_id
    assert summary.farm_id == FARM_ID
    assert summary.farmer_name
    assert summary.village
    assert summary.district
    assert summary.crop
    assert summary.problem_summary
    assert summary.spoken_summary


@pytest.mark.asyncio
async def test_routing_directory_mode_falls_back_to_any_available_agronomist():
    farm_repo, user_repo, problem_reader, treatment_reader, health_service = await _setup()
    await farm_repo.save({"id": FARM_ID, "district": "Salem"})  # no agronomist seeded for Salem
    directory = FakeAgronomistDirectory(
        [AgronomistRecord(id="agro_2", name="Dr. Karthik Subramaniam", kvk_center="TNAU KVK - Erode", district="Erode")]
    )
    settings = Settings(AGRONOMIST_ROUTING_MODE="directory")
    service = build_escalation_service(
        farm_repo, user_repo, health_service, problem_reader, treatment_reader, settings=settings, directory=directory
    )

    result = await service.create_escalation(farm_id=FARM_ID, trigger_type="manual", reason="farmer requested")

    assert result.assigned_to == "Dr. Karthik Subramaniam"


@pytest.mark.asyncio
async def test_routing_directory_mode_raises_officer_unavailable_when_nobody_is_available():
    farm_repo, user_repo, problem_reader, treatment_reader, health_service = await _setup()
    directory = FakeAgronomistDirectory([])
    settings = Settings(AGRONOMIST_ROUTING_MODE="directory")
    service = build_escalation_service(
        farm_repo, user_repo, health_service, problem_reader, treatment_reader, settings=settings, directory=directory
    )

    with pytest.raises(OfficerUnavailableError) as exc_info:
        await service.create_escalation(farm_id=FARM_ID, trigger_type="manual", reason="farmer requested")
    assert exc_info.value.code == "OFFICER_UNAVAILABLE"
