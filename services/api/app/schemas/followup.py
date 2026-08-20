"""Closed-loop follow-up check-in schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import FollowupResponse
from app.schemas.common import SpokenResponseMixin
from app.schemas.health import HealthSnapshot


class FollowupCheckinRequest(BaseModel):
    """Farmer follow-up check-in on a previous advisory or problem."""
    advisory_id: str = Field(..., description="UUID string of original advisory")
    farm_id: str = Field(..., description="UUID string of farm")
    response: FollowupResponse = Field(..., description="'improved', 'no_change', or 'got_worse'")
    farmer_notes: str | None = Field(default=None, description="Optional spoken/text feedback")
    photo_asset_id: str | None = Field(default=None, description="Optional updated crop photo")


class FollowupCheckinResponse(SpokenResponseMixin):
    """Response from follow-up evaluation."""
    followup_id: str = Field(..., description="UUID string of follow-up record")
    advisory_id: str = Field(...)
    response: FollowupResponse = Field(...)
    auto_escalated: bool = Field(..., description="Whether 'got_worse' or persistent 'no_change' triggered auto-escalation")
    escalation_id: str | None = Field(default=None, description="Escalation UUID if auto-escalated")
    updated_health_snapshot: HealthSnapshot = Field(..., description="Recalculated health score reflecting check-in")
    created_at: datetime = Field(default_factory=datetime.utcnow)
