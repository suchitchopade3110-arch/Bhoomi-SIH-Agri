"""The grounding prompt (PRD §5.7, §5.8; tech stack §1.3): a pure string
template. Building it here — rather than inline in an LLM adapter — means
the exact instructions a real LLMPort implementation would send are
inspectable and unit-testable without a network call.
"""

from typing import Any

from app.domain.rag.constants import FIVE_POINT_FIELDS, INSUFFICIENT_CONTEXT_KEY

SYSTEM_GROUNDING_INSTRUCTIONS = f"""You are an agricultural advisory assistant. You must answer ONLY using \
the retrieved context chunks provided below — never from general knowledge, \
never by guessing. This is a hard rule: a wrong answer here can cause real \
crop loss.

If the retrieved chunks do not contain enough information to confidently \
answer the query, do NOT improvise or generalize. Instead, respond with \
exactly: {{"{INSUFFICIENT_CONTEXT_KEY}": true, "reason": "<why the chunks don't support an answer>"}}

Otherwise, respond with a JSON object containing exactly these five fields, \
each a plain-language string grounded strictly in the retrieved chunks:
{chr(10).join(f"- {field}" for field in FIVE_POINT_FIELDS)}

Every claim must be traceable to a retrieved chunk. Include a "citations" \
field: a list of objects, one per chunk you actually drew from, each with \
"doc_id", "title", and "reviewed_on" copied verbatim from that chunk's \
metadata below. Never cite a chunk you did not use. Never emit an answer \
with zero citations — if you have nothing to cite, use the \
insufficient_context response instead."""


def build_grounding_prompt(
    query: str,
    chunks: list[dict[str, Any]],
    farm_context: dict[str, Any] | None = None,
) -> str:
    """Assemble the full grounding prompt sent to an LLMPort implementation.

    Args:
        query: The farmer's question (or a diagnosis-derived query string).
        chunks: Retrieved context chunks, each with ``doc_id``, ``title``,
            ``reviewed_on``, and ``chunk_text``. Pass ``[]`` for a query the
            gate has already decided to escalate before calling the LLM —
            callers should generally not reach this function with no chunks.
        farm_context: Optional extra context (crop, growth stage, etc.) to
            help the model interpret the query; never a substitute for the
            retrieved chunks themselves.

    Returns:
        The complete prompt string, ready to send to an LLMPort.
    """
    context_block = "\n\n".join(
        f"[Chunk {i + 1}] doc_id={c['doc_id']} title=\"{c['title']}\" reviewed_on={c['reviewed_on']}\n{c['chunk_text']}"
        for i, c in enumerate(chunks)
    ) or "(no chunks retrieved)"

    farm_block = ""
    if farm_context:
        farm_block = "\n\nFarm context:\n" + "\n".join(f"- {k}: {v}" for k, v in farm_context.items())

    return (
        f"{SYSTEM_GROUNDING_INSTRUCTIONS}\n\n"
        f"Retrieved context:\n{context_block}"
        f"{farm_block}\n\n"
        f"Farmer's query: {query}"
    )
