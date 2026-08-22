"""ORM model for the Scheme aggregate — dated subsidy snapshot (contract §2.14, PRD §5.12)."""

from datetime import date

from sqlalchemy import Date, Float, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import SchemeStatus
from app.models.base import Base


class Scheme(Base):
    """One curated, dated government scheme/subsidy record.

    Matching (PRD §5.12) is a plain filter over ``crop_filter`` /
    ``category_filter`` — no live government integration (PRD §2.2
    non-goal: "a self-updating national subsidy database").
    """

    __tablename__ = "schemes"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    ministry: Mapped[str] = mapped_column(String(255), nullable=False)
    jurisdiction: Mapped[str] = mapped_column(String(100), nullable=False, default="TN")
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    benefits: Mapped[str] = mapped_column(String(1000), nullable=False)
    eligibility_criteria: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    subsidy_percentage: Mapped[float | None] = mapped_column(Float, nullable=True)
    max_amount_inr: Mapped[float | None] = mapped_column(Float, nullable=True)
    portal_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=SchemeStatus.ACTIVE.value)
    last_verified: Mapped[date] = mapped_column(Date, nullable=False)

    # Simple eligibility filters (PRD §5.12: "crop cycle + farmer category").
    crop_filter: Mapped[str | None] = mapped_column(String(100), nullable=True)  # None = any crop
    category_filter: Mapped[str | None] = mapped_column(String(50), nullable=True)  # None = any category
