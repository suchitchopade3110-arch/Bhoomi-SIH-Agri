"""LLM port — typed Protocol for grounded generation and case file synthesis."""

from typing import Any, Protocol


class LLMPort(Protocol):
    """Port for grounded LLM generation and case file synthesis."""

    async def generate_grounded_advisory(
        self,
        query: str,
        context_chunks: list[dict[str, Any]],
        farm_context: dict[str, Any],
    ) -> dict[str, Any]:
        """Generate structured 5-point advisory grounded strictly in provided context chunks."""
        ...

    async def synthesize_case_summary(
        self,
        farm_data: dict[str, Any],
        events: list[dict[str, Any]],
        health_history: list[dict[str, Any]],
    ) -> str:
        """Synthesize a concise, multi-factor problem summary for expert escalation."""
        ...


__all__ = ["LLMPort"]
