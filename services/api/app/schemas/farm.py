"""Farm and crop context schemas."""

from datetime import date, datetime
from typing import Any
from pydantic import BaseModel, Field
from app.core.enums import LandStatus
from app.schemas.common import SpokenResponseMixin


class FarmCreateRequest(BaseModel):
    """Payload to register a farm profile."""
    farmer_id: str = Field(..., description="UUID string of the farmer")
    farm_name: str = Field(..., description="Identifying name of the farm")
    village: str = Field(..., description="Village or local revenue village")
    taluk: str = Field(..., description="Taluk / sub-district")
    district: str = Field(..., description="District")
    state: str = Field(default="Tamil Nadu", description="State")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Centroid latitude")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Centroid longitude")
    total_area_acres: float = Field(..., gt=0.0, description="Total farm area in acres")
    survey_number: str | None = Field(default=None, description="Cadastral survey number")
    primary_crop: str = Field(..., description="Main active crop (e.g. Paddy, Tomato, Cotton)")
    growth_stage: str = Field(default="vegetative", description="Current growth stage: initial, vegetative, mid_season, late_season")
    sowing_date: date | None = Field(default=None, description="Crop sowing date")
    soil_type: str = Field(default="Clay Loam", description="Soil classification")
    irrigation_source: str = Field(default="Borewell", description="Primary irrigation source")

    # Optional self-reported monitoring inputs the health engine needs
    # (PRD §7.2 sub-indices #1/#3/#5). Left unset, the farm stays `unrated`
    # (PRD §5.2) until these — and irrigation_delivered/required_mm, filled
    # in by the resource-plan step — are all present.
    soil_moisture_pct: float | None = Field(default=None, ge=0.0, le=100.0, description="Self-reported/sensor soil moisture %")
    days_since_planting: int | None = Field(default=None, ge=0, description="Days since sowing, as of onboarding")
    days_since_last_scan: int | None = Field(default=None, ge=0, description="Days since the last field scan/photo")


class FarmUpdateRequest(BaseModel):
    """Payload to update farm profile."""
    farm_name: str | None = None
    primary_crop: str | None = None
    growth_stage: str | None = None
    sowing_date: date | None = None
    soil_type: str | None = None
    irrigation_source: str | None = None


class FarmResponse(BaseModel):
    """Farm profile details."""
    id: str = Field(..., description="UUID string of the farm")
    farmer_id: str = Field(..., description="UUID string of the farmer")
    farm_name: str = Field(..., description="Name of farm")
    village: str = Field(...)
    taluk: str = Field(...)
    district: str = Field(...)
    state: str = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
    total_area_acres: float = Field(...)
    survey_number: str | None = None
    land_status: LandStatus = Field(default=LandStatus.UNVERIFIED)
    primary_crop: str = Field(...)
    growth_stage: str | None = None
    soil_type: str = Field(...)
    irrigation_source: str = Field(...)
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

