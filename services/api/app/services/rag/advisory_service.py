"""Orchestrates POST /advisory/query (contract §2.11): retrieval -> gate ->
grounded generation -> parse, or an honest no-retrieval escalation. No
decision logic lives here — retrieval scoring is services/rag/retrieval.py,
the compose-vs-escalate call is domain.gate.decide, and output validation is
domain.rag.parse_advisory_output.
"""

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_llm_adapter
from app.adapters.ports import LLMPort
from app.core.config import Settings, get_settings
from app.domain.gate import decide
from app.domain.rag import FivePointAdvisory, GroundedCitation, parse_advisory_output
from app.repositories.interfaces import RetrievedChunk
from app.services.rag.retrieval import RetrievalService, get_retrieval_service

# The contract's fixed literal for the no-retrieval branch (contract §2.11) —
# distinct from the gate's more detailed internal `reason` sentence, which is
# used for the /diagnose endpoint's differently-shaped reason field instead.
NO_RELEVANT_SOURCE_REASON = "no_relevant_source"

NO_SOURCE_SPOKEN_SUMMARY = "I don't have reliable information for this. Should I send it to an expert?"
COMPOSED_SPOKEN_SUMMARY = "Here's what I found, with sources."


@dataclass(frozen=True)
class AdvisoryQueryOutcome:
    """Result of one advisory query — exactly one of the two contract §2.11
    response shapes, never a mix."""

    retrieved: bool
    advisory: FivePointAdvisory | None
    citations: list[GroundedCitation]
    reason: str | None
    escalation_offered: bool | None
    spoken_summary: str


def _chunk_to_dict(chunk: RetrievedChunk) -> dict:
    return {
        "doc_id": chunk.doc_id,
        "title": chunk.title,
        "reviewed_on": chunk.reviewed_on,
        "chunk_text": chunk.chunk_text,
    }


class AdvisoryService:
    """Grounded, cited 5-point advisory for a standalone farmer query (PRD §5.7)."""

    def __init__(self, retrieval: RetrievalService, llm_port: LLMPort, settings: Settings) -> None:
        self._retrieval = retrieval
        self._llm = llm_port
        self._settings = settings

    async def answer_query(self, farm_id: str, query_text: str) -> AdvisoryQueryOutcome:
        """Run retrieval, the confidence gate, and (if it passes) grounded
        generation for one farmer query.

        Args:
            farm_id: UUID string of the farm asking (for farm_context only —
                no farm data is required to exist for this call to work).
            query_text: The farmer's question.

        Returns:
            An ``AdvisoryQueryOutcome`` — either a populated, cited advisory
            (``retrieved=True``) or an honest no-fabrication escalation
            (``retrieved=False``). Never a partial mix of the two.
        """
        chunks = await self._retrieval.retrieve(query_text)
        top_relevance = RetrievalService.top_relevance(chunks)

        decision = decide(
            image_confidence=None,
            in_scope=True,  # advisory queries aren't bounded to a crop/disease set — only retrieval gates them
            retrieval_relevance=top_relevance,
            confidence_gate=self._settings.CONFIDENCE_GATE,
            relevance_threshold=self._settings.RAG_RELEVANCE_THRESHOLD,
        )
        if decision.should_escalate:
            return AdvisoryQueryOutcome(
                retrieved=False,
                advisory=None,
                citations=[],
                reason=NO_RELEVANT_SOURCE_REASON,
                escalation_offered=True,
                spoken_summary=NO_SOURCE_SPOKEN_SUMMARY,
            )

        raw = await self._llm.generate_grounded_advisory(
            query=query_text,
            context_chunks=[_chunk_to_dict(c) for c in chunks],
            farm_context={"farm_id": farm_id},
        )
        parsed = parse_advisory_output(raw)

        if parsed.insufficient_context:
            # The gate passed on relevance, but the model itself couldn't
            # ground an answer (or its output failed validation) — still a
            # no-fabrication escalation, per execution plan item 4.
            return AdvisoryQueryOutcome(
                retrieved=False,
                advisory=None,
                citations=[],
                reason=NO_RELEVANT_SOURCE_REASON,
                escalation_offered=True,
                spoken_summary=NO_SOURCE_SPOKEN_SUMMARY,
            )

        return AdvisoryQueryOutcome(
            retrieved=True,
            advisory=parsed.advisory,
            citations=parsed.citations,
            reason=None,
            escalation_offered=None,
            spoken_summary=COMPOSED_SPOKEN_SUMMARY,
        )


def get_advisory_service(
    retrieval: Annotated[RetrievalService, Depends(get_retrieval_service)],
    llm_port: Annotated[LLMPort, Depends(get_llm_adapter)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> AdvisoryService:
    """FastAPI dependency provider assembling ``AdvisoryService`` from its ports."""
    return AdvisoryService(retrieval, llm_port, settings)
