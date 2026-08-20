"""Weather API router."""

from datetime import date
from fastapi import APIRouter, Query
from app.core.errors import NotImplementedAPIError
from app.schemas.weather import (
    WeatherCurrentResponse,
    WeatherEt0Response,
    WeatherForecastResponse,
)

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get(
    "/current",
    response_model=WeatherCurrentResponse,
    summary="Get current weather metrics for coordinates",
)
async def get_current_weather(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
) -> WeatherCurrentResponse:
    raise NotImplementedAPIError("Endpoint GET /weather/current will be implemented in subsequent phases.")


@router.get(
    "/forecast",
    response_model=WeatherForecastResponse,
    summary="Get 7-day weather and precipitation forecast",
)
async def get_weather_forecast(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    days: int = Query(default=7, ge=1, le=16),
) -> WeatherForecastResponse:
    raise NotImplementedAPIError("Endpoint GET /weather/forecast will be implemented in subsequent phases.")


@router.get(
    "/et0",
    response_model=WeatherEt0Response,
    summary="Get FAO-56 daily reference evapotranspiration (ET₀)",
)
async def get_daily_et0(
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    target_date: date | None = Query(default=None),
) -> WeatherEt0Response:
    raise NotImplementedAPIError("Endpoint GET /weather/et0 will be implemented in subsequent phases.")
