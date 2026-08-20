"""Agronomist portal case queue and resolution schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import CaseStatus, ProblemSeverity
from app.schemas.case import CaseSummary


class AgronomistQueueItem(BaseModel):
    """Item in KVK agronomist review queue."""
    escalation_id: str = Field(...)
    farm_id: str = Field(...)
    farmer_name: str = Field(...)
    village: str = Field(...)
    crop: str = Field(...)
    severity: ProblemSeverity = Field(...)
    status: CaseStatus = Field(...)
    health_score: float = Field(...)
    escalated_at: datetime = Field(...)


class ResolveCaseRequest(BaseModel):
    """Agronomist resolution payload."""
    escalation_id: str = Field(...)
    agronomist_id: str = Field(...)
    agronomist_name: str = Field(...)
    confirmed_diagnosis: str = Field(..., description="Agronomist-validated diagnosis")
    expert_advice: str = Field(..., description="Actionable prescription for farmer")
    prescribed_inputs: list[str] = Field(default_factory=list)
    audio_notes_asset_id: str | None = None


class ResolveCaseResponse(BaseModel):
    """Response confirming case resolution."""
    escalation_id: str = Field(...)
    status: CaseStatus = Field(default=CaseStatus.RESOLVED)
    resolved_at: datetime = Field(default_factory=datetime.utcnow)
    message: str = "Case successfully resolved and dispatched to farmer."
