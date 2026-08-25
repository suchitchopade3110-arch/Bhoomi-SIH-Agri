"""Tests for Interim Static Guidance Cards (Phase 4 Objective 1).

Verifies:
  1. Every label in SUPPORTED_LABELS (both disease and pest scope lists from Phase 1)
     has an authored guidance entry — no supported problem falls through.
  2. Every major crop has an authored baseline guidance entry.
  3. Universal fallback guarantees unknown crops/problems return actionable containment advice.
  4. Each GuidanceCard has non-empty containment_advice, what_to_avoid, immediate_actions, and expert_trigger.
"""

import pytest
from app.domain.gate.constants import SUPPORTED_LABELS
from app.domain.guidance.cards import (
    GuidanceCard,
    get_guidance_card,
    list_all_guidance_cards,
)

MAJOR_CROPS = [
    "rice",
    "paddy",
    "samba_paddy",
    "cotton",
    "maize",
    "tomato",
    "potato",
    "groundnut",
    "sugarcane",
    "chilli",
    "wheat",
]


def test_every_disease_label_in_supported_scope_has_guidance_card():
    """Every disease in SUPPORTED_LABELS['disease'] resolves to a valid GuidanceCard."""
    diseases = SUPPORTED_LABELS["disease"]
    assert len(diseases) > 0

    for disease_label in diseases:
        card = get_guidance_card(crop="rice", problem_label=disease_label, problem_type="disease")
        assert isinstance(card, GuidanceCard)
        assert card.problem_label == disease_label
        assert card.problem_type == "disease"
        assert len(card.title) > 0
        assert len(card.containment_advice) > 0
        assert len(card.what_to_avoid) > 0
        assert len(card.immediate_actions) >= 2
        assert len(card.expert_trigger) > 0


def test_every_pest_label_in_supported_scope_has_guidance_card():
    """Every pest in SUPPORTED_LABELS['pest'] resolves to a valid GuidanceCard."""
    pests = SUPPORTED_LABELS["pest"]
    assert len(pests) > 0

    for pest_label in pests:
        card = get_guidance_card(crop="rice", problem_label=pest_label, problem_type="pest")
        assert isinstance(card, GuidanceCard)
        assert card.problem_label == pest_label
        assert card.problem_type == "pest"
        assert len(card.title) > 0
        assert len(card.containment_advice) > 0
        assert len(card.what_to_avoid) > 0
        assert len(card.immediate_actions) >= 2
        assert len(card.expert_trigger) > 0


def test_every_major_crop_has_guidance_card():
    """Every major agricultural crop resolves to a concrete crop-specific card."""
    for crop in MAJOR_CROPS:
        card = get_guidance_card(crop=crop)
        assert isinstance(card, GuidanceCard)
        assert len(card.containment_advice) > 0
        assert len(card.what_to_avoid) > 0
        assert len(card.immediate_actions) >= 1
        assert len(card.expert_trigger) > 0


def test_unknown_crop_returns_universal_fallback():
    """Unknown crop or unclassified stress gracefully returns universal agricultural containment card."""
    card = get_guidance_card(crop="dragonfruit_special", problem_label="unknown_wilting_symptom")
    assert isinstance(card, GuidanceCard)
    assert "Interim Containment" in card.title or "Protocol" in card.title
    assert len(card.containment_advice) > 0
    assert len(card.what_to_avoid) > 0
    assert len(card.immediate_actions) >= 2
    assert len(card.expert_trigger) > 0


def test_list_all_guidance_cards():
    """list_all_guidance_cards returns all authored static cards."""
    cards = list_all_guidance_cards()
    assert len(cards) >= 20
    for c in cards:
        assert isinstance(c, GuidanceCard)
        assert c.title != ""
        assert c.containment_advice != ""
