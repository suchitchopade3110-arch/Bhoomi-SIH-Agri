"""Unit tests for the pure corpus chunker."""

from app.domain.rag.chunking import chunk_text


def test_empty_text_yields_no_chunks():
    assert chunk_text("") == []
    assert chunk_text("   \n\n  ") == []


def test_short_text_is_a_single_chunk():
    text = "Bacterial leaf blight affects paddy."
    chunks = chunk_text(text, max_chars=600)
    assert chunks == [text]


def test_long_text_is_split_into_multiple_chunks():
    paragraph = "BLB symptom description. " * 60  # well over max_chars
    text = f"{paragraph}\n\n{paragraph}\n\n{paragraph}"
    chunks = chunk_text(text, max_chars=200, overlap_chars=20)
    assert len(chunks) > 1
    assert all(len(c) <= 200 + 20 for c in chunks)  # allow overlap slack from paragraph packing


def test_chunking_is_deterministic():
    text = "Paragraph one.\n\nParagraph two.\n\nParagraph three, somewhat longer than the others."
    assert chunk_text(text) == chunk_text(text)


def test_consecutive_chunks_overlap():
    paragraph = "X" * 500
    text = f"{paragraph}\n\n{'Y' * 500}"
    chunks = chunk_text(text, max_chars=400, overlap_chars=50)
    assert len(chunks) >= 2
    # The tail of one chunk should reappear at the head of the next.
    tail = chunks[0][-50:]
    assert tail in chunks[1]


def test_no_chunk_is_empty_string():
    text = "A.\n\n\n\nB."
    for c in chunk_text(text):
        assert c.strip() != ""
