"""Embeddings port — typed Protocol for dense vector generation."""

from typing import Protocol


class EmbeddingPort(Protocol):
    """Port for generating dense vector embeddings for RAG retrieval."""

    async def embed_text(self, text: str) -> list[float]:
        """Generate vector embedding for a single text string."""
        ...

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Generate vector embeddings for a batch of text strings."""
        ...


__all__ = ["EmbeddingPort"]
