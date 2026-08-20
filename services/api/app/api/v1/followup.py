"""Closed-loop follow-up API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.followup import (
    FollowupCheckinRequest,
    FollowupCheckinResponse,
)

router = APIRouter(prefix="/followup", tags=["Closed-Loop Follow-up"])


@router.post(
    "/checkin",
    response_model=FollowupCheckinResponse,
    summary="Farmer check-in (Improved / No Change / Got Worse) with score adjustment",
)
async def checkin(request: FollowupCheckinRequest) -> FollowupCheckinResponse:
    raise NotImplementedAPIError("Endpoint POST /followup/checkin will be implemented in subsequent phases.")
