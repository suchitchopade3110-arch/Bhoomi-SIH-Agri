"""Grounded, cited 5-point advisory API router (contract §2.11)."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.core.security import get_current_token_payload
from app.schemas.advisory import AdvisoryQueryRequest, AdvisoryQueryResponse, Citation, FivePointAdvisory
from app.services.rag.advisory_service import AdvisoryQueryOutcome, AdvisoryService, get_advisory_service

router = APIRouter(prefix="/advisory", tags=["Advisory & RAG"])


def _to_schema(outcome: AdvisoryQueryOutcome) -> AdvisoryQueryResponse:
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
    return AdvisoryQueryResponse(
        retrieved=outcome.retrieved,
        advisory=advisory,
        citations=citations,
        reason=outcome.reason,
        escalation_offered=outcome.escalation_offered,
        spoken_summary=outcome.spoken_summary,
        provider=outcome.provider,
        model=outcome.model,
    )


@router.post(
    "/query",
    response_model=AdvisoryQueryResponse,
    summary="Grounded, cited 5-point advisory for a standalone farmer query — or an honest no-source escalation",
)
async def query_advisory(
    request: AdvisoryQueryRequest,
    service: Annotated[AdvisoryService, Depends(get_advisory_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> AdvisoryQueryResponse:
    """PRD §5.7, §5.8 / contract §2.11. Retrieves only from the curated
    corpus; if nothing relevant is found (or the model can't ground an
    answer), returns ``retrieved: false`` rather than fabricating advice."""
    outcome = await service.answer_query(request.farm_id, request.query_text, target_type=request.target_type)
    return _to_schema(outcome)
