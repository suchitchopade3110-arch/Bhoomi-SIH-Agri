"""Government scheme and subsidy discovery schemas."""

from datetime import date, datetime
from pydantic import BaseModel, Field
from app.core.enums import SchemeStatus
from app.schemas.common import SpokenResponseMixin


class SchemeResponse(BaseModel):
    """Government agricultural scheme details."""
    id: str = Field(..., description="UUID string of scheme")
    name: str = Field(..., description="Scheme name (e.g., PM-KISAN, Micro Irrigation Subsidy)")
    ministry: str = Field(...)
    description: str = Field(...)
    benefits: str = Field(...)
    eligibility_criteria: dict[str, str] = Field(default_factory=dict)
    subsidy_percentage: float | None = None
    max_amount_inr: float | None = None
    portal_url: str | None = None
    status: SchemeStatus = Field(default=SchemeStatus.ACTIVE)
    last_verified: date = Field(..., description="Date eligibility rules were last verified")


class SchemeMatchRequest(BaseModel):
    """Request to match active subsidies for a verified farm."""
    farm_id: str = Field(...)
    farmer_category: str | None = Field(default="Small/Marginal", description="Farmer category: Small/Marginal, SC/ST, General")


class SchemeListResponse(SpokenResponseMixin):
    """Matched schemes for a farm."""
    farm_id: str = Field(...)
    matched_schemes: list[SchemeResponse] = Field(default_factory=list)
    match_count: int = 0
