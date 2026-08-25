"""Voice ASR and TTS schemas for regional language interaction."""

from typing import Any, Optional

from pydantic import BaseModel, Field
from app.schemas.common import SpokenResponseMixin


class ParsedIntent(BaseModel):
    """A single structured field extracted from a voice transcript."""
    field: str = Field(..., description="Field name, e.g. 'land_area', 'crop', 'soil_type'")
    value: Any = Field(..., description="Parsed value")
    raw_text: str = Field(..., description="Original substring that was parsed")


class VoiceTranscribeRequest(BaseModel):
    """Request to transcribe an uploaded audio asset."""
    audio_asset_id: str = Field(..., description="UUID string of uploaded audio asset")
    language: str = Field(default="ta", description="Language code (e.g., 'ta' for Tamil, 'hi' for Hindi)")
    context: str = Field(
        default="general",
        description="Context for intent parsing: 'onboarding' | 'diagnosis' | 'followup' | 'general'",
    )


class VoiceTranscribeResponse(BaseModel):
    """Transcription response with optional parsed intent and confirmation flag."""
    transcript: str = Field(..., description="Recognized speech text")
    language: str = Field(..., description="Detected / processed language code")
    confidence: float = Field(..., ge=0.0, le=1.0, description="ASR recognition confidence score")
    parsed_intent: Optional[ParsedIntent] = Field(
        default=None,
        description="Structured field extracted from the transcript (context-dependent)",
    )
    needs_confirmation: bool = Field(
        default=False,
        description="True if the parsed value requires read-back confirmation before saving",
    )
    readback_text: Optional[str] = Field(
        default=None,
        description="Tamil confirmation prompt text (populated when needs_confirmation=True)",
    )
    provider: str = Field(
        ..., description="ASR implementation that actually produced this transcript, e.g. 'stub', 'sarvam', 'bhashini'",
    )


class VoiceSynthesizeRequest(BaseModel):
    """Request to synthesize regional speech from text."""
    text: str = Field(..., description="Text to synthesize into audio")
    language: str = Field(default="ta", description="Target language code")
    gender: str = Field(default="female", description="Voice gender preference ('female' | 'male')")


class VoiceSynthesizeResponse(BaseModel):
    """Synthesized speech audio response."""
    audio_asset_id: str = Field(..., description="UUID string of generated audio asset")
    audio_url: str = Field(..., description="Presigned URL to play or download audio")
    duration_seconds: float | None = Field(default=None, description="Audio duration in seconds")
    provider: str = Field(
        ..., description="TTS implementation that actually produced this audio, e.g. 'stub', 'sarvam', 'gtts'",
    )


class VoiceQueryRequest(BaseModel):
    """End-to-end voice query request."""
    audio_asset_id: str = Field(..., description="UUID string of farmer spoken query")
    farm_id: str = Field(..., description="UUID string of farm context")
    language: str = Field(default="ta", description="Language code")


class VoiceQueryResponse(SpokenResponseMixin):
    """End-to-end voice query response with transcript, answer, and audio URL."""
    transcript: str = Field(..., description="Transcribed query text")
    answer_text: str = Field(..., description="Generated answer text")
    audio_response_url: str = Field(..., description="Presigned URL to play generated speech response")
