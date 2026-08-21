"""Escalation & Case Management API router (Phase 4, contract §2.12/§2.13):
manual problem escalation, the closed-loop follow-up response, case
resolution, and the agronomist case reads. Zero business logic here — see
``app.services.escalation``.

These paths are additive to (not a replacement for) the Phase-0 scaffold
still living in ``escalation.py``/``followup.py``/``agronomist.py`` — see
the Phase 4 hand-off notes for why both currently exist.
"""

from typing import Annotated, Any
from uuid import uuid4

from fastapi import APIRouter, Depends, Query, status

from app.core.enums import CaseStatus, HealthBand, UserRole
from app.core.security import get_current_token_payload, require_roles
from app.models.health_snapshot import HealthSnapshot as HealthSnapshotRow
from app.schemas.agronomist import AgronomistQueueItem, ResolveCaseResponse
from app.schemas.case import CaseSummary
from app.schemas.escalation import CaseResolveRequest, EscalationResponse, ProblemEscalateRequest
from app.schemas.followup import FollowupCheckinRequest, FollowupCheckinResponse
from app.schemas.health import HealthSnapshot as HealthSnapshotSchema, SubIndexBreakdown
from app.services.escalation.escalation_service import EscalationService, get_escalation_service
from app.services.escalation.followup_service import FollowupService, get_followup_service
from app.services.escalation.resolve_service import ResolveService, get_resolve_service

router = APIRouter(tags=["Escalation & Case Management"])


def _snapshot_to_schema(row: HealthSnapshotRow) -> HealthSnapshotSchema:
    """Minimal ``HealthSnapshot`` mapping for embedding inside another
    response (contract §2.9's own spoken summary — see ``api/v1/health.py``
    — doesn't apply here; the follow-up response carries its own)."""
    return HealthSnapshotSchema(
        score=row.score,
        band=HealthBand(row.band),
        computed_at=row.computed_at,
        weights_version=row.weights_version,
        subindices=[SubIndexBreakdown(**s) for s in row.subindices],
        triggering_input=row.triggering_input,
        missing_fields=row.missing_fields,
    )


@router.post(
    "/problems/{problem_id}/escalate",
    response_model=EscalationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Manually escalate a problem to a KVK agronomist (living case file handoff)",
)
async def escalate_problem(
    problem_id: str,
    request: ProblemEscalateRequest,
    service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> EscalationResponse:
    """Phase 4 item 6. One of the four escalation triggers (item 1) — the
    farmer/officer-initiated one; the other three fire automatically from
    ``DiagnosisService``/``FollowupService``."""
    result = await service.create_escalation(
        farm_id=request.farm_id,
        trigger_type="manual",
        reason=request.reason,
        severity=request.severity,
        problem_id=problem_id,
        notes=request.notes,
    )
    return EscalationResponse(
        escalation_id=result.case_id,
        farm_id=result.farm_id,
        status=result.status,
        severity=result.severity,
        assigned_kvk_center=result.assigned_kvk_center,
        case_summary=result.case_summary,
        created_at=result.created_at,
        spoken_summary=result.case_summary.spoken_summary,
    )


@router.get(
    "/cases/{case_id}",
    response_model=CaseSummary,
    summary="Get the complete Living Case Summary for expert review (contract §2.13)",
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
    summary="Get the KVK agronomist case queue",
)
async def get_case_queue(
    service: Annotated[EscalationService, Depends(get_escalation_service)],
    _auth: Annotated[dict[str, Any], Depends(require_roles([UserRole.AGRONOMIST]))],
    case_status: Annotated[CaseStatus | None, Query(alias="status")] = None,
) -> list[AgronomistQueueItem]:
    return await service.get_queue(case_status)


@router.post(
    "/followups/{problem_id}/respond",
    response_model=FollowupCheckinResponse,
    summary="Farmer follow-up response — closes the loop, promotes severity, and may auto-escalate (contract §2.12)",
)
async def respond_to_followup(
    problem_id: str,
    request: FollowupCheckinRequest,
    service: Annotated[FollowupService, Depends(get_followup_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> FollowupCheckinResponse:
    outcome = await service.respond(
        problem_id=problem_id,
        farm_id=request.farm_id,
        response=request.response,
        farmer_notes=request.farmer_notes,
        photo_asset_id=request.photo_asset_id,
    )
    spoken_summary = (
        "This sounds serious — I've sent it to an expert."
        if outcome.auto_escalated
        else "Thanks for the update. I've recorded your farm's progress."
    )
    return FollowupCheckinResponse(
        followup_id=str(uuid4()),
        advisory_id=request.advisory_id,
        response=request.response,
        auto_escalated=outcome.auto_escalated,
        escalation_id=outcome.escalation_id,
        updated_health_snapshot=_snapshot_to_schema(outcome.snapshot),
        spoken_summary=spoken_summary,
    )


@router.post(
    "/cases/{case_id}/resolve",
    response_model=ResolveCaseResponse,
    summary="Agronomist resolves a case — clears the problem and recovers the health score (contract §2.13)",
)
async def resolve_case(
    case_id: str,
    request: CaseResolveRequest,
    service: Annotated[ResolveService, Depends(get_resolve_service)],
    _auth: Annotated[dict[str, Any], Depends(require_roles([UserRole.AGRONOMIST]))],
) -> ResolveCaseResponse:
    resolution = await service.resolve(
        case_id=case_id,
        agronomist_id=request.agronomist_id,
        agronomist_name=request.agronomist_name,
        confirmed_diagnosis=request.confirmed_diagnosis,
        expert_advice=request.expert_advice,
        prescribed_inputs=request.prescribed_inputs,
    )
    return ResolveCaseResponse(escalation_id=resolution.case_id, status=resolution.status)
