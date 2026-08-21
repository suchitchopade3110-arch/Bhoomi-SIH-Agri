"""Gated image+voice diagnosis schemas — mirror contract §2.10 exactly."""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.advisory import Citation, FivePointAdvisory
from app.schemas.common import SpokenResponseMixin


class DiagnoseRequest(BaseModel):
    """POST /farms/{id}/diagnose request (contract §2.10)."""

    image_asset_id: str = Field(..., description="UUID string of the uploaded disease photo asset")
    description_asset_id: str | None = Field(default=None, description="Optional voice-note asset ID")
    description_text: str | None = Field(
        default=None, description="Optional text, e.g. from a prior transcription"
    )


class DiagnosisResult(BaseModel):
    """The image model's raw output (contract §2.10 ``diagnosis`` object)."""

    label: str
    stage: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class HealthDelta(BaseModel):
    """Before/after health score movement caused by this diagnosis (contract §2.10)."""

    model_config = ConfigDict(populate_by_name=True)

    from_: int | None = Field(default=None, alias="from")
    to: int | None = None


class EscalationRef(BaseModel):
    """Reference to the case an escalated diagnosis was routed to (contract §2.10)."""

    case_id: str
    assigned_to: str


class DiagnoseResponse(SpokenResponseMixin):
    """POST /farms/{id}/diagnose response — exactly one of the two contract shapes.

    ``above_gate=True``: ``problem_id``/``diagnosis``/``advisory``/
    ``citations``/``health_delta`` are populated, ``reason``/``escalation``
    are ``None``.
    ``above_gate=False``: only ``reason``/``escalation`` are populated —
    the model is never allowed to compose advice it isn't sure of.
    """

    above_gate: bool
    problem_id: str | None = None
    diagnosis: DiagnosisResult | None = None
    advisory: FivePointAdvisory | None = None
    citations: list[Citation] = Field(default_factory=list)
    health_delta: HealthDelta | None = None
    reason: str | None = None
    escalation: EscalationRef | None = None
