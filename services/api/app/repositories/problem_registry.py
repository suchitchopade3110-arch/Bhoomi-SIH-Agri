"""In-memory Problem + FollowUp registry.

The Problem and FollowUp aggregates (PRD §5.9, §5.10) don't have their own
phase yet — no ORM model, no migration, no full timeline/problems GET
endpoints. This registry is the placeholder those flows need in the
meantime, extending Phase 1/3's narrower ``ProblemLoadReader``/
``ProblemWriter`` (which it still satisfies structurally, so
``HealthService`` and ``DiagnosisService`` need no changes) with the
richer read/write surface Phase 4's follow-up and escalation flows need:
look up a problem or follow-up by id, promote severity, record a
treatment, resolve a problem, and a minimal per-problem timeline slice.

Swap this for a real DB-backed implementation once Problem/FollowUp get
their own migration — nothing downstream (services or API layer) depends
on it being in-memory, only on the method signatures below.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid

from app.core.enums import FollowupResponse, ProblemSeverity, ProblemStatus
from app.repositories.health_context import OpenProblemRecord


@dataclass
class Problem:
    """Mutable — severity, status, and treatments change over its life."""

    problem_id: str
    farm_id: str
    label: str
    severity: ProblemSeverity
    status: ProblemStatus = ProblemStatus.OPEN
    treatments_tried: list[str] = field(default_factory=list)
    image_asset_ids: list[str] = field(default_factory=list)
    timeline: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class FollowUp:
    followup_id: str
    problem_id: str
    farm_id: str
    responded: bool = False
    response: FollowupResponse | None = None
    photo_asset_id: str | None = None


class ProblemRegistry:
    """Single source of truth for Problem + FollowUp records."""

    def __init__(self) -> None:
        self._problems: dict[str, Problem] = {}
        self._followups: dict[str, FollowUp] = {}

    # --- Phase 1's ProblemLoadReader / ProblemWriter Protocols ---
    # (structural — no inheritance needed; HealthService and DiagnosisService
    # keep working against these two methods unmodified.)
    async def get_open_problems(self, farm_id: str) -> list[OpenProblemRecord]:
        return [
            OpenProblemRecord(problem_id=p.problem_id, severity=p.severity)
            for p in self._problems.values()
            if p.farm_id == farm_id and p.status == ProblemStatus.OPEN
        ]

    async def add_open_problem(self, farm_id: str, problem: OpenProblemRecord) -> None:
        """Kept for Protocol compatibility; prefer ``register_problem`` when
        the caller has the full record (label, image) available."""
        if problem.problem_id not in self._problems:
            await self.register_problem(
                Problem(problem_id=problem.problem_id, farm_id=farm_id, label="unspecified", severity=problem.severity)
            )

    # --- Phase 4 additions ---
    async def register_problem(self, problem: Problem) -> Problem:
        problem.timeline.append(_event("diagnosis", f"{problem.label} ({problem.severity.value})"))
        self._problems[problem.problem_id] = problem
        return problem

    async def get_problem(self, problem_id: str) -> Problem | None:
        return self._problems.get(problem_id)

    async def get_problems_for_farm(self, farm_id: str) -> list[Problem]:
        return [p for p in self._problems.values() if p.farm_id == farm_id]

    async def update_severity(self, problem_id: str, severity: ProblemSeverity) -> None:
        problem = self._problems.get(problem_id)
        if problem is not None:
            problem.severity = severity

    async def add_treatment(self, problem_id: str, treatment: str) -> None:
        problem = self._problems.get(problem_id)
        if problem is not None:
            problem.treatments_tried.append(treatment)

    async def add_image(self, problem_id: str, asset_id: str) -> None:
        problem = self._problems.get(problem_id)
        if problem is not None and asset_id not in problem.image_asset_ids:
            problem.image_asset_ids.append(asset_id)

    async def resolve_problem(self, problem_id: str) -> None:
        problem = self._problems.get(problem_id)
        if problem is not None:
            problem.status = ProblemStatus.RESOLVED

    async def append_timeline_event(self, problem_id: str, event: str, detail: str) -> None:
        problem = self._problems.get(problem_id)
        if problem is not None:
            problem.timeline.append(_event(event, detail))

    async def schedule_followup(self, problem_id: str, farm_id: str) -> FollowUp:
        followup = FollowUp(followup_id=str(uuid.uuid4()), problem_id=problem_id, farm_id=farm_id)
        self._followups[followup.followup_id] = followup
        return followup

    async def get_followup(self, followup_id: str) -> FollowUp | None:
        return self._followups.get(followup_id)

    async def mark_followup_responded(
        self, followup_id: str, response: FollowupResponse, photo_asset_id: str | None
    ) -> None:
        followup = self._followups.get(followup_id)
        if followup is not None:
            followup.responded = True
            followup.response = response
            followup.photo_asset_id = photo_asset_id


def _event(event: str, detail: str) -> dict[str, Any]:
    return {"at": datetime.utcnow().isoformat() + "Z", "event": event, "detail": detail}
