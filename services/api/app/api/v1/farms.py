"""Farms API router."""

from fastapi import APIRouter, status
from app.core.errors import NotImplementedAPIError
from app.schemas.farm import (
    FarmCreateRequest,
    FarmResponse,
    FarmSummaryResponse,
    FarmUpdateRequest,
)

router = APIRouter(prefix="/farms", tags=["Farms"])


@router.post(
    "",
    response_model=FarmResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new farm profile",
)
async def create_farm(request: FarmCreateRequest) -> FarmResponse:
    raise NotImplementedAPIError("Endpoint POST /farms will be implemented in subsequent phases.")


@router.get(
    "/{farm_id}",
    response_model=FarmResponse,
    summary="Get farm details by UUID",
)
async def get_farm(farm_id: str) -> FarmResponse:
    raise NotImplementedAPIError("Endpoint GET /farms/{farm_id} will be implemented in subsequent phases.")


@router.put(
    "/{farm_id}",
    response_model=FarmResponse,
    summary="Update farm profile details",
)
async def update_farm(farm_id: str, request: FarmUpdateRequest) -> FarmResponse:
    raise NotImplementedAPIError("Endpoint PUT /farms/{farm_id} will be implemented in subsequent phases.")


@router.get(
    "/{farm_id}/summary",
    response_model=FarmSummaryResponse,
    summary="Get comprehensive farm summary with weather, health, and open tasks",
)
async def get_farm_summary(farm_id: str) -> FarmSummaryResponse:
    raise NotImplementedAPIError("Endpoint GET /farms/{farm_id}/summary will be implemented in subsequent phases.")
