"""Manual/automatic problem escalation API router (contract §2.13)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.errors import NotFoundError
from app.core.security import get_current_token_payload
from app.repositories.dependencies import get_problem_registry
from app.repositories.problem_registry import ProblemRegistry
from app.schemas.escalation import EscalateResponse
from app.services.escalation.escalation_service import EscalationService, get_escalation_service

router = APIRouter(prefix="/problems", tags=["Escalation & Case Summary"])

MANUAL_ESCALATION_REASON = "Manually escalated by request."
MANUAL_ESCALATION_TRIGGER = "manual"


@router.post(
    "/{problem_id}/escalate",
    response_model=EscalateResponse,
    status_code=201,
    summary="Escalate a problem — compiles a CaseSummary and routes it to an agronomist",
)
async def escalate_problem(
    problem_id: str,
    problem_registry: Annotated[ProblemRegistry, Depends(get_problem_registry)],
    escalation_service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> EscalateResponse:
    """PRD §5.11 / contract §2.13. Also fired automatically (below-gate
    diagnosis, no-relevant-source, or a Got Worse follow-up) — this is the
    same compile-and-route path those triggers use, invoked manually."""
    problem = await problem_registry.get_problem(problem_id)
    if problem is None:
        raise NotFoundError(message="Problem not found.", details={"problem_id": problem_id})

    case = await escalation_service.escalate(
        farm_id=problem.farm_id,
        problem_id=problem_id,
        reason=MANUAL_ESCALATION_REASON,
        trigger=MANUAL_ESCALATION_TRIGGER,
    )
    return EscalateResponse(case_id=case.id, assigned_to=case.assigned_to, status=case.status)
