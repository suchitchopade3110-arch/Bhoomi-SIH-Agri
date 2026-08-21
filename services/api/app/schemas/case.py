"""Case Summary schemas — mirror contract §2.13's ``GET /cases/{id}`` exactly."""

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.enums import HealthBand


class CaseFarmRef(BaseModel):
    id: str
    crop: str
    area_acres_verified: float | None = None
    soil_type: str | None = None


class CaseProblemRef(BaseModel):
    id: str
    label: str
    severity: str


class TimelineEvent(BaseModel):
    at: str
    event: str
    detail: str


class CaseImageRef(BaseModel):
    asset_id: str
    url: str


class CaseHealthRef(BaseModel):
    score: int | None = None
    band: HealthBand


class CaseSummary(BaseModel):
    """The pre-analyzed bundle an agronomist opens (PRD §5.11, contract §2.13)."""

    case_id: str
    farm: CaseFarmRef
    problem: CaseProblemRef | None = None
    timeline: list[TimelineEvent] = Field(default_factory=list)
    images: list[CaseImageRef] = Field(default_factory=list)
    treatments_tried: list[str] = Field(default_factory=list)
    followup_trend: str | None = None
    current_health: CaseHealthRef
    status: str


class CaseQueueItem(BaseModel):
    """One row of ``GET /agronomist/case-queue`` — an abbreviated CaseSummary."""

    case_id: str
    farm_id: str
    problem: CaseProblemRef | None = None
    status: str
    assigned_to: str | None = None
    trigger: str
    current_health: CaseHealthRef
    created_at: datetime
