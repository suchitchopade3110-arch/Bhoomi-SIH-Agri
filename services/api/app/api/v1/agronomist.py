"""KVK Agronomist Portal API router (contract §2.13)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.security import get_current_token_payload
from app.models.case import Case
from app.schemas.case import CaseHealthRef, CaseProblemRef, CaseQueueItem
from app.schemas.agronomist import CaseQueueResponse
from app.services.escalation.escalation_service import EscalationService, get_escalation_service

router = APIRouter(prefix="/agronomist", tags=["Agronomist Portal"])

DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100


def _to_queue_item(case: Case) -> CaseQueueItem:
    summary = case.summary or {}
    problem = summary.get("problem")
    current_health = summary.get("current_health") or {"score": None, "band": "unrated"}
    return CaseQueueItem(
        case_id=case.id,
        farm_id=case.farm_id,
        problem=CaseProblemRef(**problem) if problem else None,
        status=case.status,
        assigned_to=case.assigned_to,
        trigger=case.trigger,
        current_health=CaseHealthRef(**current_health),
        created_at=case.created_at,
    )


@router.get(
    "/case-queue",
    response_model=CaseQueueResponse,
    summary="Assigned cases, newest first",
)
async def get_case_queue(
    escalation_service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    assigned_to: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_LIMIT)] = DEFAULT_PAGE_LIMIT,
    cursor: Annotated[str | None, Query()] = None,
) -> CaseQueueResponse:
    """PRD §5.11 / contract §2.13's ``GET /agronomist/case-queue``."""
    cases, next_cursor = await escalation_service.list_queue(assigned_to=assigned_to, limit=limit, cursor=cursor)
    return CaseQueueResponse(items=[_to_queue_item(c) for c in cases], next_cursor=next_cursor)
