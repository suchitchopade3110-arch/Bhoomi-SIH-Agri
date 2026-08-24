"""Early-warning alert schemas (SPEC-ALERT-001, delta spec §3.2-3.3)."""

from datetime import datetime
from pydantic import BaseModel, Field


class AlertItem(BaseModel):
    """One active alert surfaced to a farmer."""
    alert_id: str = Field(...)
    pathogen_name: str = Field(...)
    severity: str = Field(..., description="'info' | 'advisory' | 'warning' | 'emergency'")
    trigger_reason: str = Field(...)
    preventative_action: str = Field(...)
    spoken_summary: str = Field(...)
    created_at: datetime = Field(...)
    expires_at: datetime = Field(...)


class FarmAlertsResponse(BaseModel):
    """Response for ``GET /api/v1/farms/{id}/alerts``."""
    farm_id: str = Field(...)
    active_alerts: list[AlertItem] = Field(default_factory=list)


class AlertDismissRequest(BaseModel):
    """Request for ``POST /api/v1/alerts/{id}/dismiss``."""
    farm_id: str = Field(...)
    reason: str = Field(default="action_taken")


class AlertDismissResponse(BaseModel):
    """Response for ``POST /api/v1/alerts/{id}/dismiss``."""
    status: str = Field(default="dismissed")
    alert_id: str = Field(...)
