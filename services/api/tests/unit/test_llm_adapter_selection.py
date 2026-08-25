"""Unit tests for LLM_PROVIDER-driven adapter selection
(adapters/dependencies.get_llm_adapter) — previously dead wiring:
get_llm_adapter() returned StubLLMAdapter() unconditionally regardless of
any setting (see the LLM adapter audit)."""

from app.adapters.groq_llm import GroqLLMAdapter
from app.adapters.stubs import StubLLMAdapter


def test_default_provider_is_stub(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "stub")
    from app.core.config import get_settings
    import app.adapters.dependencies as deps_module

    get_settings.cache_clear()
    deps_module.get_llm_adapter.cache_clear()
    try:
        adapter = deps_module.get_llm_adapter()
        assert isinstance(adapter, StubLLMAdapter)
    finally:
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        get_settings.cache_clear()
        deps_module.get_llm_adapter.cache_clear()


def test_groq_provider_selects_real_adapter(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "groq")
    monkeypatch.setenv("LLM_API_KEY", "gsk_realkeyvalue")
    from app.core.config import get_settings
    import app.adapters.dependencies as deps_module

    get_settings.cache_clear()
    deps_module.get_llm_adapter.cache_clear()
    try:
        adapter = deps_module.get_llm_adapter()
        assert isinstance(adapter, GroqLLMAdapter)
    finally:
        monkeypatch.delenv("LLM_PROVIDER", raising=False)
        monkeypatch.delenv("LLM_API_KEY", raising=False)
        get_settings.cache_clear()
        deps_module.get_llm_adapter.cache_clear()
