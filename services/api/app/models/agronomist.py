"""ORM model for the agronomist roster — routing target for escalation (PRD §5.11)."""

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Agronomist(Base):
    """One KVK agronomist available to receive escalated cases.

    A minimal roster, not a full staff-management aggregate: enough for
    real (queryable, capacity-aware) routing — see
    ``domain.escalation.routing`` — while ``ROUTING_MODE=demo_fixed``
    (execution plan item 3) can bypass it entirely for the pitch demo.
    """

    __tablename__ = "agronomists"

    identifier: Mapped[str] = mapped_column(String(64), nullable=False, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    kvk_center: Mapped[str] = mapped_column(String(120), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    active_case_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
