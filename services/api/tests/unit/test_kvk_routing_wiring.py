"""Phase 2 wiring: next-available KVK routing + queue position/ETA, exercised
through the real services with in-memory repositories (no DB required).
"""

from datetime import datetime, timedelta

import pytest

from app.core.enums import CaseStatus, ProblemSeverity
from app.domain.kvk_directory import KVK_CENTERS
from app.repositories.in_memory import InMemoryCaseRepository, InMemoryFarmRepository
from app.schemas.escalation import EscalationCreateRequest
from app.services.agronomist_service import AgronomistService
from app.services.escalation_service import EscalationService
from app.services.kvk_routing import route_to_next_available_kvk

# A point near Erode — the nearest KVK center for this coordinate.
FARM_NEAR_ERODE = {"latitude": 11.40, "longitude": 77.70}
ERODE_CENTER_ID = KVK_CENTERS[0].center_id
ERODE_CAPACITY = KVK_CENTERS[0].capacity


async def _farm(farm_repo: InMemoryFarmRepository, farm_id: str, **overrides) -> None:
    data = {
        "id": farm_id,
        "farmer_id": "u_1",
        "farm_name": "Test Farm",
        "village": "Test Village",
        "primary_crop": "samba_paddy",
        **FARM_NEAR_ERODE,
        **overrides,
    }
    await farm_repo.save(data)


@pytest.mark.asyncio
async def test_new_case_routes_to_nearest_center_when_capacity_available():
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    await _farm(farm_repo, "f_1")

    service = EscalationService(case_repo, farm_repo)
    response = await service.create_escalation(
        EscalationCreateRequest(farm_id="f_1", reason="farmer_requested", severity=ProblemSeverity.EARLY)
    )

    assert response.assigned_kvk_center == ERODE_CENTER_ID
    assert response.case_summary.escalated_to == ERODE_CENTER_ID


@pytest.mark.asyncio
async def test_case_reroutes_once_nearest_center_hits_capacity():
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    for i in range(ERODE_CAPACITY):
        await _farm(farm_repo, f"f_fill_{i}")
        await case_repo.save(
            {
                "farm_id": f"f_fill_{i}",
                "severity": ProblemSeverity.EARLY.value,
                "status": CaseStatus.ESCALATED.value,
                "assigned_to": ERODE_CENTER_ID,
            }
        )

    await _farm(farm_repo, "f_overflow")
    service = EscalationService(case_repo, farm_repo)
    response = await service.create_escalation(
        EscalationCreateRequest(farm_id="f_overflow", reason="farmer_requested", severity=ProblemSeverity.EARLY)
    )

    assert response.assigned_kvk_center != ERODE_CENTER_ID


@pytest.mark.asyncio
async def test_resolved_cases_dont_count_against_capacity():
    case_repo = InMemoryCaseRepository()
    for i in range(ERODE_CAPACITY):
        saved = await case_repo.save(
            {
                "farm_id": f"f_done_{i}",
                "severity": ProblemSeverity.EARLY.value,
                "status": CaseStatus.ESCALATED.value,
                "assigned_to": ERODE_CENTER_ID,
            }
        )
        await case_repo.update_status(saved["id"], CaseStatus.RESOLVED.value)

    # Erode is nominally "full" by raw count, but every case is resolved —
    # a fresh case should still route there.
    center_id = await route_to_next_available_kvk(case_repo, *FARM_NEAR_ERODE.values())
    assert center_id == ERODE_CENTER_ID


@pytest.mark.asyncio
async def test_farm_without_coordinates_falls_back_to_default_center():
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    await farm_repo.save({"id": "f_no_coords", "farmer_id": "u_1", "farm_name": "No Coords Farm"})

    service = EscalationService(case_repo, farm_repo)
    response = await service.create_escalation(
        EscalationCreateRequest(farm_id="f_no_coords", reason="farmer_requested", severity=ProblemSeverity.EARLY)
    )

    assert response.assigned_kvk_center == ERODE_CENTER_ID  # DEFAULT_KVK_CENTER_ID fallback


@pytest.mark.asyncio
async def test_queue_returns_position_and_eta_ordered_by_severity():
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    await _farm(farm_repo, "f_early")
    await _farm(farm_repo, "f_severe")

    now = datetime.utcnow()
    early = await case_repo.save(
        {
            "farm_id": "f_early",
            "severity": ProblemSeverity.EARLY.value,
            "status": CaseStatus.ESCALATED.value,
            "assigned_to": ERODE_CENTER_ID,
            "created_at": now - timedelta(minutes=10),
        }
    )
    severe = await case_repo.save(
        {
            "farm_id": "f_severe",
            "severity": ProblemSeverity.SEVERE.value,
            "status": CaseStatus.ESCALATED.value,
            "assigned_to": ERODE_CENTER_ID,
            "created_at": now,
        }
    )

    service = AgronomistService(case_repo, farm_repo, problem_writer=None, health_service=None)
    queue = await service.get_queue()
    by_id = {item.escalation_id: item for item in queue}

    # Severe jumps ahead of the earlier-created early-severity case.
    assert by_id[severe["id"]].queue_position == 1
    assert by_id[early["id"]].queue_position == 2
    assert by_id[severe["id"]].estimated_resolution_at < by_id[early["id"]].estimated_resolution_at
