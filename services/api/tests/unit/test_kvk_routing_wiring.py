"""Phase 2 wiring: next-available agronomist routing + queue position/ETA,
exercised through the real services with in-memory repositories (no DB
required).
"""

from datetime import datetime, timedelta

import pytest

from app.core.enums import CaseStatus, ProblemSeverity
from app.repositories.in_memory import InMemoryCaseRepository, InMemoryFarmRepository
from app.schemas.escalation import EscalationCreateRequest
from app.services.agronomist_service import AgronomistService
from app.services.escalation_service import EscalationService
from app.services.kvk_routing import route_to_next_available_agronomist

AGRONOMIST_A = "agronomist:a"
AGRONOMIST_B = "agronomist:b"
DEFAULT_AGRONOMIST = "agronomist:default"


class _TwoAgronomistRoster:
    async def list_agronomist_ids(self) -> list[str]:
        return [AGRONOMIST_A, AGRONOMIST_B]


class _EmptyRoster:
    async def list_agronomist_ids(self) -> list[str]:
        return []


class _FakeHealthSnapshot:
    def __init__(self, score: float | None) -> None:
        self.score = score


class _FakeHealthService:
    """Only ``get_latest`` is exercised by AgronomistService.get_queue()."""

    def __init__(self, scores: dict[str, float] | None = None) -> None:
        self._scores = scores or {}

    async def get_latest(self, farm_id: str) -> _FakeHealthSnapshot:
        return _FakeHealthSnapshot(self._scores.get(farm_id))


async def _farm(farm_repo: InMemoryFarmRepository, farm_id: str, **overrides) -> None:
    data = {
        "id": farm_id,
        "farmer_id": "u_1",
        "farm_name": "Test Farm",
        "village": "Test Village",
        "primary_crop": "samba_paddy",
        **overrides,
    }
    await farm_repo.save(data)


@pytest.mark.asyncio
async def test_routes_to_least_loaded_agronomist():
    case_repo = InMemoryCaseRepository()
    # A has 1 open case, B has 3 -> new case must go to A.
    await case_repo.save(
        {"farm_id": "f_a", "severity": "early", "status": "open", "assigned_to": AGRONOMIST_A}
    )
    for i in range(3):
        await case_repo.save(
            {"farm_id": f"f_b_{i}", "severity": "early", "status": "open", "assigned_to": AGRONOMIST_B}
        )

    result = await route_to_next_available_agronomist(
        case_repo, _TwoAgronomistRoster(), default_agronomist=DEFAULT_AGRONOMIST
    )
    assert result == AGRONOMIST_A


@pytest.mark.asyncio
async def test_ties_broken_deterministically_by_lexicographic_id():
    case_repo = InMemoryCaseRepository()  # no cases at all -> both at 0, tied

    result1 = await route_to_next_available_agronomist(
        case_repo, _TwoAgronomistRoster(), default_agronomist=DEFAULT_AGRONOMIST
    )
    result2 = await route_to_next_available_agronomist(
        case_repo, _TwoAgronomistRoster(), default_agronomist=DEFAULT_AGRONOMIST
    )
    assert result1 == result2 == AGRONOMIST_A  # "agronomist:a" < "agronomist:b"


@pytest.mark.asyncio
async def test_resolved_cases_dont_count_against_load():
    case_repo = InMemoryCaseRepository()
    for i in range(5):
        saved = await case_repo.save(
            {"farm_id": f"f_done_{i}", "severity": "early", "status": "open", "assigned_to": AGRONOMIST_A}
        )
        await case_repo.update_status(saved["id"], CaseStatus.RESOLVED.value)

    # A has 5 raw rows but zero open ones -> still picked over B (0 cases too, tie -> lexicographic).
    result = await route_to_next_available_agronomist(
        case_repo, _TwoAgronomistRoster(), default_agronomist=DEFAULT_AGRONOMIST
    )
    assert result == AGRONOMIST_A


@pytest.mark.asyncio
async def test_empty_roster_falls_back_to_default():
    case_repo = InMemoryCaseRepository()
    result = await route_to_next_available_agronomist(
        case_repo, _EmptyRoster(), default_agronomist=DEFAULT_AGRONOMIST
    )
    assert result == DEFAULT_AGRONOMIST


@pytest.mark.asyncio
async def test_escalation_service_end_to_end_routes_and_returns_queue_position():
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    await _farm(farm_repo, "f_1")

    service = EscalationService(case_repo, farm_repo, _TwoAgronomistRoster())
    response = await service.create_escalation(
        EscalationCreateRequest(farm_id="f_1", reason="farmer_requested", severity=ProblemSeverity.EARLY)
    )

    assert response.assigned_kvk_center == AGRONOMIST_A
    assert response.case_summary.escalated_to == AGRONOMIST_A
    assert response.queue_position == 1
    assert response.eta > datetime.utcnow()


@pytest.mark.asyncio
async def test_queue_position_1_indexed_and_contiguous_within_agronomist():
    case_repo = InMemoryCaseRepository()
    now = datetime.utcnow()
    case_ids = []
    for i in range(4):
        saved = await case_repo.save(
            {
                "farm_id": f"f_{i}",
                "severity": ProblemSeverity.EARLY.value,
                "status": CaseStatus.ESCALATED.value,
                "assigned_to": AGRONOMIST_A,
                "created_at": now + timedelta(minutes=i),
            }
        )
        case_ids.append(saved["id"])

    farm_repo = InMemoryFarmRepository()
    for i in range(4):
        await _farm(farm_repo, f"f_{i}")

    service = AgronomistService(case_repo, farm_repo, problem_writer=None, health_service=_FakeHealthService())
    queue = await service.get_queue()
    positions = sorted(item.queue_position for item in queue if item.escalation_id in case_ids)

    assert positions == [1, 2, 3, 4]


@pytest.mark.asyncio
async def test_queue_returns_real_health_score_and_eta_ordered_by_severity():
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
            "assigned_to": AGRONOMIST_A,
            "created_at": now - timedelta(minutes=10),
        }
    )
    severe = await case_repo.save(
        {
            "farm_id": "f_severe",
            "severity": ProblemSeverity.SEVERE.value,
            "status": CaseStatus.ESCALATED.value,
            "assigned_to": AGRONOMIST_A,
            "created_at": now,
        }
    )

    health_service = _FakeHealthService({"f_early": 74.0, "f_severe": 41.0})
    service = AgronomistService(case_repo, farm_repo, problem_writer=None, health_service=health_service)
    queue = await service.get_queue()
    by_id = {item.escalation_id: item for item in queue}

    # Severe jumps ahead of the earlier-created early-severity case.
    assert by_id[severe["id"]].queue_position == 1
    assert by_id[early["id"]].queue_position == 2
    assert by_id[severe["id"]].estimated_resolution_at < by_id[early["id"]].estimated_resolution_at

    # Real health scores, not the old hardcoded 0.0.
    assert by_id[early["id"]].health_score == 74.0
    assert by_id[severe["id"]].health_score == 41.0
