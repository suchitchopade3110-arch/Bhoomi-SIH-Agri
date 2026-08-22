"""Government Schemes and Subsidies API router (contract §2.14)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.schemes import (
    SchemeListResponse,
    SchemeMatchRequest,
    SchemeResponse,
)
from app.services.scheme_service import SchemeService, get_scheme_service

router = APIRouter(prefix="/schemes", tags=["Schemes & Subsidies"])


@router.post(
    "/match",
    response_model=SchemeListResponse,
    summary="Match eligible government subsidies for a verified farm (LAND_NOT_VERIFIED if not yet verified)",
)
async def match_schemes(
    request: SchemeMatchRequest,
    service: Annotated[SchemeService, Depends(get_scheme_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> SchemeListResponse:
    """PRD §5.12 / contract §2.14: gated on ``land_status=verified`` — never
    tells a farmer they qualify based on unverified land. Every matched
    scheme carries its ``last_verified`` date."""
    return await service.match_schemes_for_farm(request)


@router.get(
    "/{scheme_id}",
    response_model=SchemeResponse,
    summary="Get details, benefits, and eligibility criteria for a specific scheme",
)
async def get_scheme(
    scheme_id: str,
    service: Annotated[SchemeService, Depends(get_scheme_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> SchemeResponse:
    return await service.get_scheme_by_id(scheme_id)
