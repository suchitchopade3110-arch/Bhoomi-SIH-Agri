"""ORM model for the Case aggregate — an escalated Living Case File
(PRD §5.11, contract §2.13)."""

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Case(Base):
    """One escalated case, from creation through agronomist resolution.

    ``farm_id``/``problem_id`` are stored as plain UUID strings without a
    foreign-key constraint: the Farm and Problem aggregates don't have their
    own migrations yet (same rationale as ``HealthSnapshot.farm_id``) —
    constraints can be added once those tables land.

    ``case_summary`` stores the full contract §2.13 ``CaseSummary`` shape as
    JSONB, verbatim, at the moment of escalation — the same denormalize-for-
    simplicity trade-off ``KnowledgeChunk`` makes, so a case's living file
    reads back in one query rather than a repository re-compiling it from
    five other tables on every read. ``resolution`` is the agronomist's
    prescription, set only once the case is resolved.
    """

    __tablename__ = "cases"

    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    problem_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)

    # e.g. "below_confidence_gate" | "out_of_scope" | "no_relevant_source" |
    # "got_worse_followup" | "manual" — what triggered this case (Phase 4 item 1).
    trigger_type: Mapped[str] = mapped_column(String(40), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Denormalized for GET /agronomist/case-queue (contract §2.13: "assigned
    # cases, newest first") — the full CaseSummary in case_summary already
    # carries the contract's own farm/crop shape, but it's a JSONB blob, so a
    # cheap queue list needs a couple of indexable columns rather than
    # parsing every row's JSON on every queue read.
    farmer_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    village: Mapped[str | None] = mapped_column(String(120), nullable=True)
    crop: Mapped[str | None] = mapped_column(String(80), nullable=True)

    case_summary: Mapped[dict] = mapped_column(JSONB, nullable=False)

    assigned_to: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    assigned_kvk_center: Mapped[str | None] = mapped_column(String(120), nullable=True)

    # {"agronomist_id", "agronomist_name", "confirmed_diagnosis", "expert_advice", "prescribed_inputs"}
    resolution: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
