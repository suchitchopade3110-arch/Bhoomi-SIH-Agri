"""Land Verification API router (contract §2.7). HITL-only — no automated
cadastral lookup (SIH26131 feature checklist §13.3: "cut")."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_token_payload
from app.schemas.land import (
    LandVerifyRequest,
    LandVerifyResponse,
)
from app.services.land_service import LandService, get_land_service

router = APIRouter(prefix="/land", tags=["Land & Cadastral"])


@router.post(
    "/verify",
    response_model=LandVerifyResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Submit land parcel — always queues for HITL officer review (SIH26131: no auto-lookup)",
)
async def submit_land_verification(
    request: LandVerifyRequest,
    service: Annotated[LandService, Depends(get_land_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> LandVerifyResponse:
    """Contract §2.7, as narrowed by SIH26131 feature checklist §10/§13:
    every submission queues to the officer — there is no automated
    cadastral lookup that can verify a parcel without a human."""
    return await service.submit_for_verification(request)


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
