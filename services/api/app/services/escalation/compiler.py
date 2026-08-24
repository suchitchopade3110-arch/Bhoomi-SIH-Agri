"""services/escalation/compiler.py — spec-mandated escalation compiler module.

``build_case_summary`` assembles the pre-analyzed Farm Case Summary bundle
that the agronomist opens when an escalated case is assigned (PRD §5.11,
contract §2.13).

Triggers that call this function:
  - Gate fails (confidence below gate or crop out-of-scope) — Phase 2
  - Retrieval finds nothing above threshold                 — Phase 3
  - Follow-up response is ``got_worse`` past threshold     — Phase 4
"""

from typing import Any

from app.core.enums import CaseStatus, ProblemSeverity
from app.domain.escalation import (
    FALLBACK_PROBLEM_SUMMARY_TEMPLATE,
    build_case_summary as domain_build_case_summary,
    compile_case_summary_bundle,
)
from app.schemas.case import CaseSummary, CaseSummaryBundle


def build_case_summary(
    farm_id: str,
    problem_id: str,
    farm_info: dict[str, Any],
    recent_events: list[dict[str, Any]],
    images: list[Any],
    treatments_tried: list[str],
    followup_trend: str | None,
    current_health: dict[str, Any] | float | None = 0.0,
    assigned_to: str | None = None,
    severity: ProblemSeverity | str = ProblemSeverity.EARLY,
    status: CaseStatus = CaseStatus.ESCALATED,
    problem_summary_text: str | None = None,
    current_advisory_text: str | None = None,
) -> CaseSummary:
    """Compile a pre-analyzed Farm Case Summary for expert handoff (PRD §5.11).

    Gathers farm crop context, problem timeline, linked images,
    treatments tried, follow-up trend, and current health score.

    Args:
        farm_id: UUID of the farm.
        problem_id: UUID of the problem being escalated.
        farm_info: Dict containing crop, farmer_name, village, district, etc.
        recent_events: Chronological event list (diagnoses, follow-ups, treatments).
        images: List of image asset IDs or dicts.
        treatments_tried: Plain-language list of treatments the farmer has applied.
        followup_trend: Latest ``followup_response`` value or ``None``.
        current_health: Dict with ``score`` and ``band`` of the current snapshot (or float score).
        assigned_to: Target agronomist identifier, or ``None`` if unrouted yet.
        severity: Problem severity tier.
        status: Lifecycle status of case.
        problem_summary_text: Pre-synthesized LLM summary or None for template fallback.
        current_advisory_text: Phase 2 qualitative advisory text/trend.

    Returns:
        A populated ``CaseSummary`` domain model.
    """
    health_score = (
        current_health.get("score", 0.0) if isinstance(current_health, dict) else float(current_health or 0.0)
    )
    if health_score is None:
        health_score = 0.0

    problem_details = {
        "problem_id": problem_id,
        "severity": severity,
        "images": images,
        "treatments_tried": treatments_tried,
        "trend": followup_trend or "unknown",
    }

    # Ensure farm_info has farm_id
    info = dict(farm_info)
    if "id" not in info:
        info["id"] = farm_id

    return domain_build_case_summary(
        case_id=problem_id,
        farm_info=info,
        recent_events=recent_events,
        current_health_score=float(health_score),
        problem_details=problem_details,
        assigned_officer_or_kvk=assigned_to,
        status=status if isinstance(status, CaseStatus) else CaseStatus(status),
        problem_summary_text=problem_summary_text,
        current_advisory_text=current_advisory_text,
    )


__all__ = ["build_case_summary", "compile_case_summary_bundle", "CaseSummaryBundle"]

