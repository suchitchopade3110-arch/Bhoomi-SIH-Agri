"""Intent parser — context-aware extraction of structured fields from Tamil transcripts.

Keyword-based (no LLM call) for speed and reliability. Supports both Tamil
script and common romanized forms.  The parser is context-driven:

- ``onboarding``: land_area, crop, growth_stage, region
- ``diagnosis``: raw symptom text (no structured field extraction)
- ``followup``: improved / no_change / got_worse
- ``general``: no structured parsing
"""

from __future__ import annotations

import re
from typing import Any, Optional

from pydantic import BaseModel


class ParsedIntent(BaseModel):
    """A single structured field extracted from a voice transcript."""
    field: str       # e.g. "land_area", "crop", "region"
    value: Any       # parsed value
    raw_text: str    # the substring that was matched


# ── Tamil keyword → value mappings ──────────────────────────────────────────

_CROP_KEYWORDS: dict[str, str] = {
    # Tamil script
    "நெல்": "samba_paddy",
    "சம்பா": "samba_paddy",
    "சம்பா நெல்": "samba_paddy",
    "பொன்னி": "ponni_paddy",
    "குருவை நெல்": "kuruvai_paddy",
    "தக்காளி": "tomato",
    "நிலக்கடலை": "groundnut",
    "கரும்பு": "sugarcane",
    "வாழை": "banana",
    # Romanized
    "samba": "samba_paddy",
    "paddy": "samba_paddy",
    "nel": "samba_paddy",
    "ponni": "ponni_paddy",
    "tomato": "tomato",
    "groundnut": "groundnut",
}

_REGION_KEYWORDS: dict[str, str] = {
    # Tamil script (Major TN agricultural/paddy districts & common vernacular short-forms)
    "ஈரோடு": "Erode",
    "தஞ்சாவூர்": "Thanjavur",
    "தஞ்சை": "Thanjavur",
    "சேலம்": "Salem",
    "மதுரை": "Madurai",
    "கோயம்புத்தூர்": "Coimbatore",
    "கோவை": "Coimbatore",
    "திருச்சிராப்பள்ளி": "Trichy",
    "திருச்சி": "Trichy",
    "திருவாரூர்": "Thiruvarur",
    "நாகப்பட்டினம்": "Nagapattinam",
    "நாகை": "Nagapattinam",
    "விழுப்புரம்": "Villupuram",
    "கடலூர்": "Cuddalore",

    # Romanized forms & transliterations
    "erode": "Erode",
    "thanjavur": "Thanjavur",
    "tanjore": "Thanjavur",
    "salem": "Salem",
    "madurai": "Madurai",
    "coimbatore": "Coimbatore",
    "kovai": "Coimbatore",
    "trichy": "Trichy",
    "tiruchirappalli": "Trichy",
    "tiruchi": "Trichy",
    "thiruvarur": "Thiruvarur",
    "tiruvarur": "Thiruvarur",
    "nagapattinam": "Nagapattinam",
    "nagai": "Nagapattinam",
    "villupuram": "Villupuram",
    "viluppuram": "Villupuram",
    "cuddalore": "Cuddalore",
}

_GROWTH_STAGE_KEYWORDS: dict[str, str] = {
    "நாற்று": "seedling",
    "நாற்றங்கால்": "nursery",
    "வளர்ச்சி": "vegetative",
    "பூக்கும்": "reproductive",
    "கதிர்": "reproductive",
    "முதிர்வு": "ripening",
    "அறுவடை": "ripening",
    "seedling": "seedling",
    "vegetative": "vegetative",
    "reproductive": "reproductive",
    "ripening": "ripening",
}

_FOLLOWUP_KEYWORDS: dict[str, str] = {
    # Tamil script
    "சரியாகிவிட்டது": "improved",
    "மேம்பட்டது": "improved",
    "நன்றாக": "improved",
    "குணமாகிவிட்டது": "improved",
    "நல்லது": "improved",
    "மாற்றமில்லை": "no_change",
    "மாற்றம் இல்லை": "no_change",
    "அதே நிலை": "no_change",
    "மோசமாகிவிட்டது": "got_worse",
    "மோசமாகி": "got_worse",
    "மோசம்": "got_worse",
    "அதிகமாகிவிட்டது": "got_worse",
    "பரவி": "got_worse",
    # Romanized
    "improved": "improved",
    "no change": "no_change",
    "worse": "got_worse",
    "got worse": "got_worse",
}

