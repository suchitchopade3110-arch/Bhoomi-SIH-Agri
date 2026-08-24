"""Phase 2: pure next-available agronomist routing (app/domain/routing.py)."""

import pytest

from app.domain.routing import select_next_available_agronomist

AGRONOMISTS = ["agronomist:a", "agronomist:b", "agronomist:c"]


def test_picks_agronomist_with_fewest_open_cases():
    counts = {"agronomist:a": 1, "agronomist:b": 3, "agronomist:c": 5}
    assert select_next_available_agronomist(AGRONOMISTS, counts) == "agronomist:a"


def test_missing_from_counts_treated_as_zero_load():
    counts = {"agronomist:a": 2, "agronomist:b": 1}  # "agronomist:c" absent
    assert select_next_available_agronomist(AGRONOMISTS, counts) == "agronomist:c"


def test_ties_broken_lexicographically_by_id():
    counts = {"agronomist:a": 2, "agronomist:b": 2, "agronomist:c": 2}
    assert select_next_available_agronomist(AGRONOMISTS, counts) == "agronomist:a"


def test_deterministic_for_identical_inputs():
    counts = {"agronomist:a": 1, "agronomist:b": 1}
    result1 = select_next_available_agronomist(AGRONOMISTS, counts)
    result2 = select_next_available_agronomist(AGRONOMISTS, counts)
    assert result1 == result2


def test_empty_counts_picks_lexicographically_smallest():
    assert select_next_available_agronomist(AGRONOMISTS, {}) == "agronomist:a"


def test_empty_agronomist_list_raises():
    with pytest.raises(ValueError):
        select_next_available_agronomist([], {})
