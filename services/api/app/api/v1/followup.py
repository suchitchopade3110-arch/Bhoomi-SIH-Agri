"""Closed-loop follow-up API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.followup import (
    FollowupRespondRequest,
    FollowupRespondResponse,
)

router = APIRouter(prefix="/followup", tags=["Closed-Loop Follow-up"])


@router.post(
    "/checkin",
    response_model=FollowupRespondResponse,
    summary="[Superseded by POST /followups/{problem_id}/respond] Farmer check-in with score adjustment",
    deprecated=True,
)
async def checkin(request: FollowupRespondRequest) -> FollowupRespondResponse:
    raise NotImplementedAPIError("Superseded by POST /followups/{problem_id}/respond (contract §2.12).")
