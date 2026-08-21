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
    summary="[Superseded by POST /problems/{problem_id}/escalate] Create escalation case",
    deprecated=True,
)
async def create_escalation(request: EscalationCreateRequest) -> EscalationResponse:
    raise NotImplementedAPIError("Superseded by POST /problems/{problem_id}/escalate (contract §2.13).")


@router.get(
    "/{escalation_id}",
    response_model=EscalationResponse,
    summary="[Superseded by GET /cases/{case_id}] Get escalation case details and status",
    deprecated=True,
)
async def get_escalation(escalation_id: str) -> EscalationResponse:
    raise NotImplementedAPIError("Superseded by GET /cases/{case_id} (contract §2.13).")
