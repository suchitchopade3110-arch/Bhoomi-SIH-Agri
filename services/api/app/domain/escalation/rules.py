"""Pure escalation-trigger rules (PRD §5.10, §5.11). No I/O.

Named, single-source-of-truth answers to "does this event open a case?" —
kept separate from severity promotion (severity.py) because promotion and
escalation are related but distinct decisions (a follow-up always promotes
severity on Got Worse; PRD §5.10 additionally says this "auto-escalates").
"""

from app.core.enums import FollowupResponse

# execution plan item 4 / PRD §5.10: "Got Worse past a threshold auto-
# escalates." The contract's own §2.12 example escalates on the very first
# Got Worse report (severity early -> moderate), so the chosen threshold
# here is the simplest one consistent with that example: severity promotion
# itself is the threshold — every Got Worse opens a case. Improved and
# No Change never auto-escalate via this path.
AUTO_ESCALATING_RESPONSES = frozenset({FollowupResponse.GOT_WORSE})


def should_auto_escalate(response: FollowupResponse) -> bool:
    """Whether a follow-up response should automatically open a case."""
    return response in AUTO_ESCALATING_RESPONSES
