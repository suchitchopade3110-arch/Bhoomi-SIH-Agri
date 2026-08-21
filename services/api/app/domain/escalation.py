"""Pure domain logic for the Living Case Summary and the follow-up
escalation trigger (PRD §5.10/§5.11, contract §2.12/§2.13). No I/O, no DB,
no network — everything real-world (repositories, routing, persistence)
lives in ``services/escalation/``.
"""

from typing import Any

from app.core.enums import CaseStatus, HealthBand, ProblemSeverity
from app.schemas.case import CaseSummary

# --------------------------------------------------------------------------
# Severity promotion ladder (PRD §5.10): a "got worse" follow-up promotes the
# problem one tier, capped at severe — it never demotes and never skips a tier.
# --------------------------------------------------------------------------
_SEVERITY_PROMOTION: dict[ProblemSeverity, ProblemSeverity] = {
    ProblemSeverity.EARLY: ProblemSeverity.MODERATE,
    ProblemSeverity.MODERATE: ProblemSeverity.SEVERE,
    ProblemSeverity.SEVERE: ProblemSeverity.SEVERE,
}

# A follow-up that drives the recomputed health band to Poor or Critical has
# crossed below "Watch" (PRD §7.4/§7.5) — that band drop is itself the
# auto-escalation trigger, on top of (not instead of) the severity promotion.
AUTO_ESCALATE_BANDS: frozenset[HealthBand] = frozenset({HealthBand.POOR, HealthBand.CRITICAL})


def promote_severity(current: ProblemSeverity) -> ProblemSeverity:
    """One tier up the ladder (early -> moderate -> severe), capped at severe."""
    return _SEVERITY_PROMOTION[current]


def should_auto_escalate(new_band: HealthBand) -> bool:
    """True once a follow-up's recomputed health band crosses below Watch
    (PRD §7.4's worked example: 68 "watch" -> 59 "poor" auto-escalates)."""
    return new_band in AUTO_ESCALATE_BANDS


def build_case_summary(
    case_id: str,
    farm_id: str,
    farmer_name: str,
    village: str,
    district: str,
    crop: str,
    growth_stage: str,
    health_score: float,
    land_verified: bool,
    problem_summary: str,
    severity: ProblemSeverity,
    status: CaseStatus,
    timeline_summary: list[dict[str, Any]],
    latest_images: list[str],
    escalated_to: str | None,
    spoken_summary: str,
) -> CaseSummary:
    """Assemble the Living Case Summary (contract §2.13) from its already
    gathered, plain-value parts.

    This is the single point every escalation trigger — below-gate/
    out-of-scope diagnosis, no-retrieval diagnosis, a got_worse follow-up,
    or a manual escalation — funnels through, so the case file always
    carries the same complete shape regardless of what triggered it.
    ``services/escalation/case_compiler.py`` is responsible for the I/O that
    gathers these arguments from repositories; this function does no
    fetching of its own.
    """
    return CaseSummary(
        case_id=case_id,
        farm_id=farm_id,
        farmer_name=farmer_name,
        village=village,
        district=district,
        crop=crop,
        growth_stage=growth_stage,
        health_score=health_score,
        land_verified=land_verified,
        problem_summary=problem_summary,
        severity=severity,
        status=status,
        timeline_summary=timeline_summary,
        latest_images=latest_images,
        escalated_to=escalated_to,
        spoken_summary=spoken_summary,
    )
