"""Corpus loader — reads corpus markdown files, chunks, embeds, and inserts into DB.

Usage:
    python -m scripts.load_corpus --corpus-dir corpus/
    python -m scripts.load_corpus --corpus-dir ../../data/curated/Dataset_v4_validated/corpus/pests/
    python -m scripts.load_corpus --all
    python -m scripts.load_corpus --corpus-dir corpus/ ../../data/curated/Dataset_v4_validated/corpus/pests/
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import re
import uuid
from datetime import date, datetime
from pathlib import Path

from sqlalchemy import delete
import yaml

from app.utils.chunker import chunk_text

# Canonical deterministic mappings for stable doc_ids across re-ingests
PEST_DOC_MAP: dict[str, str] = {
    "stem_borer": "kb_p301",
    "rice_stem_borer": "kb_p301",
    "brown_planthopper": "kb_p302",
    "rice_brown_planthopper": "kb_p302",
    "leaf_folder": "kb_p303",
    "rice_leaf_folder": "kb_p303",
    "green_leafhopper": "kb_p304",
    "rice_green_leafhopper": "kb_p304",
    "gall_midge": "kb_p305",
    "rice_gall_midge": "kb_p305",
    "thrips": "kb_p306",
    "rice_thrips": "kb_p306",
    "whorl_maggot": "kb_p307",
    "rice_whorl_maggot": "kb_p307",
    "earhead_bug": "kb_p308",
    "rice_earhead_bug": "kb_p308",
}

DISEASE_DOC_MAP: dict[str, str] = {
    "rice_blb": "kb_d101",
    "bacterial_leaf_blight": "kb_d101",
    "rice_bacterial_leaf_blight": "kb_d101",
    "rice_blast": "kb_d102",
    "blast": "kb_d102",
    "rice_brown_spot": "kb_d103",
    "brown_spot": "kb_d103",
    "rice_seed_selection": "kb_d104",
    "rice_irrigation_vegetative": "kb_d105",
    "rice_irrigation_reproductive": "kb_d106",
    "rice_nitrogen_management": "kb_d107",
    "rice_harvest_timing": "kb_d108",
    "rice_sheath_blight": "kb_d109",
    "sheath_blight": "kb_d109",
    "rice_false_smut": "kb_d110",
    "false_smut": "kb_d110",
    "rice_sheath_rot": "kb_d111",
    "sheath_rot": "kb_d111",
    "rice_tungro_virus": "kb_d112",
    "tungro_virus": "kb_d112",
    "rice_bacterial_leaf_streak": "kb_d113",
    "bacterial_leaf_streak": "kb_d113",
}


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


def is_pest_doc(filepath: Path, metadata: dict) -> bool:
    """Same pest/disease namespace test ``derive_doc_id`` uses, exposed on
    its own so callers can also derive ``content_type`` from it (checklist
    §4.1 — every KnowledgeChunk row needs a real content_type/crop, not a
    NULL that silently drops out of scoped retrieval)."""
    return bool(
        metadata.get("target_type") == "pest"
        or metadata.get("category") == "Insect Pest"
        or "pest_name" in metadata
        or "pests" in filepath.parts
    )


def derive_doc_id(filepath: Path, metadata: dict) -> str:
    """Deterministically derive a namespaced doc_id (kb_p<NNN> or kb_d<NNN>).

    Namespace is derived from YAML frontmatter and directory path:
    - Pests -> kb_p301-kb_p308 (or kb_p<NNN>)
    - Diseases/agronomy -> kb_d101-kb_d113 (or kb_d<NNN>)
    """
    if metadata.get("doc_id"):
        return str(metadata["doc_id"])

    stem = filepath.stem.lower()
    is_pest = is_pest_doc(filepath, metadata)

    if is_pest:
        if stem in PEST_DOC_MAP:
            return PEST_DOC_MAP[stem]
        # Deterministic fallback in kb_p310-kb_p999
        offset = (int(hashlib.md5(stem.encode()).hexdigest()[:6], 16) % 690) + 310
        return f"kb_p{offset:03d}"
    else:
        if stem in DISEASE_DOC_MAP:
            return DISEASE_DOC_MAP[stem]
        # Deterministic fallback in kb_d114-kb_d999
        offset = (int(hashlib.md5(stem.encode()).hexdigest()[:6], 16) % 880) + 114
        return f"kb_d{offset:03d}"


async def load_corpus_dir(
    corpus_path: Path,
    batch_size: int = 32,
    dry_run: bool = False,
) -> dict:
    """Load a single corpus directory into the database."""
    if not corpus_path.exists():
        print(f"Corpus directory not found: {corpus_path}")
        return {"documents": 0, "chunks": 0, "error": "directory not found"}

    md_files = sorted(corpus_path.glob("*.md"))
    # Exclude README.md
    md_files = [f for f in md_files if f.name.lower() != "readme.md"]

    if not md_files:
        print(f"No markdown files found in corpus directory: {corpus_path}")
        return {"documents": 0, "chunks": 0}

    total_docs = 0
    total_chunks = 0

    print(f"Found {len(md_files)} corpus documents in {corpus_path}")
    print()

    for filepath in md_files:
        metadata, body = parse_frontmatter(filepath)

        title = (
            metadata.get("title")
            or metadata.get("source_title")
            or metadata.get("pest_name")
            or filepath.stem.replace("_", " ").title()
        )
        source = metadata.get("source") or metadata.get("source_organization", "Unknown")
        curator = metadata.get("curator", "Unknown")
        reviewed_on_str = metadata.get("reviewed_on") or metadata.get("review_date", str(date.today()))
        lang = metadata.get("lang", "en")

        # Parse reviewed_on date
        if isinstance(reviewed_on_str, date):
            reviewed_on = reviewed_on_str
        else:
            try:
                reviewed_on = datetime.strptime(str(reviewed_on_str), "%Y-%m-%d").date()
            except ValueError:
                reviewed_on = date.today()

        doc_id = derive_doc_id(filepath, metadata)

        # Chunk the body text
        chunks = chunk_text(body, max_tokens=500, overlap_tokens=50)

        print(f"  [{filepath.name}] -> {doc_id}")
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
        document_id = str(uuid.uuid4())
        content_type = "pest" if is_pest_doc(filepath, metadata) else "disease"
        crop = metadata.get("crop", "paddy")

        async with AsyncSessionLocal() as session:
            # Idempotency: delete previous chunks for this doc_id before re-inserting
            await session.execute(delete(KnowledgeChunk).where(KnowledgeChunk.doc_id == doc_id))
            await session.execute(delete(KBDocument).where(KBDocument.title == title))

            # Create KBDocument
            kb_doc = KBDocument(
                id=document_id,
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
                    document_id=document_id,
                    title=title,
                    reviewed_on=reviewed_on,
                    chunk_index=i,
                    chunk_text=chunk_text_content,
                    embedding=embedding,
                    content_type=content_type,
                    crop=crop,
                )
                session.add(kb_chunk)

            await session.commit()
            print(f"    [OK] Inserted into DB")

    return {"documents": total_docs, "chunks": total_chunks}


async def load_corpus(
    corpus_dirs: list[str] | str = "corpus/",
    batch_size: int = 32,
    dry_run: bool = False,
) -> dict:
    """Load corpus documents from one or more directories into the database."""
    if isinstance(corpus_dirs, str):
        dirs = [corpus_dirs]
    else:
        dirs = corpus_dirs

    grand_total_docs = 0
    grand_total_chunks = 0

    for d in dirs:
        res = await load_corpus_dir(Path(d), batch_size=batch_size, dry_run=dry_run)
        grand_total_docs += res.get("documents", 0)
        grand_total_chunks += res.get("chunks", 0)

    print()
    print(f"Summary: {grand_total_docs} documents, {grand_total_chunks} chunks")
    if dry_run:
        print("(dry run -- no data was written)")

    return {"documents": grand_total_docs, "chunks": grand_total_chunks}


async def main() -> None:
    parser = argparse.ArgumentParser(description="Load corpus documents into the KB")
    parser.add_argument(
        "--corpus-dir",
        nargs="*",
        default=None,
        help="One or more paths to corpus directories",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Load both disease/agronomy corpus and pest corpus in one command",
    )
    parser.add_argument("--batch-size", type=int, default=32, help="Embedding batch size")
    parser.add_argument("--dry-run", action="store_true", help="List files without DB writes")
    args = parser.parse_args()

    # Resolve directories
    dirs: list[str] = []
    if args.all:
        dirs = [
            "corpus/",
            "../../data/curated/Dataset_v4_validated/corpus/pests/",
        ]
    elif args.corpus_dir:
        dirs = args.corpus_dir
    else:
        dirs = ["corpus/"]

    await load_corpus(
        corpus_dirs=dirs,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    asyncio.run(main())
