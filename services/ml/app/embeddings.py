"""Text embedding endpoint logic.

Deterministic token-level feature hashing (the "hashing trick"): each
token hashes to a dimension it increments, then the vector is L2-normalized.
Two texts sharing vocabulary get genuine cosine overlap; unrelated text
doesn't — good enough for RAG relevance ranking without downloading real
embedding model weights.

This is the same technique as services/api's ``StubEmbeddingAdapter``,
factored out here as a standalone, dependency-free implementation so this
service can expose it over HTTP independently of the API process. It is
**not** BAAI/bge-m3 or any other trained dense embedding model — see
``README.md`` §9 for why that's still a documented gap rather than wired in
(model weights aren't checked into this repo and downloading/serving them
is a separate, heavier phase of work).
"""

from __future__ import annotations

import hashlib
import re

_STOPWORDS = frozenset(
    {
        "a", "an", "and", "are", "as", "at", "be", "been", "by", "can", "do", "does",
        "for", "from", "has", "have", "how", "if", "in", "into", "is", "it", "its",
        "of", "on", "or", "should", "that", "the", "their", "then", "there", "this",
        "to", "was", "were", "what", "when", "where", "which", "who", "will", "with",
        "your", "you", "my", "i", "not", "than", "also",
    }
)
_MIN_TOKEN_LENGTH = 3
DEFAULT_DIMENSION = 1024


def _tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if len(t) >= _MIN_TOKEN_LENGTH and t not in _STOPWORDS]


def embed_text(text: str, dimension: int = DEFAULT_DIMENSION) -> list[float]:
    vec = [0.0] * dimension
    for token in _tokenize(text):
        digest = hashlib.md5(token.encode("utf-8")).hexdigest()
        index = int(digest[:8], 16) % dimension
        sign = 1.0 if int(digest[8], 16) % 2 == 0 else -1.0
        vec[index] += sign

    norm = sum(x * x for x in vec) ** 0.5
    if norm == 0.0:
        return vec
    return [round(x / norm, 6) for x in vec]


def embed_batch(texts: list[str], dimension: int = DEFAULT_DIMENSION) -> list[list[float]]:
    return [embed_text(t, dimension) for t in texts]
