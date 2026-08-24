"""Phase 2: pure queue position + ETA (app/domain/queue.py)."""

from datetime import datetime, timedelta, timezone

import pytest

from app.core.enums import ProblemSeverity
from app.domain.queue import DEFAULT_AVG_RESOLUTION_MINUTES, QueueCase, compute_queue_positions, estimate_eta

NOW = datetime(2026, 8, 24, 6, 0, 0, tzinfo=timezone.utc)


def _case(case_id, center, severity, minutes_ago):
    return QueueCase(
        case_id=case_id,
        assigned_to=center,
        severity=severity,
        escalated_at=NOW - timedelta(minutes=minutes_ago),
    )


def test_severe_jumps_ahead_of_earlier_moderate():
    cases = [
        _case("c1", "kvk_a", ProblemSeverity.MODERATE, minutes_ago=30),
        _case("c2", "kvk_a", ProblemSeverity.SEVERE, minutes_ago=5),
    ]
    positions = compute_queue_positions(cases)
    assert positions["c2"] == 1
    assert positions["c1"] == 2


def test_same_severity_orders_by_arrival():
    cases = [
        _case("c1", "kvk_a", ProblemSeverity.EARLY, minutes_ago=5),
        _case("c2", "kvk_a", ProblemSeverity.EARLY, minutes_ago=30),
    ]
    positions = compute_queue_positions(cases)
    assert positions["c2"] == 1  # arrived first
    assert positions["c1"] == 2


def test_queue_position_scoped_per_center():
    cases = [
        _case("c1", "kvk_a", ProblemSeverity.EARLY, minutes_ago=10),
        _case("c2", "kvk_b", ProblemSeverity.EARLY, minutes_ago=999),  # much older, different center
    ]
    positions = compute_queue_positions(cases)
    # Each is #1 in its own center's queue, unaffected by the other center.
    assert positions["c1"] == 1
    assert positions["c2"] == 1


def test_deterministic_tie_break_by_case_id():
    cases = [
        _case("c2", "kvk_a", ProblemSeverity.EARLY, minutes_ago=10),
        _case("c1", "kvk_a", ProblemSeverity.EARLY, minutes_ago=10),
    ]
    positions = compute_queue_positions(cases)
    assert positions["c1"] == 1
    assert positions["c2"] == 2


def test_eta_position_one_is_one_resolution_slot_out():
    eta = estimate_eta(position=1, evaluated_at=NOW)
    assert eta == NOW + timedelta(minutes=DEFAULT_AVG_RESOLUTION_MINUTES)


def test_eta_scales_with_position():
    eta_pos_3 = estimate_eta(position=3, evaluated_at=NOW)
    assert eta_pos_3 == NOW + timedelta(minutes=DEFAULT_AVG_RESOLUTION_MINUTES * 3)


def test_eta_is_deterministic_for_same_inputs():
    assert estimate_eta(position=2, evaluated_at=NOW) == estimate_eta(position=2, evaluated_at=NOW)


def test_eta_rejects_non_positive_position():
    with pytest.raises(ValueError):
        estimate_eta(position=0, evaluated_at=NOW)
