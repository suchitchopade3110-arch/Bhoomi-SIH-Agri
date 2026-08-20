"""Voice ASR and TTS schemas for regional language interaction."""

from pydantic import BaseModel, Field
from app.schemas.common import SpokenResponseMixin


class VoiceTranscribeRequest(BaseModel):
    """Request to transcribe an uploaded audio asset."""
    audio_asset_id: str = Field(..., description="UUID string of uploaded audio asset")
    language: str = Field(default="ta", description="Language code (e.g., 'ta' for Tamil, 'hi' for Hindi)")


class VoiceTranscribeResponse(BaseModel):
    """Transcription response."""
    transcript: str = Field(..., description="Recognized speech text")
    language: str = Field(..., description="Detected / processed language code")
    confidence: float = Field(..., ge=0.0, le=1.0, description="ASR recognition confidence score")


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
