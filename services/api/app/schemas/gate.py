"""Decision gate schemas for confidence-gated diagnosis and advisory (Frozen Contract §8)."""

from pydantic import BaseModel, Field
from app.core.enums import GateOutcome
from app.schemas.common import SpokenResponseMixin


class GateObject(BaseModel):
    """The frozen confidence gate evaluation object (contract §8).

    Returned on both diagnose branches:
    - above_gate: True when confidence >= threshold and target label is in scope
    - confidence: The raw probability/confidence evaluated
    - threshold: The operating threshold floor
    - reason_code: Machine-readable explanation code if below gate or out of scope
    - alternatives: List of candidate diagnoses or labels if unconfident
    """

    above_gate: bool = Field(..., description="Whether the diagnosis passed the confidence gate")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Evaluated diagnosis confidence")
    threshold: float = Field(..., ge=0.0, le=1.0, description="Operating threshold floor")
    reason_code: str | None = Field(default=None, description="Reason code if rejected or escalated")
    alternatives: list[str] = Field(default_factory=list, description="Alternative candidate labels")


class Decision(SpokenResponseMixin):
    """Legacy/orchestration decision outcome from the confidence gate."""

    outcome: GateOutcome = Field(
        ...,
        description="Gate decision: 'answer' if confidence >= threshold, 'escalate' if below",
    )
    reason: str = Field(..., description="Inspectable explanation of why this decision was reached")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Evaluated model or retrieval confidence score")
    threshold: float = Field(..., ge=0.0, le=1.0, description="Operating threshold gate")
    advisory_ref: str | None = Field(default=None, description="UUID string reference to generated Advisory if answered")
    escalation_ref: str | None = Field(default=None, description="UUID string reference to Escalation Case if escalated")
