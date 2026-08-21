"""POST /followups/{id}/respond (contract §2.12, execution plan item 4):
closes the loop. Got Worse promotes severity one tier, Improved demotes it
(PRD §7.3), the health engine recomputes (Phase 1 — never reimplemented
here), and Got Worse auto-escalates via the shared EscalationService.
"""

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from app.core.enums import FollowupResponse
from app.core.errors import NotFoundError
from app.domain.escalation import demote_severity, promote_severity, should_auto_escalate
from app.domain.health.inputs import TriggeringInput
from app.models.health_snapshot import HealthSnapshot
from app.repositories.dependencies import get_problem_registry, get_treatment_trend_writer
from app.repositories.health_context import TreatmentTrend
from app.repositories.problem_registry import ProblemRegistry
from app.services.escalation.escalation_service import EscalationService, get_escalation_service
from app.services.health_service import HealthService, get_health_service

FOLLOWUP_ESCALATION_REASON = "follow-up reported got_worse"
FOLLOWUP_ESCALATION_TRIGGER = "got_worse"


@dataclass(frozen=True)
class FollowUpOutcome:
    problem_id: str
    severity_from: str
    severity_to: str
    health_from: int | None
    health_to: int | None
    health_band: str
    escalated: bool
    case_id: str | None


class FollowUpService:
    def __init__(
        self,
        problem_registry: ProblemRegistry,
        health_service: HealthService,
        treatment_trend_writer,
        escalation_service: EscalationService,
    ) -> None:
        self._problems = problem_registry
        self._health = health_service
        self._treatment_trend = treatment_trend_writer
        self._escalation = escalation_service

    async def respond(
        self,
        followup_id: str,
        response: FollowupResponse,
        image_asset_id: str | None,
    ) -> FollowUpOutcome:
        """Process one farmer follow-up response.

        Raises:
            NotFoundError: if ``followup_id`` doesn't exist.
        """
        followup = await self._problems.get_followup(followup_id)
        if followup is None:
            raise NotFoundError(message="Follow-up not found.", details={"followup_id": followup_id})

        problem = await self._problems.get_problem(followup.problem_id)
        if problem is None:
            raise NotFoundError(message="The problem this follow-up refers to no longer exists.")

        severity_from = problem.severity
        if response == FollowupResponse.GOT_WORSE:
            severity_to = promote_severity(severity_from)
        elif response == FollowupResponse.IMPROVED:
            severity_to = demote_severity(severity_from)
        else:
            severity_to = severity_from

        await self._problems.update_severity(problem.problem_id, severity_to)
        await self._problems.mark_followup_responded(followup_id, response, image_asset_id)
        if image_asset_id:
            await self._problems.add_image(problem.problem_id, image_asset_id)
        await self._problems.append_timeline_event(problem.problem_id, "followup", response.value)

        await self._update_treatment_trend(problem.farm_id, response)

        before: HealthSnapshot = await self._health.get_latest(problem.farm_id)
        after = await self._health.recompute(
            problem.farm_id,
            triggering_input=TriggeringInput(
                type="followup", details={"problem_id": problem.problem_id, "response": response.value}
            ),
        )

        escalated = should_auto_escalate(response)
        case_id: str | None = None
        if escalated:
            case = await self._escalation.escalate(
                farm_id=problem.farm_id,
                problem_id=problem.problem_id,
                reason=FOLLOWUP_ESCALATION_REASON,
                trigger=FOLLOWUP_ESCALATION_TRIGGER,
            )
            case_id = case.id

        return FollowUpOutcome(
            problem_id=problem.problem_id,
            severity_from=severity_from.value,
            severity_to=severity_to.value,
            health_from=before.score,
            health_to=after.score,
            health_band=after.band,
            escalated=escalated,
            case_id=case_id,
        )

    async def _update_treatment_trend(self, farm_id: str, response: FollowupResponse) -> None:
        current = await self._treatment_trend.get_treatment_trend(farm_id)
        consecutive_got_worse = current.consecutive_got_worse_count + 1 if response == FollowupResponse.GOT_WORSE else 0
        self._treatment_trend.set_trend(
            farm_id,
            TreatmentTrend(
                latest_followup_response=response,
                consecutive_got_worse_count=consecutive_got_worse,
                problem_resolved_with_confirmed_treatment=False,
            ),
        )


def get_followup_service(
    problem_registry: Annotated[ProblemRegistry, Depends(get_problem_registry)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    treatment_trend_writer: Annotated[object, Depends(get_treatment_trend_writer)],
    escalation_service: Annotated[EscalationService, Depends(get_escalation_service)],
) -> FollowUpService:
    return FollowUpService(problem_registry, health_service, treatment_trend_writer, escalation_service)
