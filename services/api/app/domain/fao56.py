"""Pure domain logic for FAO-56 crop water requirement calculations (PRD §5.4).

Architecture & Scope Note (Checklist §13.1):
Intentionally implemented directly in ``domain/fao56.py`` as an accepted single-source
pure domain calculation. No external computation libraries or duplicate calculation
paths exist; all irrigation water demand logic is centralized here.

No I/O: ET₀, effective rainfall, and Kc are all handed in by the caller
(``services/resource_plan_service.py``), which is responsible for fetching
them from ``WeatherPort`` / ``domain.farm_reference_data``. Same inputs,
same output, always.
"""

from app.schemas.resource_plan import Fao56CalculateResponse

# 1 acre = 4046.8564224 m²; 1 mm over 1 m² = 1 liter.
SQ_METERS_PER_ACRE = 4046.8564224

# Effective rainfall is credited at a fraction of gross rainfall (the rest
# runs off / percolates past the root zone before the crop can use it) — a
# simplified stand-in for the USDA SCS method named in PRD §5.4.
EFFECTIVE_RAINFALL_FACTOR = 0.8

# A standard 5HP agricultural pump's typical discharge, used only to turn a
# liters/day figure into an inspectable "how long do I run the pump" figure
# for the farmer (contract §2.8 `explanation`).
PUMP_5HP_DISCHARGE_LITERS_PER_HOUR = 12000.0

FAO56_FORMULA = "Net_Need_mm = max(0, (ET0 * Kc) - Effective_Rainfall); Liters = Net_Need_mm * Area_acres * 4046.86"


def effective_rainfall_mm(raw_rainfall_mm: float) -> float:
    """Effective rainfall credited toward crop water need (PRD §5.4)."""
    return round(raw_rainfall_mm * EFFECTIVE_RAINFALL_FACTOR, 4)


def calculate_fao56_irrigation(
    crop: str,
    growth_stage: str,
    area_acres: float,
    et0_mm_day: float,
    kc_factor: float,
    effective_rainfall_mm: float,
    soil_type: str = "Clay Loam",
) -> Fao56CalculateResponse:
    """Calculate daily irrigation water requirement via FAO-56 (PRD §5.4).

    Formula (contract §2.8):
        ETc = ET0 * Kc
        Net_Irrigation_mm = max(0, ETc - Effective_Rainfall)
        Total_Liters = Net_Irrigation_mm * Area_acres * 4046.8564224

    Args:
        crop: Crop name.
        growth_stage: Current growth stage (drives ``kc_factor`` upstream).
        area_acres: Planted/tillable area in acres.
        et0_mm_day: Reference evapotranspiration (mm/day), from ``WeatherPort``.
        kc_factor: FAO-56 crop coefficient for this crop/stage.
        effective_rainfall_mm: Rainfall actually creditable toward crop need.
        soil_type: Soil texture classification (carried through for context;
            does not yet adjust the calculation — see PRD §12 Phase-2 note
            on richer soil-water-holding modeling).

    Returns:
        The fully inspectable ``Fao56CalculateResponse`` — every number that
        fed the result, per PRD §5.4 ("why this many liters?").
    """
    etc_mm_day = round(et0_mm_day * kc_factor, 4)
    irrigation_need_mm = round(max(0.0, etc_mm_day - effective_rainfall_mm), 4)

    daily_liters_total = round(irrigation_need_mm * area_acres * SQ_METERS_PER_ACRE, 2)
    liters_per_acre = round(daily_liters_total / area_acres, 2) if area_acres > 0 else 0.0
    pump_runtime_hours_5hp = round(daily_liters_total / PUMP_5HP_DISCHARGE_LITERS_PER_HOUR, 2)

    return Fao56CalculateResponse(
        crop=crop,
        growth_stage=growth_stage,
        area_acres=area_acres,
        et0_mm_day=et0_mm_day,
        kc_factor=kc_factor,
        etc_mm_day=etc_mm_day,
        effective_rainfall_mm=effective_rainfall_mm,
        irrigation_need_mm=irrigation_need_mm,
        daily_liters_total=daily_liters_total,
        liters_per_acre=liters_per_acre,
        pump_runtime_hours_5hp=pump_runtime_hours_5hp,
        calculation_formula=FAO56_FORMULA,
        spoken_summary=(
            f"Today's water need is about {int(daily_liters_total):,} liters "
            f"for your {area_acres:g} acres of {crop.replace('_', ' ')}."
        ),
    )
