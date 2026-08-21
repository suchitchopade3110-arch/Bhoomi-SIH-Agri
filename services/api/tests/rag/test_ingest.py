"""Tests for the corpus ingestion pipeline (execution plan item 1)."""

import pytest

from app.adapters.stubs import StubEmbeddingAdapter
from app.repositories.in_memory import InMemoryKnowledgeChunkRepository
from app.services.rag.corpus_data import CORPUS_DOCS
from app.services.rag.ingest import ingest_corpus


@pytest.mark.asyncio
async def test_ingest_writes_at_least_one_chunk_per_document():
    repo = InMemoryKnowledgeChunkRepository()
    total = await ingest_corpus(repo, StubEmbeddingAdapter(), CORPUS_DOCS)
    assert total > 0

    doc_ids_written = {c.doc_id for c in repo._chunks}  # noqa: SLF001 (test introspection)
    doc_ids_expected = {d["doc_id"] for d in CORPUS_DOCS}
    assert doc_ids_written == doc_ids_expected


@pytest.mark.asyncio
async def test_ingest_seed_corpus_size_is_in_the_15_to_20_doc_range():
    assert 15 <= len(CORPUS_DOCS) <= 20


@pytest.mark.asyncio
async def test_ingest_is_idempotent_reingestion_replaces_not_duplicates():
    repo = InMemoryKnowledgeChunkRepository()
    first = await ingest_corpus(repo, StubEmbeddingAdapter(), CORPUS_DOCS)
    second = await ingest_corpus(repo, StubEmbeddingAdapter(), CORPUS_DOCS)
    assert first == second
    assert len(repo._chunks) == second  # noqa: SLF001


@pytest.mark.asyncio
async def test_every_chunk_has_required_metadata():
    repo = InMemoryKnowledgeChunkRepository()
    await ingest_corpus(repo, StubEmbeddingAdapter(), CORPUS_DOCS)
    for chunk in repo._chunks:  # noqa: SLF001
        assert chunk.doc_id
        assert chunk.title
        assert chunk.reviewed_on
        assert chunk.chunk_text.strip()
        assert len(chunk.embedding) == StubEmbeddingAdapter().dimension
