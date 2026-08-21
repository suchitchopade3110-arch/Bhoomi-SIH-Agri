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
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProblemEscalateRequest(BaseModel):
    """POST /problems/{problem_id}/escalate request body (Phase 4 item 6):
    a manual, farmer/officer-initiated escalation of one problem."""
    farm_id: str = Field(..., description="UUID string of farm")
    reason: str = Field(..., description="Why this problem needs expert review")
    severity: ProblemSeverity = Field(default=ProblemSeverity.EARLY)
    notes: str | None = Field(default=None, description="Optional extra context folded into the case summary")


class CaseResolveRequest(BaseModel):
    """POST /cases/{case_id}/resolve request body (Phase 4 item 6, contract §2.13)."""
    agronomist_id: str = Field(..., description="UUID string of the resolving agronomist")
    agronomist_name: str = Field(..., description="Agronomist display name")
    confirmed_diagnosis: str = Field(..., description="Agronomist-validated diagnosis")
    expert_advice: str = Field(..., description="Actionable prescription for the farmer")
    prescribed_inputs: list[str] = Field(default_factory=list)
