"""Early-warning alert schemas (SPEC-ALERT-001; route path per Phase 3
build order Step 4 — ``/acknowledge``, correcting the delta spec's earlier
``/dismiss`` draft; see docs/specs/api_contract_sih26131_delta.md §3.3)."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.common import SpokenResponseMixin


class AlertItem(BaseModel):
    """One active alert surfaced to a farmer."""
    alert_id: str = Field(...)
    pathogen_name: str = Field(...)
    severity: str = Field(..., description="'info' | 'advisory' | 'warning' | 'emergency'")
    trigger_reason: str = Field(...)
    preventative_action: str = Field(...)
    inspection_tasks: list[str] = Field(..., description="Corpus-sourced checklist; never empty")
    spoken_summary: str = Field(...)
    created_at: datetime = Field(...)
    expires_at: datetime = Field(...)


class FarmAlertsResponse(BaseModel):
    """Response for ``GET /api/v1/farms/{id}/alerts``."""
    farm_id: str = Field(...)
    active_alerts: list[AlertItem] = Field(default_factory=list)


class AlertAcknowledgeRequest(BaseModel):
    """Request for ``POST /api/v1/alerts/{id}/acknowledge``."""
    farm_id: str = Field(...)
    reason: str = Field(default="action_taken")


class AlertAcknowledgeResponse(SpokenResponseMixin):
    """Response for ``POST /api/v1/alerts/{id}/acknowledge``."""
    status: str = Field(default="acknowledged")
    alert_id: str = Field(...)
