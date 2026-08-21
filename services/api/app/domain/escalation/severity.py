"""Pure severity-promotion rule (PRD §7.3, §5.10). No I/O."""

from app.core.enums import ProblemSeverity

# Got Worse promotes exactly one tier; stays at the top once already severe.
SEVERITY_ESCALATION_ORDER: tuple[ProblemSeverity, ...] = (
    ProblemSeverity.EARLY,
    ProblemSeverity.MODERATE,
    ProblemSeverity.SEVERE,
)


def promote_severity(current: ProblemSeverity) -> ProblemSeverity:
    """One tier up (early -> moderate -> severe, PRD §7.3); a no-op once
    already at the top tier."""
    index = SEVERITY_ESCALATION_ORDER.index(current)
    return SEVERITY_ESCALATION_ORDER[min(index + 1, len(SEVERITY_ESCALATION_ORDER) - 1)]


def demote_severity(current: ProblemSeverity) -> ProblemSeverity:
    """One tier down (severe -> moderate -> early, PRD §7.3: "Improved
    demotes it"); a no-op once already at the lightest tier."""
    index = SEVERITY_ESCALATION_ORDER.index(current)
    return SEVERITY_ESCALATION_ORDER[max(index - 1, 0)]
