"""Case detail and resolution API router (contract §2.13)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.errors import NotFoundError
from app.core.security import get_current_token_payload
from app.schemas.agronomist import ResolveCaseHealthRef, ResolveCaseRequest, ResolveCaseResponse
from app.schemas.case import CaseSummary
from app.services.escalation.escalation_service import EscalationService, get_escalation_service
from app.services.escalation.resolve_service import ResolveService, get_resolve_service

router = APIRouter(prefix="/cases", tags=["Escalation & Case Summary"])


@router.get(
    "/{case_id}",
    response_model=CaseSummary,
    summary="Get the pre-analyzed CaseSummary bundle for an agronomist",
)
async def get_case(
    case_id: str,
    escalation_service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> CaseSummary:
    """PRD §5.11 / contract §2.13 — the pre-analyzed bundle an agronomist
    opens: farm/land/soil, problem, timeline, images, treatments tried,
    follow-up trend, current health. Compiled once at escalation time and
    read back verbatim here."""
    case = await escalation_service.get_case(case_id)
    if case is None:
        raise NotFoundError(message="Case not found.", details={"case_id": case_id})
    return CaseSummary(**case.summary)


@router.post(
    "/{case_id}/resolve",
    response_model=ResolveCaseResponse,
    summary="Expert diagnosis/treatment resolves the case and recovers the farm's health score",
)
async def resolve_case(
    case_id: str,
    request: ResolveCaseRequest,
    service: Annotated[ResolveService, Depends(get_resolve_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> ResolveCaseResponse:
    """PRD §5.11, §7.4 / contract §2.13. Clears the problem
    (active_problem_load -> 100), lifts monitoring + treatment sub-indices,
    and recomputes via Phase 1's health engine — the score recovers above
    baseline, never reimplementing the scoring itself."""
    outcome = await service.resolve(case_id, request.diagnosis, request.treatment, request.notes)
    return ResolveCaseResponse(
        case_id=outcome.case_id,
        status=outcome.status,
        problem_status=outcome.problem_status,
        health=ResolveCaseHealthRef(from_=outcome.health_from, to=outcome.health_to, band=outcome.health_band),
    )
