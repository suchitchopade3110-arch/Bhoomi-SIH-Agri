"""ORM model for the Advisory aggregate — RAG-generated structured advice (PRD §5.7, contract §2.11).

Each advisory is the 5-point output of a successful RAG pipeline run:
possible_issue, what_to_check, what_to_do_next, what_to_avoid, expert_triggers,
plus a ``citations`` list that traces every claim back to a curated corpus doc.
"""

from sqlalchemy import Float, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Advisory(Base):
    """One RAG-generated advisory for a farm, optionally linked to a Problem.

    ``citations`` is stored as JSONB: a list of
    ``{"doc_id": str, "title": str, "reviewed_on": str}`` dicts that trace
    every advisory claim back to a named, dated corpus document (PRD §5.7:
    "curated, named, dated, owned").
    """

    __tablename__ = "advisories"

    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    problem_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)

    # 5-point advisory structure (contract §2.11)
    possible_issue: Mapped[str] = mapped_column(Text, nullable=False)
    what_to_check: Mapped[str] = mapped_column(Text, nullable=False)
    what_to_do_next: Mapped[str] = mapped_column(Text, nullable=False)
    what_to_avoid: Mapped[str] = mapped_column(Text, nullable=False)
    expert_triggers: Mapped[str] = mapped_column(Text, nullable=False)

    # Provenance
    citations: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    confidence: Mapped[float | None] = mapped_column(Float, nullable=True)
    model_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    query_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    lang: Mapped[str] = mapped_column(String(10), nullable=False, default="ta-IN")
