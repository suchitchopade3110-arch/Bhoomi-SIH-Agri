"""Farm Health Score schemas — mirror contract §2.9 exactly."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.core.enums import HealthBand, SubIndexKey
from app.schemas.common import PaginatedResponse, SpokenResponseMixin


class SubIndexBreakdown(BaseModel):
    """One row of the transparent six-sub-index breakdown (contract §2.9)."""

    key: SubIndexKey
    value: int | None = Field(default=None, ge=0, le=100, description="Raw sub-index score (0-100), null when unrated")
    weight: float = Field(..., ge=0.0, le=1.0)
    contribution: float | None = Field(default=None, description="value * weight, null when unrated")


class HealthSnapshot(SpokenResponseMixin):
    """Transparent, inspectable health score snapshot for a farm (contract §2.9).

    ``score`` is ``None`` and ``band`` is ``unrated`` — never ``0`` — until
    enough inputs exist to compute a real score (PRD §5.2, §7.1).
    """

    score: int | None = Field(default=None, ge=0, le=100, description="Aggregated 0-100 score; null when unrated")
    band: HealthBand
    computed_at: datetime = Field(default_factory=datetime.utcnow)
    weights_version: str
    subindices: list[SubIndexBreakdown] = Field(default_factory=list)
    triggering_input: dict[str, Any] | None = Field(
        default=None,
        description="The event that triggered this computation, e.g. {'type': 'diagnosis', 'problem_id': 'p_7', 'severity': 'early'}",
    )
    missing_fields: list[str] = Field(
        default_factory=list,
        description="Present only when band=unrated: the onboarding/monitoring fields still needed to compute a score",
    )


class HealthHistoryResponse(PaginatedResponse[HealthSnapshot]):
    """Cursor-paginated, chronological ``HealthSnapshot`` history for a farm."""
