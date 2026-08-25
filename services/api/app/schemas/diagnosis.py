"""Gated image+voice diagnosis schemas — mirror contract §2.10 exactly.

``target_type``/pest fields extend contract §2.10 per the SIH26131 delta
spec §3.1 — see ``diagnosis_service.py``'s module docstring for what's
implemented vs. still an honest placeholder (no ``pest_count_estimate``:
the delta spec itself calls that "pending Tharun's pest classification
schema", which never arrived, so it isn't fabricated here).
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.advisory import Citation, FivePointAdvisory
from app.schemas.common import SpokenResponseMixin
from app.schemas.gate import GateObject


class DiagnoseRequest(BaseModel):
    """POST /farms/{id}/diagnose request (contract §2.10)."""

    image_asset_id: str = Field(..., description="UUID string of the uploaded disease photo asset")
    description_asset_id: str | None = Field(default=None, description="Optional voice-note asset ID")
    description_text: str | None = Field(
        default=None, description="Optional text, e.g. from a prior transcription"
    )
    target_type: Literal["disease", "pest"] = Field(
        default="disease",
        description="Whether the photo is a disease or pest diagnosis attempt (SIH26131 delta spec §3.1)",
    )
    pest_type_hint: str | None = Field(
        default=None, description="Farmer-stated pest guess, if any (enriches the retrieval query only)"
    )


class DiagnosisResult(BaseModel):
    """The image model's raw output (contract §2.10 ``diagnosis`` object)."""

    label: str
    stage: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    target_type: Literal["disease", "pest"] = "disease"


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

    The ``gate`` object is populated on BOTH branches (contract §8).
    """

    above_gate: bool
    gate: GateObject | None = None
    problem_id: str | None = None
    diagnosis: DiagnosisResult | None = None
    advisory: FivePointAdvisory | None = None
    citations: list[Citation] = Field(default_factory=list)
    health_delta: HealthDelta | None = None
    reason: str | None = None
    escalation: EscalationRef | None = None