# Tamil number words → digit mapping
_TAMIL_NUMBERS: dict[str, float] = {
    "ஒரு": 1.0,
    "ஒன்று": 1.0,
    "இரண்டு": 2.0,
    "மூன்று": 3.0,
    "நான்கு": 4.0,
    "ஐந்து": 5.0,
    "ஆறு": 6.0,
    "ஏழு": 7.0,
    "எட்டு": 8.0,
    "ஒன்பது": 9.0,
    "பத்து": 10.0,
    "அரை": 0.5,
}


def _extract_land_area(text: str) -> Optional[ParsedIntent]:
    """Extract land area in acres from text.

    Matches patterns like:
    - "2 ஏக்கர்" (2 acres)
    - "இரண்டு ஏக்கர்" (two acres)
    - "2.5 acres"
    - "1 ஹெக்டேர்" → converts to acres (* 2.471)
    """
    # Try numeric + ஏக்கர் / acre
    m = re.search(r"(\d+\.?\d*)\s*(ஏக்கர்|acre|acres|eker)", text, re.IGNORECASE)
    if m:
        value = float(m.group(1))
        return ParsedIntent(field="land_area", value=value, raw_text=m.group(0))

    # Try numeric + ஹெக்டேர் / hectare → convert to acres
    m = re.search(r"(\d+\.?\d*)\s*(ஹெக்டேர்|hectare|hectares)", text, re.IGNORECASE)
    if m:
        value = round(float(m.group(1)) * 2.471, 2)
        return ParsedIntent(field="land_area", value=value, raw_text=m.group(0))

    # Try Tamil number words + ஏக்கர்
    for word, num in _TAMIL_NUMBERS.items():
        if word in text and "ஏக்கர்" in text:
            return ParsedIntent(field="land_area", value=num, raw_text=f"{word} ஏக்கர்")

    return None


def _match_keywords(text: str, keywords: dict[str, str], field: str) -> Optional[ParsedIntent]:
    """Match the longest keyword found in text.

    Longer keywords are checked first so "சம்பா நெல்" wins over "சம்பா".
    """
    text_lower = text.lower()
    # Sort by length descending so longer matches win
    for keyword in sorted(keywords.keys(), key=len, reverse=True):
        if keyword.lower() in text_lower or keyword in text:
            return ParsedIntent(field=field, value=keywords[keyword], raw_text=keyword)
    return None


class IntentParser:
    """Context-aware intent parser for Tamil voice transcripts.

    Uses keyword matching (no LLM call) for speed and reliability.
    """

    async def parse(self, text: str, lang: str, context: str) -> Optional[ParsedIntent]:
        """Parse a transcript into a structured intent based on context.

        Args:
            text: The transcribed text (Tamil or romanized).
            lang: BCP-47 language code (e.g. "ta-IN").
            context: One of "onboarding", "diagnosis", "followup", "general".

        Returns:
            A ``ParsedIntent`` if a structured field was extracted, else ``None``.
        """
        if context == "onboarding":
            return self._parse_onboarding(text)
        elif context == "followup":
            return self._parse_followup(text)
        elif context == "diagnosis":
            # Diagnosis context: return raw symptom text, no structured extraction
            return None
        else:  # "general" or unknown
            return None

    def _parse_onboarding(self, text: str) -> Optional[ParsedIntent]:
        """Extract onboarding fields in priority order."""
        # Land area is highest priority (numeric, consequential)
        result = _extract_land_area(text)
        if result:
            return result

        # Try crop, region, growth stage
        for keywords, field in [
            (_CROP_KEYWORDS, "crop"),
            (_REGION_KEYWORDS, "region"),
            (_GROWTH_STAGE_KEYWORDS, "growth_stage"),
        ]:
            result = _match_keywords(text, keywords, field)
            if result:
                return result

        return None

    def _parse_followup(self, text: str) -> Optional[ParsedIntent]:
        """Extract followup response from transcript."""
        return _match_keywords(text, _FOLLOWUP_KEYWORDS, "followup_response")

    def parse_field(self, text: str, field: str) -> Optional[Any]:
        """Extract a single field's value specifically from a correction text."""
        if field == "crop":
            res = _match_keywords(text, _CROP_KEYWORDS, "crop")
            return res.value if res else None
        elif field == "region":
            res = _match_keywords(text, _REGION_KEYWORDS, "region")
            return res.value if res else None
        elif field == "growth_stage":
            res = _match_keywords(text, _GROWTH_STAGE_KEYWORDS, "growth_stage")
            return res.value if res else None
        elif field == "land_area":
            res = _extract_land_area(text)
            return res.value if res else None
        return None
