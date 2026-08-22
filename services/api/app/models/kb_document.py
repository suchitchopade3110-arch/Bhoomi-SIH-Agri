"""ORM model for KBDocument — curated corpus document metadata (PRD §5.7).

Each curated document (e.g. "ICAR PoP: Rice — Bacterial Leaf Blight") gets
one row here.  Its text is chunked and embedded into ``KnowledgeChunk`` rows
that carry a ``document_id`` FK back to this table.
"""

from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class KBDocument(Base):
    """One curated knowledge base document — the parent of chunked embeddings.

    Fields mirror the YAML frontmatter in the corpus markdown files:
    ``title``, ``source``, ``curator``, ``reviewed_on``, ``lang``.
    """

    __tablename__ = "kb_documents"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    curator: Mapped[str] = mapped_column(String(100), nullable=False)
    reviewed_on: Mapped[date] = mapped_column(Date, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    lang: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
