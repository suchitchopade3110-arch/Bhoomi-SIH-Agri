"""Orchestration service for Grounded 5-Point Advisory generation via RAG."""

from typing import Any
from app.schemas.advisory import Advisory, AdvisoryGenerateRequest


class AdvisoryService:
    """Orchestrates RAG retrieval, citation verification, and 5-point advisory construction."""

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs

    async def generate_advisory(self, request: AdvisoryGenerateRequest) -> Advisory:
        """Retrieve verified corpus chunks, ground LLM advice, and enforce no-fabrication gate."""
        raise NotImplementedError("AdvisoryService.generate_advisory will be implemented in subsequent phases.")

    async def get_advisory_by_id(self, advisory_id: str) -> Advisory:
        """Fetch existing advisory record by UUID."""
        raise NotImplementedError("AdvisoryService.get_advisory_by_id will be implemented in subsequent phases.")
