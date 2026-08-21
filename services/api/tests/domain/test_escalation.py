"""Unit tests for the pure escalation domain functions (PRD §5.10/§5.11,
contract §2.13): severity promotion, the auto-escalation band check, and the
CaseSummary assembler.
"""

from app.core.enums import CaseStatus, FollowupResponse, HealthBand, ProblemSeverity
from app.domain.escalation import build_case_summary, promote_severity, should_auto_escalate
from app.schemas.case import CaseImage, TimelineEvent

# ---------------------------------------------------------------------------
# promote_severity — the ladder is fixed, one tier at a time, capped at severe.
# ---------------------------------------------------------------------------


def test_promote_severity_early_to_moderate():
    assert promote_severity(ProblemSeverity.EARLY) == ProblemSeverity.MODERATE


def test_promote_severity_moderate_to_severe():
    assert promote_severity(ProblemSeverity.MODERATE) == ProblemSeverity.SEVERE


def test_promote_severity_severe_stays_severe():
    assert promote_severity(ProblemSeverity.SEVERE) == ProblemSeverity.SEVERE


# ---------------------------------------------------------------------------
# should_auto_escalate — PRD §7.4: crossing below Watch triggers escalation.
# ---------------------------------------------------------------------------


def test_should_auto_escalate_true_for_poor_and_critical():
    assert should_auto_escalate(HealthBand.POOR) is True
    assert should_auto_escalate(HealthBand.CRITICAL) is True


def test_should_auto_escalate_false_for_watch_good_excellent_unrated():
    assert should_auto_escalate(HealthBand.WATCH) is False
    assert should_auto_escalate(HealthBand.GOOD) is False
    assert should_auto_escalate(HealthBand.EXCELLENT) is False
    assert should_auto_escalate(HealthBand.UNRATED) is False


# ---------------------------------------------------------------------------
# build_case_summary — a complete, non-empty CaseSummary every time.
# ---------------------------------------------------------------------------


def test_build_case_summary_populates_every_contract_field():
    summary = build_case_summary(
        case_id="c_1",
        farm_id="f_1",
        crop="Paddy",
        area_acres_verified=1.9,
        soil_type="clay_loam",
        problem_id="p_7",
        problem_label="bacterial_leaf_blight",
        severity=ProblemSeverity.MODERATE,
        timeline=[TimelineEvent(at="2026-08-21T00:00:00Z", event="diagnosis", detail="bacterial_leaf_blight (moderate)")],
        images=[CaseImage(asset_id="a_9", url="https://storage.example/a_9")],
        treatments_tried=["field drainage"],
        followup_trend=FollowupResponse.GOT_WORSE,
        health_score=59,
        health_band=HealthBand.POOR,
        status=CaseStatus.ASSIGNED,
    )

    assert summary.case_id == "c_1"
    assert summary.farm.id == "f_1"
    assert summary.farm.crop == "Paddy"
    assert summary.farm.area_acres_verified == 1.9
    assert summary.farm.soil_type == "clay_loam"
    assert summary.problem.id == "p_7"
    assert summary.problem.label == "bacterial_leaf_blight"
    assert summary.problem.severity == ProblemSeverity.MODERATE
    assert summary.timeline
    assert summary.images
    assert summary.treatments_tried
    assert summary.followup_trend == FollowupResponse.GOT_WORSE
    assert summary.current_health.score == 59
    assert summary.current_health.band == HealthBand.POOR
    assert summary.status == CaseStatus.ASSIGNED
