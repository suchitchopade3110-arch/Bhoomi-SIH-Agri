"""Unit tests for parse_advisory_output — the structural "never fabricate" guard."""

from app.domain.rag.advisory import parse_advisory_output

VALID_RAW = {
    "possible_issue": "Early bacterial leaf blight.",
    "what_to_check": "Water-soaked lesions along leaf margins.",
    "what_to_do_next": "Drain the field.",
    "what_to_avoid": "Excess nitrogen.",
    "expert_triggers": "If lesions spread past 25% of leaf area.",
    "citations": [{"doc_id": "kb_211", "title": "ICAR PoP: BLB", "reviewed_on": "2025-11-02"}],
}


def test_valid_output_parses_to_a_populated_advisory():
    result = parse_advisory_output(VALID_RAW)
    assert result.insufficient_context is False
    assert result.advisory is not None
    assert result.advisory.possible_issue == VALID_RAW["possible_issue"]
    assert len(result.citations) == 1
    assert result.citations[0].doc_id == "kb_211"


def test_explicit_insufficient_context_signal_is_honored():
    raw = {"insufficient_context": True, "reason": "chunks don't cover this crop"}
    result = parse_advisory_output(raw)
    assert result.insufficient_context is True
    assert result.advisory is None
    assert result.citations == []
    assert "chunks don't cover" in result.reason


def test_missing_required_field_is_insufficient_context():
    for field in VALID_RAW:
        if field == "citations":
            continue
        raw = {**VALID_RAW}
        del raw[field]
        result = parse_advisory_output(raw)
        assert result.insufficient_context is True, f"missing {field} should be insufficient_context"
        assert result.advisory is None


def test_blank_required_field_is_insufficient_context():
    raw = {**VALID_RAW, "what_to_avoid": "   "}
    result = parse_advisory_output(raw)
    assert result.insufficient_context is True


def test_no_citations_is_insufficient_context():
    raw = {**VALID_RAW, "citations": []}
    result = parse_advisory_output(raw)
    assert result.insufficient_context is True
    assert result.advisory is None


def test_missing_citations_key_is_insufficient_context():
    raw = {k: v for k, v in VALID_RAW.items() if k != "citations"}
    result = parse_advisory_output(raw)
    assert result.insufficient_context is True


def test_citation_missing_required_subfield_is_insufficient_context():
    raw = {**VALID_RAW, "citations": [{"doc_id": "kb_211", "title": "ICAR PoP: BLB"}]}  # no reviewed_on
    result = parse_advisory_output(raw)
    assert result.insufficient_context is True


def test_non_dict_output_is_insufficient_context():
    result = parse_advisory_output("not a dict")  # type: ignore[arg-type]
    assert result.insufficient_context is True


def test_valid_output_always_has_at_least_one_citation():
    result = parse_advisory_output(VALID_RAW)
    assert not result.insufficient_context
    assert len(result.citations) >= 1
