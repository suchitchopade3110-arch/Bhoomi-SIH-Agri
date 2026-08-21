"""ORM model for persisted Farm Health Score snapshots."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class HealthSnapshot(Base):
    """One computed-and-persisted health score for a farm (PRD §7, contract §2.9).

    ``farm_id`` is stored as a plain UUID string without a foreign-key
    constraint: the Farm aggregate's own table/migration belongs to a later
    (onboarding) phase and does not exist yet. The constraint can be added
    once that table lands.

    The full sub-index breakdown is stored as JSONB rather than six separate
    columns so the audit trail (PRD §7.1: "every point movement traceable to
    an input") is captured verbatim, in the same shape the API returns it.
    """

    __tablename__ = "health_snapshots"

    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    band: Mapped[str] = mapped_column(String(20), nullable=False)
    weights_version: Mapped[str] = mapped_column(String(20), nullable=False)
    computed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, index=True)

    # list[{"key": str, "value": int|None, "weight": float, "contribution": float|None}]
    subindices: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # {"type": str, ...} or None
    triggering_input: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    # list[str] — onboarding/monitoring fields still missing when band=unrated
    missing_fields: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
