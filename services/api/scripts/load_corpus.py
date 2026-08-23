"""Corpus loader — reads corpus markdown files, chunks, embeds, and inserts into DB.

Usage:
    python -m scripts.load_corpus --corpus-dir corpus/ --batch-size 32
    python -m scripts.load_corpus --corpus-dir corpus/ --dry-run
"""

from __future__ import annotations

import argparse
import asyncio
import re
import uuid
from datetime import date, datetime
from pathlib import Path

import yaml

from app.utils.chunker import chunk_text


def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and body from a markdown file.

    Returns:
        (metadata_dict, body_text)
    """
    text = filepath.read_text(encoding="utf-8")

    # Match YAML frontmatter delimited by ---
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text

    frontmatter_str = match.group(1)
    body = match.group(2).strip()

    try:
        metadata = yaml.safe_load(frontmatter_str) or {}
    except yaml.YAMLError:
        metadata = {}

    return metadata, body


async def load_corpus(
    corpus_dir: str = "corpus/",
    batch_size: int = 32,
    dry_run: bool = False,
) -> dict:
    """Load corpus documents into the database.

    Args:
        corpus_dir: Path to the corpus directory containing markdown files.
        batch_size: Batch size for embedding (unused in stub mode).
        dry_run: If True, only list what would be loaded without DB writes.

    Returns:
        Summary dict with counts.
    """
    corpus_path = Path(corpus_dir)
    if not corpus_path.exists():
        print(f"Corpus directory not found: {corpus_path}")
        return {"documents": 0, "chunks": 0, "error": "directory not found"}

    md_files = sorted(corpus_path.glob("*.md"))
    # Exclude README.md
    md_files = [f for f in md_files if f.name.lower() != "readme.md"]

    if not md_files:
        print("No markdown files found in corpus directory.")
        return {"documents": 0, "chunks": 0}

    total_docs = 0
    total_chunks = 0

    print(f"Found {len(md_files)} corpus documents in {corpus_path}")
    print()

    for filepath in md_files:
        metadata, body = parse_frontmatter(filepath)

        title = metadata.get("title", filepath.stem)
        source = metadata.get("source", "Unknown")
        curator = metadata.get("curator", "Unknown")
        reviewed_on_str = metadata.get("reviewed_on", str(date.today()))
        lang = metadata.get("lang", "en")

        # Parse reviewed_on date
        if isinstance(reviewed_on_str, date):
            reviewed_on = reviewed_on_str
        else:
            try:
                reviewed_on = datetime.strptime(str(reviewed_on_str), "%Y-%m-%d").date()
            except ValueError:
                reviewed_on = date.today()

        # Chunk the body text
        chunks = chunk_text(body, max_tokens=500, overlap_tokens=50)

        print(f"  [{filepath.name}]")
        print(f"    Title: {title}")
        print(f"    Source: {source}")
        print(f"    Curator: {curator}")
        print(f"    Reviewed: {reviewed_on}")
        print(f"    Chunks: {len(chunks)}")

        total_docs += 1
        total_chunks += len(chunks)

        if dry_run:
            for i, chunk in enumerate(chunks):
                words = len(chunk.split())
                print(f"      Chunk {i}: {words} words — {chunk[:80]}...")
            continue

        # Insert into DB
        from app.adapters.dependencies import get_embedding_adapter
        from app.core.db import AsyncSessionLocal
        from app.models.kb_document import KBDocument
        from app.models.knowledge_chunk import KnowledgeChunk

        embedding_adapter = get_embedding_adapter()
        doc_id = str(uuid.uuid4())

        async with AsyncSessionLocal() as session:
            # Create KBDocument
            kb_doc = KBDocument(
                id=doc_id,
                title=title,
                source=source,
                curator=curator,
                reviewed_on=reviewed_on,
                content=body,
                lang=lang,
            )
            session.add(kb_doc)

            # Embed and create KnowledgeChunks
            for i, chunk_text_content in enumerate(chunks):
                embedding = await embedding_adapter.embed_text(chunk_text_content)
                chunk_id = str(uuid.uuid4())

                kb_chunk = KnowledgeChunk(
                    id=chunk_id,
                    doc_id=doc_id,
                    document_id=doc_id,
                    title=title,
                    reviewed_on=reviewed_on,
                    chunk_index=i,
                    chunk_text=chunk_text_content,
                    embedding=embedding,
                )
                session.add(kb_chunk)

            await session.commit()
            print(f"    [OK] Inserted into DB")

    print()
    print(f"Summary: {total_docs} documents, {total_chunks} chunks")
    if dry_run:
        print("(dry run -- no data was written)")

    return {"documents": total_docs, "chunks": total_chunks}


async def main() -> None:
    parser = argparse.ArgumentParser(description="Load corpus documents into the KB")
    parser.add_argument("--corpus-dir", default="corpus/", help="Path to corpus directory")
    parser.add_argument("--batch-size", type=int, default=32, help="Embedding batch size")
    parser.add_argument("--dry-run", action="store_true", help="List files without DB writes")
    args = parser.parse_args()

    await load_corpus(
        corpus_dir=args.corpus_dir,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    asyncio.run(main())
