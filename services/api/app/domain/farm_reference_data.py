"""Named agronomic reference tables shared by the resource planner and the
health engine (PRD §5.4, §7). Pure data — no I/O — deliberately centralized
here instead of scattered as literals through services/*.py.

Coverage is intentionally bounded to the Phase-5 demo crop (samba paddy,
PRD §13 recommendation) with a generic fallback for any other crop name, so
the planner and health engine never crash on an unmodeled crop — they just
fall back to a documented, conservative default instead of guessing.
"""

from app.domain.health.inputs import CropIdealConditions

# --------------------------------------------------------------------------
# FAO-56 crop coefficient (Kc) table, by (crop, growth_stage).
# Source: FAO-56 / ICAR package-of-practices (contract §2.8 `kc_source`).
# --------------------------------------------------------------------------
DEFAULT_KC = 0.95

CROP_KC_TABLE: dict[tuple[str, str], float] = {
    ("samba_paddy", "initial"): 1.10,
    ("samba_paddy", "vegetative"): 1.05,
    ("samba_paddy", "mid_season"): 1.20,
    ("samba_paddy", "late_season"): 0.90,
}


def get_kc(crop: str, growth_stage: str) -> float:
    """FAO-56 crop coefficient for ``crop`` at ``growth_stage``.

    Falls back to ``DEFAULT_KC`` for any crop/stage combination not in the
    curated table (PRD §12 Phase-2 note: "widen crop/disease coverage").
    """
    return CROP_KC_TABLE.get((crop, growth_stage), DEFAULT_KC)


# --------------------------------------------------------------------------
# Seed rate (kg/acre), by crop.
# --------------------------------------------------------------------------
DEFAULT_SEED_RATE_KG_PER_ACRE = 20.0

SEED_RATE_KG_PER_ACRE: dict[str, float] = {
    "samba_paddy": 30.0,
}


def get_seed_rate_kg_per_acre(crop: str) -> float:
    return SEED_RATE_KG_PER_ACRE.get(crop, DEFAULT_SEED_RATE_KG_PER_ACRE)


# --------------------------------------------------------------------------
# Expected days-since-planting at the *start* of each growth stage, used by
# the health engine's crop_stage_progression sub-index (PRD §7.2 #3) to
# judge whether a farm is on-schedule. One shared calendar across crops —
# a per-crop calendar is a documented Phase-2 follow-up (PRD §12).
# --------------------------------------------------------------------------
GROWTH_STAGE_EXPECTED_DAY: dict[str, int] = {
    "initial": 10,
    "vegetative": 30,
    "mid_season": 75,
    "late_season": 110,
}
DEFAULT_EXPECTED_STAGE_DAY = 30


def get_expected_stage_day(growth_stage: str) -> int:
    return GROWTH_STAGE_EXPECTED_DAY.get(growth_stage, DEFAULT_EXPECTED_STAGE_DAY)


# --------------------------------------------------------------------------
# Ideal environmental band consumed by the health engine's
# environmental_suitability sub-index (PRD §7.2 #1). One shared band across
# crops for this phase — see the same per-crop-calendar note above.
# --------------------------------------------------------------------------
DEFAULT_CROP_IDEAL = CropIdealConditions(
    temp_min_c=25.0,
    temp_max_c=35.0,
    humidity_min_pct=60.0,
    humidity_max_pct=80.0,
    soil_moisture_min_pct=65.0,
)


def get_crop_ideal(crop: str) -> CropIdealConditions:
    return DEFAULT_CROP_IDEAL
