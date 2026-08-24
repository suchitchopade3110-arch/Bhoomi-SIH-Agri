"""Farm Health Score aggregation (PRD §7.2): weighted sum -> band, with a
full, inspectable breakdown. Pure and deterministic — no I/O.
"""

from dataclasses import dataclass

from app.core.enums import HealthBand
from app.domain.health import constants as c
from app.domain.health.inputs import HealthScoreInputs, TriggeringInput
from app.domain.health.subindices import SubIndexBreakdown, compute_all_subindices


@dataclass(frozen=True)
class HealthScoreResult:
    """The domain-layer result of a health computation.

    ``services/health_service.py`` maps this onto the persisted
    ``HealthSnapshot`` ORM row and the API response schema — this type has
    no knowledge of either.
    """

    score: int | None
    band: HealthBand
    subindices: list[SubIndexBreakdown]
    triggering_input: TriggeringInput
    weights_version: str
    missing_fields: list[str]


def band_for(score: int | None) -> HealthBand:
    """Map a score (or ``None``) to its health band (PRD §7.5).

    ``None`` always maps to ``UNRATED`` — a low number and "no data" are
    never conflated (PRD §7.1).
    """
    if score is None:
        return HealthBand.UNRATED
    for upper_bound, band in c.BAND_THRESHOLDS:
        if score <= upper_bound:
            return band
    return HealthBand.EXCELLENT  # unreachable given BAND_THRESHOLDS covers 0-100, kept for safety


def _missing_fields(inputs: HealthScoreInputs) -> list[str]:
    missing = []
    if inputs.weather is None:
        missing.append("weather")
    if inputs.crop_ideal is None:
        missing.append("crop_ideal")
    if not inputs.has_interaction:
        missing.append("interactions")
    return missing


def compute_health(inputs: HealthScoreInputs) -> HealthScoreResult:
    """Compute the transparent, weighted Farm Health Score (PRD §7.2).

    Args:
        inputs: A fully-assembled ``HealthScoreInputs`` for one farm at one
            point in time. Fields may be ``None`` to represent genuinely
            missing data.

    Returns:
        A ``HealthScoreResult`` with ``score=None`` and ``band=UNRATED`` if
        any required input is missing (PRD §5.2, §7.1: Day 0 is Unrated, not
        0). Otherwise the weighted sum of the six sub-indices, rounded and
        clamped to ``[0, 100]``, with the full per-sub-index breakdown.
    """
    if not inputs.required_inputs_present():
        return HealthScoreResult(
            score=None,
            band=HealthBand.UNRATED,
            subindices=[],
            triggering_input=inputs.triggering_input,
            weights_version=c.WEIGHTS_VERSION,
            missing_fields=_missing_fields(inputs),
        )

    subindices = compute_all_subindices(inputs)
    weighted_sum = sum(s.contribution for s in subindices)
    score = max(0, min(100, round(weighted_sum)))

    return HealthScoreResult(
        score=score,
        band=band_for(score),
        subindices=subindices,
        triggering_input=inputs.triggering_input,
        weights_version=c.WEIGHTS_VERSION,
        missing_fields=[],
    )
