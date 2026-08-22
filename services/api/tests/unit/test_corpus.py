"""Corpus and chunker tests — Phase 3 verification."""

import pytest

from app.utils.chunker import chunk_text


class TestChunker:
    """Tests for the text chunking utility."""

    def test_empty_text_returns_empty(self):
        assert chunk_text("") == []
        assert chunk_text("   ") == []

    def test_short_text_single_chunk(self):
        """Text shorter than max_tokens → single chunk."""
        text = "This is a short sentence."
        chunks = chunk_text(text, max_tokens=500)
        assert len(chunks) == 1
        assert chunks[0] == text

    def test_respects_sentence_boundaries(self):
        """Chunks should not split mid-sentence."""
        # Create text with known sentence boundaries
        sentences = [f"Sentence number {i} here." for i in range(50)]
        text = " ".join(sentences)
        chunks = chunk_text(text, max_tokens=100, overlap_tokens=20)

        for chunk in chunks:
            # Each chunk should end with a period (sentence boundary)
            assert chunk.rstrip().endswith(".")

    def test_overlap_carries_context(self):
        """Consecutive chunks should share overlapping content."""
        sentences = [f"This is sentence number {i} about farming." for i in range(30)]
        text = " ".join(sentences)
        chunks = chunk_text(text, max_tokens=100, overlap_tokens=30)

        if len(chunks) > 1:
            # Overlap means some words from chunk N appear in chunk N+1
            chunk0_words = set(chunks[0].split())
            chunk1_words = set(chunks[1].split())
            overlap = chunk0_words & chunk1_words
            # Should have some overlap (at least some common words)
            assert len(overlap) > 0

    def test_paragraph_boundary_handling(self):
        """Paragraphs separated by blank lines are handled correctly."""
        text = "First paragraph here.\n\nSecond paragraph here.\n\nThird paragraph here."
        chunks = chunk_text(text, max_tokens=500)
        assert len(chunks) == 1  # Short enough for one chunk
        assert "First" in chunks[0]
        assert "Third" in chunks[0]

    def test_max_tokens_respected(self):
        """No chunk should exceed max_tokens (approximately)."""
        text = " ".join([f"Word{i}" for i in range(1000)])
        chunks = chunk_text(text, max_tokens=100, overlap_tokens=10)

        for chunk in chunks:
            word_count = len(chunk.split())
            # Approximate: max_tokens=100 → max_words ≈ 77
            # Allow some slack for sentence boundary alignment
            assert word_count < 120, f"Chunk too long: {word_count} words"


class TestCorpusParsing:
    """Tests for corpus YAML frontmatter parsing."""

    def test_parse_frontmatter_basic(self):
        """YAML frontmatter parsing extracts title, source, curator, reviewed_on."""
        from pathlib import Path
        from scripts.load_corpus import parse_frontmatter
        import tempfile

        content = """---
title: "Test Document"
source: "Test Source"
curator: "Tester"
reviewed_on: "2025-01-01"
lang: "en"
---

# Test Content

This is the body text.
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False, encoding="utf-8") as f:
            f.write(content)
            f.flush()
            filepath = Path(f.name)

        metadata, body = parse_frontmatter(filepath)
        assert metadata["title"] == "Test Document"
        assert metadata["source"] == "Test Source"
        assert metadata["curator"] == "Tester"
        assert "Test Content" in body

        # Cleanup
        filepath.unlink()

    def test_corpus_files_exist(self):
        """All 8 corpus files exist in the corpus directory."""
        from pathlib import Path

        corpus_dir = Path(__file__).parent.parent.parent / "corpus"

        expected_files = [
            "rice_blb.md",
            "rice_brown_spot.md",
            "rice_blast.md",
            "rice_irrigation_vegetative.md",
            "rice_irrigation_reproductive.md",
            "rice_harvest_timing.md",
            "rice_nitrogen_management.md",
            "rice_seed_selection.md",
        ]

        for fname in expected_files:
            assert (corpus_dir / fname).exists(), f"Missing corpus file: {fname}"

    def test_corpus_files_have_frontmatter(self):
        """All corpus files have valid YAML frontmatter."""
        from pathlib import Path
        from scripts.load_corpus import parse_frontmatter

        corpus_dir = Path(__file__).parent.parent.parent / "corpus"

        for md_file in corpus_dir.glob("*.md"):
            if md_file.name.lower() == "readme.md":
                continue
            metadata, body = parse_frontmatter(md_file)
            assert "title" in metadata, f"{md_file.name}: missing 'title' in frontmatter"
            assert "source" in metadata, f"{md_file.name}: missing 'source' in frontmatter"
            assert "curator" in metadata, f"{md_file.name}: missing 'curator' in frontmatter"
            assert len(body) > 100, f"{md_file.name}: body too short ({len(body)} chars)"
