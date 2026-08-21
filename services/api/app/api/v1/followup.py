"""Closed-loop follow-up API router (contract §2.12)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.followup import FollowupRespondRequest, FollowupRespondResponse, FollowupHealthRef, SeverityChange
from app.services.escalation.followup_service import FollowUpOutcome, FollowUpService, get_followup_service

router = APIRouter(prefix="/followups", tags=["Closed-Loop Follow-up"])


def _to_schema(outcome: FollowUpOutcome) -> FollowupRespondResponse:
    return FollowupRespondResponse(
        problem_id=outcome.problem_id,
        severity_change=SeverityChange(from_=outcome.severity_from, to=outcome.severity_to),
        health=FollowupHealthRef(from_=outcome.health_from, to=outcome.health_to, band=outcome.health_band),
        escalated=outcome.escalated,
        case_id=outcome.case_id,
    )


@router.post(
    "/{followup_id}/respond",
    response_model=FollowupRespondResponse,
    summary="Farmer follow-up response — closes the loop, may auto-escalate",
)
async def respond(
    followup_id: str,
    request: FollowupRespondRequest,
    service: Annotated[FollowUpService, Depends(get_followup_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FollowupRespondResponse:
    """PRD §5.10 / contract §2.12. Got Worse promotes severity, recomputes
    health via Phase 1's engine, and auto-escalates — returning the new
    case_id."""
    outcome = await service.respond(followup_id, request.response, request.image_asset_id)
    return _to_schema(outcome)
