"""Expert escalation and case file schemas."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import CaseStatus, ProblemSeverity, ProblemStatus
from app.schemas.case import CaseSummary
from app.schemas.common import HealthMovement, SpokenResponseMixin


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
    status: CaseStatus = Field(default=CaseStatus.ASSIGNED)
    severity: ProblemSeverity = Field(...)
    assigned_kvk_center: str = Field(default="TNAU KVK - Madurai", description="Assigned Krishi Vigyan Kendra center")
    case_summary: CaseSummary = Field(..., description="Auto-compiled living case file summary")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ProblemEscalateRequest(BaseModel):
    """POST /problems/{problem_id}/escalate request body (contract §2.13):
    a manual, farmer/officer-initiated escalation of one problem. The same
    trigger also fires automatically from DiagnosisService/FollowupService."""
    farm_id: str = Field(..., description="UUID string of farm")
    reason: str = Field(..., description="Why this problem needs expert review")
    severity: ProblemSeverity = Field(default=ProblemSeverity.EARLY)
    notes: str | None = Field(default=None, description="Optional extra context folded into the case summary")


class ProblemEscalateResponse(BaseModel):
    """POST /problems/{problem_id}/escalate response — mirrors contract
    §2.13's example exactly: ``{"case_id", "assigned_to", "status"}``."""
    case_id: str
    assigned_to: str = Field(..., description="Agronomist assigned to the case")
    status: CaseStatus
    spoken_summary: str | None = Field(
        default=None, description="Concise localized summary text optimized for voice readback"
    )


class CaseResolveRequest(BaseModel):
    """POST /cases/{case_id}/resolve request body — mirrors contract §2.13 exactly."""
    diagnosis: str = Field(..., description="Agronomist-confirmed diagnosis")
    treatment: str = Field(..., description="Prescribed treatment")
    notes: str | None = Field(default=None, description="Optional follow-up guidance, e.g. 'Recheck in 5 days.'")


class CaseResolveResponse(BaseModel):
    """POST /cases/{case_id}/resolve response — mirrors contract §2.13 exactly."""
    case_id: str
    status: CaseStatus
    problem_status: ProblemStatus
    health: HealthMovement
