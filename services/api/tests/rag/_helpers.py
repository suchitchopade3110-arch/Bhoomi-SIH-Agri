"""Shared test helpers for the RAG pipeline — all offline, all deterministic."""

from app.adapters.stubs import StubEmbeddingAdapter
from app.repositories.in_memory import InMemoryKnowledgeChunkRepository
from app.services.rag.corpus_data import CORPUS_DOCS, CorpusDoc
from app.services.rag.ingest import ingest_corpus


async def build_ingested_repo(docs: list[CorpusDoc] = CORPUS_DOCS) -> InMemoryKnowledgeChunkRepository:
    """An in-memory corpus repository, ingested via the real ingestion
    pipeline (chunk -> embed -> write) against the stub embedding adapter.
    Exercises services.rag.ingest.ingest_corpus itself, not just a hand-built
    fixture."""
    embedding_port = StubEmbeddingAdapter()
    repo = InMemoryKnowledgeChunkRepository()
    await ingest_corpus(repo, embedding_port, docs)
    return repo
