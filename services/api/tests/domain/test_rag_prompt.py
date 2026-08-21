"""Unit tests for the grounding prompt builder — pure string assembly, no network."""

from app.domain.rag.constants import FIVE_POINT_FIELDS, INSUFFICIENT_CONTEXT_KEY
from app.domain.rag.prompt import build_grounding_prompt


def test_prompt_instructs_answer_only_from_chunks():
    prompt = build_grounding_prompt("why are my leaves yellow?", [])
    assert "ONLY" in prompt
    assert "never" in prompt.lower()


def test_prompt_names_the_insufficient_context_signal():
    prompt = build_grounding_prompt("q", [])
    assert INSUFFICIENT_CONTEXT_KEY in prompt


def test_prompt_lists_all_five_fields():
    prompt = build_grounding_prompt("q", [])
    for field in FIVE_POINT_FIELDS:
        assert field in prompt


def test_prompt_requires_citations():
    prompt = build_grounding_prompt("q", [])
    assert "citations" in prompt.lower()


def test_prompt_includes_chunk_metadata_and_text():
    chunks = [{"doc_id": "kb_211", "title": "ICAR PoP: BLB", "reviewed_on": "2025-11-02", "chunk_text": "Symptoms include lesions."}]
    prompt = build_grounding_prompt("why are my leaves yellow?", chunks)
    assert "kb_211" in prompt
    assert "ICAR PoP: BLB" in prompt
    assert "2025-11-02" in prompt
    assert "Symptoms include lesions." in prompt
    assert "why are my leaves yellow?" in prompt


def test_prompt_with_no_chunks_says_so_explicitly():
    prompt = build_grounding_prompt("q", [])
    assert "no chunks retrieved" in prompt.lower()


def test_prompt_includes_farm_context_when_provided():
    prompt = build_grounding_prompt("q", [], farm_context={"crop": "samba_paddy"})
    assert "samba_paddy" in prompt


def test_prompt_is_deterministic():
    chunks = [{"doc_id": "kb_1", "title": "T", "reviewed_on": "2025-01-01", "chunk_text": "text"}]
    assert build_grounding_prompt("q", chunks) == build_grounding_prompt("q", chunks)
