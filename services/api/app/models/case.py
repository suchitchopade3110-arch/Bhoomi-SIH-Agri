"""ORM model for the Case (escalation) aggregate (contract §2.13, PRD §5.11)."""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import CaseStatus, ProblemSeverity
from app.models.base import Base


class Case(Base):
    """One AI-to-expert escalation and its compiled case file."""

    __tablename__ = "cases"

    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    problem_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)

    reason: Mapped[str | None] = mapped_column(String(500), nullable=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, default=ProblemSeverity.EARLY.value)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=CaseStatus.ESCALATED.value, index=True)
    assigned_to: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Frozen CaseSummary payload as of escalation time (contract §2.13) —
    # inspectable without re-joining every source table.
    case_summary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    resolution: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
