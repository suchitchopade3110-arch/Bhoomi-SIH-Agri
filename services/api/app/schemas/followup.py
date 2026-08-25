"""Closed-loop follow-up check-in schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.core.enums import FollowupResponse, ProblemSeverity
from app.schemas.common import SpokenResponseMixin
from app.schemas.health import HealthSnapshot, RiskChange


class SeverityChange(BaseModel):
    """Before/after problem severity tier caused by this check-in.
    ``to=None`` means the problem resolved outright (an ``improved`` report
    at the lightest tier), not that severity is unknown."""

    model_config = ConfigDict(populate_by_name=True)

    from_: ProblemSeverity = Field(..., alias="from", description="Severity before this check-in")
    to: ProblemSeverity | None = Field(default=None, description="Severity after this check-in; null if resolved")


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
    severity_change: SeverityChange = Field(..., description="Problem severity tier before/after this check-in")
    risk: RiskChange = Field(..., description="Health score before/after this check-in, plus the resulting band")
    updated_health_snapshot: HealthSnapshot = Field(..., description="Recalculated health score reflecting check-in")
    created_at: datetime = Field(default_factory=datetime.utcnow)
