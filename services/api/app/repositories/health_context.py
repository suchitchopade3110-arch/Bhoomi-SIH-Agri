"""Narrow read interfaces the health engine needs from aggregates that do not
have their own phase yet (Farm profile, Problem, FollowUp).

Each is a small ``Protocol`` plus an in-memory, settable implementation —
the same ports-and-adapters shape used for ``adapters/``. When the
Farm/Problem/FollowUp phases land with real SQLAlchemy-backed repositories,
swap the provider in ``repositories/dependencies.py``; ``health_service.py``
never changes.
"""

from dataclasses import dataclass, replace
from typing import Protocol

from app.core.enums import FollowupResponse, ProblemSeverity
from app.domain.escalation import promote_severity
from app.domain.health.inputs import CropIdealConditions


@dataclass(frozen=True)
class OpenProblemRecord:
    """One currently-open problem, as read from the Problem aggregate."""

    problem_id: str
    severity: ProblemSeverity
    label: str | None = None


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

    async def find_farm_id(self, problem_id: str) -> str | None:
        """The farm a given ``problem_id`` currently belongs to, or ``None``
        if it isn't open on any farm (Phase 4: resolving the path-only
        ``problem_id`` on POST /followups/{problem_id}/respond)."""
        ...


class ProblemWriter(Protocol):
    """Write access for a farm's open problems (Phase-3 diagnose flow, Phase-4
    follow-up/resolution flows).

    Split from ``ProblemLoadReader`` so a pure read-only caller (the health
    engine) never accidentally gets write access — but both are backed by
    the same in-memory store today, so a write here is immediately visible
    to reads.
    """

    async def add_open_problem(self, farm_id: str, problem: OpenProblemRecord) -> None: ...

    async def promote_severity(self, farm_id: str, problem_id: str) -> ProblemSeverity | None:
        """Promote one open problem one tier (PRD §5.10's ``domain.escalation.promote_severity``
        ladder). Returns the new severity, or ``None`` if no such open problem exists."""
        ...

    async def resolve_problem(self, farm_id: str, problem_id: str) -> None:
        """Remove one problem from the farm's open list (PRD §7.4: an expert
        resolution returns ``active_problem_load`` to 100). A no-op if the
        problem isn't currently open."""
        ...


class TreatmentTrendReader(Protocol):
    """Read access to a farm's closed-loop follow-up trend (sub-index #6)."""

    async def get_treatment_trend(self, farm_id: str) -> TreatmentTrend: ...


class TreatmentTrendWriter(Protocol):
    """Write access to a farm's closed-loop follow-up trend (Phase 4)."""

    async def record_followup(self, farm_id: str, response: FollowupResponse) -> TreatmentTrend:
        """Record one farmer follow-up response. ``got_worse`` increments the
        consecutive-worse streak; anything else resets it to zero."""
        ...

    async def record_confirmed_resolution(self, farm_id: str) -> TreatmentTrend:
        """Mark the farm's trend as a confirmed expert resolution (PRD §7.4:
        always yields ``treatment_response``'s maximum score), keeping the
        follow-up history that led up to it."""
        ...


class FarmHealthContextReader(Protocol):
    """Read access to the farm-profile fields the health engine needs."""

    async def get_context(self, farm_id: str) -> FarmHealthContext | None: ...


class FarmHealthContextWriter(Protocol):
    """Write access to the farm-profile fields the health engine needs (Phase 4)."""

    async def touch_last_scan(self, farm_id: str) -> None:
        """Reset ``days_since_last_scan`` to 0 — a fresh monitoring touchpoint
        (a follow-up photo, or an agronomist's confirmed resolution). A no-op
        if the farm has no context yet."""
        ...


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

    async def find_farm_id(self, problem_id: str) -> str | None:
        for farm_id, problems in self._by_farm.items():
            if any(p.problem_id == problem_id for p in problems):
                return farm_id
        return None

    async def promote_severity(self, farm_id: str, problem_id: str) -> ProblemSeverity | None:
        problems = self._by_farm.get(farm_id, [])
        for i, p in enumerate(problems):
            if p.problem_id == problem_id:
                new_severity = promote_severity(p.severity)
                problems[i] = replace(p, severity=new_severity)
                return new_severity
        return None

    async def resolve_problem(self, farm_id: str, problem_id: str) -> None:
        problems = self._by_farm.get(farm_id, [])
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

    async def record_followup(self, farm_id: str, response: FollowupResponse) -> TreatmentTrend:
        current = await self.get_treatment_trend(farm_id)
        new_count = current.consecutive_got_worse_count + 1 if response == FollowupResponse.GOT_WORSE else 0
        new_trend = TreatmentTrend(
            latest_followup_response=response,
            consecutive_got_worse_count=new_count,
            # A fresh follow-up reopens the trend — confirmed resolution is a
            # distinct, explicit act (record_confirmed_resolution), never implied.
            problem_resolved_with_confirmed_treatment=False,
        )
        self._by_farm[farm_id] = new_trend
        return new_trend

    async def record_confirmed_resolution(self, farm_id: str) -> TreatmentTrend:
        current = await self.get_treatment_trend(farm_id)
        new_trend = replace(current, problem_resolved_with_confirmed_treatment=True)
        self._by_farm[farm_id] = new_trend
        return new_trend


class InMemoryFarmHealthContextReader:
    """Settable in-memory ``FarmHealthContextReader`` for demo/dev/tests."""

    def __init__(self) -> None:
        self._by_farm: dict[str, FarmHealthContext] = {}

    def set_context(self, farm_id: str, context: FarmHealthContext) -> None:
        self._by_farm[farm_id] = context

    async def get_context(self, farm_id: str) -> FarmHealthContext | None:
        return self._by_farm.get(farm_id)

    async def touch_last_scan(self, farm_id: str) -> None:
        context = self._by_farm.get(farm_id)
        if context is not None:
            self._by_farm[farm_id] = replace(context, days_since_last_scan=0)
