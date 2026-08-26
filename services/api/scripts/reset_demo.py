"""One-command demo reset script (Phase 4).

Re-seeds the demo database and re-loads the curated knowledge base corpus.

Usage:
    python -m scripts.reset_demo
"""

import asyncio
from scripts.seed_demo import seed_demo
from scripts.load_corpus import load_corpus
from scripts.seed_full_demo import seed_stage


async def reset():
    print("==================================================")
    print("  Bhoomi SIH25076 — One-Command Demo Reset")
    print("==================================================")

    print("\n1. Seeding demo users, farm, and cadastral record...")
    await seed_demo()

    print("\n2. Loading 8 ICAR/TNAU curated corpus documents into pgvector...")
    await load_corpus(corpus_dirs=["corpus/"], dry_run=False)

    print("\n3. Seeding full stage history (82 -> 68 -> 59 -> 86)...")
    await seed_stage("full")

    print("\n==================================================")
    print("  ✓ Demo Reset Complete & Ready for Presentation!")
    print("==================================================")


if __name__ == "__main__":
    asyncio.run(reset())
