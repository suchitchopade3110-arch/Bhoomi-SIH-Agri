"""Named constants for the Farm Health Score rubric (PRD §7).

Every weight and penalty the scoring engine uses lives here, named, so a judge
(or a reviewer) can point at a single number instead of hunting for a literal
buried in a formula. Nothing in this module performs I/O or depends on any
other layer.
"""

from app.core.enums import HealthBand, ProblemSeverity, SubIndexKey

# --------------------------------------------------------------------------
# PRD §7.2 — the six sub-index weights. Must sum to exactly 1.0.
# --------------------------------------------------------------------------
WEIGHTS: dict[SubIndexKey, float] = {
    SubIndexKey.ENVIRONMENTAL_SUITABILITY: 0.20,
    SubIndexKey.RESOURCE_ADEQUACY: 0.15,
    SubIndexKey.CROP_STAGE_PROGRESSION: 0.15,
    SubIndexKey.ACTIVE_PROBLEM_LOAD: 0.30,
    SubIndexKey.MONITORING_RECENCY: 0.10,
    SubIndexKey.TREATMENT_RESPONSE: 0.10,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "Sub-index weights must sum to exactly 1.0 (PRD §7.2)."

# The fixed response order used everywhere a sub-index breakdown is rendered
# (API responses, spoken summaries) — mirrors the contract's §2.9 example order.
SUBINDEX_ORDER: tuple[SubIndexKey, ...] = (
    SubIndexKey.ENVIRONMENTAL_SUITABILITY,
    SubIndexKey.RESOURCE_ADEQUACY,
    SubIndexKey.CROP_STAGE_PROGRESSION,
    SubIndexKey.ACTIVE_PROBLEM_LOAD,
    SubIndexKey.MONITORING_RECENCY,
    SubIndexKey.TREATMENT_RESPONSE,
)

# --------------------------------------------------------------------------
# PRD §7.3 — active problem load severity penalties (illustrative, tunable,
# documented — never hidden inside the formula).
# --------------------------------------------------------------------------
SEVERITY_PENALTY: dict[ProblemSeverity, int] = {
    ProblemSeverity.EARLY: 30,
    ProblemSeverity.MODERATE: 55,
    ProblemSeverity.SEVERE: 80,
}

# --------------------------------------------------------------------------
# PRD §7.5 — health bands. Upper bounds are inclusive; UNRATED is handled
# separately (it is not a numeric range, see domain/health/score.py).
# --------------------------------------------------------------------------
BAND_THRESHOLDS: tuple[tuple[int, HealthBand], ...] = (
    (39, HealthBand.CRITICAL),
    (59, HealthBand.POOR),
    (74, HealthBand.WATCH),
    (89, HealthBand.GOOD),
    (100, HealthBand.EXCELLENT),
)

WEIGHTS_VERSION = "v1"

# --------------------------------------------------------------------------
# Sub-index #1 — environmental_suitability
# Penalizes deviation of the current weather/soil reading from the crop's
# ideal range at its current growth stage.
# --------------------------------------------------------------------------
TEMP_DEVIATION_PENALTY_PER_DEGREE_C = 2.0
HUMIDITY_DEVIATION_PENALTY_PER_PCT = 1.25
SOIL_MOISTURE_DEFICIT_PENALTY_PER_PCT = 2.0

# --------------------------------------------------------------------------
# Sub-index #2 — resource_adequacy
# Ratio of irrigation actually delivered vs. the ET0-derived requirement,
# expressed 0-100. Over-delivery is treated as fully adequate (capped at 100)
# rather than penalized — the sub-index measures shortfall risk, not waste.
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Sub-index #3 — crop_stage_progression
# Penalizes the farm being ahead of / behind the days-since-planting a
# typical crop calendar expects for the current growth stage.
# --------------------------------------------------------------------------
STAGE_DEVIATION_PENALTY_PER_DAY = 2.0

# --------------------------------------------------------------------------
# Sub-index #5 — monitoring_recency
# Penalizes staleness of the last farm scan/data point.
# Baseline neutral default is 70; expert verification achieves 90.
# --------------------------------------------------------------------------
MONITORING_RECENCY_DEFAULT = 70
MONITORING_RECENCY_EXPERT_VERIFIED = 90
MONITORING_RECENCY_PENALTY_PER_DAY = 5.0

# --------------------------------------------------------------------------
# Sub-index #6 — treatment_response
# Discrete score driven by the latest closed-loop follow-up (PRD §5.10).
# Neutral baseline is 70; untreated active is 20; got_worse is 5; resolved is 90.
# --------------------------------------------------------------------------
TREATMENT_RESPONSE_DEFAULT = 70
TREATMENT_RESPONSE_UNTREATED_ACTIVE = 20
TREATMENT_RESPONSE_GOT_WORSE = 5
TREATMENT_RESPONSE_IMPROVED = 100
TREATMENT_RESPONSE_NO_CHANGE = 70
TREATMENT_RESPONSE_CONFIRMED_RESOLVED = 90

