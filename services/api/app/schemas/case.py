"""Case Summary schema per API Contract §2.13 for human expert escalation."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from app.core.enums import CaseStatus, ProblemSeverity
from app.schemas.common import SpokenResponseMixin


class CaseSummaryBundle(BaseModel):
    """Living Case Summary Bundle compiled for expert agronomist handoff (SIH26131).

    Strictly contains 8 keys:
      - crop: Active crop variety
      - region: Geographical region/district/village
      - growth_stage: Current crop growth stage
      - problem_history: Timeline slice of past/active problems
      - images: List of image asset IDs or URLs
      - treatments_tried: Treatments and inputs applied by farmer
      - followup_trend: Farmer-reported followup trend
      - current_advisory: Current qualitative advisory text or trend summary
    """
    crop: str
    region: str
    growth_stage: str
    problem_history: list[dict[str, Any]] = Field(default_factory=list)
    images: list[Any] = Field(default_factory=list)
    treatments_tried: list[str] = Field(default_factory=list)
    followup_trend: str | None = None
    current_advisory: str | None = None


class CaseSummary(SpokenResponseMixin):
    """Living case file summary compiled for KVK agronomist / officer review."""
    case_id: str = Field(..., description="UUID string of the case file")
    farm_id: str = Field(..., description="UUID string of the associated farm")
    farmer_name: str = Field(..., description="Full name of the farmer")
    village: str = Field(..., description="Village or local revenue division")
    district: str = Field(..., description="District name")
    crop: str = Field(..., description="Active crop variety")
    growth_stage: str = Field(..., description="Current crop growth stage")
    health_score: float | None = Field(default=None, ge=0.0, le=100.0, description="Current transparent health score, or None if unrated")
    problem_summary: str = Field(..., description="Concise multi-factor summary of crop condition and issue")
    severity: ProblemSeverity = Field(..., description="Assessed problem severity")
    status: CaseStatus = Field(..., description="Current case status")
    timeline_summary: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Key chronological timeline milestones leading up to escalation",
    )
    latest_images: list[str] = Field(
        default_factory=list,
        description="Presigned URLs or asset IDs of recently uploaded disease/field photos",
    )
    escalated_to: str | None = Field(
        default=None,
        description="Identifier or name of assigned KVK agronomist or officer",
    )
    bundle: CaseSummaryBundle | None = Field(
        default=None,
        description="The 8-key escalation bundle for expert handoff",
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, description="ISO 8601 UTC creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="ISO 8601 UTC update timestamp")

