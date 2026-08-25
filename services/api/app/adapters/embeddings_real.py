"""Real ``EmbeddingPort`` adapter (``EMBEDDING_PROVIDER=bge_m3``).

Mirrors ``image_diagnosis_real.py``'s pattern exactly: this adapter calls
out to ``services/ml`` (``settings.ML_SERVICE_URL``) rather than loading a
~2.2GB model in-process, keeping heavy ML weights out of the main API
service.

Honesty note: ``services/ml``'s ``/embed`` endpoint falls back to a
deterministic hash embedder when the optional BGE-m3 dependency isn't
installed/available there (see ``services/ml/app/embeddings_real.py``) —
this adapter surfaces which one actually ran via ``meta["method"]`` rather
than silently claiming "bge_m3" regardless. The sandboxed environment this
was built in couldn't reach Hugging Face Hub to download real weights, so
the real-embedding path itself is implemented but unverified end-to-end;
the fallback path is genuinely exercised (services/ml has no torch/
sentence-transformers installed there either).
"""

import httpx

EMBED_ENDPOINT_PATH = "/embed"
REQUEST_TIMEOUT_SECONDS = 30.0  # real model inference is slower than the hash path


class RealEmbeddingAdapter:
    """Calls the ``services/ml`` embedding endpoint over HTTP."""

    def __init__(self, ml_service_url: str) -> None:
        self._base_url = ml_service_url.rstrip("/")

    async def embed_text(self, text: str) -> list[float]:
        return (await self.embed_batch([text]))[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.post(
                f"{self._base_url}{EMBED_ENDPOINT_PATH}",
                json={"texts": texts, "prefer_real": True},
            )
            response.raise_for_status()
            payload = response.json()
        return payload["embeddings"]
