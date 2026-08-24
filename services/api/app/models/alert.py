"""ORM model for the Alert aggregate (SPEC-ALERT-001 §5.1, Phase 3).

``id`` is set explicitly to the domain's deterministic ``alert_id``
(uuid5, not the ``Base`` default uuid4) so re-evaluating identical inputs on
the same day is idempotent — the second ``save`` is a no-op upsert on the
same primary key, not a duplicate row.
"""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Alert(Base):
    """One early-warning alert — per-farm or a district regional broadcast."""

    __tablename__ = "alerts"

    farm_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    district: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    pathogen_name: Mapped[str] = mapped_column(String(255), nullable=False)
    target_crop: Mapped[str | None] = mapped_column(String(100), nullable=True)
    target: Mapped[str] = mapped_column(String(30), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    trigger_reason: Mapped[str] = mapped_column(String(1000), nullable=False)
    preventative_action: Mapped[str] = mapped_column(String(1000), nullable=False)
    # Non-nullable by design (Phase 3 "never cut" list) — an alert cannot be
    # issued without at least one corpus-sourced inspection task. Enforced
    # in app/services/alerts/alert_service.py, not just this NOT NULL.
    inspection_tasks: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    spoken_summary: Mapped[str] = mapped_column(String(1000), nullable=False)
    delivery_channels: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False, default=list)

    cooldown_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)
    dismissed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    dismiss_reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
