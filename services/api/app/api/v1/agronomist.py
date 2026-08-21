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
    summary="[Superseded by GET /agronomist/case-queue] Get queue of escalated cases",
    deprecated=True,
)
async def get_queue() -> list[AgronomistQueueItem]:
    raise NotImplementedAPIError("Superseded by GET /agronomist/case-queue (contract §2.13).")


@router.get(
    "/case/{escalation_id}",
    response_model=CaseSummary,
    summary="[Superseded by GET /cases/{case_id}] Get complete living case summary",
    deprecated=True,
)
async def get_case_detail(escalation_id: str) -> CaseSummary:
    raise NotImplementedAPIError("Superseded by GET /cases/{case_id} (contract §2.13).")


@router.post(
    "/resolve",
    response_model=ResolveCaseResponse,
    summary="[Superseded by POST /cases/{case_id}/resolve] Resolve case with expert diagnosis",
    deprecated=True,
)
async def resolve_case(request: ResolveCaseRequest) -> ResolveCaseResponse:
    raise NotImplementedAPIError("Superseded by POST /cases/{case_id}/resolve (contract §2.13).")
