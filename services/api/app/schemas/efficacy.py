"""Treatment efficacy schemas (SPEC-EFFICACY-001 §4.2)."""

from typing import Literal

from pydantic import BaseModel, Field


class EfficacyResponse(BaseModel):
    """GET /treatments/{treatment_id}/efficacy response — exactly one of
    the two contract shapes (below/at the sample-size floor, or not)."""

    treatment_id: str = Field(...)
    pathogen: str = Field(...)
    crop: str = Field(...)
    region: str = Field(...)
    status: Literal["insufficient_data", "statistically_significant"] = Field(...)
    sample_size: int = Field(...)
    min_sample_threshold: int = Field(...)
    efficacy_percentage: float | None = Field(default=None)
    avg_days_to_recovery: float | None = Field(default=None)
