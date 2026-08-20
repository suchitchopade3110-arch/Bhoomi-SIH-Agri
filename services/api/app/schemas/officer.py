"""Extension Officer portal schemas for HITL Land Boundary Verification."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from app.core.enums import LandStatus


class OfficerQueueItem(BaseModel):
    """Pending land verification item in the officer's jurisdiction."""
    parcel_id: str = Field(..., description="UUID string of land parcel")
    farm_id: str = Field(..., description="UUID string of associated farm")
    farmer_name: str = Field(...)
    village: str = Field(...)
    survey_number: str = Field(...)
    submitted_at: datetime = Field(...)
    status: LandStatus = Field(default=LandStatus.PENDING_REVIEW)
    patta_asset_url: str | None = None


class OfficerReviewDetail(BaseModel):
    """Detailed parcel review payload for map editing."""
    parcel_id: str = Field(...)
    farm_id: str = Field(...)
    farmer_name: str = Field(...)
    farmer_phone: str = Field(...)
    village: str = Field(...)
    taluk: str = Field(...)
    survey_number: str = Field(...)
    cadastral_boundary: dict[str, Any] | None = None
    satellite_overlay_url: str | None = None


class OfficerActionRequest(BaseModel):
    """Officer decision on a land boundary."""
    parcel_id: str = Field(...)
    action: LandStatus = Field(..., description="'verified' or 'rejected'")
    confirmed_boundary_geojson: dict[str, Any] | None = Field(default=None, description="Officer-edited GeoJSON polygon")
    confirmed_area_acres: float | None = None
    officer_notes: str | None = None


class OfficerActionResponse(BaseModel):
    """Response confirming officer action."""
    parcel_id: str = Field(...)
    status: LandStatus = Field(...)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    message: str = "Land parcel status successfully updated."
