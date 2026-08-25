"""Pure domain logic for assembling Farm Living Case Summaries (PRD §5.11).

No I/O: every value is handed in by the caller (``services/escalation_service.py``
/ ``services/agronomist_service.py``), which is responsible for gathering it
from repositories. Same inputs, same ``CaseSummary``, always.
"""

from typing import Any

from app.core.enums import CaseStatus, ProblemSeverity
from app.schemas.case import CaseSummary, CaseSummaryBundle

# A deterministic fallback formatter used when no LLM-synthesized problem
# summary is available (e.g. StubLLMAdapter unreachable) — never blocks
# escalation on the LLM being up (PRD §5.11: routing must not silently fail).
FALLBACK_PROBLEM_SUMMARY_TEMPLATE = (
    "{crop} showing {label} symptoms (severity: {severity}). "
    "Health score: {health_score}. Farmer-reported trend: {trend}."
)


def compile_case_summary_bundle(
    crop: str,
    region: str,
    growth_stage: str,
    problem_history: list[dict[str, Any]] | None = None,
    images: list[Any] | None = None,
    treatments_tried: list[str] | None = None,
    followup_trend: str | None = None,
    current_advisory: str | None = None,
) -> CaseSummaryBundle:
    """Compile the standardized 8-key CaseSummaryBundle (SIH26131).

    Strictly:
      crop, region, growth_stage, problem_history, images,
      treatments_tried, followup_trend, current_advisory
    No land/soil fields (e.g. area_acres_verified, soil_type) are present.
    """
    clean_growth = growth_stage if growth_stage and growth_stage.lower() != "unknown" else "Stage unrecorded"
    clean_region = region if region and region.lower() != "unknown" else "Region unrecorded"
    clean_trend = followup_trend if followup_trend and followup_trend.lower() not in ("unknown", "none") else None

    return CaseSummaryBundle(
        crop=crop,
        region=clean_region,
        growth_stage=clean_growth,
        problem_history=problem_history or [],
        images=images or [],
        treatments_tried=treatments_tried or [],
        followup_trend=clean_trend,
        current_advisory=current_advisory,
    )


def build_case_summary(
    case_id: str,
    farm_info: dict[str, Any],
    recent_events: list[dict[str, Any]],
    current_health_score: float | None,
    problem_details: dict[str, Any],
    assigned_officer_or_kvk: str | None,
    status: CaseStatus,
    problem_summary_text: str | None = None,
    current_advisory_text: str | None = None,
) -> CaseSummary:
    """Compile the multi-factor Farm Case Summary for human expert handoff.

    Args:
        case_id: UUID string of the case/escalation.
        farm_info: Farm profile fields (id, farmer name, village, district,
            crop, growth_stage).
        recent_events: Chronological timeline entries leading up to escalation.
        current_health_score: Current transparent health score (0-100) or None if unrated.
        problem_details: The specific issue (label, severity, images, treatments_tried, trend).
        assigned_officer_or_kvk: Target expert identifier, or ``None`` if not
            yet routed.
        status: Current lifecycle status of the case.
        problem_summary_text: Pre-synthesized summary (e.g. from ``LLMPort
            .synthesize_case_summary``); falls back to a deterministic
            grammatical template if not supplied.
        current_advisory_text: Phase 2 qualitative advisory text/trend.

    Returns:
        A structured ``CaseSummary`` with an 8-key ``bundle`` ready to hand to an agronomist.
    """
    severity = problem_details.get("severity", ProblemSeverity.EARLY)
    severity_val = severity.value if isinstance(severity, ProblemSeverity) else str(severity)
    crop_name = farm_info.get("primary_crop") or farm_info.get("crop") or "Crop"
    village = (farm_info.get("village") or "").strip()
    district = (farm_info.get("district") or farm_info.get("region") or "").strip()
    if village and district:
        region_str = f"{village}, {district}"
    elif district:
        region_str = district
    elif village:
        region_str = village
    else:
        region_str = "Region unrecorded"

    growth_stage = farm_info.get("growth_stage")
    clean_growth_stage = growth_stage if growth_stage and growth_stage.lower() != "unknown" else "Stage unrecorded"
    images = problem_details.get("images", [])
    treatments_tried = problem_details.get("treatments_tried", [])
    trend = problem_details.get("trend") or farm_info.get("trend")

    label = problem_details.get("label")
    if label and str(label).strip() and str(label).strip().lower() not in ("unspecified", "unknown", "none", "an unspecified issue"):
        clean_label = str(label).replace("_", " ")
        problem_clause = f"{crop_name} showing {clean_label} symptoms (severity: {severity_val})"
    else:
        problem_clause = f"{crop_name} under observation for {severity_val} severity symptoms"

    if current_health_score is not None:
        health_str = f"Health score: {current_health_score:.0f}"
    else:
        health_str = "Health score: Unrated"

    if trend and str(trend).lower() in ("got_worse", "worsening", "worse"):
        trend_str = "Farmer-reported trend: worsening"
    elif trend and str(trend).lower() in ("improved", "improving"):
        trend_str = "Farmer-reported trend: improving"
    elif trend and str(trend).lower() in ("no_change", "stable"):
        trend_str = "Farmer-reported trend: stable"
    elif not trend or str(trend).lower() in ("unknown", "none", ""):
        trend_str = "No prior follow-ups recorded"
    else:
        trend_str = f"Farmer-reported trend: {trend}"

    summary_text = problem_summary_text or f"{problem_clause}. {health_str}. {trend_str}."

    bundle = compile_case_summary_bundle(
        crop=crop_name,
        region=region_str,
        growth_stage=clean_growth_stage,
        problem_history=recent_events,
        images=images,
        treatments_tried=treatments_tried,
        followup_trend=trend if trend and str(trend).lower() not in ("unknown", "none", "") else None,
        current_advisory=current_advisory_text or summary_text,
    )

    raw_farmer_name = farm_info.get("farmer_name")
    if raw_farmer_name and str(raw_farmer_name).strip() and str(raw_farmer_name).strip().lower() not in ("unknown", "none"):
        farmer_subject = str(raw_farmer_name).strip()
        clean_farmer_name = str(raw_farmer_name).strip()
    else:
        farmer_subject = f"this {crop_name} farm" if crop_name and crop_name != "Crop" else "this farm"
        clean_farmer_name = "Unregistered Farmer"

    target_expert = assigned_officer_or_kvk or "an expert"

    return CaseSummary(
        case_id=case_id,
        farm_id=farm_info.get("id", ""),
        farmer_name=clean_farmer_name,
        village=village,
        district=district,
        crop=crop_name,
        growth_stage=clean_growth_stage,
        health_score=current_health_score,
        problem_summary=summary_text,
        severity=severity if isinstance(severity, ProblemSeverity) else ProblemSeverity(severity),
        status=status if isinstance(status, CaseStatus) else CaseStatus(status),
        timeline_summary=recent_events,
        latest_images=[img if isinstance(img, str) else img.get("url", img.get("asset_id", "")) for img in images],
        escalated_to=assigned_officer_or_kvk,
        bundle=bundle,
        spoken_summary=f"A case for {farmer_subject} has been sent to {target_expert}.",
    )


