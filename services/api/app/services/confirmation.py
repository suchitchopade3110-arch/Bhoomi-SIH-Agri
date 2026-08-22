"""Read-back confirmation logic — PRD §5.1 voice safety net.

"Every number the system commits to is confirmed back by voice before it's saved."

The ConfirmationService decides whether a parsed intent needs verbal confirmation
and generates the Tamil read-back prompt.
"""

from __future__ import annotations

from typing import Optional

from app.services.intent_parser import ParsedIntent


# Fields that always require confirmation (consequential data)
_CONSEQUENTIAL_FIELDS = frozenset({
    "land_area", "crop", "soil_type", "growth_stage",
    "irrigation", "season",
})

# Fields with numeric values always require confirmation regardless of confidence
_NUMERIC_FIELDS = frozenset({"land_area"})

# Configurable via CONFIRMATION_CONFIDENCE_FLOOR env var (default 0.85)
DEFAULT_CONFIDENCE_FLOOR = 0.85

# Tamil readback templates per field
_READBACK_TEMPLATES: dict[str, str] = {
    "land_area": "நீங்கள் சொன்னது {value} ஏக்கர் நிலம், சரிதானா?",
    "crop": "நீங்கள் {value_display} பயிர் என்று சொன்னீர்கள், சரிதானா?",
    "soil_type": "மண் வகை {value_display}, சரிதானா?",
    "growth_stage": "பயிர் வளர்ச்சி நிலை {value_display}, சரிதானா?",
    "irrigation": "நீர்ப்பாசன வகை {value_display}, சரிதானா?",
    "season": "பருவம் {value_display}, சரிதானா?",
    "followup_response": "நீங்கள் {value_display} என்று சொன்னீர்கள், சரிதானா?",
}

# Value → Tamil display name mapping
_VALUE_DISPLAY: dict[str, str] = {
    # Crops
    "samba_paddy": "சம்பா நெல்",
    "ponni_paddy": "பொன்னி நெல்",
    "kuruvai_paddy": "குருவை நெல்",
    "tomato": "தக்காளி",
    "groundnut": "நிலக்கடலை",
    "sugarcane": "கரும்பு",
    "banana": "வாழை",
    # Soil types
    "clay_loam": "களிமண்",
    "sandy": "மணல்",
    "red_soil": "செம்மண்",
    "alluvial": "வண்டல்",
    "black_soil": "கருப்பு மண்",
    # Growth stages
    "seedling": "நாற்று",
    "nursery": "நாற்றங்கால்",
    "vegetative": "வளர்ச்சி",
    "reproductive": "பூக்கும்",
    "ripening": "முதிர்வு",
    # Irrigation
    "canal": "கால்வாய்",
    "borewell": "ஆழ்குழாய்",
    "well": "கிணறு",
    "rainfed": "மழை நீர்",
    # Season
    "samba": "சம்பா",
    "navarai": "நவராய்",
    "kuruvai": "குருவை",
    # Followup
    "improved": "மேம்பட்டது",
    "no_change": "மாற்றமில்லை",
    "got_worse": "மோசமாகிவிட்டது",
}


class ConfirmationService:
    """Decides whether voice input needs read-back confirmation and generates the prompt."""

    def __init__(self, confidence_floor: float = DEFAULT_CONFIDENCE_FLOOR) -> None:
        self._confidence_floor = confidence_floor

    def needs_confirmation(
        self,
        parsed_intent: Optional[ParsedIntent],
        confidence: float,
    ) -> bool:
        """Returns True when the voice input must be confirmed before saving.

        Confirmation is required when:
        - A consequential onboarding field was parsed
        - ASR confidence is below the confidence floor
        - The parsed value is numeric (land_area, quantities)
        """
        if parsed_intent is None:
            return False

        # Numeric fields always need confirmation (PRD §5.1)
        if parsed_intent.field in _NUMERIC_FIELDS:
            return True

        # Low confidence → confirm
        if confidence < self._confidence_floor:
            return True

        # Consequential fields need confirmation
        if parsed_intent.field in _CONSEQUENTIAL_FIELDS:
            return True

        return False

    def generate_readback_text(
        self,
        parsed_intent: ParsedIntent,
        lang: str = "ta-IN",
    ) -> str:
        """Generate a Tamil confirmation prompt for the parsed intent.

        Example output: "நீங்கள் சொன்னது 2 ஏக்கர் நிலம், சரிதானா?"
        (You said 2 acres of land, is that correct?)
        """
        template = _READBACK_TEMPLATES.get(parsed_intent.field)
        if template is None:
            # Fallback for unknown fields
            return f"நீங்கள் சொன்னது {parsed_intent.value}, சரிதானா?"

        value_display = _VALUE_DISPLAY.get(str(parsed_intent.value), str(parsed_intent.value))

        return template.format(
            value=parsed_intent.value,
            value_display=value_display,
        )
