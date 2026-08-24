"""Unit test suite for Confidence Gate (Phase 1 — Contract Freeze & Confidence Gate).

Verifies the single orchestration-layer decision point for disease and pest diagnosis.
Tests structural invariants:
- exactly one outcome: COMPOSE or ESCALATE (never both, never neither)
- image confidence floor (CONFIDENCE_GATE = 0.70)
- target-specific scope validation against SUPPORTED_LABELS
- retrieval relevance gating
"""

import pytest

from app.core.enums import GateOutcome
from app.domain.constants import CONFIDENCE_GATE
from app.domain.gate import (
    GateDecision,
    SUPPORTED_LABELS,
    check_gate,
    decide,
)


def _assert_decision_invariants(d: GateDecision) -> None:
    """Every decision must carry exactly one outcome and valid metadata."""
    if d.outcome == GateOutcome.COMPOSE:
        assert d.above_gate is True
        assert d.action == "compose_advisory"
        assert d.should_compose is True
        assert d.should_escalate is False
        assert d.reason is None
        assert d.error_code is None
        assert d.spoken_summary is None
    elif d.outcome == GateOutcome.ESCALATE:
        assert d.above_gate is False
        assert d.action == "escalate"
        assert d.should_compose is False
        assert d.should_escalate is True
        assert d.reason is not None
        assert d.error_code is not None
        assert d.spoken_summary is not None
    else:
        pytest.fail(f"Unknown gate outcome: {d.outcome!r}")


# ---------------------------------------------------------------------------
# 1. Disease Gate Tests
# ---------------------------------------------------------------------------


