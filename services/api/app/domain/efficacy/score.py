"""Pure treatment-efficacy scoring engine (SPEC-EFFICACY-001 §4-5).

No I/O, no ``date.today()``: the caller (``EfficacyAggregatorService``)
assembles ``TreatmentApplicationSnapshot`` rows and passes an injected
``as_of``. Same inputs, same output, always. The write side —
``treatment_applications`` table, and the synchronous lifecycle hooks
inside ``FollowupService.checkin`` / ``AgronomistService.resolve`` — lives
in ``services/efficacy/tracking_service.py``.
"""

from datetime import date, timedelta

from app.domain.efficacy.models import EfficacyResult, TreatmentApplicationSnapshot

# Applications with either of these final_outcome values (or None) carry no
# efficacy signal — switched away from, or not yet resolved (spec §4.1).
_EXCLUDED_OUTCOMES = {"superseded", None}

# A failed_on_got_worse=False followups_to_resolution above this is treated
# as a stalled, unresolved-in-time application by lifecycle rules (spec
# §3.3's own "> 2 consecutive no_change -> failed" rule already sets
# final_outcome="failed" for that case) — kept here only as the success
# guard spec §4.1 names explicitly.
_MAX_FOLLOWUPS_FOR_SUCCESS = 2


def _is_success(app: TreatmentApplicationSnapshot) -> bool:
    return (
        app.final_outcome in ("resolved", "improved")
        and not app.failed_on_got_worse
        and (app.followups_to_resolution is None or app.followups_to_resolution <= _MAX_FOLLOWUPS_FOR_SUCCESS)
    )


def _is_failure(app: TreatmentApplicationSnapshot) -> bool:
    return app.failed_on_got_worse or app.final_outcome == "failed"


# Edge case beyond the spec's literal text: an application with
# final_outcome="improved" but followups_to_resolution > 2 fails the
# success guard yet isn't failed_on_got_worse or final_outcome=="failed"
# either. In practice the lifecycle hooks (spec §3.3) shouldn't produce
# this combination — "improved" closes an application immediately, and the
# >2-no_change rule sets final_outcome="failed" before followups could
# exceed 2 on a still-open one. Decision: treat it as excluded (like
# superseded/NULL), not a failure — it's genuinely ambiguous signal, not
# evidence the treatment failed.


def compute_efficacy(
    *,
    treatment_name: str,
    pathogen_type: str,
    crop: str,
    district: str,
    applications: list[TreatmentApplicationSnapshot],
    as_of: date,
    window_days: int = 365,
    min_sample_threshold: int = 10,
) -> EfficacyResult:
    """Population-level success rate for one (pathogen_type, treatment_name,
    crop, district) combination within the trailing ``window_days`` window.

    Defensively re-filters ``applications`` to the requested combination and
    window rather than trusting the caller pre-filtered exactly right — the
    determinism contract ("same inputs -> byte-identical result") holds
    regardless of what the caller hands in.
    """
    window_start = as_of - timedelta(days=window_days)

    in_scope = [
        app
        for app in applications
        if app.pathogen_type == pathogen_type
        and app.treatment_name == treatment_name
        and app.crop == crop
        and app.district == district
        and window_start <= app.applied_on <= as_of
    ]

    successes = [app for app in in_scope if _is_success(app)]
    failures = [app for app in in_scope if not _is_success(app) and _is_failure(app)]
    # Excluded (superseded / NULL outcome, or any other in-progress state)
    # contribute no signal and are simply not counted in either bucket.

    n_success = len(successes)
    n_total = n_success + len(failures)

    if n_total < min_sample_threshold:
        return EfficacyResult(
            treatment_id=treatment_name,
            pathogen=pathogen_type,
            crop=crop,
            region=district,
            status="insufficient_data",
            sample_size=n_total,
            min_sample_threshold=min_sample_threshold,
            efficacy_percentage=None,
            avg_days_to_recovery=None,
        )

    recovery_days = [app.days_to_resolution for app in successes if app.days_to_resolution is not None]
    avg_days_to_recovery = round(sum(recovery_days) / len(recovery_days), 1) if recovery_days else None

    return EfficacyResult(
        treatment_id=treatment_name,
        pathogen=pathogen_type,
        crop=crop,
        region=district,
        status="statistically_significant",
        sample_size=n_total,
        min_sample_threshold=min_sample_threshold,
        efficacy_percentage=round((n_success / n_total) * 100, 1),
        avg_days_to_recovery=avg_days_to_recovery,
    )
