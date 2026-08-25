"""Startup validation for LLM_PROVIDER=groq (no-fabrication rule, PRD): a
real provider with a missing/mock/malformed key must fail loudly rather than
silently booting into a state that could later be mistaken for a working
real-generation path.
"""

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_stub_provider_boots_with_mock_key():
    settings = Settings(LLM_PROVIDER="stub", LLM_API_KEY="mock-llm-api-key")
    assert settings.LLM_PROVIDER == "stub"


def test_groq_provider_rejects_mock_placeholder_key():
    with pytest.raises(ValidationError, match="mock placeholder"):
        Settings(LLM_PROVIDER="groq", LLM_API_KEY="mock-llm-api-key")


def test_groq_provider_rejects_empty_key():
    with pytest.raises(ValidationError, match="real LLM_API_KEY"):
        Settings(LLM_PROVIDER="groq", LLM_API_KEY="")


def test_groq_provider_rejects_malformed_key():
    with pytest.raises(ValidationError, match="does not look like a Groq key"):
        Settings(LLM_PROVIDER="groq", LLM_API_KEY="sk-not-a-groq-key")


def test_groq_provider_accepts_well_formed_key():
    settings = Settings(LLM_PROVIDER="groq", LLM_API_KEY="gsk_realkeyvalue")
    assert settings.LLM_PROVIDER == "groq"
    assert settings.LLM_API_KEY == "gsk_realkeyvalue"
