"""Tamil spoken summary generator for farmer-facing API responses.

Every consequential response must carry a ``spoken_summary`` field in Tamil
(PRD §5.1, API contract §2). The Flutter app TTS's this locally.
"""

from __future__ import annotations

from typing import Optional


# Health band → Tamil display name
BAND_TAMIL: dict[str, str] = {
    "unrated": "மதிப்பீடு இல்லை",
    "critical": "மிகவும் ஆபத்தான",
    "poor": "மோசமான",
    "watch": "கவனிக்க வேண்டிய",
    "good": "நல்ல",
    "excellent": "சிறப்பான",
}

# Confidence level → Tamil word
CONFIDENCE_WORDS: dict[str, str] = {
    "high": "உயர்ந்த",      # >= 0.80
    "medium": "நடுத்தர",     # >= 0.60
    "low": "குறைந்த",       # < 0.60
}


def _confidence_word(confidence: float) -> str:
    """Map a numeric confidence to a Tamil word."""
    if confidence >= 0.80:
        return CONFIDENCE_WORDS["high"]
    elif confidence >= 0.60:
        return CONFIDENCE_WORDS["medium"]
    return CONFIDENCE_WORDS["low"]


class SpokenSummaryService:
    """Generates Tamil spoken summaries for API responses."""

    def for_health(
        self,
        score: Optional[int],
        band: str,
        reason: str = "",
    ) -> str:
        """Spoken summary for health score endpoint."""
        if score is None or band == "unrated":
            return "மதிப்பீடு செய்ய போதுமான தகவல்கள் இல்லை."

        band_name = BAND_TAMIL.get(band, band)
        summary = f"உங்கள் மதிப்பெண் {score}."
        if reason:
            summary += f" {reason}"
        return summary

    def for_diagnosis(
        self,
        above_gate: bool,
        disease: str = "",
        confidence: float = 0,
    ) -> str:
        """Spoken summary for diagnosis endpoint."""
        if not above_gate:
            return "எனக்கு உறுதியாகத் தெரியவில்லை. நிபுணருக்கு அனுப்பப்பட்டது."

        conf_word = _confidence_word(confidence)
        return f"இது {disease} நோயாக இருக்கலாம். நம்பகத்தன்மை: {conf_word}."

    def for_advisory(
        self,
        retrieved: bool,
    ) -> str:
        """Spoken summary for RAG advisory endpoint."""
        if retrieved:
            return "உங்கள் கேள்விக்கான பதில் கிடைத்தது."
        return "இதற்கான நம்பகமான தகவல் என்னிடம் இல்லை. நிபுணருக்கு அனுப்பலாமா?"

    def for_resource_plan(self, liters: int) -> str:
        """Spoken summary for resource plan endpoint."""
        return f"இன்றைய நீர் தேவை சுமார் {liters} லிட்டர்."

    def for_followup(
        self,
        response: str,
        score: Optional[int] = None,
    ) -> str:
        """Spoken summary for followup response."""
        if response == "improved":
            base = "நிலைமை மேம்பட்டுள்ளது."
            if score is not None:
                base += f" மதிப்பெண்: {score}."
            return base
        elif response == "got_worse":
            return "நிலைமை மோசமாகியுள்ளது. நிபுணருக்கு அனுப்பப்பட்டது."
        else:  # no_change
            return "நிலைமை மாறவில்லை."

    def for_farm_summary(
        self,
        score: Optional[int],
        band: str,
    ) -> str:
        """Spoken summary for farm summary / dashboard."""
        band_name = BAND_TAMIL.get(band, band)
        if score is None:
            return f"உங்கள் பண்ணை {band_name} நிலையில் உள்ளது."
        return f"உங்கள் பண்ணை {band_name} நிலையில் உள்ளது. மதிப்பெண் {score}."

    def for_scheme(self, count: int) -> str:
        """Spoken summary for scheme matching."""
        return f"{count} திட்டங்கள் பொருந்துகின்றன."

    def for_escalation(self) -> str:
        """Spoken summary for escalation."""
        return "உங்கள் பிரச்சனை நிபுணருக்கு அனுப்பப்பட்டது."

    def for_land_status(self, status: str) -> str:
        """Spoken summary for land verification status."""
        if status == "verified":
            return "உங்கள் நிலம் சரிபார்க்கப்பட்டது."
        elif status == "rejected":
            return "உங்கள் நிலம் நிராகரிக்கப்பட்டது."
        return "உங்கள் நில சரிபார்ப்பு நிலுவையில் உள்ளது."
