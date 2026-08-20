"""Health Score schemas matching the transparent 6-sub-index rubric."""

from datetime import datetime
from pydantic import BaseModel, Field
from app.core.enums import HealthBand, SubIndexKey
from app.schemas.common import SpokenResponseMixin


class SubIndexBreakdown(BaseModel):
    """Breakdown for one of the six transparent health sub-indices."""
    key: SubIndexKey = Field(..., description="Unique sub-index identifier")
    label: str = Field(..., description="Human-readable sub-index label")
    value: float = Field(..., ge=0.0, le=100.0, description="Raw sub-index score (0-100)")
    weight: float = Field(..., ge=0.0, le=1.0, description="Rubric weight allocated to this sub-index")
    contribution: float = Field(..., ge=0.0, le=100.0, description="Weighted contribution to total score (value * weight)")
    notes: str | None = Field(default=None, description="Explanation of factors driving this sub-index score")


class HealthSnapshot(SpokenResponseMixin):
    """Transparent, inspectable health score snapshot for a farm."""
    score: float = Field(..., ge=0.0, le=100.0, description="Aggregated farm health score (0-100)")
    band: HealthBand = Field(..., description="Health band classification")
    sub_indices: list[SubIndexBreakdown] = Field(
        ...,
        min_length=6,
        max_length=6,
        description="Full breakdown of all 6 weighted sub-indices",
    )
    triggering_input: str = Field(
        ...,
        description="The event or data ingestion that triggered this health score computation",
    )
    computed_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="ISO 8601 UTC timestamp of computation",
    )
    weights_version: str = Field(
        default="v1.0.0",
        description="Version identifier of the scoring weight rubric applied",
    )


class HealthHistoryResponse(BaseModel):
    """Historical timeline of health score snapshots for a farm."""
    farm_id: str = Field(..., description="UUID string of farm")
    snapshots: list[HealthSnapshot] = Field(default_factory=list, description="Chronological health score snapshots")
