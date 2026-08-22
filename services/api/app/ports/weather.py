"""Weather port — typed Protocol for meteorological data (ET₀, rainfall, forecast)."""

from datetime import date
from typing import Any, Protocol


class WeatherPort(Protocol):
    """Port for retrieving meteorological data, ET₀, and rainfall forecasts."""

    async def get_current_weather(self, latitude: float, longitude: float) -> dict[str, Any]:
        """Fetch current weather metrics (temperature, humidity, precipitation)."""
        ...

    async def get_daily_et0(self, latitude: float, longitude: float, target_date: date) -> float:
        """Fetch FAO-56 reference evapotranspiration (ET₀) in mm/day."""
        ...

    async def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> list[dict[str, Any]]:
        """Fetch daily weather and precipitation forecast for specified days."""
        ...


__all__ = ["WeatherPort"]
