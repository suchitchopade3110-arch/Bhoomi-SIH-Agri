"""Escalation & Case Management API router (Phase 4, contract §2.12/§2.13):
manual problem escalation, the closed-loop follow-up response, case
resolution, and the agronomist case reads. Zero business logic here — see
``app.services.escalation``.

These paths are additive to (not a replacement for) the Phase-0 scaffold
still living in ``escalation.py``/``followup.py``/``agronomist.py`` — see
the Phase 4 hand-off notes for why both currently exist.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query, status

from app.core.enums import CaseStatus, UserRole
from app.core.security import get_current_token_payload, require_roles
from app.schemas.agronomist import AgronomistQueueItem
from app.schemas.case import CaseSummary
from app.schemas.escalation import (
    CaseResolveRequest,
    CaseResolveResponse,
    ProblemEscalateRequest,
    ProblemEscalateResponse,
)
from app.schemas.followup import FollowupRespondRequest, FollowupRespondResponse, SeverityChange
from app.schemas.common import HealthMovement
from app.services.escalation.escalation_service import EscalationService, get_escalation_service
from app.services.escalation.followup_service import FollowupService, get_followup_service
from app.services.escalation.resolve_service import ResolveService, get_resolve_service

router = APIRouter(tags=["Escalation & Case Management"])


@router.post(
    "/problems/{problem_id}/escalate",
    response_model=ProblemEscalateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Escalate a problem to a KVK agronomist — compiles the Living Case Summary and routes it (contract §2.13)",
)
async def escalate_problem(
    problem_id: str,
    request: ProblemEscalateRequest,
    service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> ProblemEscalateResponse:
    """Contract §2.13. One of the four escalation triggers (Phase 4 item 1)
    — the farmer/officer-initiated one; the other three fire automatically
    from ``DiagnosisService``/``FollowupService``."""
    result = await service.create_escalation(
        farm_id=request.farm_id,
        trigger_type="manual",
        reason=request.reason,
        severity=request.severity,
        problem_id=problem_id,
        notes=request.notes,
    )
    return ProblemEscalateResponse(
        case_id=result.case_id,
        assigned_to=result.assigned_to,
        status=result.status,
        spoken_summary=f"Your problem has been sent to {result.assigned_to}.",
    )


@router.get(
    "/cases/{case_id}",
    response_model=CaseSummary,
    summary="Get the pre-analyzed case bundle for expert review (contract §2.13)",
)
async def get_case(
    case_id: str,
    service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> CaseSummary:
    return await service.get_case(case_id)


@router.get(
    "/agronomist/case-queue",
    response_model=list[AgronomistQueueItem],
    summary="Get the KVK agronomist's assigned cases, newest first (contract §2.13)",
)
async def get_case_queue(
    service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(require_roles([UserRole.AGRONOMIST]))],
    case_status: Annotated[CaseStatus | None, Query(alias="status")] = None,
) -> list[AgronomistQueueItem]:
    return await service.get_queue(case_status)


@router.post(
    "/followups/{problem_id}/respond",
    response_model=FollowupRespondResponse,
    summary="Farmer follow-up response — closes the loop, promotes severity, and may auto-escalate (contract §2.12)",
)
async def respond_to_followup(
    problem_id: str,
    request: FollowupRespondRequest,
    service: Annotated[FollowupService, Depends(get_followup_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FollowupRespondResponse:
    outcome = await service.respond(
        problem_id=problem_id, response=request.response, image_asset_id=request.image_asset_id
    )
    severity_change = (
        SeverityChange(**{"from": outcome.severity_from, "to": outcome.severity_to})
        if outcome.severity_from is not None
        else None
    )
    spoken_summary = (
        "This sounds serious — I've sent it to an expert."
        if outcome.escalated
        else "Thanks for the update. I've recorded your farm's progress."
    )
    return FollowupRespondResponse(
        problem_id=outcome.problem_id,
        severity_change=severity_change,
        health=HealthMovement(**{"from": outcome.health_from, "to": outcome.health_to, "band": outcome.health_band}),
        escalated=outcome.escalated,
        case_id=outcome.case_id,
        spoken_summary=spoken_summary,
    )


@router.post(
    "/cases/{case_id}/resolve",
    response_model=CaseResolveResponse,
    summary="Agronomist resolves a case — clears the problem and recovers the health score (contract §2.13)",
)
async def resolve_case(
    case_id: str,
    request: CaseResolveRequest,
    service: Annotated[ResolveService, Depends(get_resolve_service)],
    _auth: Annotated[dict[str, Any], Depends(require_roles([UserRole.AGRONOMIST]))],
) -> CaseResolveResponse:
    resolution = await service.resolve(
        case_id=case_id, diagnosis=request.diagnosis, treatment=request.treatment, notes=request.notes
    )
    return CaseResolveResponse(
        case_id=resolution.case_id,
        status=resolution.status,
        problem_status=resolution.problem_status,
        health=HealthMovement(
            **{"from": resolution.health_from, "to": resolution.health_to, "band": resolution.health_band}
        ),
    )
