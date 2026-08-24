"""Named constants for the Farm Health / Risk Score rubric (SIH26131).

Every weight and penalty the scoring engine uses lives here, named, so a judge
(or a reviewer) can point at a single number instead of hunting for a literal
buried in a formula. Nothing in this module performs I/O or depends on any
other layer.
"""

from app.core.enums import HealthBand, ProblemSeverity, SubIndexKey

# --------------------------------------------------------------------------
# SIH26131 — the four sub-index weights. Must sum to exactly 1.0.
# --------------------------------------------------------------------------
WEIGHTS: dict[SubIndexKey, float] = {
    SubIndexKey.ACTIVE_PROBLEM_SEVERITY: 0.40,
    SubIndexKey.ENVIRONMENTAL_RISK: 0.25,
    SubIndexKey.MONITORING_RECENCY: 0.15,
    SubIndexKey.TREATMENT_RESPONSE: 0.20,
}
WEIGHTS_V2_SIH26131 = WEIGHTS
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "Sub-index weights must sum to exactly 1.0 (SIH26131)."

# The fixed response order used everywhere a sub-index breakdown is rendered
# (API responses, spoken summaries).
SUBINDEX_ORDER: tuple[SubIndexKey, ...] = (
    SubIndexKey.ACTIVE_PROBLEM_SEVERITY,
    SubIndexKey.ENVIRONMENTAL_RISK,
    SubIndexKey.MONITORING_RECENCY,
    SubIndexKey.TREATMENT_RESPONSE,
)

# --------------------------------------------------------------------------
# Active problem severity penalties (Early: 30, Moderate: 55, Severe: 80)
# --------------------------------------------------------------------------
SEVERITY_PENALTY: dict[ProblemSeverity, int] = {
    ProblemSeverity.EARLY: 30,
    ProblemSeverity.MODERATE: 55,
    ProblemSeverity.SEVERE: 80,
}

# --------------------------------------------------------------------------
# Health bands. Upper bounds are inclusive; UNRATED is handled
# separately (it is not a numeric range, see domain/health/score.py).
# --------------------------------------------------------------------------
BAND_THRESHOLDS: tuple[tuple[int, HealthBand], ...] = (
    (39, HealthBand.CRITICAL),
    (59, HealthBand.POOR),
    (74, HealthBand.WATCH),
    (89, HealthBand.GOOD),
    (100, HealthBand.EXCELLENT),
)

WEIGHTS_VERSION = "v2-sih26131"

# --------------------------------------------------------------------------
# Sub-index #2 — environmental_risk
# Penalizes deviation of the current weather reading from the crop's
# ideal range at its current growth stage.
# Baseline environmental risk when no live weather reading is available.
# Mirrors MONITORING_RECENCY_DEFAULT: an honest "no data yet" anchor rather
# than a computed value. Pinned to the SIH26131 spec §1.5 fixture baseline.
# --------------------------------------------------------------------------
ENVIRONMENTAL_RISK_DEFAULT = 70
TEMP_DEVIATION_PENALTY_PER_DEGREE_C = 2.0
HUMIDITY_DEVIATION_PENALTY_PER_PCT = 1.25

# --------------------------------------------------------------------------
# Sub-index #3 — monitoring_recency
# Penalizes staleness of the last farm scan/data point.
# Baseline neutral default is 70; expert verification achieves 90 / 95.
# --------------------------------------------------------------------------
MONITORING_RECENCY_DEFAULT = 70
MONITORING_RECENCY_EXPERT_VERIFIED = 95
MONITORING_RECENCY_PENALTY_PER_DAY = 5.0

# --------------------------------------------------------------------------
# Sub-index #4 — treatment_response
# Driven by the latest closed-loop follow-up and expert resolution.
# Baseline is 70 (spec §1.4); got_worse is 40 (spec §1.4);
# no_change is 50 (spec §1.4 ratified); improved is 90 (spec §1.4 ratified);
# confirmed resolution is 95 (spec §1.4).
# --------------------------------------------------------------------------
TREATMENT_RESPONSE_DEFAULT = 70
TREATMENT_RESPONSE_GOT_WORSE = 40
TREATMENT_RESPONSE_NO_CHANGE = 50
TREATMENT_RESPONSE_IMPROVED = 90
TREATMENT_RESPONSE_CONFIRMED_RESOLVED = 95

