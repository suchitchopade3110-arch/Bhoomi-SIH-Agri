"""Extension Officer portal API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.officer import (
    OfficerActionRequest,
    OfficerActionResponse,
    OfficerQueueItem,
    OfficerReviewDetail,
)

router = APIRouter(prefix="/officer", tags=["Officer Portal"])


@router.get(
    "/queue",
    response_model=list[OfficerQueueItem],
    summary="Get pending land verification queue for officer jurisdiction",
)
async def get_queue() -> list[OfficerQueueItem]:
    raise NotImplementedAPIError("Endpoint GET /officer/queue will be implemented in subsequent phases.")


@router.get(
    "/review/{parcel_id}",
    response_model=OfficerReviewDetail,
    summary="Get detailed parcel boundary and satellite overlay for editing",
)
async def get_review_detail(parcel_id: str) -> OfficerReviewDetail:
    raise NotImplementedAPIError("Endpoint GET /officer/review/{parcel_id} will be implemented in subsequent phases.")


@router.post(
    "/action",
    response_model=OfficerActionResponse,
    summary="Submit officer decision (verify boundary or reject)",
)
async def process_action(request: OfficerActionRequest) -> OfficerActionResponse:
    raise NotImplementedAPIError("Endpoint POST /officer/action will be implemented in subsequent phases.")
