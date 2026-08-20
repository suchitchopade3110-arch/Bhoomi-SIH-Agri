"""Cadastral Land Verification API router."""

from fastapi import APIRouter, status
from app.core.errors import NotImplementedAPIError
from app.schemas.land import (
    CadastralLookupRequest,
    CadastralLookupResponse,
    LandVerifyRequest,
    LandVerifyResponse,
)

router = APIRouter(prefix="/land", tags=["Land & Cadastral"])


@router.post(
    "/cadastral-lookup",
    response_model=CadastralLookupResponse,
    summary="Automated cadastral boundary lookup from revenue records",
)
async def cadastral_lookup(request: CadastralLookupRequest) -> CadastralLookupResponse:
    raise NotImplementedAPIError("Endpoint POST /land/cadastral-lookup will be implemented in subsequent phases.")


@router.post(
    "/verify",
    response_model=LandVerifyResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit land parcel for human-in-the-loop officer verification",
)
async def submit_land_verification(request: LandVerifyRequest) -> LandVerifyResponse:
    raise NotImplementedAPIError("Endpoint POST /land/verify will be implemented in subsequent phases.")


@router.get(
    "/{farm_id}",
    response_model=LandVerifyResponse,
    summary="Get land verification status for farm",
)
async def get_land_status(farm_id: str) -> LandVerifyResponse:
    raise NotImplementedAPIError("Endpoint GET /land/{farm_id} will be implemented in subsequent phases.")
