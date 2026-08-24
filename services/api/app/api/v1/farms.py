"""Farms API router (contract §2.6)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.core.config import Settings, get_settings
from app.core.errors import NotFoundError
from app.core.security import get_current_token_payload
from app.repositories.dependencies import get_farm_repository
from app.repositories.interfaces import FarmRepository
from app.schemas.farm import (
    FarmCreateRequest,
    FarmResponse,
    FarmRiskTrendResponse,
    FarmSummaryResponse,
    FarmSummaryTrendResponse,
    FarmUpdateRequest,
)
from app.schemas.land import ThinLandSubmissionRequest, ThinLandSubmissionResponse
from app.schemas.schemes import SchemeListResponse, SchemeMatchRequest
from app.services.farm_service import FarmService, get_farm_service
from app.services.health_service import HealthService, get_health_service
from app.services.scheme_service import SchemeService, get_scheme_service

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
    "/{farm_id}/risk",
    response_model=FarmRiskTrendResponse,
    summary="Get qualitative crop condition risk summary (SIH26131)",
)
async def get_farm_risk(
    farm_id: str,
    health_service: Annotated[HealthService, Depends(get_health_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmRiskTrendResponse:
    return await health_service.get_farm_risk(farm_id)


@router.get(
    "/{farm_id}/summary",
    response_model=FarmSummaryResponse | FarmSummaryTrendResponse,
    summary="Get comprehensive farm summary with weather, health, and open tasks",
)
async def get_farm_summary(
    farm_id: str,
    service: Annotated[FarmService, Depends(get_farm_service)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    settings: Annotated[Settings, Depends(get_settings)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FarmSummaryResponse | FarmSummaryTrendResponse:
    if settings.PROBLEM_STATEMENT == "sih26131":
        farm = await service.get_farm(farm_id)
        return await health_service.get_farm_summary_trend(
            farm_id=farm_id,
            farm_name=farm.farm_name,
            village=farm.village,
            primary_crop=farm.primary_crop,
        )
    return await service.get_farm_summary(farm_id)


@router.post(
    "/{farm_id}/land",
    response_model=ThinLandSubmissionResponse,
    summary="Submit cadastral survey number for thin land verification (trust side-feature)",
)
async def submit_farm_land(
    farm_id: str,
    request: ThinLandSubmissionRequest,
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> ThinLandSubmissionResponse:
    """Thin land submission endpoint (trust side-feature).

    Takes a survey number, stores it on the farm profile, and sets
    land_status to 'pending_verification'. Zero spatial geometry,
    zero auto-lookup mock.
    """
    farm = await farm_repo.get_by_id(farm_id)
    if farm is None:
        raise NotFoundError("Farm not found.", details={"farm_id": farm_id})

    await farm_repo.update(farm_id, {
        "survey_number": request.survey_number,
        "land_status": "pending_verification",
    })

    return ThinLandSubmissionResponse(
        farm_id=farm_id,
        survey_number=request.survey_number,
        status="pending_verification",
    )


@router.get(
    "/{farm_id}/schemes",
    response_model=SchemeListResponse,
    summary="Get eligible government subsidies for a verified farm",
)
async def get_farm_schemes(
    farm_id: str,
    service: Annotated[SchemeService, Depends(get_scheme_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> SchemeListResponse:
    """PRD §5.12 / contract §2.14: gated on land_status=verified (409 LAND_NOT_VERIFIED if unverified)."""
    return await service.match_schemes_for_farm(SchemeMatchRequest(farm_id=farm_id))


