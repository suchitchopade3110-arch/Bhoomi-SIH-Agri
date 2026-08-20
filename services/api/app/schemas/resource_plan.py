"""FAO-56 Resource Planner schemas: Daily irrigation and seed requirements."""

from datetime import date, datetime
from pydantic import BaseModel, Field
from app.schemas.common import SpokenResponseMixin


class Fao56CalculateRequest(BaseModel):
    """Parameters for FAO-56 crop water requirement calculation."""
    crop: str = Field(..., description="Crop name (e.g. Paddy, Tomato, Cotton)")
    growth_stage: str = Field(..., description="Current growth stage: initial, development, mid_season, late_season")
    area_acres: float = Field(..., gt=0.0, description="Planted area in acres")
    soil_type: str = Field(default="Clay Loam", description="Soil texture classification")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    calculation_date: date | None = Field(default=None, description="Date for calculation")


class Fao56CalculateResponse(SpokenResponseMixin):
    """FAO-56 inspectable calculation outputs."""
    crop: str = Field(...)
    growth_stage: str = Field(...)
    area_acres: float = Field(...)
    
    # Inspectable Input Components
    et0_mm_day: float = Field(..., description="Reference evapotranspiration (ET₀) in mm/day from weather")
    kc_factor: float = Field(..., description="Crop coefficient (Kc) for current growth stage")
    etc_mm_day: float = Field(..., description="Crop evapotranspiration (ETc = ET₀ * Kc) in mm/day")
    effective_rainfall_mm: float = Field(..., description="Effective precipitation credited")
    irrigation_need_mm: float = Field(..., description="Net irrigation requirement in mm")
    
    # Actionable Volumes
    daily_liters_total: float = Field(..., description="Total liters of water required today")
    liters_per_acre: float = Field(..., description="Liters required per acre today")
    pump_runtime_hours_5hp: float = Field(..., description="Estimated pump run time for a standard 5HP agricultural pump")
    
    calculation_formula: str = "Net_Need = max(0, (ET0 * Kc) - Effective_Rainfall) * Area * 4046.86"
    computed_at: datetime = Field(default_factory=datetime.utcnow)


class ResourcePlanResponse(SpokenResponseMixin):
    """Combined resource plan for water, seeds, and fertilizers."""
    farm_id: str = Field(...)
    irrigation_plan: Fao56CalculateResponse
    recommended_seed_kg: float = Field(..., description="Calculated seed mass in kg for farm area")
    seed_variety: str = Field(...)
    fertilizer_schedule: list[dict[str, str]] = Field(default_factory=list)
