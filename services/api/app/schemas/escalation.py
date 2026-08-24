"""Expert escalation and case file schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import CaseStatus, ProblemSeverity
from app.schemas.case import CaseSummary
from app.schemas.common import SpokenResponseMixin


class EscalationCreateRequest(BaseModel):
    """Manual or system escalation request."""
    farm_id: str = Field(..., description="UUID string of farm")
    reason: str = Field(..., description="Trigger reason (e.g., 'below_confidence_gate', 'farmer_requested')")
    severity: ProblemSeverity = Field(default=ProblemSeverity.EARLY)
    notes: str | None = None
    related_diagnosis_id: str | None = None
    related_advisory_id: str | None = None


class EscalationResponse(SpokenResponseMixin):
    """Escalation receipt with compiled CaseSummary."""
    escalation_id: str = Field(..., description="UUID string of escalation")
    farm_id: str = Field(...)
    status: CaseStatus = Field(default=CaseStatus.ESCALATED)
    severity: ProblemSeverity = Field(...)
    assigned_kvk_center: str = Field(default="TNAU KVK - Madurai", description="Assigned Krishi Vigyan Kendra center")
    case_summary: CaseSummary = Field(..., description="Auto-compiled living case file summary")
    queue_position: int = Field(..., description="1-based position in the assigned agronomist's queue")
    eta: datetime = Field(..., description="Estimated time this case will be reached, e.g. 'you're 3rd, ~24 min'")
    created_at: datetime = Field(default_factory=datetime.utcnow)
