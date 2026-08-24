"""Pure domain logic for deriving qualitative farm advisory sentences and trend trajectories.

Replaces numeric health/risk scoring with a single qualitative sentence + trend indicator
derived directly from three signals:
  1. Active problem load (open problem count, severity, primary issue)
  2. Monitoring recency (days elapsed since last scan or field check-in)
  3. Treatment response (latest follow-up response: improved / no_change / got_worse)

Invariants:
  - Zero numeric scoring, zero weights, zero sub-indices.
  - Pure & deterministic: same inputs always produce identical sentences and trends.
  - No I/O, no datetime.now() inside the derivation (caller passes elapsed days/timestamps).
  - Day-0 case: honest unrated-equivalent message when no problem and no scan data exist.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Literal


class AdvisoryTrend(str, Enum):
    """Trend direction of crop condition."""

    IMPROVING = "improving"
    STABLE = "stable"
    WORSENING = "worsening"


@dataclass(frozen=True)
class QualitativeAdvisoryResult:
    """Pure domain outcome containing one qualitative sentence and trend indicator."""

    advisory: str
    trend: AdvisoryTrend


def derive_qualitative_advisory(
    *,
    open_problems_count: int = 0,
    highest_severity: Literal["early", "moderate", "severe"] | str | None = None,
    primary_problem_label: str | None = None,
    days_since_last_scan: int | None = None,
    latest_followup_response: Literal["improved", "no_change", "got_worse"] | str | None = None,
) -> QualitativeAdvisoryResult:
    """Derive a single qualitative advisory sentence and trend from farm status signals."""
    # 1. Day-0 / Unrated state: no problems recorded and no monitoring data recorded
    if open_problems_count == 0 and days_since_last_scan is None and latest_followup_response is None:
        return QualitativeAdvisoryResult(
            advisory="Insufficient monitoring data recorded yet to assess crop condition. Submit a crop photo or record a field check-in to begin tracking.",
            trend=AdvisoryTrend.STABLE,
        )

    # 2. Treatment response signals take precedence for ongoing management
    if latest_followup_response == "got_worse":
        if primary_problem_label:
            name = primary_problem_label.replace("_", " ")
            sentence = f"Crop condition has worsened following treatment for {name}; expert intervention recommended."
        else:
            sentence = "Crop condition has worsened following recent treatment; expert intervention recommended."
        return QualitativeAdvisoryResult(
            advisory=sentence,
            trend=AdvisoryTrend.WORSENING,
        )

    if latest_followup_response == "improved":
        if open_problems_count == 0:
            return QualitativeAdvisoryResult(
                advisory="Crop recovery confirmed following treatment; no active pest or disease detected.",
                trend=AdvisoryTrend.IMPROVING,
            )
        if primary_problem_label:
            name = primary_problem_label.replace("_", " ")
            sentence = f"Crop recovery observed following treatment for {name}; continue recommended care."
        else:
            sentence = "Crop recovery observed following recent treatment; continue recommended care."
        return QualitativeAdvisoryResult(
            advisory=sentence,
            trend=AdvisoryTrend.IMPROVING,
        )

    # 3. Active problem load (without follow-up improvement)
    if open_problems_count > 0:
        sev = highest_severity or "active"
        if sev == "severe" or open_problems_count >= 2:
            if primary_problem_label:
                name = primary_problem_label.replace("_", " ")
                sentence = f"Severe {name} pressure detected requiring immediate attention."
            else:
                sentence = "Multiple active crop stress factors detected requiring immediate attention."
            return QualitativeAdvisoryResult(
                advisory=sentence,
                trend=AdvisoryTrend.WORSENING,
            )

        # Early or moderate single problem
        if primary_problem_label:
            name = primary_problem_label.replace("_", " ")
            sentence = f"Managing {sev} {name}; follow recommended advisory actions and monitor closely."
        else:
            sentence = f"Managing {sev} crop condition; follow recommended advisory actions and monitor closely."
        
        # If follow-up reported no change, trend is stable; otherwise stable by default
        trend = AdvisoryTrend.STABLE
        return QualitativeAdvisoryResult(
            advisory=sentence,
            trend=trend,
        )

    # 4. Zero active problems: evaluate monitoring recency
    if days_since_last_scan is not None and days_since_last_scan > 7:
        return QualitativeAdvisoryResult(
            advisory=f"No active pest or disease detected, but last scan was {days_since_last_scan} days ago; new scan recommended.",
            trend=AdvisoryTrend.STABLE,
        )

    return QualitativeAdvisoryResult(
        advisory="Crop condition is clear with no active pest or disease problems reported.",
        trend=AdvisoryTrend.STABLE,
    )
