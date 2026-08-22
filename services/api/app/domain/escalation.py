"""Pure domain logic for assembling Farm Living Case Summaries (PRD §5.11).

No I/O: every value is handed in by the caller (``services/escalation_service.py``
/ ``services/agronomist_service.py``), which is responsible for gathering it
from repositories. Same inputs, same ``CaseSummary``, always.
"""

from typing import Any

from app.core.enums import CaseStatus, ProblemSeverity
from app.schemas.case import CaseSummary

# A short, deterministic fallback used when no LLM-synthesized problem
# summary is available (e.g. StubLLMAdapter unreachable) — never blocks
# escalation on the LLM being up (PRD §5.11: routing must not silently fail).
FALLBACK_PROBLEM_SUMMARY_TEMPLATE = (
    "{crop} showing {label} symptoms (severity: {severity}). "
    "Health score {health_score:.0f}. Farmer-reported trend: {trend}."
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
) -> CaseSummary:
    """Compile the multi-factor Farm Case Summary for human expert handoff.

    Args:
        case_id: UUID string of the case/escalation.
        farm_info: Farm profile fields (id, farmer name, village, district,
            crop, growth_stage, land_status).
        recent_events: Chronological timeline entries leading up to escalation.
        current_health_score: Current transparent health score (0-100).
        problem_details: The specific issue (label, severity, images).
        assigned_officer_or_kvk: Target expert identifier, or ``None`` if not
            yet routed.
        status: Current lifecycle status of the case.
        problem_summary_text: Pre-synthesized summary (e.g. from ``LLMPort
            .synthesize_case_summary``); falls back to a deterministic
            template if not supplied.

    Returns:
        A structured ``CaseSummary`` ready to hand to an agronomist/officer.
    """
    severity = problem_details.get("severity", ProblemSeverity.EARLY)
    summary_text = problem_summary_text or FALLBACK_PROBLEM_SUMMARY_TEMPLATE.format(
        crop=farm_info.get("primary_crop", "crop"),
        label=problem_details.get("label", "an unspecified issue"),
        severity=severity.value if isinstance(severity, ProblemSeverity) else severity,
        health_score=current_health_score,
        trend=problem_details.get("trend", "unknown"),
    )

    return CaseSummary(
        case_id=case_id,
        farm_id=farm_info["id"],
        farmer_name=farm_info.get("farmer_name", "Unknown"),
        village=farm_info.get("village", ""),
        district=farm_info.get("district", ""),
        crop=farm_info.get("primary_crop", ""),
        growth_stage=farm_info.get("growth_stage") or "unknown",
        health_score=current_health_score,
        land_verified=farm_info.get("land_status") == "verified",
        problem_summary=summary_text,
        severity=severity if isinstance(severity, ProblemSeverity) else ProblemSeverity(severity),
        status=status,
        timeline_summary=recent_events,
        latest_images=problem_details.get("images", []),
        escalated_to=assigned_officer_or_kvk,
        spoken_summary=f"A case for {farm_info.get('farmer_name', 'this farmer')} has been sent to {assigned_officer_or_kvk or 'an expert'}.",
    )
