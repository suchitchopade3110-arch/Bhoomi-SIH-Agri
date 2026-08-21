"""Tests for RoutingService — the demo_fixed/real routing modes (execution
plan item 3): "assign to nearest available agronomist; if none,
OFFICER_UNAVAILABLE -> next available."
"""

import pytest

from app.core.config import Settings
from app.core.errors import OfficerUnavailableError
from app.domain.escalation import AgronomistCandidate
from app.services.escalation.routing_service import RoutingService


class _FakeAgronomistRepo:
    def __init__(self, candidates: list[AgronomistCandidate]) -> None:
        self._candidates = candidates
        self.incremented: list[str] = []
        self.decremented: list[str] = []

    async def list_candidates(self):
        return self._candidates

    async def increment_case_count(self, identifier: str) -> None:
        self.incremented.append(identifier)

    async def decrement_case_count(self, identifier: str) -> None:
        self.decremented.append(identifier)


@pytest.mark.asyncio
async def test_demo_fixed_mode_always_assigns_the_configured_agronomist():
    settings = Settings(ROUTING_MODE="demo_fixed", DEMO_FIXED_AGRONOMIST="agronomist:kvk_erode")
    service = RoutingService(agronomist_repo=None, settings=settings)  # never touched in this mode

    assert await service.assign_agronomist() == "agronomist:kvk_erode"
    assert await service.assign_agronomist(jurisdiction="madurai") == "agronomist:kvk_erode"


@pytest.mark.asyncio
async def test_real_mode_assigns_nearest_available():
    repo = _FakeAgronomistRepo(
        [
            AgronomistCandidate("agronomist:erode", "erode", True, 2),
            AgronomistCandidate("agronomist:madurai", "madurai", True, 0),
        ]
    )
    service = RoutingService(agronomist_repo=repo, settings=Settings(ROUTING_MODE="real"))

    assigned = await service.assign_agronomist(jurisdiction="erode")
    assert assigned == "agronomist:erode"

    await service.record_assignment(assigned)
    assert repo.incremented == ["agronomist:erode"]


@pytest.mark.asyncio
async def test_real_mode_falls_back_to_next_available_when_local_is_unavailable():
    repo = _FakeAgronomistRepo(
        [
            AgronomistCandidate("agronomist:erode", "erode", False, 0),
            AgronomistCandidate("agronomist:madurai", "madurai", True, 1),
        ]
    )
    service = RoutingService(agronomist_repo=repo, settings=Settings(ROUTING_MODE="real"))

    assert await service.assign_agronomist(jurisdiction="erode") == "agronomist:madurai"


@pytest.mark.asyncio
async def test_real_mode_raises_officer_unavailable_when_nobody_is_available():
    repo = _FakeAgronomistRepo(
        [
            AgronomistCandidate("agronomist:erode", "erode", False, 0),
            AgronomistCandidate("agronomist:madurai", "madurai", False, 0),
        ]
    )
    service = RoutingService(agronomist_repo=repo, settings=Settings(ROUTING_MODE="real"))

    with pytest.raises(OfficerUnavailableError) as exc_info:
        await service.assign_agronomist(jurisdiction="erode")
    assert exc_info.value.code == "OFFICER_UNAVAILABLE"


@pytest.mark.asyncio
async def test_record_resolution_decrements_load_in_real_mode():
    repo = _FakeAgronomistRepo([])
    service = RoutingService(agronomist_repo=repo, settings=Settings(ROUTING_MODE="real"))
    await service.record_resolution("agronomist:erode")
    assert repo.decremented == ["agronomist:erode"]


@pytest.mark.asyncio
async def test_demo_fixed_mode_never_touches_the_repository():
    service = RoutingService(agronomist_repo=None, settings=Settings(ROUTING_MODE="demo_fixed"))
    # Would raise AttributeError on None if it tried to call the repo.
    await service.record_assignment("agronomist:kvk_erode")
    await service.record_resolution("agronomist:kvk_erode")
