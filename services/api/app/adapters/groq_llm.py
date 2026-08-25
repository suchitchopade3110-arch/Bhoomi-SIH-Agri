"""Real ``LLMPort`` adapter — Groq's OpenAI-compatible chat completions API
(``LLM_PROVIDER=groq``).

No fallback-to-canned-text anywhere in this module: every failure mode
(network error, non-2xx status, malformed JSON body) raises instead of
returning fabricated advisory text. ``AdvisoryService``/``parse_advisory_output``
never see a canned response from this adapter — either they see a real
model output, or they see an exception (contract: no-fabrication rule).

The grounding prompt (``app.domain.rag.prompt.build_grounding_prompt``) is
sent verbatim as a single user message — this adapter does not rewrite,
shorten, or otherwise "adapt" it for Llama.
"""

from __future__ import annotations

import json
import logging
from typing import Any

import httpx

from app.domain.rag.prompt import build_grounding_prompt

logger = logging.getLogger("bhoomi.llm.groq")

CHAT_COMPLETIONS_PATH = "/chat/completions"
REQUEST_TIMEOUT_SECONDS = 30.0


class LLMGenerationError(Exception):
    """A Groq generation call failed. Callers must propagate this — never
    substitute advisory text the model did not produce."""


class LLMRateLimitError(LLMGenerationError):
    """Groq rate-limited the request (HTTP 429) — distinct from every other
    failure so it's identifiable in logs during rehearsal."""


class LLMOutputParseError(LLMGenerationError):
    """The model's response body wasn't valid JSON (or wasn't a JSON object)."""


class GroqLLMAdapter:
    """Calls Groq's OpenAI-compatible ``/chat/completions`` endpoint."""

    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._model = model

    async def generate_grounded_advisory(
        self,
        query: str,
        context_chunks: list[dict[str, Any]],
        farm_context: dict[str, Any],
    ) -> dict[str, Any]:
        prompt = build_grounding_prompt(query, context_chunks, farm_context)
        content = await self._chat(prompt, json_mode=True)

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise LLMOutputParseError(
                f"Groq response was not valid JSON: {content[:500]!r}"
            ) from exc
        if not isinstance(parsed, dict):
            raise LLMOutputParseError(
                f"Groq response JSON was not an object: {content[:500]!r}"
            )

        parsed.setdefault("provider", "groq")
        parsed.setdefault("model", self._model)
        return parsed

    async def synthesize_case_summary(
        self,
        farm_data: dict[str, Any],
        events: list[dict[str, Any]],
        health_history: list[dict[str, Any]],
    ) -> str:
        prompt = (
            "Summarize this farm case in 2-3 plain-language sentences for an "
            "agronomist reviewing an escalation. Do not invent facts not present "
            "below.\n\n"
            f"Farm data: {json.dumps(farm_data)}\n"
            f"Recent events: {json.dumps(events)}\n"
            f"Health history: {json.dumps(health_history)}"
        )
        return await self._chat(prompt, json_mode=False)

    async def _chat(self, prompt: str, *, json_mode: bool) -> str:
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload: dict[str, Any] = {
            "model": self._model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            try:
                response = await client.post(
                    f"{self._base_url}{CHAT_COMPLETIONS_PATH}", json=payload, headers=headers
                )
            except httpx.HTTPError as exc:
                logger.error("Groq request failed (network/transport error): %s", exc)
                raise LLMGenerationError(f"Groq request failed: {exc}") from exc

        if response.status_code == 429:
            logger.error("Groq rate limit hit (HTTP 429): %s", response.text[:500])
            raise LLMRateLimitError(f"Groq rate-limited the request (HTTP 429): {response.text[:500]}")

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error("Groq call failed (HTTP %s): %s", response.status_code, response.text[:500])
            raise LLMGenerationError(
                f"Groq call failed (HTTP {response.status_code}): {response.text[:500]}"
            ) from exc

        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMOutputParseError(
                f"Groq response missing choices[0].message.content: {data}"
            ) from exc


__all__ = ["GroqLLMAdapter", "LLMGenerationError", "LLMRateLimitError", "LLMOutputParseError"]
