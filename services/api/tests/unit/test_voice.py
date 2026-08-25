"""Voice layer unit tests — intent parsing, confirmation, read-back, stub providers.

Covers the Phase 2 spec's 8 required tests:
  1. test_transcribe_onboarding_parses_land_area
  2. test_transcribe_low_confidence_needs_confirmation
  3. test_transcribe_high_confidence_numeric_still_confirms
  4. test_intent_parser_tamil_crop_detection
  5. test_intent_parser_followup_got_worse
  6. test_readback_generates_tamil
  7. test_synthesize_returns_url
  8. test_stub_provider_returns_valid_response
"""

import pytest

from app.services.intent_parser import IntentParser, ParsedIntent
from app.services.confirmation import ConfirmationService


# ---------------------------------------------------------------------------
# IntentParser tests
# ---------------------------------------------------------------------------

@pytest.fixture
def parser() -> IntentParser:
    return IntentParser()


@pytest.fixture
def confirmation() -> ConfirmationService:
    return ConfirmationService(confidence_floor=0.85)


class TestIntentParser:
    """Tests for context-aware Tamil intent parsing."""

    @pytest.mark.asyncio
    async def test_onboarding_parses_land_area(self, parser: IntentParser):
        """Tamil onboarding audio → parsed_intent.field == 'land_area', value == 2.0"""
        text = "என் நிலம் இரண்டு ஏக்கர் சம்பா நெல்"
        result = await parser.parse(text, "ta-IN", "onboarding")
        assert result is not None
        assert result.field == "land_area"
        assert result.value == 2.0

    @pytest.mark.asyncio
    async def test_onboarding_parses_numeric_acres(self, parser: IntentParser):
        """Numeric acres: '2.5 ஏக்கர்' → land_area = 2.5"""
        result = await parser.parse("என் நிலம் 2.5 ஏக்கர்", "ta-IN", "onboarding")
        assert result is not None
        assert result.field == "land_area"
        assert result.value == 2.5

    @pytest.mark.asyncio
    async def test_intent_parser_tamil_crop_detection(self, parser: IntentParser):
        """Tamil crop keyword: 'சம்பா நெல்' → crop = 'samba_paddy'"""
        result = await parser.parse("சம்பா நெல் பயிர் செய்கிறேன்", "ta-IN", "onboarding")
        assert result is not None
        assert result.field == "crop"
        assert result.value == "samba_paddy"

    @pytest.mark.asyncio
    async def test_intent_parser_region_extraction_tamil_script(self, parser: IntentParser):
        """Tamil district keywords (Tamil script) → region extraction."""
        # Test Erode ("ஈரோடு")
        res1 = await parser.parse("ஈரோடு மாவட்டம்", "ta-IN", "onboarding")
        assert res1 is not None
        assert res1.field == "region"
        assert res1.value == "Erode"

        # Test Thanjavur ("தஞ்சாவூர்")
        res2 = await parser.parse("தஞ்சாவூர்", "ta-IN", "onboarding")
        assert res2 is not None
        assert res2.field == "region"
        assert res2.value == "Thanjavur"

        # Test Madurai ("மதுரை")
        res3 = await parser.parse("மதுரை பகுதி", "ta-IN", "onboarding")
        assert res3 is not None
        assert res3.field == "region"
        assert res3.value == "Madurai"

    @pytest.mark.asyncio
    async def test_intent_parser_region_extraction_romanized(self, parser: IntentParser):
        """Romanized district keywords → region extraction."""
        # Test Erode ("erode")
        res1 = await parser.parse("my farm is in erode district", "ta-IN", "onboarding")
        assert res1 is not None
        assert res1.field == "region"
        assert res1.value == "Erode"

        # Test Salem ("salem")
        res2 = await parser.parse("salem", "ta-IN", "onboarding")
        assert res2 is not None
        assert res2.field == "region"
        assert res2.value == "Salem"

        # Test Coimbatore ("coimbatore")
        res3 = await parser.parse("coimbatore region", "ta-IN", "onboarding")
        assert res3 is not None
        assert res3.field == "region"
        assert res3.value == "Coimbatore"

    @pytest.mark.asyncio
    async def test_intent_parser_removed_fields_not_extracted(self, parser: IntentParser):
        """Removed fields (soil_type, irrigation, season) no longer parse as onboarding fields."""
        # Soil keyword (formerly soil_type)
        res_soil = await parser.parse("களிமண் நிலம்", "ta-IN", "onboarding")
        assert res_soil is None

        # Irrigation keyword (formerly irrigation)
        res_irr = await parser.parse("கால்வாய் பாசனம்", "ta-IN", "onboarding")
        assert res_irr is None

        # Season keyword (formerly season)
        res_season = await parser.parse("நவராய் பருவம்", "ta-IN", "onboarding")
        assert res_season is None

    @pytest.mark.asyncio
    async def test_diagnosis_context_returns_none(self, parser: IntentParser):
        """Diagnosis context: returns None (raw text, no structured extraction)."""
        result = await parser.parse("இலை மஞ்சள் நிறமாக உள்ளது", "ta-IN", "diagnosis")
        assert result is None

    @pytest.mark.asyncio
    async def test_general_context_returns_none(self, parser: IntentParser):
        """General context: returns None."""
        result = await parser.parse("வணக்கம்", "ta-IN", "general")
        assert result is None


