"""Extension Officer portal API router (contract §2.7 officer-portal section)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.security import get_current_token_payload
from app.schemas.officer import (
    OfficerActionRequest,
    OfficerActionResponse,
    OfficerQueueItem,
    OfficerReviewDetail,
)
from app.services.officer_service import OfficerService, get_officer_service

router = APIRouter(prefix="/officer", tags=["Officer Portal"])


@router.get(
    "/queue",
    response_model=list[OfficerQueueItem],
    summary="Get pending land verification queue for officer jurisdiction",
)
async def get_queue(
    service: Annotated[OfficerService, Depends(get_officer_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    district: Annotated[str | None, Query()] = None,
) -> list[OfficerQueueItem]:
    return await service.get_queue(district)


@router.get(
    "/review/{parcel_id}",
    response_model=OfficerReviewDetail,
    summary="Get detailed parcel boundary for editing",
)
async def get_review_detail(
    parcel_id: str,
    service: Annotated[OfficerService, Depends(get_officer_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> OfficerReviewDetail:
    return await service.get_parcel_detail(parcel_id)


@router.post(
    "/action",
    response_model=OfficerActionResponse,
    summary="Submit officer decision (verify boundary or reject) — contract §2.7 review endpoint",
)
async def process_action(
    request: OfficerActionRequest,
    service: Annotated[OfficerService, Depends(get_officer_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> OfficerActionResponse:
    return await service.process_action(request)
