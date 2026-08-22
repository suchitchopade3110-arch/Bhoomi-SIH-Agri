"""Farms API router (contract §2.6)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_token_payload
from app.schemas.farm import (
    FarmCreateRequest,
    FarmResponse,
    FarmSummaryResponse,
    FarmUpdateRequest,
)
from app.services.farm_service import FarmService, get_farm_service

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new farm profile",
)
async def create_farm(
    request: FarmCreateRequest,
    service: Annotated[FarmService, Depends(get_farm_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmResponse:
    return await service.create_farm(request)


@router.get(
    "/{farm_id}",
    response_model=FarmResponse,
    summary="Get farm details by UUID",
)
async def get_farm(
    farm_id: str,
    service: Annotated[FarmService, Depends(get_farm_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmResponse:
    return await service.get_farm(farm_id)


@router.put(
    "/{farm_id}",
    response_model=FarmResponse,
    summary="Update farm profile details",
)
async def update_farm(
    farm_id: str,
    request: FarmUpdateRequest,
    service: Annotated[FarmService, Depends(get_farm_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmResponse:
    return await service.update_farm(farm_id, request)


@router.get(
    "/{farm_id}/summary",
    response_model=FarmSummaryResponse,
    summary="Get comprehensive farm summary with weather, health, and open tasks",
)
async def get_farm_summary(
    farm_id: str,
    service: Annotated[FarmService, Depends(get_farm_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmSummaryResponse:
    return await service.get_farm_summary(farm_id)
