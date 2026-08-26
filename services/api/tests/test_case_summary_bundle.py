"""Tests for CaseSummaryBundle and compilation (Phase 3 Objective 2).

Verifies:
  - Bundle contains strictly the 8 required keys:
    {crop, region, growth_stage, problem_history, images, treatments_tried, followup_trend, current_advisory}
  - Zero land or soil keys (e.g. area_acres_verified, soil_type, total_area_acres) exist in the bundle.
  - Compilation functions (compile_case_summary_bundle, build_case_summary) produce valid bundles.
"""

import pytest
from app.core.enums import CaseStatus, ProblemSeverity
from app.domain.escalation import build_case_summary, compile_case_summary_bundle
from app.schemas.case import CaseSummaryBundle

EXPECTED_BUNDLE_KEYS = {
    "crop",
    "region",
    "growth_stage",
    "problem_history",
    "images",
    "treatments_tried",
    "followup_trend",
    "current_advisory",
    "diagnosis",
}

FORBIDDEN_LAND_SOIL_KEYS = {
    "area_acres_verified",
    "soil_type",
    "total_area_acres",
    "boundary_geojson",
    "land_status",
    "land_verified",
    "patta_passbook_asset_id",
}


def test_case_summary_bundle_keys_exact_match():
    """Bundle dictionary keys must exactly match the 8 defined keys."""
    bundle = compile_case_summary_bundle(
        crop="Rice (ADT 45)",
        region="Thiruvallur, Tamil Nadu",
        growth_stage="tillering",
        problem_history=[{"date": "2025-11-01", "event": "BLB symptoms noted"}],
        images=["asset_img_123"],
        treatments_tried=["Copper Hydroxide 2g/L"],
        followup_trend="got_worse",
        current_advisory="Apply streptocycline spray; consult local KVK immediately.",
    )

    data = bundle.model_dump()
    actual_keys = set(data.keys())

    assert actual_keys == EXPECTED_BUNDLE_KEYS, f"Bundle keys mismatch. Diff: {actual_keys ^ EXPECTED_BUNDLE_KEYS}"
    for forbidden in FORBIDDEN_LAND_SOIL_KEYS:
        assert forbidden not in data, f"Forbidden land/soil key '{forbidden}' found in bundle!"


def test_build_case_summary_attaches_clean_bundle():
    """build_case_summary attaches a CaseSummaryBundle with no land/soil fields."""
    farm_info = {
        "id": "farm_test_101",
        "farmer_name": "Murugan",
        "village": "Alanganallur",
        "district": "Madurai",
        "primary_crop": "Rice",
        "growth_stage": "panicle_initiation",
        "total_area_acres": 2.5,  # present in farm db row, but MUST NOT leak into bundle
        "soil_type": "clay_loam",  # present in farm db row, but MUST NOT leak into bundle
    }
    problem_details = {
        "label": "bacterial_leaf_blight",
        "severity": ProblemSeverity.MODERATE,
        "images": [{"asset_id": "img_001", "url": "https://bhoomi.local/assets/img_001.jpg"}],
        "treatments_tried": ["neem oil 3%"],
        "trend": "got_worse",
    }
    recent_events = [{"event": "diagnosis", "stage": "early", "days_ago": 4}]

    case_summary = build_case_summary(
        case_id="case_abc_1",
        farm_info=farm_info,
        recent_events=recent_events,
        current_health_score=68.0,
        problem_details=problem_details,
        assigned_officer_or_kvk="TNAU KVK - Madurai",
        status=CaseStatus.ESCALATED,
        current_advisory_text="Condition worsening. Expert review requested.",
    )

    assert case_summary.bundle is not None
    bundle_dict = case_summary.bundle.model_dump()

    # Exact 8-key bundle assertion
    assert set(bundle_dict.keys()) == EXPECTED_BUNDLE_KEYS

    # Verify values mapped accurately
    assert bundle_dict["crop"] == "Rice"
    assert "Madurai" in bundle_dict["region"]
    assert bundle_dict["growth_stage"] == "panicle_initiation"
    assert bundle_dict["followup_trend"] == "got_worse"
    assert len(bundle_dict["treatments_tried"]) == 1
    assert bundle_dict["current_advisory"] == "Condition worsening. Expert review requested."

    # Verify zero leakage of soil or land keys
    for forbidden in FORBIDDEN_LAND_SOIL_KEYS:
        assert forbidden not in bundle_dict, f"Forbidden key '{forbidden}' leaked into bundle!"


