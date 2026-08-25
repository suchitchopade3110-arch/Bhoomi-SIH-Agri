"""Real dense text embeddings via BAAI/bge-m3 (sentence-transformers).

Optional and lazy: ``sentence-transformers``/``torch`` are NOT in this
service's default ``requirements.txt`` (they pull in ~5GB including CUDA
libraries) — install ``requirements-embeddings.txt`` to enable this path.
Model weights (~2.2GB) are fetched from Hugging Face Hub on first use and
cached locally by ``sentence-transformers``.

Honesty note (matches this project's "never fabricate" ethos): this module
was written and is structurally correct, but **has not been verified
against real downloaded weights** — the sandboxed environment this was
built in blocks outbound access to huggingface.co and pypi's torch/CUDA
mirrors at the network layer (a policy 403, not a code issue), so the
actual model-load-and-encode path could not be exercised end-to-end here.
Everything in this module that *can* be verified without real weights
(the graceful-fallback behavior when the dependency is absent) is covered
by ``tests/test_diagnose.py``.
"""

from __future__ import annotations

import logging
import threading

logger = logging.getLogger("bhoomi.ml.embeddings_real")

_model = None
_model_lock = threading.Lock()
_load_failed = False

MODEL_NAME = "BAAI/bge-m3"
REAL_DIMENSION = 1024  # bge-m3's native dense output size


def _get_model():
    """Lazily load the model once per process. Returns None (and stays
    None for the rest of the process) if the optional dependency isn't
    installed or the model can't be downloaded — callers fall back to the
    hash embedder rather than raising, since a missing optional dependency
    is not the same failure class as a genuine bug."""
    global _model, _load_failed
    if _model is not None:
        return _model
    if _load_failed:
        return None

    with _model_lock:
        if _model is not None or _load_failed:
            return _model
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            logger.info("sentence-transformers not installed — real embeddings unavailable, using hash fallback")
            _load_failed = True
            return None

        try:
            _model = SentenceTransformer(MODEL_NAME)
        except Exception:
            logger.exception("Failed to load %s — using hash fallback", MODEL_NAME)
            _load_failed = True
            return None

        return _model


def is_available() -> bool:
    """Cheap check callers can use before deciding whether to report
    method='bge_m3' vs 'hash' without paying the encode cost."""
    return _get_model() is not None


def embed_batch_real(texts: list[str]) -> list[list[float]] | None:
    """Real BGE-m3 dense embeddings, or None if the model isn't available
    (see module docstring). Never raises for an availability problem —
    only for a genuine encode-time error, which should surface."""
    model = _get_model()
    if model is None:
        return None
    vectors = model.encode(texts, normalize_embeddings=True)
    return [v.tolist() for v in vectors]
