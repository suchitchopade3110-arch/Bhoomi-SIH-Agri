"""Opens and compiles a Case (PRD §5.11, execution plan items 1-3, 6).

Every escalation trigger — a diagnosis failing the confidence gate
(below-gate confidence, out-of-scope, no relevant source; Phase 2/3) or a
follow-up reporting Got Worse (Phase 4's ``followup_service.py``) — routes
through this one ``escalate`` method, so every case gets the same
compiled, pre-analyzed CaseSummary (execution plan item 2) regardless of
what triggered it.
"""

from dataclasses import asdict
from typing import Annotated

from fastapi import Depends

from app.models.case import Case
from app.repositories.case_repository import EscalationCaseRepository
from app.repositories.dependencies import get_escalation_case_repository
from app.services.escalation.case_summary_service import CaseSummaryService, get_case_summary_service
from app.services.escalation.routing_service import RoutingService, get_routing_service


class EscalationService:
    def __init__(
        self,
        case_repo: EscalationCaseRepository,
        routing: RoutingService,
        case_summary: CaseSummaryService,
    ) -> None:
        self._cases = case_repo
        self._routing = routing
        self._case_summary = case_summary

    async def escalate(
        self,
        farm_id: str,
        problem_id: str | None,
        reason: str,
        trigger: str,
        jurisdiction: str | None = None,
    ) -> Case:
        """Open a case, assign it, and attach its compiled CaseSummary.

        Args:
            farm_id: UUID string of the farm.
            problem_id: The confirmed problem this case is about, or
                ``None`` for a case opened before any problem exists (e.g.
                a diagnosis that failed the confidence gate).
            reason: Human-readable trigger reason (contract §2.1 error
                envelope style, or a plain sentence for non-error triggers).
            trigger: One of ``below_gate`` | ``out_of_scope`` |
                ``no_relevant_source`` | ``got_worse`` | ``manual``.
            jurisdiction: Optional district/taluk hint for routing.

        Returns:
            The persisted, fully-summarized ``Case``.
        """
        assigned_to = await self._routing.assign_agronomist(jurisdiction)

        case = await self._cases.create(
            farm_id=farm_id,
            problem_id=problem_id,
            reason=reason,
            trigger=trigger,
            assigned_to=assigned_to,
            summary={},
            status="assigned",
        )

        await self._routing.record_assignment(assigned_to)

        summary = await self._case_summary.build(case.id, farm_id, problem_id, status=case.status)
        case = await self._cases.update_summary(case.id, asdict(summary))
        return case

    async def get_case(self, case_id: str) -> Case | None:
        return await self._cases.get_by_id(case_id)

    async def list_queue(
        self, assigned_to: str | None = None, limit: int = 20, cursor: str | None = None
    ) -> tuple[list[Case], str | None]:
        """``GET /agronomist/case-queue``: assigned cases, newest first (contract §2.13)."""
        return await self._cases.list_queue(assigned_to=assigned_to, limit=limit, cursor=cursor)


def get_escalation_service(
    case_repo: Annotated[EscalationCaseRepository, Depends(get_escalation_case_repository)],
    routing: Annotated[RoutingService, Depends(get_routing_service)],
    case_summary: Annotated[CaseSummaryService, Depends(get_case_summary_service)],
) -> EscalationService:
    return EscalationService(case_repo, routing, case_summary)
