"""POST /cases/{id}/resolve (contract §2.13, execution plan item 5): expert
diagnosis/treatment clears the problem and recovers the score via Phase 1's
health engine — never reimplemented here.
"""

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from app.core.errors import NotFoundError
from app.domain.health.inputs import TriggeringInput
from app.models.health_snapshot import HealthSnapshot
from app.repositories.case_repository import EscalationCaseRepository
from app.repositories.dependencies import (
    get_escalation_case_repository,
    get_problem_registry,
    get_treatment_trend_writer,
)
from app.repositories.health_context import TreatmentTrend
from app.repositories.problem_registry import ProblemRegistry
from app.services.escalation.routing_service import RoutingService, get_routing_service
from app.services.health_service import HealthService, get_health_service


@dataclass(frozen=True)
class ResolveOutcome:
    case_id: str
    status: str
    problem_status: str | None
    health_from: int | None
    health_to: int | None
    health_band: str


class ResolveService:
    def __init__(
        self,
        case_repo: EscalationCaseRepository,
        problem_registry: ProblemRegistry,
        health_service: HealthService,
        treatment_trend_writer,
        routing: RoutingService,
    ) -> None:
        self._cases = case_repo
        self._problems = problem_registry
        self._health = health_service
        self._treatment_trend = treatment_trend_writer
        self._routing = routing

    async def resolve(self, case_id: str, diagnosis: str, treatment: str, notes: str | None) -> ResolveOutcome:
        """Record the expert's resolution and recover the farm's health score.

        Raises:
            NotFoundError: if ``case_id`` doesn't exist.
        """
        case = await self._cases.resolve(case_id, diagnosis, treatment, notes)
        if case is None:
            raise NotFoundError(message="Case not found.", details={"case_id": case_id})

        problem_status: str | None = None
        if case.problem_id:
            await self._problems.add_treatment(case.problem_id, treatment)
            await self._problems.resolve_problem(case.problem_id)
            await self._problems.append_timeline_event(case.problem_id, "resolution", diagnosis)
            problem_status = "resolved"

            trend = await self._treatment_trend.get_treatment_trend(case.farm_id)
            self._treatment_trend.set_trend(
                case.farm_id,
                TreatmentTrend(
                    latest_followup_response=trend.latest_followup_response,
                    consecutive_got_worse_count=trend.consecutive_got_worse_count,
                    problem_resolved_with_confirmed_treatment=True,
                ),
            )

        if case.assigned_to:
            await self._routing.record_resolution(case.assigned_to)

        before: HealthSnapshot = await self._health.get_latest(case.farm_id)
        after = await self._health.recompute(
            case.farm_id,
            triggering_input=TriggeringInput(
                type="case_resolution", details={"case_id": case.id, "problem_id": case.problem_id}
            ),
        )

        return ResolveOutcome(
            case_id=case.id,
            status=case.status,
            problem_status=problem_status,
            health_from=before.score,
            health_to=after.score,
            health_band=after.band,
        )


def get_resolve_service(
    case_repo: Annotated[EscalationCaseRepository, Depends(get_escalation_case_repository)],
    problem_registry: Annotated[ProblemRegistry, Depends(get_problem_registry)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    treatment_trend_writer: Annotated[object, Depends(get_treatment_trend_writer)],
    routing: Annotated[RoutingService, Depends(get_routing_service)],
) -> ResolveService:
    return ResolveService(case_repo, problem_registry, health_service, treatment_trend_writer, routing)
