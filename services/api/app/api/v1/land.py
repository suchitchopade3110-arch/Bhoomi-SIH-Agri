"""Cadastral Land Verification API router (contract §2.7)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Response, status

from app.core.enums import LandStatus
from app.core.security import get_current_token_payload
from app.schemas.land import (
    CadastralLookupRequest,
    CadastralLookupResponse,
    LandVerifyRequest,
    LandVerifyResponse,
)
from app.services.land_service import LandService, get_land_service

router = APIRouter(prefix="/land", tags=["Land & Cadastral"])


@router.post(
    "/cadastral-lookup",
    response_model=CadastralLookupResponse,
    summary="Automated cadastral boundary lookup from revenue records",
)
async def cadastral_lookup(
    request: CadastralLookupRequest,
    service: Annotated[LandService, Depends(get_land_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> CadastralLookupResponse:
    return await service.lookup_cadastral_record(request)


@router.post(
    "/verify",
    response_model=LandVerifyResponse,
    summary="Submit land parcel — auto-verifies on a matched cadastral lookup (200), else queues for HITL officer review (202)",
)
async def submit_land_verification(
    request: LandVerifyRequest,
    response: Response,
    service: Annotated[LandService, Depends(get_land_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> LandVerifyResponse:
    """Contract §2.7: 200 when auto-lookup matched (verified immediately),
    202 when it fell into HITL (queued to the officer) — the common case."""
    result = await service.submit_for_verification(request)
    response.status_code = (
        status.HTTP_200_OK if result.status == LandStatus.VERIFIED else status.HTTP_202_ACCEPTED
    )
    return result


@router.get(
    "/{farm_id}",
    response_model=LandVerifyResponse,
    summary="Get land verification status for farm",
)
async def get_land_status(
    farm_id: str,
    service: Annotated[LandService, Depends(get_land_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> LandVerifyResponse:
    return await service.get_land_status(farm_id)
