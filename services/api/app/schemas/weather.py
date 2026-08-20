"""Weather API schemas (Open-Meteo integration)."""

from datetime import date, datetime
from pydantic import BaseModel, Field
from app.schemas.common import SpokenResponseMixin


class WeatherCurrentResponse(SpokenResponseMixin):
    """Current atmospheric weather conditions."""
    latitude: float
    longitude: float
    temperature_c: float
    relative_humidity_pct: float
    wind_speed_kmh: float
    precipitation_mm: float
    condition_description: str
    observed_at: datetime = Field(default_factory=datetime.utcnow)


class DailyWeatherForecast(BaseModel):
    """Daily forecast item."""
    forecast_date: date
    temp_max_c: float
    temp_min_c: float
    precipitation_sum_mm: float
    et0_fao_evapotranspiration_mm: float
    precipitation_probability_pct: int


class WeatherForecastResponse(SpokenResponseMixin):
    """7-day forecast output."""
    latitude: float
    longitude: float
    daily_forecasts: list[DailyWeatherForecast] = Field(default_factory=list)


class WeatherEt0Response(BaseModel):
    """Daily reference evapotranspiration (ET₀) response."""
    latitude: float
    longitude: float
    date: date
    et0_mm_day: float
    effective_rainfall_mm: float
