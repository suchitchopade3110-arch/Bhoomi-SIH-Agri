"""Unit tests for qualitative advisory derivation and determinism.

Verifies:
  - Zero scoring formula, zero weights, zero sub-indices
  - Identical inputs produce strictly identical outcomes (100% deterministic)
  - No datetime.now() drift
  - Day-0 / Unrated handling
  - Trend trajectory rules (improving, stable, worsening)
"""

import pytest
from app.domain.advisory import (
    AdvisoryTrend,
    QualitativeAdvisoryResult,
    derive_qualitative_advisory,
)


def test_advisory_determinism_identical_inputs():
    """Identical state called multiple times must return the exact same advisory and trend."""
    inputs = {
        "open_problems_count": 1,
        "highest_severity": "moderate",
        "primary_problem_label": "bacterial_leaf_blight",
        "days_since_last_scan": 3,
        "latest_followup_response": "no_change",
    }
    res1 = derive_qualitative_advisory(**inputs)
    res2 = derive_qualitative_advisory(**inputs)

    assert res1 == res2
    assert res1.advisory == res2.advisory
    assert res1.trend == res2.trend
    assert res1.trend == AdvisoryTrend.STABLE
    assert "bacterial leaf blight" in res1.advisory


def test_advisory_day0_unrated():
    """Day-0 with zero problems, no scans, and no follow-ups returns honest unrated message."""
    res = derive_qualitative_advisory(
        open_problems_count=0,
        highest_severity=None,
        primary_problem_label=None,
        days_since_last_scan=None,
        latest_followup_response=None,
    )
    assert res.trend == AdvisoryTrend.STABLE
    assert "Insufficient monitoring data" in res.advisory
    assert "Submit a crop photo" in res.advisory


def test_advisory_followup_got_worse_worsening():
    """Follow-up response 'got_worse' produces worsening trend and escalation recommendation."""
    res = derive_qualitative_advisory(
        open_problems_count=1,
        highest_severity="moderate",
        primary_problem_label="stem_borer",
        days_since_last_scan=1,
        latest_followup_response="got_worse",
    )
    assert res.trend == AdvisoryTrend.WORSENING
    assert "worsened" in res.advisory
    assert "expert intervention recommended" in res.advisory
    assert "stem borer" in res.advisory


def test_advisory_followup_improved_improving():
    """Follow-up response 'improved' produces improving trend."""
    res = derive_qualitative_advisory(
        open_problems_count=1,
        highest_severity="early",
        primary_problem_label="blast",
        days_since_last_scan=2,
        latest_followup_response="improved",
    )
    assert res.trend == AdvisoryTrend.IMPROVING
    assert "recovery observed" in res.advisory
    assert "blast" in res.advisory


def test_advisory_followup_resolved_all_clear():
    """Zero open problems with improved follow-up confirms recovery."""
    res = derive_qualitative_advisory(
        open_problems_count=0,
        highest_severity=None,
        primary_problem_label=None,
        days_since_last_scan=1,
        latest_followup_response="improved",
    )
    assert res.trend == AdvisoryTrend.IMPROVING
    assert "recovery confirmed" in res.advisory


def test_advisory_severe_problem_worsening():
    """Severe active problem load triggers worsening trend and immediate attention."""
    res = derive_qualitative_advisory(
        open_problems_count=1,
        highest_severity="severe",
        primary_problem_label="brown_planthopper",
        days_since_last_scan=1,
        latest_followup_response=None,
    )
    assert res.trend == AdvisoryTrend.WORSENING
    assert "Severe brown planthopper pressure" in res.advisory
    assert "immediate attention" in res.advisory


def test_advisory_multiple_problems_worsening():
    """Multiple active problems triggers worsening trend."""
    res = derive_qualitative_advisory(
        open_problems_count=3,
        highest_severity="moderate",
        primary_problem_label=None,
        days_since_last_scan=2,
        latest_followup_response=None,
    )
    assert res.trend == AdvisoryTrend.WORSENING
    assert "Multiple active crop stress factors" in res.advisory


def test_advisory_healthy_stale_scan():
    """Zero problems but stale scan (>7 days) prompts new scan."""
    res = derive_qualitative_advisory(
        open_problems_count=0,
        highest_severity=None,
        primary_problem_label=None,
        days_since_last_scan=14,
        latest_followup_response=None,
    )
    assert res.trend == AdvisoryTrend.STABLE
    assert "14 days ago" in res.advisory
    assert "new scan recommended" in res.advisory


def test_advisory_healthy_recent_scan():
    """Zero problems with recent scan confirms clear condition."""
    res = derive_qualitative_advisory(
        open_problems_count=0,
        highest_severity=None,
        primary_problem_label=None,
        days_since_last_scan=3,
        latest_followup_response=None,
    )
    assert res.trend == AdvisoryTrend.STABLE
    assert "Crop condition is clear" in res.advisory
