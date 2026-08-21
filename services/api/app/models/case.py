"""ORM model for the escalation Case aggregate (PRD §5.11, contract §2.13)."""

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Case(Base):
    """One escalation case: a pre-analyzed bundle routed to an agronomist.

    ``farm_id``/``problem_id`` are plain unconstrained UUID strings — the
    Farm and Problem aggregates don't have their own migrations yet (Farm:
    no phase yet; Problem: tracked by the in-memory ``ProblemRegistry``
    placeholder, see repositories/problem_registry.py). ``problem_id`` is
    nullable: a diagnosis that fails the confidence gate before a problem
    is ever confirmed still opens a case (contract §2.10's escalation
    branch), just one with no problem to reference yet.
    """

    __tablename__ = "cases"

    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    problem_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    trigger: Mapped[str] = mapped_column(
        String(40), nullable=False, comment="What originated this case: below_gate | out_of_scope | "
        "no_relevant_source | got_worse | manual"
    )

    assigned_to: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # Denormalized CaseSummary snapshot (contract §2.13), captured at the
    # moment of escalation and re-read verbatim by GET /cases/{id} — the
    # "pre-analyzed bundle" the agronomist opens.
    summary: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Expert resolution (POST /cases/{id}/resolve)
    diagnosis: Mapped[str | None] = mapped_column(Text, nullable=True)
    treatment: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