def test_disease_above_gate_composes():
    """Disease with in-scope label and confidence >= 0.70 signals compose."""
    d = check_gate(
        target_type="disease",
        label="bacterial_leaf_blight",
        confidence=0.85,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.COMPOSE
    assert d.above_gate is True
    assert d.action == "compose_advisory"


def test_disease_below_gate_escalates():
    """Disease with in-scope label but confidence < 0.70 escalates with BELOW_CONFIDENCE_GATE."""
    d = check_gate(
        target_type="disease",
        label="bacterial_leaf_blight",
        confidence=0.62,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.above_gate is False
    assert d.error_code == "BELOW_CONFIDENCE_GATE"
    assert "0.62" in d.reason and "0.70" in d.reason


# ---------------------------------------------------------------------------
# 2. Pest Gate Tests
# ---------------------------------------------------------------------------


def test_pest_above_gate_composes():
    """Pest with in-scope label and confidence >= 0.70 signals compose."""
    d = check_gate(
        target_type="pest",
        label="stem_borer",
        confidence=0.88,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.COMPOSE
    assert d.above_gate is True
    assert d.action == "compose_advisory"


def test_pest_below_gate_escalates():
    """Pest with in-scope label but confidence < 0.70 escalates with BELOW_CONFIDENCE_GATE."""
    d = check_gate(
        target_type="pest",
        label="stem_borer",
        confidence=0.45,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.above_gate is False
    assert d.error_code == "BELOW_CONFIDENCE_GATE"
    assert "0.45" in d.reason and "0.70" in d.reason


# ---------------------------------------------------------------------------
# 3. Scope Validation Tests
# ---------------------------------------------------------------------------


def test_out_of_scope_label_escalates_with_out_of_scope_code():
    """An unknown label or cross-type label triggers OUT_OF_SCOPE_TARGET."""
    # Unknown label
    d1 = check_gate(
        target_type="disease",
        label="unknown_disease_xyz",
        confidence=0.99,
    )
    _assert_decision_invariants(d1)
    assert d1.outcome == GateOutcome.ESCALATE
    assert d1.error_code == "OUT_OF_SCOPE_TARGET"
    assert "unknown_disease_xyz" in d1.reason

    # Pest label submitted under target_type="disease"
    d2 = check_gate(
        target_type="disease",
        label="stem_borer",
        confidence=0.95,
    )
    _assert_decision_invariants(d2)
    assert d2.outcome == GateOutcome.ESCALATE
    assert d2.error_code == "OUT_OF_SCOPE_TARGET"


def test_pest_scope_validation():
    """Disease label submitted under target_type="pest" triggers OUT_OF_SCOPE_TARGET."""
    d = check_gate(
        target_type="pest",
        label="bacterial_leaf_blight",
        confidence=0.95,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.error_code == "OUT_OF_SCOPE_TARGET"


# ---------------------------------------------------------------------------
# 4. Retrieval Relevance Tests
# ---------------------------------------------------------------------------


def test_below_relevance_threshold_escalates():
    """Retrieval relevance below threshold escalates with NO_RELEVANT_SOURCE."""
    d = check_gate(
        target_type="disease",
        label="blast",
        confidence=0.90,
        retrieval_relevance=0.20,
        relevance_threshold=0.60,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.error_code == "NO_RELEVANT_SOURCE"
    assert "0.20" in d.reason and "0.60" in d.reason


def test_above_relevance_threshold_composes():
    """Retrieval relevance at or above threshold allows composing."""
    d = check_gate(
        target_type="disease",
        label="blast",
        confidence=0.90,
        retrieval_relevance=0.75,
        relevance_threshold=0.60,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.COMPOSE


# ---------------------------------------------------------------------------
# 5. Boundary and Invariance Tests
# ---------------------------------------------------------------------------


def test_confidence_exactly_at_gate_composes():
    """Confidence exactly equal to CONFIDENCE_GATE (0.70) passes."""
    d = check_gate(
        target_type="disease",
        label="early_blight",
        confidence=CONFIDENCE_GATE,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.COMPOSE


def test_confidence_just_below_gate_escalates():
    """Confidence just below CONFIDENCE_GATE (0.69) escalates."""
    d = check_gate(
        target_type="disease",
        label="early_blight",
        confidence=CONFIDENCE_GATE - 0.01,
    )
    _assert_decision_invariants(d)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.error_code == "BELOW_CONFIDENCE_GATE"


def test_gate_decide_compatibility():
    """Legacy decide() entry point functions with identical invariants."""
    d_compose = decide(
        image_confidence=0.80,
        in_scope=True,
        retrieval_relevance=0.70,
        confidence_gate=0.70,
        relevance_threshold=0.60,
    )
    _assert_decision_invariants(d_compose)
    assert d_compose.outcome == GateOutcome.COMPOSE

    d_escalate = decide(
        image_confidence=0.50,
        in_scope=True,
        retrieval_relevance=0.70,
        confidence_gate=0.70,
        relevance_threshold=0.60,
    )
    _assert_decision_invariants(d_escalate)
    assert d_escalate.outcome == GateOutcome.ESCALATE


def test_gate_is_pure_and_deterministic():
    """Gate is pure function: same arguments return identical results."""
    kwargs = {
        "target_type": "pest",
        "label": "stem_borer",
        "confidence": 0.85,
        "retrieval_relevance": 0.65,
        "relevance_threshold": 0.60,
    }
    assert check_gate(**kwargs) == check_gate(**kwargs)


# ---------------------------------------------------------------------------
# 6. Schema Freeze and Contract Verification Tests (Task A)
# ---------------------------------------------------------------------------


def test_five_point_advisory_field_order():
    """Advisory schema MUST declare what_to_avoid ahead of what_to_do_next in field order."""
    from app.schemas.advisory import FivePointAdvisory
    from app.domain.rag.constants import FIVE_POINT_FIELDS

    expected_order = [
        "possible_issue",
        "what_to_check",
        "what_to_avoid",
        "what_to_do_next",
        "expert_triggers",
    ]
    # Pydantic v2 field declaration order in model_fields
    actual_fields = list(FivePointAdvisory.model_fields.keys())
    assert actual_fields == expected_order, f"Expected {expected_order}, got {actual_fields}"
    assert list(FIVE_POINT_FIELDS) == expected_order


def test_gate_object_frozen_shape():
    """GateObject schema matches frozen contract §8 exactly."""
    from app.schemas.gate import GateObject

    gate_obj = GateObject(
        above_gate=True,
        confidence=0.88,
        threshold=0.70,
        reason_code=None,
        alternatives=["stem_borer", "leaf_folder"],
    )
    assert gate_obj.above_gate is True
    assert gate_obj.confidence == 0.88
    assert gate_obj.threshold == 0.70
    assert gate_obj.alternatives == ["stem_borer", "leaf_folder"]
    assert set(GateObject.model_fields.keys()) == {
        "above_gate",
        "confidence",
        "threshold",
        "reason_code",
        "alternatives",
    }


def test_land_status_thin_values():
    """LandStatus enum contains the thin verification statuses."""
    from app.core.enums import LandStatus

    assert LandStatus.PENDING_VERIFICATION == "pending_verification"
    assert LandStatus.VERIFIED == "verified"
    assert LandStatus.REJECTED == "rejected"

