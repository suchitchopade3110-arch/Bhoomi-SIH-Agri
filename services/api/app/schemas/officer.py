"""Extension Officer portal schemas for HITL Land Verification. No boundary
geometry — SIH26131 feature checklist §10.2: "No boundary correction UI"."""

from datetime import datetime
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
    """Detailed parcel review payload."""
    parcel_id: str = Field(...)
    farm_id: str = Field(...)
    farmer_name: str = Field(...)
    farmer_phone: str = Field(...)
    village: str = Field(...)
    taluk: str = Field(...)
    survey_number: str = Field(...)


class OfficerActionRequest(BaseModel):
    """Officer decision on a land parcel — approve/reject + reason only,
    no boundary correction."""
    parcel_id: str = Field(...)
    action: LandStatus = Field(..., description="'verified' or 'rejected'")
    officer_notes: str | None = None


class OfficerActionResponse(BaseModel):
    """Response confirming officer action."""
    parcel_id: str = Field(...)
    status: LandStatus = Field(...)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    message: str = "Land parcel status successfully updated."