# ---------------------------------------------------------------------------
# ConfirmationService tests
# ---------------------------------------------------------------------------

class TestConfirmationService:
    """Tests for the read-back confirmation gate."""

    def test_low_confidence_needs_confirmation(self, confirmation: ConfirmationService):
        """Confidence 0.60 → needs_confirmation True"""
        intent = ParsedIntent(field="crop", value="samba_paddy", raw_text="சம்பா")
        assert confirmation.needs_confirmation(intent, confidence=0.60) is True

    def test_high_confidence_numeric_still_confirms(self, confirmation: ConfirmationService):
        """Confidence 0.95 but numeric field → needs_confirmation True (PRD §5.1)"""
        intent = ParsedIntent(field="land_area", value=2.0, raw_text="2 ஏக்கர்")
        assert confirmation.needs_confirmation(intent, confidence=0.95) is True

    def test_high_confidence_consequential_confirms(self, confirmation: ConfirmationService):
        """High confidence + consequential field → still confirms"""
        intent = ParsedIntent(field="crop", value="samba_paddy", raw_text="சம்பா")
        assert confirmation.needs_confirmation(intent, confidence=0.95) is True

    def test_no_intent_no_confirmation(self, confirmation: ConfirmationService):
        """None parsed_intent → needs_confirmation False"""
        assert confirmation.needs_confirmation(None, confidence=0.90) is False

    def test_readback_generates_tamil(self, confirmation: ConfirmationService):
        """Land area 2.0 → Tamil confirmation string contains '2' and 'ஏக்கர்'"""
        intent = ParsedIntent(field="land_area", value=2.0, raw_text="2 ஏக்கர்")
        readback = confirmation.generate_readback_text(intent)
        assert "2" in readback
        assert "ஏக்கர்" in readback
        assert "சரிதானா" in readback  # "is that correct?"

    def test_readback_crop_tamil(self, confirmation: ConfirmationService):
        """Crop readback contains Tamil crop name"""
        intent = ParsedIntent(field="crop", value="samba_paddy", raw_text="சம்பா")
        readback = confirmation.generate_readback_text(intent)
        assert "சம்பா நெல்" in readback
        assert "சரிதானா" in readback

    def test_readback_region(self, confirmation: ConfirmationService):
        """Region readback contains district name and confirmation question"""
        intent = ParsedIntent(field="region", value="Erode", raw_text="ஈரோடு")
        readback = confirmation.generate_readback_text(intent)
        assert "Erode" in readback
        assert "மாவட்டம்" in readback
        assert "சரிதானா" in readback
        assert confirmation.needs_confirmation(intent, confidence=0.95) is True


# ---------------------------------------------------------------------------
# Stub provider tests
# ---------------------------------------------------------------------------

class TestStubProvider:
    """Tests for the StubAsrTtsAdapter."""

    @pytest.mark.asyncio
    async def test_stub_provider_returns_valid_response(self):
        """Stub mode returns valid transcript + confidence."""
        from app.adapters.stubs import StubAsrTtsAdapter
        adapter = StubAsrTtsAdapter()
        text, confidence = await adapter.transcribe_audio("test-audio-id")
        assert isinstance(text, str)
        assert len(text) > 0
        assert 0.0 <= confidence <= 1.0

    @pytest.mark.asyncio
    async def test_stub_onboarding_context(self):
        """Stub with 'onboarding' hint returns Tamil farm text."""
        from app.adapters.stubs import StubAsrTtsAdapter
        adapter = StubAsrTtsAdapter()
        text, confidence = await adapter.transcribe_audio("onboarding-audio-123")
        assert "ஏக்கர்" in text or "நெல்" in text
        assert confidence > 0.85

    @pytest.mark.asyncio
    async def test_stub_followup_context(self):
        """Stub with 'followup' hint returns Tamil followup response."""
        from app.adapters.stubs import StubAsrTtsAdapter
        adapter = StubAsrTtsAdapter()
        text, confidence = await adapter.transcribe_audio("followup-audio-456")
        assert "மோசமாகிவிட்டது" in text
        assert confidence > 0.85

    @pytest.mark.asyncio
    async def test_synthesize_returns_url(self):
        """Synthesize returns an audio URL."""
        from app.adapters.stubs import StubAsrTtsAdapter
        adapter = StubAsrTtsAdapter()
        asset_id, url = await adapter.synthesize_speech("வணக்கம்", "ta")
        assert isinstance(url, str)
        assert url.startswith("http")
        assert asset_id  # non-empty
