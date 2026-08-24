# BHOOMI RAG Runtime Isolation & Storage Separation Audit

**Assessment Date:** August 2026  
**Scope:** Verifying physical storage, index memory, caching, and dependency injection isolation between `v4.2.0-validated` (Active Production) and `v4.3.0-candidate` (Canary Candidate).

---

## 1. Storage & Index Isolation Invariant

1. **Physical File Segregation:**
   - Production Knowledge Base: `data/curated/Dataset_v4_validated/`
   - Candidate Knowledge Base: `data/curated/Dataset_v4_3_candidate/`
   - Rollback Knowledge Base: `data/curated/Dataset_v4_1_validated/` (Fall-back operational baseline)

2. **Index Artifact Namespacing:**
   - Production: `rag/indexes/evidence_objects_v4_2_0_validated.json`, `rag/indexes/semantic_chunks_v4_2_0_validated.json`, `rag/indexes/vector_index_v4_2_0_validated.json`
   - Candidate: `rag/indexes/evidence_objects_v4_3_0_candidate.json`, `rag/indexes/semantic_chunks_v4_3_0_candidate.json`, `rag/indexes/vector_index_v4_3_0_candidate.json`

3. **Runtime Zero-Contamination Verification:**
   - Evaluated using `run_candidate_vs_production_eval.py`:
   - Candidate-only objects (`SEV-DIS-005`, `SEV-DIS-006`) are strictly excluded from `v4.2.0-validated` query flows.
   - Contamination count = **0**.
