"""ORM model for the Problem aggregate (contract §2.12, PRD §5.9)."""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import ProblemStatus
from app.models.base import Base


class Problem(Base):
    """One diagnosed crop problem on a farm, tracked open -> resolved.

    Backs both the health engine's active-problem-load sub-index (via
    ``repositories/health_context_postgres.py``) and the case-file timeline
    (contract §2.12). ``opened_at`` mirrors the inherited ``created_at`` at
    insert time and is not repeated as a separate concept elsewhere.
    """

    __tablename__ = "problems"

    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=ProblemStatus.OPEN.value, index=True)
    image_asset_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
