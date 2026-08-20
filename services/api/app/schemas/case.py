"""Case Summary schema per API Contract §2.13 for human expert escalation."""

from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field
from app.core.enums import CaseStatus, ProblemSeverity
from app.schemas.common import SpokenResponseMixin


class CaseSummary(SpokenResponseMixin):
    """Living case file summary compiled for KVK agronomist / officer review."""
    case_id: str = Field(..., description="UUID string of the case file")
    farm_id: str = Field(..., description="UUID string of the associated farm")
    farmer_name: str = Field(..., description="Full name of the farmer")
    village: str = Field(..., description="Village or local revenue division")
    district: str = Field(..., description="District name")
    crop: str = Field(..., description="Active crop variety")
    growth_stage: str = Field(..., description="Current crop growth stage")
    health_score: float = Field(..., ge=0.0, le=100.0, description="Current transparent health score")
    land_verified: bool = Field(..., description="Whether land boundary has passed HITL verification")
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
    created_at: datetime = Field(default_factory=datetime.utcnow, description="ISO 8601 UTC creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="ISO 8601 UTC update timestamp")
