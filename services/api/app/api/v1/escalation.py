"""Expert Escalation API router."""

from fastapi import APIRouter, status
from app.core.errors import NotImplementedAPIError
from app.schemas.escalation import (
    EscalationCreateRequest,
    EscalationResponse,
)

router = APIRouter(prefix="/escalation", tags=["Expert Escalation"])


@router.post(
    "/create",
    response_model=EscalationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create escalation case and package living case file for KVK agronomist",
)
async def create_escalation(request: EscalationCreateRequest) -> EscalationResponse:
    raise NotImplementedAPIError("Endpoint POST /escalation/create will be implemented in subsequent phases.")


@router.get(
    "/{escalation_id}",
    response_model=EscalationResponse,
    summary="Get escalation case details and status",
)
async def get_escalation(escalation_id: str) -> EscalationResponse:
    raise NotImplementedAPIError("Endpoint GET /escalation/{escalation_id} will be implemented in subsequent phases.")
