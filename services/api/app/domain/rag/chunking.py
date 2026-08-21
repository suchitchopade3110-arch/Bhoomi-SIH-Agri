"""Pure text chunker for corpus ingestion. No I/O — takes a string, returns strings."""

from app.domain.rag.constants import CHUNK_MAX_CHARS, CHUNK_OVERLAP_CHARS


def chunk_text(
    text: str,
    max_chars: int = CHUNK_MAX_CHARS,
    overlap_chars: int = CHUNK_OVERLAP_CHARS,
) -> list[str]:
    """Split ``text`` into overlapping, paragraph-aware chunks.

    Paragraphs (blank-line-separated) are packed greedily into chunks up to
    ``max_chars``; a paragraph longer than ``max_chars`` on its own is
    hard-split. Consecutive chunks share ``overlap_chars`` of trailing/
    leading text so a fact split across a chunk boundary isn't lost to
    retrieval. Deterministic: same text in, same chunks out, always.

    Args:
        text: The document body to chunk.
        max_chars: Soft maximum characters per chunk.
        overlap_chars: Characters of overlap carried from the end of one
            chunk into the start of the next.

    Returns:
        A list of chunk strings, in document order. Empty input yields an
        empty list — never a list containing an empty string.
    """
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}" if current else paragraph

        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
            carry = current[-overlap_chars:] if overlap_chars else ""
            current = f"{carry}\n\n{paragraph}".strip() if carry else paragraph
        else:
            current = paragraph

        # A single paragraph longer than max_chars is hard-split on its own.
        while len(current) > max_chars:
            chunks.append(current[:max_chars])
            current = current[max_chars - overlap_chars :] if overlap_chars else current[max_chars:]

    if current:
        chunks.append(current)

    return chunks
