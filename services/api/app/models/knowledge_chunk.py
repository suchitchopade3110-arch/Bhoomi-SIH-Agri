"""ORM model for the curated RAG corpus (PRD §5.7)."""

from datetime import date

from pgvector.sqlalchemy import Vector
from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

# BGE-m3 (the real EmbeddingPort's model) emits 1024-dim dense vectors; the
# stub embedding adapter matches this dimension so the two are interchangeable
# without touching this schema.
EMBEDDING_DIM = 1024


class KnowledgeChunk(Base):
    """One chunk of one curated corpus document, with its embedding.

    ``doc_id``/``title``/``reviewed_on`` are denormalized onto every chunk
    row (rather than a separate documents table) so a similarity search
    returns everything a citation needs in one query — the corpus is small
    and curated (PRD §5.7: "named, dated, owned"), so this trades a little
    redundancy for simplicity.
    """

    __tablename__ = "knowledge_chunks"

    doc_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    reviewed_on: Mapped[date] = mapped_column(Date, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(EMBEDDING_DIM), nullable=False)
