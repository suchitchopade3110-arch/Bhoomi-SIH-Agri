"""Escalation & case summary — the pure pieces (PRD §5.9-§5.11).

Severity promotion, the auto-escalate rule, CaseSummary assembly, and
agronomist selection: all deterministic, all zero I/O. Fetching the data
those pieces need, and persisting the result, is orchestration and lives in
``services/escalation/``.
"""

from app.domain.escalation.case_summary import (
    CaseSummaryData,
    FarmRef,
    HealthRef,
    ImageRef,
    ProblemRef,
    TimelineEntry,
    compile_case_summary,
)
from app.domain.escalation.routing import AgronomistCandidate, select_agronomist
from app.domain.escalation.rules import should_auto_escalate
from app.domain.escalation.severity import demote_severity, promote_severity

__all__ = [
    "CaseSummaryData",
    "FarmRef",
    "ProblemRef",
    "TimelineEntry",
    "ImageRef",
    "HealthRef",
    "compile_case_summary",
    "AgronomistCandidate",
    "select_agronomist",
    "should_auto_escalate",
    "promote_severity",
    "demote_severity",
]
