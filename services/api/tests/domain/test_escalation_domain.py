"""Unit tests for the pure escalation domain pieces: severity promotion/
demotion, the auto-escalate rule, agronomist selection, and CaseSummary
compilation/validation.
"""

import pytest

from app.core.enums import FollowupResponse, ProblemSeverity
from app.domain.escalation import (
    AgronomistCandidate,
    FarmRef,
    HealthRef,
    compile_case_summary,
    demote_severity,
    promote_severity,
    select_agronomist,
    should_auto_escalate,
)

# ---------------------------------------------------------------------------
# Severity promotion / demotion (PRD §7.3)
# ---------------------------------------------------------------------------


def test_promote_severity_early_to_moderate():
    assert promote_severity(ProblemSeverity.EARLY) == ProblemSeverity.MODERATE


def test_promote_severity_moderate_to_severe():
    assert promote_severity(ProblemSeverity.MODERATE) == ProblemSeverity.SEVERE


def test_promote_severity_severe_stays_severe():
    assert promote_severity(ProblemSeverity.SEVERE) == ProblemSeverity.SEVERE


def test_demote_severity_severe_to_moderate():
    assert demote_severity(ProblemSeverity.SEVERE) == ProblemSeverity.MODERATE


def test_demote_severity_early_stays_early():
    assert demote_severity(ProblemSeverity.EARLY) == ProblemSeverity.EARLY


# ---------------------------------------------------------------------------
# Auto-escalate rule
# ---------------------------------------------------------------------------


def test_got_worse_auto_escalates():
    assert should_auto_escalate(FollowupResponse.GOT_WORSE) is True


def test_improved_does_not_auto_escalate():
    assert should_auto_escalate(FollowupResponse.IMPROVED) is False


def test_no_change_does_not_auto_escalate():
    assert should_auto_escalate(FollowupResponse.NO_CHANGE) is False


# ---------------------------------------------------------------------------
# Agronomist selection (execution plan item 3)
# ---------------------------------------------------------------------------


def test_select_agronomist_prefers_local_jurisdiction():
    candidates = [
        AgronomistCandidate("agronomist:a", "erode", True, 3),
        AgronomistCandidate("agronomist:b", "madurai", True, 0),
    ]
    chosen = select_agronomist(candidates, jurisdiction="erode")
    assert chosen.identifier == "agronomist:a"


def test_select_agronomist_falls_back_to_next_available_when_no_local_match():
    candidates = [
        AgronomistCandidate("agronomist:a", "trichy", False, 0),
        AgronomistCandidate("agronomist:b", "madurai", True, 2),
    ]
    chosen = select_agronomist(candidates, jurisdiction="erode")
    assert chosen.identifier == "agronomist:b"


def test_select_agronomist_prefers_lower_case_load_among_available():
    candidates = [
        AgronomistCandidate("agronomist:a", "erode", True, 5),
        AgronomistCandidate("agronomist:b", "erode", True, 1),
    ]
    chosen = select_agronomist(candidates, jurisdiction="erode")
    assert chosen.identifier == "agronomist:b"


def test_select_agronomist_returns_none_when_nobody_available():
    candidates = [
        AgronomistCandidate("agronomist:a", "erode", False, 0),
        AgronomistCandidate("agronomist:b", "madurai", False, 0),
    ]
    assert select_agronomist(candidates, jurisdiction="erode") is None


def test_select_agronomist_empty_pool_returns_none():
    assert select_agronomist([]) is None


# ---------------------------------------------------------------------------
# CaseSummary compilation
# ---------------------------------------------------------------------------


def _health() -> HealthRef:
    return HealthRef(score=68, band="watch")


def _farm() -> FarmRef:
    return FarmRef(id="f_1", crop="samba_paddy", area_acres_verified=1.9, soil_type="clay_loam")


def test_compile_case_summary_requires_case_id():
    with pytest.raises(ValueError):
        compile_case_summary("", _farm(), None, [], [], [], None, _health(), "open")


def test_compile_case_summary_requires_farm():
    with pytest.raises(ValueError):
        compile_case_summary("c_1", None, None, [], [], [], None, _health(), "open")


def test_compile_case_summary_requires_current_health():
    with pytest.raises(ValueError):
        compile_case_summary("c_1", _farm(), None, [], [], [], None, None, "open")


def test_compile_case_summary_allows_no_problem_yet():
    """A case opened before any problem is confirmed (below-gate diagnosis)."""
    summary = compile_case_summary("c_1", _farm(), None, [], [], [], None, _health(), "assigned")
    assert summary.problem is None
    assert summary.case_id == "c_1"


def test_compile_case_summary_is_a_defensive_copy():
    timeline = []
    summary = compile_case_summary("c_1", _farm(), None, timeline, [], [], None, _health(), "open")
    timeline.append("mutate after the fact")
    assert summary.timeline == []
