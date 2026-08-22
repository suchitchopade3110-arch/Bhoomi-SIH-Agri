"""ORM model for the LandRecord aggregate — HITL land verification (contract §2.7, PRD §5.3)."""

from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import LandStatus
from app.models.base import Base


class LandParcel(Base):
    """One farm's cadastral submission and its HITL verification lifecycle.

    Boundary geometry is stored as GeoJSON in JSONB rather than a native
    PostGIS ``geometry`` column — see ``README`` / final report for the
    documented assumption (no PostGIS geometry model exists yet anywhere in
    this codebase; JSONB keeps this consistent with that precedent and with
    exactly what the contract's ``boundary_geojson`` field already is).
    """

    __tablename__ = "land_parcels"

    farm_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)

    survey_number: Mapped[str] = mapped_column(String(100), nullable=False)
    patta_passbook_asset_id: Mapped[str | None] = mapped_column(String(36), nullable=True)

    status: Mapped[str] = mapped_column(String(30), nullable=False, default=LandStatus.PENDING_REVIEW.value, index=True)
    auto_lookup_outcome: Mapped[str] = mapped_column(String(20), nullable=False)  # "matched" | "failed"
    district: Mapped[str] = mapped_column(String(255), nullable=False)

    suggested_boundary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    confirmed_boundary: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    submitted_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    verified_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    officer_notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)
