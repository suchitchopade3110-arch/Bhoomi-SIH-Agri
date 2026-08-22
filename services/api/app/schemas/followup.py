"""Closed-loop follow-up check-in schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import FollowupResponse
from app.schemas.common import SpokenResponseMixin
from app.schemas.health import HealthSnapshot


class FollowupCheckinRequest(BaseModel):
    """Farmer follow-up check-in on a previous advisory or problem."""
    farm_id: str = Field(..., description="UUID string of farm")
    response: FollowupResponse = Field(..., description="'improved', 'no_change', or 'got_worse'")
    problem_id: str | None = Field(
        default=None,
        description="UUID string of the problem being checked in on; defaults to the farm's latest open problem",
    )
    advisory_id: str | None = Field(default=None, description="UUID string of original advisory, if any")
    farmer_notes: str | None = Field(default=None, description="Optional spoken/text feedback")
    photo_asset_id: str | None = Field(default=None, description="Optional updated crop photo")


class FollowupCheckinResponse(SpokenResponseMixin):
    """Response from follow-up evaluation."""
    followup_id: str = Field(..., description="UUID string of follow-up record")
    problem_id: str | None = Field(default=None, description="UUID string of the problem this check-in applies to")
    response: FollowupResponse = Field(...)
    auto_escalated: bool = Field(..., description="Whether 'got_worse' or persistent 'no_change' triggered auto-escalation")
    escalation_id: str | None = Field(default=None, description="Escalation UUID if auto-escalated")
    updated_health_snapshot: HealthSnapshot = Field(..., description="Recalculated health score reflecting check-in")
    created_at: datetime = Field(default_factory=datetime.utcnow)
