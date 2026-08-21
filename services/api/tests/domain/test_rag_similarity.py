"""Unit tests for cosine_similarity."""

import pytest

from app.domain.rag.similarity import cosine_similarity


def test_identical_vectors_are_similarity_one():
    v = [1.0, 2.0, 3.0]
    assert cosine_similarity(v, v) == pytest.approx(1.0)


def test_orthogonal_vectors_are_similarity_zero():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


def test_opposite_vectors_clamp_to_zero_not_negative():
    assert cosine_similarity([1.0, 0.0], [-1.0, 0.0]) == 0.0


def test_zero_vector_is_similarity_zero():
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_mismatched_lengths_raise():
    with pytest.raises(ValueError):
        cosine_similarity([1.0, 2.0], [1.0])


def test_result_always_in_unit_interval():
    import random

    random.seed(42)
    for _ in range(20):
        a = [random.uniform(-5, 5) for _ in range(16)]
        b = [random.uniform(-5, 5) for _ in range(16)]
        score = cosine_similarity(a, b)
        assert 0.0 <= score <= 1.0
