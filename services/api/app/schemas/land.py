"""Land Verification schemas. No boundary geometry, no cadastral lookup —
SIH26131 feature checklist §10.1/§13.2: HITL survey-number submission only."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import LandStatus, ThinLandStatus


class LandVerifyRequest(BaseModel):
    """Submission of land parcel for officer verification."""
    farm_id: str = Field(..., description="UUID string of farm")
    survey_number: str = Field(...)
    patta_passbook_asset_id: str | None = None


class LandVerifyResponse(BaseModel):
    """Land verification status response."""
    parcel_id: str = Field(..., description="UUID string of parcel record")
    farm_id: str = Field(...)
    status: LandStatus = Field(...)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    officer_notes: str | None = None


class ThinLandVerification(BaseModel):
    """Thin land status schema without cut boundary/geometry fields (strictly 3 states)."""
    farm_id: str = Field(..., description="UUID string of farm")
    status: ThinLandStatus = Field(..., description="Thin status: pending_verification | verified | rejected")
    last_verified_at: datetime | None = Field(default=None, description="Timestamp of status update")


class ThinLandSubmissionRequest(BaseModel):
    """Thin cadastral land submission request (trust side-feature)."""
    survey_number: str = Field(..., min_length=1, description="Cadastral survey number, e.g. 142/3B")


class ThinLandSubmissionResponse(BaseModel):
    """Thin land submission response (trust side-feature)."""
    farm_id: str = Field(..., description="UUID string of farm")
    survey_number: str = Field(..., description="Cadastral survey number")
    status: str = Field(default="pending_verification", description="Verification status")

