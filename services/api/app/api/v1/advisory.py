"""Grounded 5-Point Advisory API router."""

from fastapi import APIRouter
from app.core.errors import NotImplementedAPIError
from app.schemas.advisory import (
    Advisory,
    AdvisoryGenerateRequest,
)

router = APIRouter(prefix="/advisory", tags=["Advisory & RAG"])


@router.post(
    "/generate",
    response_model=Advisory,
    summary="Generate grounded 5-point advisory from verified corpus with citations",
)
async def generate_advisory(request: AdvisoryGenerateRequest) -> Advisory:
    raise NotImplementedAPIError("Endpoint POST /advisory/generate will be implemented in subsequent phases.")


@router.get(
    "/{advisory_id}",
    response_model=Advisory,
    summary="Get advisory by UUID",
)
async def get_advisory(advisory_id: str) -> Advisory:
    raise NotImplementedAPIError("Endpoint GET /advisory/{advisory_id} will be implemented in subsequent phases.")