def test_bundle_handles_minimal_empty_inputs_safely():
    """Bundle compiles cleanly when optional lists or trends are empty/None."""
    bundle = compile_case_summary_bundle(
        crop="Cotton",
        region="Coimbatore",
        growth_stage="flowering",
    )
    data = bundle.model_dump()
    assert set(data.keys()) == EXPECTED_BUNDLE_KEYS
    assert data["problem_history"] == []
    assert data["images"] == []
    assert data["treatments_tried"] == []
    assert data["followup_trend"] is None
    assert data["current_advisory"] is None


def test_bare_escalation_no_prior_problem_has_zero_placeholders():
    """Bare escalation with no prior history must never produce 'Unknown', 'unspecified', 'Health score 0', or 'trend: unknown'."""
    farm_info = {
        "id": "farm_bare_101",
        "primary_crop": "samba_paddy",
        # farmer_name, village, district, growth_stage are omitted/None
    }
    problem_details = {
        "severity": ProblemSeverity.EARLY,
        # label, trend, images, treatments_tried omitted
    }

    summary = build_case_summary(
        case_id="case_bare_001",
        farm_info=farm_info,
        recent_events=[],
        current_health_score=None,  # Unrated
        problem_details=problem_details,
        assigned_officer_or_kvk="agronomist:kvk_coimbatore",
        status=CaseStatus.ESCALATED,
    )

    # 1. No 'Unknown' in spoken_summary
    assert "Unknown" not in summary.spoken_summary
    assert summary.spoken_summary == "A case for this samba_paddy farm has been sent to agronomist:kvk_coimbatore."

    # 2. No ungrammatical 'an unspecified issue symptoms'
    assert "an unspecified issue" not in summary.problem_summary
    assert "samba_paddy under observation for early severity symptoms" in summary.problem_summary

    # 3. No misleading 'Health score 0' (PRD Unrated != 0 invariant)
    assert "Health score 0" not in summary.problem_summary
    assert "Health score: Unrated" in summary.problem_summary
    assert summary.health_score is None

    # 4. No 'Farmer-reported trend: unknown'
    assert "trend: unknown" not in summary.problem_summary
    assert "No prior follow-ups recorded" in summary.problem_summary
    assert summary.bundle.followup_trend is None

    # 5. Whole dumped dict has zero forbidden placeholders
    dumped_str = summary.model_dump_json()
    assert "Unknown" not in dumped_str
    assert "an unspecified issue" not in dumped_str
    assert "N/A" not in dumped_str


def test_full_history_escalation_grammatical_summary():
    """Escalation with full diagnosis and follow-up history formats cleanly."""
    farm_info = {
        "id": "farm_full_101",
        "farmer_name": "Murugan",
        "village": "Alanganallur",
        "district": "Madurai",
        "primary_crop": "samba_paddy",
        "growth_stage": "tillering",
    }
    problem_details = {
        "label": "bacterial_leaf_blight",
        "severity": ProblemSeverity.MODERATE,
        "trend": "got_worse",
        "treatments_tried": ["neem_oil"],
        "images": ["img_001"],
    }
    recent_events = [{"event": "diagnosis", "stage": "early"}, {"event": "followup", "response": "got_worse"}]

    summary = build_case_summary(
        case_id="case_full_001",
        farm_info=farm_info,
        recent_events=recent_events,
        current_health_score=57.0,
        problem_details=problem_details,
        assigned_officer_or_kvk="agronomist:kvk_madurai",
        status=CaseStatus.ESCALATED,
    )

    assert summary.spoken_summary == "A case for Murugan has been sent to agronomist:kvk_madurai."
    assert "samba_paddy showing bacterial leaf blight symptoms (severity: moderate)" in summary.problem_summary
    assert "Health score: 57" in summary.problem_summary
    assert "Farmer-reported trend: worsening" in summary.problem_summary
    assert summary.health_score == 57.0
    assert summary.bundle.followup_trend == "got_worse"
    assert summary.bundle.region == "Alanganallur, Madurai"

