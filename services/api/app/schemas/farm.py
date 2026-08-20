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
    sowing_date: date | None = Field(default=None, description="Crop sowing date")
    soil_type: str = Field(default="Clay Loam", description="Soil classification")
    irrigation_source: str = Field(default="Borewell", description="Primary irrigation source")


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
