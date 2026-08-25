"""Unit tests for EMBEDDING_PROVIDER-driven adapter selection
(adapters/dependencies.get_embedding_adapter) — the wiring that was
previously dead: EMBEDDING_PROVIDER=bge_m3 was accepted by config but
always returned the stub regardless (see README.md §9 history)."""

from app.adapters.embeddings_real import RealEmbeddingAdapter
from app.adapters.stubs import StubEmbeddingAdapter


def test_default_provider_is_stub(monkeypatch):
    monkeypatch.delenv("EMBEDDING_PROVIDER", raising=False)
    from app.core.config import get_settings
    import app.adapters.dependencies as deps_module

    get_settings.cache_clear()
    deps_module.get_embedding_adapter.cache_clear()
    try:
        adapter = deps_module.get_embedding_adapter()
        assert isinstance(adapter, StubEmbeddingAdapter)
    finally:
        get_settings.cache_clear()
        deps_module.get_embedding_adapter.cache_clear()


def test_bge_m3_provider_selects_real_adapter(monkeypatch):
    monkeypatch.setenv("EMBEDDING_PROVIDER", "bge_m3")
    from app.core.config import get_settings
    import app.adapters.dependencies as deps_module

    get_settings.cache_clear()
    deps_module.get_embedding_adapter.cache_clear()
    try:
        adapter = deps_module.get_embedding_adapter()
        assert isinstance(adapter, RealEmbeddingAdapter)
    finally:
        monkeypatch.delenv("EMBEDDING_PROVIDER", raising=False)
        get_settings.cache_clear()
        deps_module.get_embedding_adapter.cache_clear()
