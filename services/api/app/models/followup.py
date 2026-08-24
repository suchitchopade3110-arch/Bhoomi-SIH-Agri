"""ORM model for the FollowUp aggregate — closed-loop check-ins (contract §2.12, PRD §5.10)."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class FollowUp(Base):
    """One farmer check-in (Improved / No Change / Got Worse) on a Problem.

    Ordering/recency uses the inherited ``Base.created_at`` — no separate
    event timestamp needed.
    """

    __tablename__ = "followups"

    problem_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    response: Mapped[str] = mapped_column(String(20), nullable=False)
    farmer_notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    photo_asset_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    treatment_application_id: Mapped[str | None] = mapped_column(
        String(36),
        ForeignKey("treatment_applications.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
