"""Weather API router (contract §2.15)."""

from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.core.security import get_current_token_payload
from app.schemas.weather import (
    WeatherCurrentResponse,
    WeatherEt0Response,
    WeatherForecastResponse,
)
from app.services.weather_service import WeatherService, get_weather_service

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get(
    "/current",
    response_model=WeatherCurrentResponse,
    summary="Get current weather metrics for coordinates",
)
async def get_current_weather(
    service: Annotated[WeatherService, Depends(get_weather_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
) -> WeatherCurrentResponse:
    return await service.get_current(latitude, longitude)


@router.get(
    "/forecast",
    response_model=WeatherForecastResponse,
    summary="Get short-term weather and precipitation forecast",
)
async def get_weather_forecast(
    service: Annotated[WeatherService, Depends(get_weather_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    days: int = Query(default=7, ge=1, le=16),
) -> WeatherForecastResponse:
    return await service.get_forecast(latitude, longitude, days)


@router.get(
    "/et0",
    response_model=WeatherEt0Response,
    summary="Get FAO-56 daily reference evapotranspiration (ET₀)",
)
async def get_daily_et0(
    service: Annotated[WeatherService, Depends(get_weather_service)],
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    latitude: float = Query(..., ge=-90.0, le=90.0),
    longitude: float = Query(..., ge=-180.0, le=180.0),
    target_date: date | None = Query(default=None),
) -> WeatherEt0Response:
    return await service.get_et0(latitude, longitude, target_date)
