"""Text chunking utility for the RAG corpus (Phase 3).

Splits text into chunks for embedding storage. Prefers paragraph boundaries,
then sentence boundaries. Never splits mid-sentence.
"""

from __future__ import annotations

import re


def chunk_text(
    text: str,
    max_tokens: int = 500,
    overlap_tokens: int = 50,
) -> list[str]:
    """Split text into overlapping chunks for embedding.

    Args:
        text: The input text to chunk.
        max_tokens: Maximum tokens per chunk (approximated as words × 1.3).
        overlap_tokens: Token overlap between consecutive chunks.

    Returns:
        List of text chunks, each ≤ max_tokens.
    """
    if not text.strip():
        return []

    # Approximate max words from max tokens (tokens ≈ words × 1.3)
    max_words = int(max_tokens / 1.3)
    overlap_words = int(overlap_tokens / 1.3)

    # Split into paragraphs first
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]

    # Split each paragraph into sentences
    sentences: list[str] = []
    for para in paragraphs:
        # Split on sentence boundaries: ., !, ? followed by space or end
        para_sents = re.split(r"(?<=[.!?])\s+", para)
        sentences.extend(s.strip() for s in para_sents if s.strip())

    if not sentences:
        return [text.strip()]

    chunks: list[str] = []
    current_sentences: list[str] = []
    current_word_count = 0

    for sentence in sentences:
        sentence_words = len(sentence.split())

        # If a single sentence exceeds max, break it down by word count
        if sentence_words > max_words:
            # Flush current buffer
            if current_sentences:
                chunks.append(" ".join(current_sentences))
                current_sentences = []
                current_word_count = 0

            words = sentence.split()
            step = max(1, max_words - overlap_words)
            for i in range(0, len(words), step):
                chunk_slice = words[i : i + max_words]
                if chunk_slice:
                    chunks.append(" ".join(chunk_slice))
                if i + max_words >= len(words):
                    break
            continue

        # Check if adding this sentence would exceed the limit
        if current_word_count + sentence_words > max_words and current_sentences:
            # Flush current buffer as a chunk
            chunks.append(" ".join(current_sentences))

            # Overlap: carry over the last few sentences
            overlap_sents: list[str] = []
            overlap_count = 0
            for s in reversed(current_sentences):
                s_words = len(s.split())
                if overlap_count + s_words > overlap_words:
                    break
                overlap_sents.insert(0, s)
                overlap_count += s_words

            current_sentences = overlap_sents
            current_word_count = overlap_count

        current_sentences.append(sentence)
        current_word_count += sentence_words

    # Flush remaining
    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks
