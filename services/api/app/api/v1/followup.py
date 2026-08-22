"""Closed-loop follow-up API router (contract §2.12, PRD §5.10)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.followup import (
    FollowupCheckinRequest,
    FollowupCheckinResponse,
)
from app.services.followup_service import FollowupService, get_followup_service

router = APIRouter(prefix="/followup", tags=["Closed-Loop Follow-up"])


@router.post(
    "/checkin",
    response_model=FollowupCheckinResponse,
    summary="Farmer check-in (Improved / No Change / Got Worse) with score adjustment",
)
async def checkin(
    request: FollowupCheckinRequest,
    service: Annotated[FollowupService, Depends(get_followup_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FollowupCheckinResponse:
    """PRD §5.10: "Got Worse past a threshold auto-escalates" — this
    version's threshold is "any Got Worse report" (see contract §2.12's own
    worked example, which auto-escalates on a single Got Worse)."""
    return await service.checkin(request)
