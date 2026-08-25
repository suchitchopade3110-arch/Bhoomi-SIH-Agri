"""Domain result types for the grounded advisory, and the pure parser that
turns a raw LLMPort dict into one of them.

"Never fabricate" is enforced here, structurally: ``parse_advisory_output``
can only return a populated ``FivePointAdvisory`` with citations attached
when every one of the five fields is present and at least one citation with
all required fields is present. Anything short of that — a missing field, an
empty citation list, or the model's own insufficient-context signal —
collapses to the same ``insufficient_context=True`` result, which callers
must treat as "escalate," never as "compose with gaps."
"""

from dataclasses import dataclass, field
from typing import Any

from app.domain.rag.constants import FIVE_POINT_FIELDS, INSUFFICIENT_CONTEXT_KEY, REQUIRED_CITATION_FIELDS


@dataclass(frozen=True)
class FivePointAdvisory:
    """The fixed 5-point structure (PRD §5.8). Citations travel alongside
    this, not inside it — see ``ParsedAdvisoryResult``. ``what_to_avoid`` is
    declared first — never-cut, meant to be the loudest/first point a farmer
    hears or reads (SIH26131 feature checklist §4)."""

    what_to_avoid: str
    possible_issue: str
    what_to_check: str
    what_to_do_next: str
    expert_triggers: str


@dataclass(frozen=True)
class GroundedCitation:
    """One source citation (contract §2.10/§2.11): ``doc_id``, ``title``,
    ``reviewed_on`` — copied verbatim from the retrieved chunk's metadata."""

    doc_id: str
    title: str
    reviewed_on: str


@dataclass(frozen=True)
class ParsedAdvisoryResult:
    """Result of parsing/validating a raw LLMPort response.

    Exactly one of two states: a populated ``advisory`` + non-empty
    ``citations`` (``insufficient_context=False``), or
    ``insufficient_context=True`` with everything else empty/``None``.
    """

    advisory: FivePointAdvisory | None
    citations: list[GroundedCitation] = field(default_factory=list)
    insufficient_context: bool = False
    reason: str | None = None


def _insufficient(reason: str) -> ParsedAdvisoryResult:
    return ParsedAdvisoryResult(advisory=None, citations=[], insufficient_context=True, reason=reason)


def parse_advisory_output(raw: dict[str, Any]) -> ParsedAdvisoryResult:
    """Validate and parse a raw LLMPort response into a ``ParsedAdvisoryResult``.

    Treats each of the following as "insufficient context" — i.e. the
    no-fabrication escalation branch, never a partial answer:
        - The model explicitly signaled ``insufficient_context: true``.
        - Any of the five required fields is missing, not a string, or blank.
        - ``citations`` is missing, empty, or any entry is missing a
          required field (``doc_id``, ``title``, ``reviewed_on``).

    Args:
        raw: The dict returned by ``LLMPort.generate_grounded_advisory``.

    Returns:
        A ``ParsedAdvisoryResult``.
    """
    if not isinstance(raw, dict):
        return _insufficient("LLM output was not a JSON object")

    if raw.get(INSUFFICIENT_CONTEXT_KEY):
        return _insufficient(str(raw.get("reason", "model signaled insufficient context")))

    missing_fields = [f for f in FIVE_POINT_FIELDS if not isinstance(raw.get(f), str) or not raw.get(f).strip()]
    if missing_fields:
        return _insufficient(f"missing or empty required field(s): {', '.join(missing_fields)}")

    raw_citations = raw.get("citations")
    if not isinstance(raw_citations, list) or len(raw_citations) == 0:
        return _insufficient("no citations provided — an ungrounded answer is never returned")

    citations: list[GroundedCitation] = []
    for entry in raw_citations:
        if not isinstance(entry, dict) or any(
            not isinstance(entry.get(f), str) or not entry.get(f).strip() for f in REQUIRED_CITATION_FIELDS
        ):
            return _insufficient("a citation was missing doc_id/title/reviewed_on")
        citations.append(
            GroundedCitation(doc_id=entry["doc_id"], title=entry["title"], reviewed_on=entry["reviewed_on"])
        )

    advisory = FivePointAdvisory(**{f: raw[f].strip() for f in FIVE_POINT_FIELDS})
    return ParsedAdvisoryResult(advisory=advisory, citations=citations, insufficient_context=False, reason=None)
