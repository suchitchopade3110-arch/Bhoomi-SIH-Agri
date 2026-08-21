"""Unit tests for the pure escalation domain functions (PRD §5.10/§5.11,
contract §2.13): severity promotion, the auto-escalation band check, and the
CaseSummary assembler.
"""

from app.core.enums import CaseStatus, HealthBand, ProblemSeverity
from app.domain.escalation import build_case_summary, promote_severity, should_auto_escalate

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
        farmer_name="Murugan",
        village="Thottipalayam",
        district="Erode",
        crop="Paddy",
        growth_stage="vegetative",
        health_score=59.0,
        land_verified=True,
        problem_summary="Bacterial leaf blight, moderate severity, worsening.",
        severity=ProblemSeverity.MODERATE,
        status=CaseStatus.ESCALATED,
        timeline_summary=[{"type": "diagnosis", "problem_id": "p_7"}],
        latest_images=["asset_9"],
        escalated_to="Dr. Meena Krishnan",
        spoken_summary="Murugan's Paddy case has been sent to an expert.",
    )

    assert summary.case_id == "c_1"
    assert summary.farm_id == "f_1"
    assert summary.farmer_name == "Murugan"
    assert summary.village == "Thottipalayam"
    assert summary.district == "Erode"
    assert summary.crop == "Paddy"
    assert summary.growth_stage == "vegetative"
    assert summary.health_score == 59.0
    assert summary.land_verified is True
    assert summary.problem_summary
    assert summary.severity == ProblemSeverity.MODERATE
    assert summary.status == CaseStatus.ESCALATED
    assert summary.timeline_summary
    assert summary.latest_images == ["asset_9"]
    assert summary.escalated_to == "Dr. Meena Krishnan"
    assert summary.spoken_summary
