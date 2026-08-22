"""Expert Escalation API router (contract §2.13)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.core.security import get_current_token_payload
from app.schemas.escalation import (
    EscalationCreateRequest,
    EscalationResponse,
)
from app.services.escalation_service import EscalationService, get_escalation_service

router = APIRouter(prefix="/escalation", tags=["Expert Escalation"])


@router.post(
    "/create",
    response_model=EscalationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create escalation case and package living case file for KVK agronomist",
)
async def create_escalation(
    request: EscalationCreateRequest,
    service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> EscalationResponse:
    return await service.create_escalation(request)


@router.get(
    "/{escalation_id}",
    response_model=EscalationResponse,
    summary="Get escalation case details and status",
)
async def get_escalation(
    escalation_id: str,
    service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> EscalationResponse:
    return await service.get_escalation_by_id(escalation_id)
