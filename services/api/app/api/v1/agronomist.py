"""KVK Agronomist Portal API router (contract §2.13 agronomist-portal section)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.agronomist import (
    AgronomistQueueItem,
    ResolveCaseRequest,
    ResolveCaseResponse,
)
from app.schemas.case import CaseSummary
from app.services.agronomist_service import AgronomistService, get_agronomist_service

router = APIRouter(prefix="/agronomist", tags=["Agronomist Portal"])


@router.get(
    "/queue",
    response_model=list[AgronomistQueueItem],
    summary="Get queue of escalated cases assigned to agronomist KVK center",
)
async def get_queue(
    service: Annotated[AgronomistService, Depends(get_agronomist_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> list[AgronomistQueueItem]:
    return await service.get_queue()


@router.get(
    "/case/{escalation_id}",
    response_model=CaseSummary,
    summary="Get complete living case summary for review and prescription",
)
async def get_case_detail(
    escalation_id: str,
    service: Annotated[AgronomistService, Depends(get_agronomist_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> CaseSummary:
    return await service.get_case_detail(escalation_id)


@router.post(
    "/resolve",
    response_model=ResolveCaseResponse,
    summary="Resolve case with expert diagnosis, prescription, and optional voice notes",
)
async def resolve_case(
    request: ResolveCaseRequest,
    service: Annotated[AgronomistService, Depends(get_agronomist_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> ResolveCaseResponse:
    """PRD §7.4: resolution clears the problem and lifts monitoring/
    treatment sub-indices, which is why the score recovers above baseline."""
    return await service.resolve_case(request)
