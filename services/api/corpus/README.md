# Bhoomi Knowledge Corpus

Curated, dated advisory documents for the RAG pipeline (PRD §5.7).

## Corpus structure

Each document file should be JSON with the following shape:

```json
{
  "doc_id": "kb_211",
  "title": "ICAR PoP: Rice — Bacterial Leaf Blight",
  "reviewed_on": "2025-11-02",
  "source": "ICAR Package of Practices for Rice, 2025",
  "crops": ["samba_paddy", "rice"],
  "diseases": ["bacterial_leaf_blight"],
  "chunks": [
    {
      "chunk_id": "kb_211_c1",
      "text": "Bacterial Leaf Blight (BLB) is caused by Xanthomonas oryzae pv. oryzae...",
      "section": "Overview"
    }
  ]
}
```

## Priority slice (demo)

The first corpus slice covers **Samba paddy, Tamil Nadu** — specifically Bacterial Leaf Blight (BLB), which is the showcase disease for the `82 → 68 → 86` walkthrough in PRD §7.4.

Target: 15–20 well-curated BLB documents from ICAR / state agricultural university packages-of-practices and KVK advisories.

## Curator responsibility

- Each document carries a `reviewed_on` date — the date a domain expert last verified its contents.
- Expired or superseded documents must be updated before the next corpus refresh.
- Out-of-scope queries correctly return `retrieved: false` with `reason: no_relevant_source`.

## Phase 3 ingestion

Run `python -m app.services.rag.ingest` to embed and upsert chunks into pgvector.
