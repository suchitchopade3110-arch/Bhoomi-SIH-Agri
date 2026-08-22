"""Weather service — thin ``WeatherPort`` passthrough (contract §2.15)."""

from datetime import date
from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_weather_adapter
from app.ports.weather import WeatherPort
from app.domain.fao56 import effective_rainfall_mm
from app.schemas.weather import DailyWeatherForecast, WeatherCurrentResponse, WeatherEt0Response, WeatherForecastResponse


class WeatherService:
    """Exposes current/forecast/ET0 weather for the UI's "why this number?" views."""

    def __init__(self, weather: WeatherPort) -> None:
        self._weather = weather

    async def get_current(self, latitude: float, longitude: float) -> WeatherCurrentResponse:
        current = await self._weather.get_current_weather(latitude, longitude)
        return WeatherCurrentResponse(
            latitude=latitude,
            longitude=longitude,
            temperature_c=current["temperature_c"],
            relative_humidity_pct=current["relative_humidity_pct"],
            wind_speed_kmh=current.get("wind_speed_kmh", 0.0),
            precipitation_mm=current.get("precipitation_mm", 0.0),
            condition_description=current.get("condition_description", "Unknown"),
        )

    async def get_forecast(self, latitude: float, longitude: float, days: int = 7) -> WeatherForecastResponse:
        forecast = await self._weather.get_forecast(latitude, longitude, days)
        return WeatherForecastResponse(
            latitude=latitude,
            longitude=longitude,
            daily_forecasts=[
                DailyWeatherForecast(
                    forecast_date=day["forecast_date"],
                    temp_max_c=day["temp_max_c"],
                    temp_min_c=day["temp_min_c"],
                    precipitation_sum_mm=day["precipitation_sum_mm"],
                    et0_fao_evapotranspiration_mm=day["et0_fao_evapotranspiration_mm"],
                    precipitation_probability_pct=day["precipitation_probability_pct"],
                )
                for day in forecast
            ],
        )

    async def get_et0(self, latitude: float, longitude: float, target_date: date | None = None) -> WeatherEt0Response:
        target = target_date or date.today()
        et0 = await self._weather.get_daily_et0(latitude, longitude, target)
        current = await self._weather.get_current_weather(latitude, longitude)
        return WeatherEt0Response(
            latitude=latitude,
            longitude=longitude,
            date=target,
            et0_mm_day=et0,
            effective_rainfall_mm=effective_rainfall_mm(float(current.get("precipitation_mm", 0.0))),
        )


def get_weather_service(weather: Annotated[WeatherPort, Depends(get_weather_adapter)]) -> WeatherService:
    return WeatherService(weather)
