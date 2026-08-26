"""Farm and crop context schemas."""

from datetime import date, datetime
from typing import Any
from pydantic import BaseModel, Field
from app.core.enums import LandStatus, UiMode
from app.schemas.common import SpokenResponseMixin


class FarmCreateRequest(BaseModel):
    """Payload to register a farm profile (SIH26131 simplified onboarding)."""

    farmer_id: str | None = Field(default=None, description="UUID string of the farmer")
    crop: str = Field(..., description="Main active crop (e.g. samba_paddy, cotton)")
    growth_stage: str = Field(..., description="Current growth stage: initial, vegetative, reproductive, ripening")
    region: str = Field(..., description="Regional jurisdiction / agro-climatic zone")
    soil_type: str | None = None
    irrigation_access: str | None = None
    season: str | None = None


class FarmUpdateRequest(BaseModel):
    """Payload to update farm profile."""
    farm_name: str | None = None
    primary_crop: str | None = None
    growth_stage: str | None = None
    region: str | None = None
    sowing_date: date | None = None
    soil_type: str | None = None
    irrigation_source: str | None = None
    ui_mode: UiMode | None = Field(
        default=None, description="Veteran/novice UI density toggle (checklist §1.5)"
    )


class FarmResponse(BaseModel):
    """Farm profile details."""
    id: str = Field(..., description="UUID string of the farm")
    farmer_id: str = Field(..., description="UUID string of the farmer")
    farm_name: str | None = None
    village: str | None = None
    taluk: str | None = None
    district: str | None = None
    state: str = "Tamil Nadu"
    latitude: float | None = None
    longitude: float | None = None
    total_area_acres: float | None = None
    survey_number: str | None = None
    land_status: LandStatus = Field(default=LandStatus.UNVERIFIED)
    primary_crop: str = Field(...)
    growth_stage: str | None = None
    region: str | None = None
    soil_type: str | None = None
    irrigation_source: str | None = None
    ui_mode: UiMode = Field(
        default=UiMode.NOVICE, description="Veteran/novice UI density toggle (checklist §1.5)"
    )
    current_health_score: float | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class FarmSummaryResponse(SpokenResponseMixin):
    """Holistic summary of farm status, weather, health, and open tasks."""
    farm: FarmResponse
    weather_summary: dict[str, Any] = Field(default_factory=dict)
    active_advisories_count: int = 0
    open_cases_count: int = 0
    recommended_irrigation_liters_today: float | None = None


class FarmRiskTrendResponse(SpokenResponseMixin):
    """Qualitative risk trend response (frozen shape: advisory-not-score for SIH26131).

    Returns a qualitative advisory string plus a trend indicator, without numeric
    scores or sub-index breakdowns.
    """

    farm_id: str = Field(..., description="UUID string of farm")
    advisory: str = Field(..., description="Qualitative crop risk advisory summary")
    trend: str = Field(..., description="Risk trajectory: 'improving' | 'stable' | 'worsening'")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of latest risk evaluation")


class FarmSummaryTrendResponse(SpokenResponseMixin):
    """Qualitative farm summary card (frozen shape: advisory-not-score for SIH26131).

    Returns a qualitative farm status advisory and trend indicator, without numeric
    scores or sub-indices.
    """

    farm_id: str = Field(..., description="UUID string of farm")
    advisory: str = Field(..., description="Qualitative holistic farm health advisory")
    trend: str = Field(..., description="Overall trend indicator: 'improving' | 'stable' | 'worsening'")
    open_cases_count: int = Field(default=0, description="Active open escalated cases count")
    last_interaction_at: datetime | None = Field(default=None, description="Timestamp of latest scan or consultation")

