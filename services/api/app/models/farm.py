"""ORM model for the Farm aggregate (contract §2.6, PRD §5.2)."""

from datetime import date

from sqlalchemy import Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import LandStatus
from app.models.base import Base


class Farm(Base):
    """A farmer's onboarded farm profile plus its current monitoring state.

    The monitoring columns (``soil_moisture_pct`` .. ``days_since_last_scan``)
    are the live inputs ``FarmHealthContextReader`` feeds the health engine
    (PRD §7). They start ``NULL`` — a brand-new farm is genuinely
    ``unrated`` (PRD §5.2, §7.1) — and are filled in / updated by the
    onboarding, resource-plan, diagnose, follow-up, and case-resolution
    flows as real events happen, never guessed.
    """

    __tablename__ = "farms"

    farmer_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    farm_name: Mapped[str] = mapped_column(String(255), nullable=False)
    village: Mapped[str] = mapped_column(String(255), nullable=False)
    taluk: Mapped[str] = mapped_column(String(255), nullable=False)
    district: Mapped[str] = mapped_column(String(255), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False, default="Tamil Nadu")
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    total_area_acres: Mapped[float] = mapped_column(Float, nullable=False)
    survey_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    land_status: Mapped[str] = mapped_column(String(30), nullable=False, default=LandStatus.UNVERIFIED.value)

    primary_crop: Mapped[str] = mapped_column(String(100), nullable=False)
    growth_stage: Mapped[str | None] = mapped_column(String(30), nullable=True)
    sowing_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    soil_type: Mapped[str] = mapped_column(String(50), nullable=False, default="Clay Loam")
    irrigation_source: Mapped[str] = mapped_column(String(50), nullable=False, default="Borewell")

    # -- Health-engine monitoring state (PRD §7.2) -------------------------
    soil_moisture_pct: Mapped[float | None] = mapped_column(Float, nullable=True)
    irrigation_delivered_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    irrigation_required_mm: Mapped[float | None] = mapped_column(Float, nullable=True)
    days_since_planting: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expected_stage_day: Mapped[int | None] = mapped_column(Integer, nullable=True)
    days_since_last_scan: Mapped[int | None] = mapped_column(Integer, nullable=True)
