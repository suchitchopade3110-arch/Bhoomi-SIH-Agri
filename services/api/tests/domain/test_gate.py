"""Unit tests for the confidence gate (PRD §5.6, §5.7): the single decision
point for answer-vs-escalate. Every case asserts the structural invariant
too — exactly one outcome, never both, never neither.
"""

import itertools

import pytest

from app.core.enums import GateOutcome
from app.domain.gate import GateDecision, decide

CONFIDENCE_GATE = 0.70
RELEVANCE_THRESHOLD = 0.35


def _assert_exactly_one_outcome(d: GateDecision) -> None:
    """A compose decision carries no escalation metadata; an escalate
    decision always carries all of it. Never a mix, never neither."""
    if d.outcome == GateOutcome.COMPOSE:
        assert d.reason is None
        assert d.error_code is None
        assert d.spoken_summary is None
    elif d.outcome == GateOutcome.ESCALATE:
        assert d.reason is not None
        assert d.error_code is not None
        assert d.spoken_summary is not None
    else:
        pytest.fail(f"Unknown outcome: {d.outcome!r}")


def _decide(image_confidence=None, in_scope=True, retrieval_relevance=None):
    d = decide(
        image_confidence=image_confidence,
        in_scope=in_scope,
        retrieval_relevance=retrieval_relevance,
        confidence_gate=CONFIDENCE_GATE,
        relevance_threshold=RELEVANCE_THRESHOLD,
    )
    _assert_exactly_one_outcome(d)
    return d


# ---------------------------------------------------------------------------
# Image confidence gate
# ---------------------------------------------------------------------------


def test_above_image_gate_composes():
    d = _decide(image_confidence=0.87, in_scope=True, retrieval_relevance=0.50)
    assert d.outcome == GateOutcome.COMPOSE


def test_below_image_gate_escalates_with_below_confidence_gate_code():
    d = _decide(image_confidence=0.41, in_scope=True, retrieval_relevance=0.50)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.error_code == "BELOW_CONFIDENCE_GATE"
    assert "0.41" in d.reason and "0.70" in d.reason


def test_image_confidence_exactly_at_gate_composes():
    """The rule is strictly '< gate', so an exact match passes."""
    d = _decide(image_confidence=CONFIDENCE_GATE, in_scope=True, retrieval_relevance=0.50)
    assert d.outcome == GateOutcome.COMPOSE


def test_image_confidence_just_below_gate_escalates():
    d = _decide(image_confidence=CONFIDENCE_GATE - 0.01, in_scope=True, retrieval_relevance=0.50)
    assert d.outcome == GateOutcome.ESCALATE


# ---------------------------------------------------------------------------
# Scope
# ---------------------------------------------------------------------------


def test_in_scope_does_not_escalate_on_scope():
    d = _decide(image_confidence=0.90, in_scope=True, retrieval_relevance=0.90)
    assert d.outcome == GateOutcome.COMPOSE


def test_out_of_scope_escalates_even_with_high_confidence():
    d = _decide(image_confidence=0.99, in_scope=False, retrieval_relevance=0.99)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.error_code == "OUT_OF_SCOPE_TARGET"
    assert "supported set" in d.reason


# ---------------------------------------------------------------------------
# Retrieval relevance
# ---------------------------------------------------------------------------


def test_above_relevance_threshold_composes():
    d = _decide(image_confidence=None, in_scope=True, retrieval_relevance=0.80)
    assert d.outcome == GateOutcome.COMPOSE


def test_below_relevance_threshold_escalates_with_no_relevant_source_code():
    d = _decide(image_confidence=None, in_scope=True, retrieval_relevance=0.10)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.error_code == "NO_RELEVANT_SOURCE"
    assert "0.10" in d.reason and "0.35" in d.reason


def test_relevance_exactly_at_threshold_composes():
    d = _decide(image_confidence=None, in_scope=True, retrieval_relevance=RELEVANCE_THRESHOLD)
    assert d.outcome == GateOutcome.COMPOSE


# ---------------------------------------------------------------------------
# Missing inputs: None must never fabricate a pass — it just isn't checked.
# ---------------------------------------------------------------------------


def test_missing_image_confidence_is_skipped_not_faked():
    """No image was involved (e.g. text-only advisory query, PRD §5.7) —
    the gate must not invent a confidence value to justify composing."""
    d = _decide(image_confidence=None, in_scope=True, retrieval_relevance=0.90)
    assert d.outcome == GateOutcome.COMPOSE


def test_missing_retrieval_relevance_is_skipped_not_faked():
    """Retrieval wasn't performed for this call (e.g. Phase-2 image
    diagnosis before Phase 3 wires RAG) — same rule."""
    d = _decide(image_confidence=0.95, in_scope=True, retrieval_relevance=None)
    assert d.outcome == GateOutcome.COMPOSE


def test_both_signals_missing_with_in_scope_composes():
    d = _decide(image_confidence=None, in_scope=True, retrieval_relevance=None)
    assert d.outcome == GateOutcome.COMPOSE


def test_missing_image_confidence_does_not_suppress_out_of_scope_escalation():
    """A missing signal is skipped, not treated as a free pass on every check."""
    d = _decide(image_confidence=None, in_scope=False, retrieval_relevance=0.90)
    assert d.outcome == GateOutcome.ESCALATE
    assert d.error_code == "OUT_OF_SCOPE_TARGET"


# ---------------------------------------------------------------------------
# Multiple simultaneous failures: still exactly one decision, one reason.
# ---------------------------------------------------------------------------


def test_multiple_failures_still_yield_a_single_escalate_decision():
    d = _decide(image_confidence=0.10, in_scope=False, retrieval_relevance=0.01)
    assert d.outcome == GateOutcome.ESCALATE
    # Image confidence is checked first — its reason wins, and there is only one.
    assert d.error_code == "BELOW_CONFIDENCE_GATE"
    assert "0.10" in d.reason


def test_out_of_scope_and_low_relevance_without_image_signal():
    d = _decide(image_confidence=None, in_scope=False, retrieval_relevance=0.01)
    assert d.outcome == GateOutcome.ESCALATE
    assert "supported set" in d.reason  # scope checked before relevance


# ---------------------------------------------------------------------------
# Exhaustive sweep: no branch ever composes when a provided signal is below
# its threshold, and no branch ever escalates when everything provided
# clears its threshold and the item is in scope.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "image_confidence,in_scope,retrieval_relevance",
    list(
        itertools.product(
            [None, 0.10, 0.69, 0.70, 0.71, 0.99],
            [True, False],
            [None, 0.10, 0.34, 0.35, 0.36, 0.99],
        )
    ),
)
def test_decide_never_composes_when_a_provided_signal_fails(image_confidence, in_scope, retrieval_relevance):
    d = _decide(image_confidence=image_confidence, in_scope=in_scope, retrieval_relevance=retrieval_relevance)

    image_fails = image_confidence is not None and image_confidence < CONFIDENCE_GATE
    relevance_fails = retrieval_relevance is not None and retrieval_relevance < RELEVANCE_THRESHOLD
    scope_fails = not in_scope
    should_escalate = image_fails or scope_fails or relevance_fails

    if should_escalate:
        assert d.outcome == GateOutcome.ESCALATE
    else:
        assert d.outcome == GateOutcome.COMPOSE


def test_decide_is_deterministic():
    kwargs = dict(image_confidence=0.55, in_scope=True, retrieval_relevance=0.20)
    assert _decide(**kwargs) == _decide(**kwargs)
