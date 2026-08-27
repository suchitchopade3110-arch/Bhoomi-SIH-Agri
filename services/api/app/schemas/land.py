"""Thin cadastral land-submission schemas (trust side-feature on the Farm
profile). The officer-reviewed HITL land-verification workflow (survey
submission -> officer approve/reject) has been removed; this is the
separate, standalone "submit a survey number" endpoint on
``POST /farms/{farm_id}/land`` and is unaffected by that removal."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import ThinLandStatus


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
