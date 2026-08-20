"""Government Schemes and Subsidies API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.schemes import (
    SchemeListResponse,
    SchemeMatchRequest,
    SchemeResponse,
)

router = APIRouter(prefix="/schemes", tags=["Schemes & Subsidies"])


@router.post(
    "/match",
    response_model=SchemeListResponse,
    summary="Match eligible government subsidies and welfare schemes for a verified farm",
)
async def match_schemes(request: SchemeMatchRequest) -> SchemeListResponse:
    raise NotImplementedAPIError("Endpoint POST /schemes/match will be implemented in subsequent phases.")


@router.get(
    "/{scheme_id}",
    response_model=SchemeResponse,
    summary="Get details, benefits, and eligibility criteria for a specific scheme",
)
async def get_scheme(scheme_id: str) -> SchemeResponse:
    raise NotImplementedAPIError("Endpoint GET /schemes/{scheme_id} will be implemented in subsequent phases.")
