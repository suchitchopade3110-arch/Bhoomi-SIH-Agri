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
    label: str = ""


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


class ProblemWriter(Protocol):
    """Write access for originating a new open problem (Phase-3 diagnose flow).

    Split from ``ProblemLoadReader`` so a pure read-only caller (the health
    engine) never accidentally gets write access — but both are backed by
    the same in-memory store today, so a write here is immediately visible
    to reads.
    """

    async def add_open_problem(self, farm_id: str, problem: OpenProblemRecord) -> None: ...

    async def get_latest_open_problem(self, farm_id: str) -> OpenProblemRecord | None:
        """The most recently opened still-open problem for a farm (Phase-5
        follow-up flow: the check-in target when the caller doesn't name a
        specific ``problem_id``)."""
        ...

    async def set_problem_severity(self, problem_id: str, severity: ProblemSeverity) -> None:
        """Promote/demote one problem's severity (PRD §7.3: "Got Worse ...
        promotes a problem up one severity tier; Improved demotes it")."""
        ...

    async def resolve_problem(self, problem_id: str) -> None:
        """Mark one problem resolved (PRD §7.3: "resolution clears it" —
        sub-index #4 returns to 100 for this problem)."""
        ...


class TreatmentTrendReader(Protocol):
    """Read access to a farm's closed-loop follow-up trend (sub-index #6)."""

    async def get_treatment_trend(self, farm_id: str) -> TreatmentTrend: ...


class FollowUpWriter(Protocol):
    """Write access for recording one farmer check-in (Phase-5 follow-up
    flow, contract §2.12). Split from ``TreatmentTrendReader`` the same way
    ``ProblemWriter`` is split from ``ProblemLoadReader``."""

    async def record_followup(
        self,
        followup_id: str,
        problem_id: str,
        farm_id: str,
        response: FollowupResponse,
        farmer_notes: str | None,
        photo_asset_id: str | None,
    ) -> None: ...


class FarmHealthContextReader(Protocol):
    """Read access to the farm-profile fields the health engine needs."""

    async def get_context(self, farm_id: str) -> FarmHealthContext | None: ...


class InMemoryProblemLoadReader:
    """Settable in-memory ``ProblemLoadReader`` for demo/dev/tests."""

    def __init__(self) -> None:
        self._by_farm: dict[str, list[OpenProblemRecord]] = {}

    def set_open_problems(self, farm_id: str, problems: list[OpenProblemRecord]) -> None:
        self._by_farm[farm_id] = problems

    async def add_open_problem(self, farm_id: str, problem: OpenProblemRecord) -> None:
        """Append one newly-diagnosed problem (Phase-3 diagnose flow) without
        disturbing any problems already tracked for this farm."""
        self._by_farm.setdefault(farm_id, []).append(problem)

    async def get_open_problems(self, farm_id: str) -> list[OpenProblemRecord]:
        return self._by_farm.get(farm_id, [])

    async def get_latest_open_problem(self, farm_id: str) -> OpenProblemRecord | None:
        problems = self._by_farm.get(farm_id, [])
        return problems[-1] if problems else None

    async def set_problem_severity(self, problem_id: str, severity: ProblemSeverity) -> None:
        for problems in self._by_farm.values():
            for i, p in enumerate(problems):
                if p.problem_id == problem_id:
                    problems[i] = OpenProblemRecord(problem_id=p.problem_id, severity=severity, label=p.label)
                    return

    async def resolve_problem(self, problem_id: str) -> None:
        for farm_id, problems in self._by_farm.items():
            self._by_farm[farm_id] = [p for p in problems if p.problem_id != problem_id]


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

    async def record_followup(
        self,
        followup_id: str,
        problem_id: str,
        farm_id: str,
        response: FollowupResponse,
        farmer_notes: str | None,
        photo_asset_id: str | None,
    ) -> None:
        """Convenience helper for tests: folds the new response straight
        into this farm's ``TreatmentTrend`` (real consecutive-count math is
        the Postgres reader's job — see ``PostgresTreatmentTrendReader``)."""
        current = await self.get_treatment_trend(farm_id)
        consecutive = current.consecutive_got_worse_count + 1 if response == FollowupResponse.GOT_WORSE else 0
        self._by_farm[farm_id] = TreatmentTrend(
            latest_followup_response=response,
            consecutive_got_worse_count=consecutive,
            problem_resolved_with_confirmed_treatment=current.problem_resolved_with_confirmed_treatment,
        )


class InMemoryFarmHealthContextReader:
    """Settable in-memory ``FarmHealthContextReader`` for demo/dev/tests."""

    def __init__(self) -> None:
        self._by_farm: dict[str, FarmHealthContext] = {}

    def set_context(self, farm_id: str, context: FarmHealthContext) -> None:
        self._by_farm[farm_id] = context

    async def get_context(self, farm_id: str) -> FarmHealthContext | None:
        return self._by_farm.get(farm_id)
