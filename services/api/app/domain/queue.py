"""Pure domain logic for agronomist queue position + ETA (PRD §5.11, Phase 2).

No I/O, no clock calls: the caller (a service) fetches the raw case rows
and hands in ``evaluated_at``. Same inputs, same output, always.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta

from app.core.enums import ProblemSeverity

# Severe cases are worked first regardless of arrival order; within a
# severity tier, first-escalated is first-served.
_SEVERITY_QUEUE_PRIORITY: dict[ProblemSeverity, int] = {
    ProblemSeverity.SEVERE: 0,
    ProblemSeverity.MODERATE: 1,
    ProblemSeverity.EARLY: 2,
}

# Conservative default average time an agronomist spends resolving one case
# end to end, used only until real historical resolution-time data exists.
DEFAULT_AVG_RESOLUTION_MINUTES = 45.0


@dataclass(frozen=True)
class QueueCase:
    case_id: str
    assigned_to: str
    severity: ProblemSeverity
    escalated_at: datetime


def compute_queue_positions(cases: list[QueueCase]) -> dict[str, int]:
    """1-based queue position for each case, scoped to its own
    ``assigned_to`` center — a farmer cares how many cases are ahead of
    theirs at *their* KVK center, not the platform-wide count.

    Ordered by severity (severe first), then earliest ``escalated_at``,
    then ``case_id`` for a fully deterministic tie-break.
    """
    positions: dict[str, int] = {}
    by_center: dict[str, list[QueueCase]] = {}
    for case in cases:
        by_center.setdefault(case.assigned_to, []).append(case)

    for center_cases in by_center.values():
        ordered = sorted(
            center_cases,
            key=lambda c: (_SEVERITY_QUEUE_PRIORITY[c.severity], c.escalated_at, c.case_id),
        )
        for index, case in enumerate(ordered, start=1):
            positions[case.case_id] = index

    return positions


def estimate_eta(
    position: int,
    evaluated_at: datetime,
    avg_resolution_minutes: float = DEFAULT_AVG_RESOLUTION_MINUTES,
) -> datetime:
    """Estimated time this case will be reached, given ``position`` cases
    (including itself) ahead of or at it in its center's queue.

    Position 1 (next up) resolves in one resolution slot; each case ahead
    of it adds another slot.
    """
    if position < 1:
        raise ValueError("position must be >= 1")
    return evaluated_at + timedelta(minutes=avg_resolution_minutes * position)
