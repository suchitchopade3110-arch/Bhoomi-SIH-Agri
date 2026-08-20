"""Farm Living Timeline API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.timeline import (
    TimelineEventResponse,
    TimelineResponse,
)

router = APIRouter(prefix="/timeline", tags=["Timeline & Cases"])


@router.get(
    "/{farm_id}",
    response_model=TimelineResponse,
    summary="Get continuous case timeline and milestones for farm",
)
async def get_timeline(farm_id: str) -> TimelineResponse:
    raise NotImplementedAPIError("Endpoint GET /timeline/{farm_id} will be implemented in subsequent phases.")


@router.post(
    "/events",
    response_model=TimelineEventResponse,
    summary="Append an event to the farm timeline",
)
async def append_event(event: TimelineEventResponse) -> TimelineEventResponse:
    raise NotImplementedAPIError("Endpoint POST /timeline/events will be implemented in subsequent phases.")
