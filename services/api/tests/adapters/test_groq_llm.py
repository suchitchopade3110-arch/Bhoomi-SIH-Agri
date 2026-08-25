"""GroqLLMAdapter — verified against a mock HTTP transport, never a live
Groq call (Groq's free-tier daily token cap is easy to burn on a debugging
loop; live verification is a separate, manual step).

Covers: grounding prompt passed unchanged, provider/model tagged on success,
429 raises a distinguishable error, other failures raise instead of
returning canned advisory text, and malformed model output raises rather
than looping the parser.
"""

from functools import partial
import json

import httpx
import pytest

from app.adapters.groq_llm import (
    GroqLLMAdapter,
    LLMGenerationError,
    LLMOutputParseError,
    LLMRateLimitError,
)
from app.domain.rag.prompt import build_grounding_prompt

CHUNKS = [
    {
        "doc_id": "doc-1",
        "title": "Bacterial Leaf Blight",
        "reviewed_on": "2026-01-01",
        "chunk_text": "Apply copper-based bactericide at first sign of water-soaked lesions.",
    }
]
FARM_CONTEXT = {"farm_id": "f_1"}


def _install_transport(monkeypatch, handler):
    transport = httpx.MockTransport(handler)
    monkeypatch.setattr(
        "app.adapters.groq_llm.httpx.AsyncClient",
        partial(httpx.AsyncClient, transport=transport),
    )


async def test_generate_grounded_advisory_sends_grounding_prompt_unchanged(monkeypatch):
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["body"] = json.loads(request.content)
        body = {
            "possible_issue": "Likely bacterial leaf blight",
            "what_to_check": "Check for water-soaked lesions",
            "what_to_avoid": "Do not use unapproved chemicals",
            "what_to_do_next": "Apply copper bactericide",
            "expert_triggers": "If spread continues after treatment",
            "citations": [{"doc_id": "doc-1", "title": "Bacterial Leaf Blight", "reviewed_on": "2026-01-01"}],
        }
        return httpx.Response(200, json={"choices": [{"message": {"content": json.dumps(body)}}]})

    _install_transport(monkeypatch, handler)
    adapter = GroqLLMAdapter(api_key="gsk_test", base_url="https://api.groq.com/openai/v1", model="llama-3.3-70b-versatile")

    result = await adapter.generate_grounded_advisory("why are my leaves yellow", CHUNKS, FARM_CONTEXT)

    expected_prompt = build_grounding_prompt("why are my leaves yellow", CHUNKS, FARM_CONTEXT)
    assert captured["body"]["messages"] == [{"role": "user", "content": expected_prompt}]
    assert captured["body"]["response_format"] == {"type": "json_object"}
    assert result["provider"] == "groq"
    assert result["model"] == "llama-3.3-70b-versatile"
    assert result["possible_issue"] == "Likely bacterial leaf blight"


async def test_429_raises_rate_limit_error_distinct_from_other_failures(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, json={"error": "rate limit exceeded"})

    _install_transport(monkeypatch, handler)
    adapter = GroqLLMAdapter(api_key="gsk_test", base_url="https://api.groq.com/openai/v1", model="llama-3.3-70b-versatile")

    with pytest.raises(LLMRateLimitError):
        await adapter.generate_grounded_advisory("q", CHUNKS, FARM_CONTEXT)


async def test_401_raises_generation_error_not_rate_limit(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"error": "invalid api key"})

    _install_transport(monkeypatch, handler)
    adapter = GroqLLMAdapter(api_key="gsk_bad", base_url="https://api.groq.com/openai/v1", model="llama-3.3-70b-versatile")

    with pytest.raises(LLMGenerationError) as exc_info:
        await adapter.generate_grounded_advisory("q", CHUNKS, FARM_CONTEXT)
    assert not isinstance(exc_info.value, LLMRateLimitError)


async def test_malformed_json_output_raises_parse_error_never_canned_advisory(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"choices": [{"message": {"content": "not valid json"}}]})

    _install_transport(monkeypatch, handler)
    adapter = GroqLLMAdapter(api_key="gsk_test", base_url="https://api.groq.com/openai/v1", model="llama-3.3-70b-versatile")

    with pytest.raises(LLMOutputParseError):
        await adapter.generate_grounded_advisory("q", CHUNKS, FARM_CONTEXT)


async def test_network_error_propagates_never_falls_back(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    _install_transport(monkeypatch, handler)
    adapter = GroqLLMAdapter(api_key="gsk_test", base_url="https://api.groq.com/openai/v1", model="llama-3.3-70b-versatile")

    with pytest.raises(LLMGenerationError):
        await adapter.generate_grounded_advisory("q", CHUNKS, FARM_CONTEXT)
