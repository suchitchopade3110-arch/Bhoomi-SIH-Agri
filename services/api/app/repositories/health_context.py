"""Narrow read interfaces the health engine needs from aggregates that do not
have their own phase yet (Farm profile, Problem, FollowUp).

Each is a small ``Protocol`` plus an in-memory, settable implementation —
the same ports-and-adapters shape used for ``adapters/``. When the
Farm/Problem/FollowUp phases land with real SQLAlchemy-backed repositories,
swap the provider in ``repositories/dependencies.py``; ``health_service.py``
never changes.
"""

from dataclasses import dataclass
from typing import Protocol

from app.core.enums import FollowupResponse, ProblemSeverity
from app.domain.health.inputs import CropIdealConditions


@dataclass(frozen=True)
class OpenProblemRecord:
    """One currently-open problem, as read from the Problem aggregate."""

    problem_id: str
    severity: ProblemSeverity


@dataclass(frozen=True)
class TreatmentTrend:
    """The closed-loop follow-up trend for a farm's most recent problem."""

    latest_followup_response: FollowupResponse | None
    consecutive_got_worse_count: int
    problem_resolved_with_confirmed_treatment: bool


@dataclass(frozen=True)
class FarmHealthContext:
    """The subset of the Farm profile the health engine needs.

    ``latitude``/``longitude`` feed ``WeatherPort``; the rest come from the
    farm's onboarding record and its active resource plan.
    """

    latitude: float
    longitude: float
    crop_ideal: CropIdealConditions
    soil_moisture_pct: float | None
    irrigation_delivered_mm: float | None
    irrigation_required_mm: float | None
    days_since_planting: int | None
    expected_stage_day: int
    days_since_last_scan: int | None


class ProblemLoadReader(Protocol):
    """Read access to a farm's currently-open problems (sub-index #4)."""

    async def get_open_problems(self, farm_id: str) -> list[OpenProblemRecord]: ...


class TreatmentTrendReader(Protocol):
    """Read access to a farm's closed-loop follow-up trend (sub-index #6)."""

    async def get_treatment_trend(self, farm_id: str) -> TreatmentTrend: ...


class FarmHealthContextReader(Protocol):
    """Read access to the farm-profile fields the health engine needs."""

    async def get_context(self, farm_id: str) -> FarmHealthContext | None: ...


class InMemoryProblemLoadReader:
    """Settable in-memory ``ProblemLoadReader`` for demo/dev/tests."""

    def __init__(self) -> None:
        self._by_farm: dict[str, list[OpenProblemRecord]] = {}

    def set_open_problems(self, farm_id: str, problems: list[OpenProblemRecord]) -> None:
        self._by_farm[farm_id] = problems

    async def get_open_problems(self, farm_id: str) -> list[OpenProblemRecord]:
        return self._by_farm.get(farm_id, [])


class InMemoryTreatmentTrendReader:
    """Settable in-memory ``TreatmentTrendReader`` for demo/dev/tests."""

    def __init__(self) -> None:
        self._by_farm: dict[str, TreatmentTrend] = {}

    def set_trend(self, farm_id: str, trend: TreatmentTrend) -> None:
        self._by_farm[farm_id] = trend

    async def get_treatment_trend(self, farm_id: str) -> TreatmentTrend:
        return self._by_farm.get(
            farm_id,
            TreatmentTrend(
                latest_followup_response=None,
                consecutive_got_worse_count=0,
                problem_resolved_with_confirmed_treatment=False,
            ),
        )


class InMemoryFarmHealthContextReader:
    """Settable in-memory ``FarmHealthContextReader`` for demo/dev/tests."""

    def __init__(self) -> None:
        self._by_farm: dict[str, FarmHealthContext] = {}

    def set_context(self, farm_id: str, context: FarmHealthContext) -> None:
        self._by_farm[farm_id] = context

    async def get_context(self, farm_id: str) -> FarmHealthContext | None:
        return self._by_farm.get(farm_id)
