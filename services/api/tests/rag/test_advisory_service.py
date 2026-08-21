"""Tests for AdvisoryService — POST /advisory/query's orchestration (contract §2.11).

All offline and deterministic: StubEmbeddingAdapter, StubLLMAdapter, and an
in-memory corpus ingested via the real ingestion pipeline.
"""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter, StubLLMAdapter
from app.core.config import Settings
from app.domain.rag.constants import FIVE_POINT_FIELDS
from app.services.rag.advisory_service import AdvisoryService, NO_RELEVANT_SOURCE_REASON
from app.services.rag.retrieval import RetrievalService
from tests.rag._helpers import build_ingested_repo

SETTINGS = Settings(CONFIDENCE_GATE=0.70, RAG_RELEVANCE_THRESHOLD=0.18)


async def _make_service(repo=None) -> AdvisoryService:
    repo = repo or await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    return AdvisoryService(retrieval, StubLLMAdapter(), SETTINGS)


@pytest.mark.asyncio
async def test_on_topic_query_returns_retrieved_advisory_with_citation():
    service = await _make_service()
    outcome = await service.answer_query(
        "f_1", "my paddy leaves have water soaked yellow lesions bacterial leaf blight"
    )
    assert outcome.retrieved is True
    assert outcome.advisory is not None
    assert len(outcome.citations) >= 1
    assert outcome.reason is None
    assert outcome.escalation_offered is None


@pytest.mark.asyncio
async def test_advisory_output_conforms_to_five_point_schema():
    service = await _make_service()
    outcome = await service.answer_query("f_1", "bacterial leaf blight copper spray treatment")
    assert outcome.advisory is not None
    for field in FIVE_POINT_FIELDS:
        value = getattr(outcome.advisory, field)
        assert isinstance(value, str)
        assert value.strip() != ""


@pytest.mark.asyncio
async def test_every_citation_has_required_fields():
    service = await _make_service()
    outcome = await service.answer_query("f_1", "bacterial leaf blight symptoms and treatment")
    assert outcome.citations
    for citation in outcome.citations:
        assert citation.doc_id
        assert citation.title
        assert citation.reviewed_on


@pytest.mark.asyncio
async def test_empty_corpus_never_fabricates_escalates_instead():
    """No chunks at all -> retrieval_relevance is 0.0, never None -> gate must fail."""
    empty_repo = await build_ingested_repo(docs=[])
    service = await _make_service(repo=empty_repo)

    outcome = await service.answer_query("f_1", "why are my paddy leaves yellow")

    assert outcome.retrieved is False
    assert outcome.advisory is None
    assert outcome.citations == []
    assert outcome.reason == NO_RELEVANT_SOURCE_REASON
    assert outcome.escalation_offered is True
    assert outcome.spoken_summary  # a plain-language message is always present


@pytest.mark.asyncio
async def test_low_relevance_query_escalates_and_generates_no_advisory_text():
    """A query with essentially no vocabulary overlap with the corpus must
    escalate — and critically, the LLM must never even be asked to compose,
    so no advisory text is generated at all."""
    service = await _make_service()

    outcome = await service.answer_query("f_1", "zzz qqq unrelated gibberish xyzzy plugh")

    assert outcome.retrieved is False
    assert outcome.advisory is None
    assert outcome.citations == []
    assert outcome.reason == NO_RELEVANT_SOURCE_REASON
    assert outcome.escalation_offered is True


@pytest.mark.asyncio
async def test_high_threshold_forces_escalation_even_for_a_relevant_query():
    """Raising the threshold above every retrievable score must still
    escalate — proves the gate, not luck, is what's deciding."""
    repo = await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    strict_settings = Settings(CONFIDENCE_GATE=0.70, RAG_RELEVANCE_THRESHOLD=0.99)
    service = AdvisoryService(retrieval, StubLLMAdapter(), strict_settings)

    outcome = await service.answer_query("f_1", "bacterial leaf blight treatment")

    assert outcome.retrieved is False
    assert outcome.advisory is None


@pytest.mark.asyncio
async def test_answer_query_is_deterministic():
    service = await _make_service()
    a = await service.answer_query("f_1", "bacterial leaf blight treatment")
    b = await service.answer_query("f_1", "bacterial leaf blight treatment")
    assert a == b
