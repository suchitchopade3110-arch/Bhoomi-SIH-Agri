"""Farm Living Timeline API router (contract §2.12, PRD §5.9)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.timeline import (
    TimelineEventResponse,
    TimelineResponse,
)
from app.services.timeline_service import TimelineService, get_timeline_service

router = APIRouter(prefix="/timeline", tags=["Timeline & Cases"])


@router.get(
    "/{farm_id}",
    response_model=TimelineResponse,
    summary="Get continuous case timeline and milestones for farm",
)
async def get_timeline(
    farm_id: str,
    service: Annotated[TimelineService, Depends(get_timeline_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> TimelineResponse:
    return await service.get_timeline(farm_id)


@router.post(
    "/events",
    response_model=TimelineEventResponse,
    summary="Append a client-side annotation event to a farm's timeline",
)
async def append_event(
    event: TimelineEventResponse,
    service: Annotated[TimelineService, Depends(get_timeline_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> TimelineEventResponse:
    return await service.append_event(event)
