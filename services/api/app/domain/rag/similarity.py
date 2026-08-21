"""Pure vector similarity math. No I/O, no DB — used by both the real
pgvector-backed repository's Python-side helpers and the in-memory test
double, so the two never silently disagree on what "relevance" means.
"""


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors, clamped to ``[0.0, 1.0]``.

    Embeddings in this system are always L2-normalized (see
    ``adapters.stubs.StubEmbeddingAdapter``), so cosine similarity reduces to
    a dot product — but this function normalizes defensively regardless, so
    it is correct even for non-normalized input.

    Returns ``0.0`` for a zero vector (rather than raising) since a chunk or
    query that hashed to nothing carries no relevance signal.
    """
    if len(a) != len(b):
        raise ValueError(f"Vector length mismatch: {len(a)} != {len(b)}")

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5

    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0

    similarity = dot / (norm_a * norm_b)
    return max(0.0, min(1.0, similarity))
