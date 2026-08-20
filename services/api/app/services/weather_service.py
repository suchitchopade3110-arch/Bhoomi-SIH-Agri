"""Weather and ET₀ service."""

from datetime import date
from typing import Any
from app.schemas.weather import WeatherCurrentResponse, WeatherEt0Response, WeatherForecastResponse


class WeatherService:
    """Provides weather observations, forecasts, and FAO-56 ET₀ data."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def get_current(self, latitude: float, longitude: float) -> WeatherCurrentResponse:
        raise NotImplementedError("WeatherService.get_current will be implemented in subsequent phases.")

    async def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> WeatherForecastResponse:
        raise NotImplementedError("WeatherService.get_forecast will be implemented in subsequent phases.")

    async def get_et0(self, latitude: float, longitude: float, target_date: date) -> WeatherEt0Response:
        raise NotImplementedError("WeatherService.get_et0 will be implemented in subsequent phases.")
