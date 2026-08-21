"""Pure domain logic for the Living Case Summary and the follow-up
escalation trigger (PRD §5.10/§5.11, contract §2.12/§2.13). No I/O, no DB,
no network — everything real-world (repositories, routing, persistence)
lives in ``services/escalation/``.
"""

from app.core.enums import CaseStatus, FollowupResponse, HealthBand, ProblemSeverity
from app.schemas.case import CaseFarmRef, CaseHealthRef, CaseImage, CaseProblemRef, CaseSummary, TimelineEvent

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
    crop: str,
    area_acres_verified: float | None,
    soil_type: str,
    problem_id: str,
    problem_label: str,
    severity: ProblemSeverity,
    timeline: list[TimelineEvent],
    images: list[CaseImage],
    treatments_tried: list[str],
    followup_trend: FollowupResponse | None,
    health_score: int | None,
    health_band: HealthBand,
    status: CaseStatus,
) -> CaseSummary:
    """Assemble the Living Case Summary (contract §2.13's ``GET /cases/{id}``
    shape, exactly) from its already gathered, plain-value parts.

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
        farm=CaseFarmRef(id=farm_id, crop=crop, area_acres_verified=area_acres_verified, soil_type=soil_type),
        problem=CaseProblemRef(id=problem_id, label=problem_label, severity=severity),
        timeline=timeline,
        images=images,
        treatments_tried=treatments_tried,
        followup_trend=followup_trend,
        current_health=CaseHealthRef(score=health_score, band=health_band),
        status=status,
    )
