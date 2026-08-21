"""Gated image+voice diagnosis API router (contract §2.10)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.advisory import Citation, FivePointAdvisory
from app.schemas.diagnosis import DiagnoseRequest, DiagnoseResponse, DiagnosisResult, EscalationRef, HealthDelta
from app.services.diagnosis_service import DiagnoseOutcome, DiagnosisService, get_diagnosis_service

router = APIRouter(prefix="/farms", tags=["Diagnosis & Advisory"])


def _to_schema(outcome: DiagnoseOutcome) -> DiagnoseResponse:
    diagnosis = (
        DiagnosisResult(label=outcome.label, stage=outcome.stage, confidence=outcome.confidence)
        if outcome.above_gate
        else None
    )
    advisory = (
        FivePointAdvisory(
            possible_issue=outcome.advisory.possible_issue,
            what_to_check=outcome.advisory.what_to_check,
            what_to_do_next=outcome.advisory.what_to_do_next,
            what_to_avoid=outcome.advisory.what_to_avoid,
            expert_triggers=outcome.advisory.expert_triggers,
        )
        if outcome.advisory
        else None
    )
    citations = [Citation(doc_id=c.doc_id, title=c.title, reviewed_on=c.reviewed_on) for c in outcome.citations]
    health_delta = (
        HealthDelta(from_=outcome.health_delta_from, to=outcome.health_delta_to) if outcome.above_gate else None
    )
    escalation = (
        EscalationRef(case_id=outcome.escalation.case_id, assigned_to=outcome.escalation.assigned_to)
        if outcome.escalation
        else None
    )
    return DiagnoseResponse(
        above_gate=outcome.above_gate,
        problem_id=outcome.problem_id,
        diagnosis=diagnosis,
        advisory=advisory,
        citations=citations,
        health_delta=health_delta,
        reason=outcome.reason,
        escalation=escalation,
        spoken_summary=outcome.spoken_summary,
    )


@router.post(
    "/{farm_id}/diagnose",
    response_model=DiagnoseResponse,
    summary="Confidence-gated image+voice diagnosis — grounded advisory, or an honest escalation",
)
async def diagnose(
    farm_id: str,
    request: DiagnoseRequest,
    service: Annotated[DiagnosisService, Depends(get_diagnosis_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> DiagnoseResponse:
    """PRD §5.6, §5.7 / contract §2.10. Combines the image model's
    confidence with RAG retrieval relevance in the confidence gate — below
    either threshold, or an out-of-scope crop/disease, always escalates
    instead of composing advice the model isn't sure of."""
    outcome = await service.diagnose(farm_id, request.image_asset_id, request.description_text)
    return _to_schema(outcome)
