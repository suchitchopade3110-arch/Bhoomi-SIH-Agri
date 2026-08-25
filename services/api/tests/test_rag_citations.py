"""Tests for RAG pipeline citations and grounded 5-point advisory generation (Phase 2 Part B).

Verifies:
  - RAG pipeline explicitly exercises against RAG_RELEVANCE_THRESHOLD_STUB (0.18) in test mode
  - On-topic queries return retrieved=True with >=1 GroundedCitation
  - Every citation contains valid doc_id, title, and reviewed_on
  - Output conforms strictly to the 5-point advisory schema
  - Responses are 100% deterministic
"""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter, StubLLMAdapter
from app.core.config import Settings
from app.domain.constants import RAG_RELEVANCE_THRESHOLD_STUB
from app.domain.rag.constants import FIVE_POINT_FIELDS
from app.services.rag.advisory_service import AdvisoryService
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


async def _make_service(repo=None) -> AdvisoryService:
    repo = repo or await build_ingested_repo()
    retrieval = RetrievalService(repo, StubEmbeddingAdapter())
    return AdvisoryService(retrieval, StubLLMAdapter(), TEST_SETTINGS)


@pytest.mark.asyncio
async def test_on_topic_query_returns_retrieved_true_with_citations():
    """On-topic query matches corpus chunks above stub threshold and returns citations."""
    service = await _make_service()
    outcome: AdvisoryQueryOutcome = await service.answer_query(
        farm_id="farm_test_1",
        query_text="my paddy leaves have water soaked yellow lesions bacterial leaf blight",
    )

    assert outcome.retrieved is True
    assert outcome.advisory is not None
    assert isinstance(outcome.citations, list)
    assert len(outcome.citations) >= 1
    assert outcome.reason is None
    assert outcome.escalation_offered is None


@pytest.mark.asyncio
async def test_every_citation_has_required_metadata_fields():
    """Every citation returned must contain doc_id, title, and reviewed_on."""
    service = await _make_service()
    outcome = await service.answer_query(
        farm_id="farm_test_1",
        query_text="bacterial leaf blight symptoms and treatment for rice",
    )

    assert outcome.retrieved is True
    assert len(outcome.citations) >= 1

    for citation in outcome.citations:
        assert citation.doc_id is not None and citation.doc_id.strip() != ""
        assert citation.title is not None and citation.title.strip() != ""
        assert citation.reviewed_on is not None and citation.reviewed_on.strip() != ""


@pytest.mark.asyncio
async def test_advisory_conforms_to_five_point_schema():
    """Advisory output must contain all 5 required fields populated with non-empty strings."""
    service = await _make_service()
    outcome = await service.answer_query(
        farm_id="farm_test_1",
        query_text="bacterial leaf blight copper spray treatment",
    )

    assert outcome.advisory is not None
    for field_name in FIVE_POINT_FIELDS:
        val = getattr(outcome.advisory, field_name)
        assert isinstance(val, str)
        assert len(val.strip()) > 0


@pytest.mark.asyncio
async def test_rag_pipeline_determinism():
    """Calling answer_query multiple times with identical query produces identical outcome."""
    service = await _make_service()
    query = "bacterial leaf blight management in paddy"

    run1 = await service.answer_query(farm_id="farm_test_1", query_text=query)
    run2 = await service.answer_query(farm_id="farm_test_1", query_text=query)

    assert run1 == run2
    assert run1.retrieved == run2.retrieved
    assert run1.advisory == run2.advisory
    assert run1.citations == run2.citations
    assert run1.spoken_summary == run2.spoken_summary


@pytest.mark.asyncio
async def test_citations_match_verbatim_corpus_source_documents():
    """Authenticity verification: every returned citation must match a verbatim entry in CORPUS_DOCS."""
    from app.services.rag.corpus_data import CORPUS_DOCS

    service = await _make_service()
    outcome = await service.answer_query(
        farm_id="farm_test_1",
        query_text="my paddy leaves have water soaked yellow lesions bacterial leaf blight",
    )

    assert outcome.retrieved is True
    assert len(outcome.citations) >= 1

    for citation in outcome.citations:
        matched_docs = [d for d in CORPUS_DOCS if d["doc_id"] == citation.doc_id]
        assert len(matched_docs) == 1, f"Citation doc_id {citation.doc_id} not found in CORPUS_DOCS source!"
        src = matched_docs[0]
        assert citation.title == src["title"], f"Citation title '{citation.title}' does not match source '{src['title']}'"
        assert str(citation.reviewed_on) == str(src["reviewed_on"]), (
            f"Citation reviewed_on '{citation.reviewed_on}' does not match source '{src['reviewed_on']}'"
        )

