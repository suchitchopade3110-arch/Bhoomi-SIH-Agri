"""Case Summary schema — mirrors contract §2.13 ``GET /cases/{id}`` exactly:
the pre-analyzed bundle a KVK agronomist opens."""

from pydantic import BaseModel, Field

from app.core.enums import CaseStatus, FollowupResponse, HealthBand, ProblemSeverity


class CaseFarmRef(BaseModel):
    """Contract §2.13 ``case.farm``."""
    id: str = Field(..., description="UUID string of the farm")
    crop: str
    area_acres_verified: float | None = Field(
        default=None, description="Verified area; null if land isn't verified yet"
    )
    soil_type: str


class CaseProblemRef(BaseModel):
    """Contract §2.13 ``case.problem``."""
    id: str = Field(..., description="UUID string of the problem")
    label: str
    severity: ProblemSeverity


class TimelineEvent(BaseModel):
    """Contract §2.13 ``case.timeline[]`` entry."""
    at: str = Field(..., description="ISO 8601 UTC timestamp")
    event: str = Field(..., description="e.g. 'diagnosis', 'followup'")
    detail: str


class CaseImage(BaseModel):
    """Contract §2.13 ``case.images[]`` entry."""
    asset_id: str
    url: str


class CaseHealthRef(BaseModel):
    """Contract §2.13 ``case.current_health``."""
    score: int | None = Field(default=None, ge=0, le=100)
    band: HealthBand


class CaseSummary(BaseModel):
    """The Living Case Summary (contract §2.13 ``GET /cases/{id}``) — the
    pre-analyzed bundle the agronomist opens (PRD §5.11)."""

    case_id: str = Field(..., description="UUID string of the case file")
    farm: CaseFarmRef
    problem: CaseProblemRef
    timeline: list[TimelineEvent] = Field(default_factory=list)
    images: list[CaseImage] = Field(default_factory=list)
    treatments_tried: list[str] = Field(default_factory=list)
    followup_trend: FollowupResponse | None = None
    current_health: CaseHealthRef
    status: CaseStatus
