"""ORM model for the curated RAG corpus (PRD §5.7)."""

from datetime import date

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# BGE-m3 (the real EmbeddingPort's model) emits 1024-dim dense vectors; the
# stub embedding adapter matches this dimension so the two are interchangeable
# without touching this schema.
EMBEDDING_DIM = 1024


class KnowledgeChunk(Base):
    """One chunk of one curated corpus document, with its embedding.

    ``doc_id``/``title``/``reviewed_on`` are denormalized onto every chunk
    row so a similarity search returns everything a citation needs in one
    query.  ``document_id`` is the normalized FK to ``kb_documents`` for
    joins when full document metadata is needed.

    The HNSW index on ``embedding`` enables fast approximate nearest-neighbor
    cosine similarity search via pgvector.
    """

    __tablename__ = "knowledge_chunks"

    doc_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    # Normalized FK to KBDocument — nullable for backward compat with
    # existing rows that predate the kb_documents table.
    document_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    reviewed_on: Mapped[date] = mapped_column(Date, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIM), nullable=False)


# HNSW index for cosine similarity search — pgvector's recommended index
# type for ANN queries.  Parameters tuned for a small curated corpus.
ix_kb_chunk_embedding_cosine = Index(
    "ix_kb_chunk_embedding_cosine",
    KnowledgeChunk.embedding,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_cosine_ops"},
)
