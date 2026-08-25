# BHOOMI RAG Architecture: Deterministic Index Build Specification

**Knowledge Base Versions:**
- Production: `v4.2.0-validated`
- Staging Candidate: `v4.3.0-candidate`
- Rollback: `v4.1.0-validated`

---

## 1. Deterministic Build Procedure

The build process ingests curated ICAR/TNAU markdown knowledge documents, CSV lexicons, and normalized JSONL tables into canonical JSON indexes without floating-point drift or network dependency.

```powershell
# Build active production index
& "d:\Project\BHOOMI\services\api\.venv\Scripts\python.exe" -m rag.ingestion.build_corpus --knowledge-version v4.2.0-validated

# Build shadow candidate index
& "d:\Project\BHOOMI\services\api\.venv\Scripts\python.exe" -m rag.ingestion.build_corpus --knowledge-version v4.3.0-candidate
```

---

## 2. Generated Artifact Specifications

| Output File | Format | Schema | Description |
|---|---|---|---|
| `evidence_objects_v4_2_0_validated.json` | JSON Array | `RAG_EVIDENCE_SCHEMA.json` | 65 Canonical Evidence Objects |
| `semantic_chunks_v4_2_0_validated.json` | JSON Array | `RAG_EVIDENCE_SCHEMA.json` | 140 Context-Preserving Semantic Chunks |
| `vector_index_v4_2_0_validated.json` | JSON Array (Floats) | 256-dim Dense Array | 140 Dense Multi-Hash Projections |
| `evidence_objects_v4_3_0_candidate.json` | JSON Array | `RAG_EVIDENCE_SCHEMA.json` | 68 Candidate Evidence Objects |
| `semantic_chunks_v4_3_0_candidate.json` | JSON Array | `RAG_EVIDENCE_SCHEMA.json` | 151 Candidate Semantic Chunks |
| `vector_index_v4_3_0_candidate.json` | JSON Array (Floats) | 256-dim Dense Array | 151 Dense Multi-Hash Projections |

---

## 3. Cryptographic Build Invariant

Rebuilding the indexes from unchanged source files yields identical SHA-256 digests. Two builds on different machines produce identical token dictionaries, term frequencies, and vector embeddings.
