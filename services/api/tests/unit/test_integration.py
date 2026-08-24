"""Integration tests — spoken summary, health reason, confirmation flow.

Phase 4 verification tests.
"""

import pytest

from app.services.spoken_summary import SpokenSummaryService
from app.services.health_reason import explain_health_change


class TestSpokenSummary:
    """Tests for Tamil spoken summary generation."""

    @pytest.fixture
    def svc(self) -> SpokenSummaryService:
        return SpokenSummaryService()

    def test_health_unrated(self, svc: SpokenSummaryService):
        """Unrated health → Tamil 'not enough info' message."""
        result = svc.for_health(None, "unrated")
        assert "போதுமான" in result or "தகவல்" in result

    def test_health_with_score(self, svc: SpokenSummaryService):
        """Score 82 → Tamil summary contains '82'."""
        result = svc.for_health(82, "good")
        assert "82" in result

    def test_diagnosis_above_gate(self, svc: SpokenSummaryService):
        """Above gate → Tamil summary contains disease name."""
        result = svc.for_diagnosis(True, "BLB", 0.85)
        assert "BLB" in result

    def test_diagnosis_below_gate(self, svc: SpokenSummaryService):
        """Below gate → Tamil escalation message."""
        result = svc.for_diagnosis(False)
        assert "நிபுணருக்கு" in result

    def test_advisory_retrieved(self, svc: SpokenSummaryService):
        """Retrieved → Tamil 'answer found' message."""
        result = svc.for_advisory(True)
        assert "பதில்" in result

    def test_advisory_not_retrieved(self, svc: SpokenSummaryService):
        """Not retrieved → Tamil 'no reliable info' message."""
        result = svc.for_advisory(False)
        assert "நிபுணருக்கு" in result

    def test_followup_improved(self, svc: SpokenSummaryService):
        result = svc.for_followup("improved", score=86)
        assert "86" in result

    def test_followup_got_worse(self, svc: SpokenSummaryService):
        result = svc.for_followup("got_worse")
        assert "மோசம" in result or "நிபுணருக்கு" in result

    def test_scheme_count(self, svc: SpokenSummaryService):
        result = svc.for_scheme(3)
        assert "3" in result

    def test_escalation(self, svc: SpokenSummaryService):
        result = svc.for_escalation()
        assert "நிபுணருக்கு" in result


class TestHealthReason:
    """Tests for the health score change reason mapper."""

    def test_first_assessment(self):
        """No previous snapshot → 'First assessment' in Tamil."""
        result = explain_health_change({"subindices": {}}, None)
        assert "முதல்" in result

    def test_drop_due_to_problem(self):
        """Active problem severity dropped → Tamil reason about disease."""
        current = {"subindices": [
            {"key": "active_problem_severity", "value": 40},
            {"key": "environmental_risk", "value": 80},
        ]}
        previous = {"subindices": [
            {"key": "active_problem_severity", "value": 90},
            {"key": "environmental_risk", "value": 80},
        ]}
        result = explain_health_change(current, previous)
        assert "நோய்" in result or "பாதிப்பு" in result  # disease-related reason

    def test_rise_due_to_treatment(self):
        """Treatment response improved → Tamil reason about treatment."""
        current = {"subindices": {"treatment_response": 85, "environmental_risk": 80}}
        previous = {"subindices": {"treatment_response": 40, "environmental_risk": 80}}
        result = explain_health_change(current, previous)
        assert "சிகிச்சை" in result  # treatment-related reason

    def test_no_subindices(self):
        """Empty subindices → generic 'score changed'."""
        result = explain_health_change({"subindices": {}}, {"subindices": {}})
        assert len(result) > 0  # Non-empty string
