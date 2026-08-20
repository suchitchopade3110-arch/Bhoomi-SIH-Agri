"""KVK Agronomist Portal API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.agronomist import (
    AgronomistQueueItem,
    ResolveCaseRequest,
    ResolveCaseResponse,
)
from app.schemas.case import CaseSummary

router = APIRouter(prefix="/agronomist", tags=["Agronomist Portal"])


@router.get(
    "/queue",
    response_model=list[AgronomistQueueItem],
    summary="Get queue of escalated cases assigned to agronomist KVK center",
)
async def get_queue() -> list[AgronomistQueueItem]:
    raise NotImplementedAPIError("Endpoint GET /agronomist/queue will be implemented in subsequent phases.")


@router.get(
    "/case/{escalation_id}",
    response_model=CaseSummary,
    summary="Get complete living case summary for review and prescription",
)
async def get_case_detail(escalation_id: str) -> CaseSummary:
    raise NotImplementedAPIError("Endpoint GET /agronomist/case/{escalation_id} will be implemented in subsequent phases.")


@router.post(
    "/resolve",
    response_model=ResolveCaseResponse,
    summary="Resolve case with expert diagnosis, prescription, and optional voice notes",
)
async def resolve_case(request: ResolveCaseRequest) -> ResolveCaseResponse:
    raise NotImplementedAPIError("Endpoint POST /agronomist/resolve will be implemented in subsequent phases.")
