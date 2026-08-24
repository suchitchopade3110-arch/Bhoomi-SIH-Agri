"""Guidance Cards API router (PRD §5.8, Phase 4)."""

from typing import Annotated, Any
from fastapi import APIRouter, Depends, Query
from app.core.security import get_current_token_payload
from app.domain.guidance.cards import GuidanceCard, get_guidance_card, list_all_guidance_cards

router = APIRouter(prefix="/guidance", tags=["Interim Guidance Cards"])


@router.get(
    "",
    response_model=list[GuidanceCard],
    summary="List all static interim guidance containment cards",
)
async def list_guidance(
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
) -> list[GuidanceCard]:
    return list_all_guidance_cards()


@router.get(
    "/{crop}",
    response_model=GuidanceCard,
    summary="Get interim containment guidance card for a specific crop and optional problem",
)
async def get_crop_guidance(
    crop: str,
    _auth: Annotated[dict[str, Any], Depends(get_current_token_payload)],
    problem_label: str | None = Query(default=None, description="Optional specific problem identifier"),
    problem_type: str | None = Query(default=None, description="Optional problem category: disease | pest | general"),
) -> GuidanceCard:
    return get_guidance_card(crop=crop, problem_label=problem_label, problem_type=problem_type)
