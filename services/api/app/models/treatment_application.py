"""ORM model for the TreatmentApplication aggregate — real-world treatment efficacy tracking (spec §3.2, SIH26131)."""

from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TreatmentApplication(Base):
    """One recorded treatment intervention applied on a farm for a diagnosed pathogen.

    Aggregated across farms to compute population-level treatment efficacy,
    regional failure rates, and detect emerging chemical/biological resistance
    (spec §1, §2).
    """

    __tablename__ = "treatment_applications"

    problem_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("problems.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    farm_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("farms.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Normalized ICAR PoP vocabulary
    pathogen_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # e.g., "bacterial_leaf_blight"
    treatment_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)  # e.g., "copper_hydroxide_77_wp"
    treatment_category: Mapped[str] = mapped_column(String(50), nullable=False)  # "chemical", "biological", "cultural"

    applied_on: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    crop: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    # Resolved outcome state
    final_outcome: Mapped[str | None] = mapped_column(String(50), nullable=True)  # "resolved", "improved", "failed", "superseded"
    followups_to_resolution: Mapped[int | None] = mapped_column(Integer, nullable=True)
    days_to_resolution: Mapped[int | None] = mapped_column(Integer, nullable=True)
    failed_on_got_worse: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    escalated_for_expert: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
