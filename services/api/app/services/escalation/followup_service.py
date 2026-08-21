"""Orchestrates POST /followups/{problem_id}/respond (contract §2.12): the
closed-loop follow-up. Promotes severity one tier on 'got_worse', recomputes
health via the Phase 1 engine (reused unchanged, never reimplemented), and
auto-escalates once the recomputed band crosses below Watch (Phase 4 item 4).
"""

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from app.core.enums import FollowupResponse, HealthBand, ProblemSeverity
from app.core.errors import NotFoundError
from app.domain.escalation import should_auto_escalate
from app.domain.health.inputs import TriggeringInput
from app.repositories.dependencies import (
    get_farm_health_context_writer,
    get_problem_load_reader,
    get_problem_writer,
    get_treatment_trend_writer,
)
from app.repositories.health_context import (
    FarmHealthContextWriter,
    ProblemLoadReader,
    ProblemWriter,
    TreatmentTrendWriter,
)
from app.services.escalation.escalation_service import EscalationService, get_escalation_service
from app.services.health_service import HealthService, get_health_service

FOLLOWUP_TRIGGER_TYPE = "got_worse_followup"
FOLLOWUP_TRIGGERING_INPUT_TYPE = "followup"


@dataclass(frozen=True)
class FollowupOutcome:
    """Result of one follow-up response — mirrors contract §2.12's
    ``POST /followups/{id}/respond`` response exactly."""

    problem_id: str
    severity_from: ProblemSeverity | None
    severity_to: ProblemSeverity | None
    health_from: int | None
    health_to: int | None
    health_band: HealthBand
    escalated: bool
    case_id: str | None


class FollowupService:
    """Closes the loop on one farmer follow-up response."""

    def __init__(
        self,
        problem_reader: ProblemLoadReader,
        problem_writer: ProblemWriter,
        treatment_writer: TreatmentTrendWriter,
        context_writer: FarmHealthContextWriter,
        health_service: HealthService,
        escalation_service: EscalationService,
    ) -> None:
        self._problem_reader = problem_reader
        self._problem_writer = problem_writer
        self._treatment_writer = treatment_writer
        self._context_writer = context_writer
        self._health = health_service
        self._escalation = escalation_service

    async def respond(
        self,
        problem_id: str,
        response: FollowupResponse,
        image_asset_id: str | None = None,
    ) -> FollowupOutcome:
        """Record a farmer's follow-up on ``problem_id`` (PRD §5.10, contract §2.12).

        Args:
            problem_id: The open problem being followed up on (the path's
                ``{id}`` — resolved to its owning farm via ``find_farm_id``,
                since the contract's request body carries no ``farm_id``).
            response: 'improved' / 'no_change' / 'got_worse'.
            image_asset_id: Optional updated crop photo — counts as a fresh
                monitoring touchpoint, resetting monitoring recency.

        Returns:
            A ``FollowupOutcome`` carrying the severity change (if any), the
            recomputed health movement, and — if the recomputed band crossed
            below Watch — the new case's id.

        Raises:
            NotFoundError: ``problem_id`` isn't currently open on any farm.
        """
        farm_id = await self._problem_reader.find_farm_id(problem_id)
        if farm_id is None:
            raise NotFoundError(message=f"No open problem {problem_id!r}.")

        before_snapshot = await self._health.get_latest(farm_id)
        severity_before = await self._current_severity(farm_id, problem_id)

        new_severity = severity_before
        if response == FollowupResponse.GOT_WORSE and severity_before is not None:
            new_severity = await self._problem_writer.promote_severity(farm_id, problem_id)

        await self._treatment_writer.record_followup(farm_id, response)
        if image_asset_id is not None:
            await self._context_writer.touch_last_scan(farm_id)

        details: dict = {"problem_id": problem_id, "response": response.value}
        if new_severity is not None:
            details["severity"] = new_severity.value
        snapshot = await self._health.recompute(
            farm_id, triggering_input=TriggeringInput(type=FOLLOWUP_TRIGGERING_INPUT_TYPE, details=details)
        )

        auto_escalated = response == FollowupResponse.GOT_WORSE and should_auto_escalate(HealthBand(snapshot.band))
        escalation_id: str | None = None
        if auto_escalated:
            result = await self._escalation.create_escalation(
                farm_id=farm_id,
                trigger_type=FOLLOWUP_TRIGGER_TYPE,
                reason=(
                    f"Follow-up reported 'got_worse' on problem {problem_id}; "
                    f"health band fell to '{snapshot.band}'."
                ),
                severity=new_severity or ProblemSeverity.EARLY,
                problem_id=problem_id,
                latest_images=[image_asset_id] if image_asset_id else None,
            )
            escalation_id = result.case_id

        severity_changed = response == FollowupResponse.GOT_WORSE and new_severity != severity_before
        return FollowupOutcome(
            problem_id=problem_id,
            severity_from=severity_before if severity_changed else None,
            severity_to=new_severity if severity_changed else None,
            health_from=before_snapshot.score,
            health_to=snapshot.score,
            health_band=HealthBand(snapshot.band),
            escalated=auto_escalated,
            case_id=escalation_id,
        )

    async def _current_severity(self, farm_id: str, problem_id: str) -> ProblemSeverity | None:
        open_problems = await self._problem_reader.get_open_problems(farm_id)
        match = next((p for p in open_problems if p.problem_id == problem_id), None)
        return match.severity if match else None


def get_followup_service(
    problem_reader: Annotated[ProblemLoadReader, Depends(get_problem_load_reader)],
    problem_writer: Annotated[ProblemWriter, Depends(get_problem_writer)],
    treatment_writer: Annotated[TreatmentTrendWriter, Depends(get_treatment_trend_writer)],
    context_writer: Annotated[FarmHealthContextWriter, Depends(get_farm_health_context_writer)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    escalation_service: Annotated[EscalationService, Depends(get_escalation_service)],
) -> FollowupService:
    """FastAPI dependency provider assembling ``FollowupService`` from its ports."""
    return FollowupService(
        problem_reader, problem_writer, treatment_writer, context_writer, health_service, escalation_service
    )
