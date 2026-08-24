"""Phase 2: pure next-available KVK routing (app/domain/routing.py)."""

import pytest

from app.domain.kvk_directory import KvkCenter
from app.domain.routing import select_next_available_kvk

ERODE = KvkCenter("agronomist:kvk_erode", "ICAR-KVK Erode", "Erode", 11.3410, 77.7172, capacity=2)
COIMBATORE = KvkCenter("agronomist:kvk_coimbatore", "ICAR-KVK Coimbatore", "Coimbatore", 11.0168, 76.9558, capacity=2)
MADURAI = KvkCenter("agronomist:kvk_madurai", "TNAU KVK Madurai", "Madurai", 9.9252, 78.1198, capacity=2)

CENTERS = [ERODE, COIMBATORE, MADURAI]

# A point close to Erode.
FARM_NEAR_ERODE = (11.40, 77.70)


def test_picks_nearest_available_center():
    result = select_next_available_kvk(*FARM_NEAR_ERODE, centers=CENTERS, current_caseload={})
    assert result.center_id == ERODE.center_id


def test_skips_center_at_capacity_even_if_nearest():
    caseload = {ERODE.center_id: 2}  # at capacity
    result = select_next_available_kvk(*FARM_NEAR_ERODE, centers=CENTERS, current_caseload=caseload)
    assert result.center_id != ERODE.center_id
    # Coimbatore is the next-nearest to a point near Erode.
    assert result.center_id == COIMBATORE.center_id


def test_falls_back_to_least_loaded_when_all_at_capacity():
    caseload = {ERODE.center_id: 2, COIMBATORE.center_id: 2, MADURAI.center_id: 5}
    result = select_next_available_kvk(*FARM_NEAR_ERODE, centers=CENTERS, current_caseload=caseload)
    # Erode and Coimbatore are tied at capacity=2; nearest of the tied pair wins.
    assert result.center_id == ERODE.center_id


def test_deterministic_tie_break_by_center_id():
    # Two centers equidistant and equally loaded: identical inputs must
    # always produce the identical result (alphabetical center_id wins).
    a = KvkCenter("agronomist:kvk_b", "B", "X", 10.0, 78.0, capacity=5)
    b = KvkCenter("agronomist:kvk_a", "A", "X", 10.0, 78.0, capacity=5)
    result1 = select_next_available_kvk(10.0, 78.0, centers=[a, b], current_caseload={})
    result2 = select_next_available_kvk(10.0, 78.0, centers=[a, b], current_caseload={})
    assert result1.center_id == result2.center_id == "agronomist:kvk_a"


def test_empty_centers_raises():
    with pytest.raises(ValueError):
        select_next_available_kvk(11.0, 77.0, centers=[], current_caseload={})


def test_caseload_defaults_to_zero_for_unlisted_centers():
    result = select_next_available_kvk(*FARM_NEAR_ERODE, centers=[ERODE], current_caseload={})
    assert result.center_id == ERODE.center_id
