"""Case PDF / share-sheet payload schema (Phase 4 Objective 2).

Structured backend payload derived strictly as a presentation superset of the Phase 3
CaseSummaryBundle for app-side PDF and share-sheet rendering.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.case import CaseSummaryBundle


class CasePDFPayload(BaseModel):
    """Structured data payload for rendering a case PDF or agronomist share sheet."""

    case_id: str = Field(..., description="Unique UUID string of the escalation case")
    farm_id: str = Field(..., description="UUID string of the farm")
    farmer_name: str = Field(default="Farmer", description="Farmer name")
    village: str = Field(default="", description="Village location")
    district: str = Field(default="", description="District")
    assigned_kvk: str | None = Field(default=None, description="Assigned KVK center name or ID")
    severity: str = Field(..., description="Problem severity: early | moderate | severe")
    status: str = Field(..., description="Case status: escalated | in_review | resolved")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Payload compilation timestamp")
    bundle: CaseSummaryBundle = Field(..., description="Core 8-key case summary bundle from Phase 3")
    summary_headline: str = Field(..., description="One-line summary for header presentation")
    prescribed_actions_summary: str | None = Field(default=None, description="Agronomist prescription if resolved")
    share_url: str | None = Field(default=None, description="Deep-link URL for sharing case with extension officers")

    model_config = {"frozen": True}
