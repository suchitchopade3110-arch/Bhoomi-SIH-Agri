"""Government scheme and subsidy discovery schemas."""

from datetime import date, datetime
from typing import Any
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


class SchemeRequirementsRequest(BaseModel):
    """Farmer-submitted eligibility details for a specific scheme.

    ``farm_id`` gates this the same way ``SchemeMatchRequest`` does — never
    confirm eligibility against unverified land. ``additional_data`` (e.g.
    ``category``, ``annual_income_bracket``) is accepted for eligibility
    display purposes only; there is no per-farmer scheme-application table
    in this schema (PRD §2.2 non-goal: no live government integration), so
    it is not persisted anywhere yet — this endpoint verifies the farm's
    land status and returns the scheme's real details, it does not fabricate
    a stored "application" record.
    """
    farm_id: str = Field(..., description="UUID string of farm — used to gate on verified land status")
    additional_data: dict[str, Any] = Field(
        default_factory=dict,
        description="Farmer-provided details (e.g. category, annual_income_bracket) — display-only, not persisted",
    )
