"""Pure domain logic for assembling Farm Living Case Summaries (PRD §5.11).

No I/O: every value is handed in by the caller (``services/escalation_service.py``
/ ``services/agronomist_service.py``), which is responsible for gathering it
from repositories. Same inputs, same ``CaseSummary``, always.
"""

from typing import Any

from app.core.enums import CaseStatus, ProblemSeverity
from app.schemas.case import CaseSummary, CaseSummaryBundle

# A short, deterministic fallback used when no LLM-synthesized problem
# summary is available (e.g. StubLLMAdapter unreachable) — never blocks
# escalation on the LLM being up (PRD §5.11: routing must not silently fail).
FALLBACK_PROBLEM_SUMMARY_TEMPLATE = (
    "{crop} showing {label} symptoms (severity: {severity}). "
    "Health score {health_score:.0f}. Farmer-reported trend: {trend}."
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
    return CaseSummaryBundle(
        crop=crop,
        region=region,
        growth_stage=growth_stage,
        problem_history=problem_history or [],
        images=images or [],
        treatments_tried=treatments_tried or [],
        followup_trend=followup_trend,
        current_advisory=current_advisory,
    )


def build_case_summary(
    case_id: str,
    farm_info: dict[str, Any],
    recent_events: list[dict[str, Any]],
    current_health_score: float,
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
        current_health_score: Current transparent health score (0-100).
        problem_details: The specific issue (label, severity, images, treatments_tried, trend).
        assigned_officer_or_kvk: Target expert identifier, or ``None`` if not
            yet routed.
        status: Current lifecycle status of the case.
        problem_summary_text: Pre-synthesized summary (e.g. from ``LLMPort
            .synthesize_case_summary``); falls back to a deterministic
            template if not supplied.
        current_advisory_text: Phase 2 qualitative advisory text/trend.

    Returns:
        A structured ``CaseSummary`` with an 8-key ``bundle`` ready to hand to an agronomist.
    """
    severity = problem_details.get("severity", ProblemSeverity.EARLY)
    crop_name = farm_info.get("primary_crop") or farm_info.get("crop") or "crop"
    village = farm_info.get("village", "")
    district = farm_info.get("district", "")
    region_str = f"{village}, {district}".strip(", ") or district or village or "Unknown"
    growth_stage = farm_info.get("growth_stage") or "unknown"
    images = problem_details.get("images", [])
    treatments_tried = problem_details.get("treatments_tried", [])
    trend = problem_details.get("trend") or farm_info.get("trend") or "unknown"

    summary_text = problem_summary_text or FALLBACK_PROBLEM_SUMMARY_TEMPLATE.format(
        crop=crop_name,
        label=problem_details.get("label", "an unspecified issue"),
        severity=severity.value if isinstance(severity, ProblemSeverity) else severity,
        health_score=current_health_score,
        trend=trend,
    )

    bundle = compile_case_summary_bundle(
        crop=crop_name,
        region=region_str,
        growth_stage=growth_stage,
        problem_history=recent_events,
        images=images,
        treatments_tried=treatments_tried,
        followup_trend=trend if trend != "unknown" else None,
        current_advisory=current_advisory_text or summary_text,
    )

    return CaseSummary(
        case_id=case_id,
        farm_id=farm_info.get("id", ""),
        farmer_name=farm_info.get("farmer_name", "Unknown"),
        village=village,
        district=district,
        crop=crop_name,
        growth_stage=growth_stage,
        health_score=current_health_score,
        problem_summary=summary_text,
        severity=severity if isinstance(severity, ProblemSeverity) else ProblemSeverity(severity),
        status=status,
        timeline_summary=recent_events,
        latest_images=[img if isinstance(img, str) else img.get("url", img.get("asset_id", "")) for img in images],
        escalated_to=assigned_officer_or_kvk,
        bundle=bundle,
        spoken_summary=f"A case for {farm_info.get('farmer_name', 'this farmer')} has been sent to {assigned_officer_or_kvk or 'an expert'}.",
    )

