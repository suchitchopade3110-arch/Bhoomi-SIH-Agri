"""Tests for RAG pipeline no-retrieval fallback and anti-fabrication gating (Phase 2 Part B).

Verifies:
  - RAG pipeline explicitly exercises against RAG_RELEVANCE_THRESHOLD_STUB (0.18) in test mode
  - Empty corpus returns honest retrieved=False with escalation offered (no LLM fabrication)
  - Low-relevance / off-topic queries fail the relevance threshold and escalate
  - High threshold override forces escalation even on matched vocabulary
  - Strict mutual exclusivity between composed advisory and escalation response shapes
"""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter, StubLLMAdapter
from app.core.config import Settings
from app.domain.constants import RAG_RELEVANCE_THRESHOLD_STUB
from app.services.rag.advisory_service import AdvisoryService, NO_RELEVANT_SOURCE_REASON
from app.services.rag.pipeline import AdvisoryQueryOutcome
from app.services.rag.retrieval import RetrievalService
from tests.rag._helpers import build_ingested_repo

# Explicitly lock to RAG_RELEVANCE_THRESHOLD_STUB for deterministic testing
TEST_SETTINGS = Settings(
    CONFIDENCE_GATE=0.70,
    EMBEDDING_PROVIDER="stub",
    RAG_RELEVANCE_THRESHOLD_OVERRIDE=RAG_RELEVANCE_THRESHOLD_STUB,
)


def test_rag_threshold_stub_configured():
    """Verify TEST_SETTINGS explicitly uses RAG_RELEVANCE_THRESHOLD_STUB."""
    assert TEST_SETTINGS.RAG_RELEVANCE_THRESHOLD == RAG_RELEVANCE_THRESHOLD_STUB
    assert TEST_SETTINGS.RAG_RELEVANCE_THRESHOLD == 0.18


async def _make_service(repo=None, custom_settings: Settings | None = None) -> AdvisoryService:
    repo = repo or await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    return AdvisoryService(retrieval, StubLLMAdapter(), custom_settings or TEST_SETTINGS)


@pytest.mark.asyncio
async def test_empty_corpus_returns_honest_no_retrieval_escalation():
    """When corpus has 0 chunks, retrieval_relevance is 0.0 -> must escalate without LLM generation."""
    empty_repo = await build_ingested_repo(docs=[])
    service = await _make_service(repo=empty_repo)

    outcome: AdvisoryQueryOutcome = await service.answer_query(
        farm_id="farm_test_1",
        query_text="why are my paddy leaves turning yellow",
    )

    assert outcome.retrieved is False
    assert outcome.advisory is None
    assert outcome.citations == []
    assert outcome.reason == NO_RELEVANT_SOURCE_REASON
    assert outcome.escalation_offered is True
    assert "don't have reliable information" in outcome.spoken_summary or "expert" in outcome.spoken_summary


@pytest.mark.asyncio
async def test_low_relevance_query_below_threshold_escalates_without_fabrication():
    """Off-topic query with similarity below 0.18 threshold must escalate with zero citations."""
    service = await _make_service()

    outcome: AdvisoryQueryOutcome = await service.answer_query(
        farm_id="farm_test_1",
        query_text="quantum neural network blockchain satellite orbital trajectory",
    )

    assert outcome.retrieved is False
    assert outcome.advisory is None
    assert outcome.citations == []
    assert outcome.reason == NO_RELEVANT_SOURCE_REASON
    assert outcome.escalation_offered is True


@pytest.mark.asyncio
async def test_high_threshold_override_forces_escalation():
    """When threshold is raised above achievable similarity (e.g. 0.99), gate must force escalation."""
    high_threshold_settings = Settings(
        CONFIDENCE_GATE=0.70,
        EMBEDDING_PROVIDER="stub",
        RAG_RELEVANCE_THRESHOLD_OVERRIDE=0.99,
    )
    service = await _make_service(custom_settings=high_threshold_settings)

    outcome: AdvisoryQueryOutcome = await service.answer_query(
        farm_id="farm_test_1",
        query_text="bacterial leaf blight copper spray treatment",
    )

    assert outcome.retrieved is False
    assert outcome.advisory is None
    assert outcome.citations == []
    assert outcome.reason == NO_RELEVANT_SOURCE_REASON
    assert outcome.escalation_offered is True


@pytest.mark.asyncio
async def test_structural_invariant_mutual_exclusivity():
    """Advisory and escalation branches must never mix fields."""
    service = await _make_service()

    # Branch 1: On-topic query -> Composed advisory
    composed = await service.answer_query(
        farm_id="farm_test_1",
        query_text="bacterial leaf blight management and control",
    )
    assert composed.retrieved is True
    assert composed.advisory is not None
    assert len(composed.citations) >= 1
    assert composed.reason is None
    assert composed.escalation_offered is None

    # Branch 2: Off-topic query -> Escalation
    escalated = await service.answer_query(
        farm_id="farm_test_1",
        query_text="completely unrelated non agricultural gibberish zzzxxx",
    )
    assert escalated.retrieved is False
    assert escalated.advisory is None
    assert escalated.citations == []
    assert escalated.reason is not None
    assert escalated.escalation_offered is True
