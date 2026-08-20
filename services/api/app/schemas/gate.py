"""Decision gate schemas for confidence-gated diagnosis and advisory."""

from pydantic import BaseModel, Field
from app.core.enums import GateOutcome
from app.schemas.common import SpokenResponseMixin


class Decision(SpokenResponseMixin):
    """Decision outcome from the confidence gate."""
    outcome: GateOutcome = Field(
        ...,
        description="Gate decision: 'answer' if confidence >= threshold, 'escalate' if below",
    )
    reason: str = Field(..., description="Inspectable explanation of why this decision was reached")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Evaluated model or retrieval confidence score")
    threshold: float = Field(..., ge=0.0, le=1.0, description="Operating threshold gate")
    advisory_ref: str | None = Field(default=None, description="UUID string reference to generated Advisory if answered")
    escalation_ref: str | None = Field(default=None, description="UUID string reference to Escalation Case if escalated")
