# BHOOMI RAG System Implementation Audit

**Document:** `RAG_IMPLEMENTATION_AUDIT.md`  
**Audit Date:** August 2026  
**Audited Baseline:** `rag/v1-evidence-retrieval` against Active Production `v4.2.0-validated`  
**Candidate Knowledge:** `v4.3.0-candidate`  
**Auditor Role:** Lead RAG Architect, Agricultural Knowledge Engineer & Safety Lead  

---

## 1. Executive Summary

This audit evaluates the BHOOMI Evidence-First Agricultural Retrieval-Augmented Generation (RAG) subsystem. BHOOMI provides voice-first agricultural decision support to Tamil Nadu paddy farmers. In crop advisory, unconstrained LLM generative responses create life-threatening, crop-destroying, and regulatory risks (e.g., advising restricted molecules like Carbofuran, miscalculating pre-harvest intervals, transferring paddy pesticide dosages to horticultural crops, or spraying during anthesis).

The BHOOMI RAG architecture decouples **Query Understanding**, **Hybrid Evidence Retrieval**, **Source Conflict Resolution**, **Independent Safety Gating**, and **Structured Decision Contract Generation**.

This audit identifies:
1. Architectural compliance and component inventory.
2. A critical evaluation reporting bug in top-K recall computation.
3. Indexing and provenance isolation status across `v4.2.0-validated` and `v4.3.0-candidate`.
4. Known technical debt, security and safety boundaries, and deployment risks.

---

## 2. Component Inventory

| Component Path | Class / Module | Purpose | Status |
|---|---|---|---|
| `rag/schema/RAG_EVIDENCE_SCHEMA.json` | JSON Schema | Schema for canonical evidence objects and semantic chunks | Compliant |
| `rag/schema/RAG_DECISION_CONTRACT.json` | JSON Schema | Schema for downstream response policy contract | Needs 8-state expansion |
| `rag/ingestion/build_corpus.py` | `CorpusBuilder` | Markdown, ETL, Severity, Chemical, Tree parser & chunker | Operational |
| `rag/ingestion/validate_corpus.py` | Validation Harness | Verifies schema compliance and provenance chains | Operational |
| `rag/query/query_parser.py` | `QueryParser` | Extracts crop, stage, intent, symptoms, chemicals | Operational |
| `rag/query/query_expander.py` | `QueryExpander` | Expands Tamil aliases, Latin binomials, preserves ambiguity | Operational |
| `rag/retrieval/bm25_retriever.py` | `BM25Retriever` | Okapi BM25 with Tamil unicode tokenization | Operational |
| `rag/retrieval/vector_retriever.py` | `DenseVectorRetriever` | Semantic hash embedding projection & cosine similarity | Operational |
| `rag/retrieval/structured_retriever.py` | `StructuredRetriever` | Exact index filtering for ETL, chemicals, SES tiers | Needs input ID fix |
| `rag/retrieval/reranker.py` | `AgronomicReranker` | Authority weighting ($10 \rightarrow 1.0, 9 \rightarrow 0.95, 8 \rightarrow 0.90$) | Operational |
| `rag/retrieval/conflict_resolver.py` | `SourceConflictResolver` | Resolves conflicting agricultural sources by authority tier | To be implemented |
| `rag/diagnostic/diagnostic_retriever.py` | `DiagnosticRetriever` | Differential decision trees (Zinc vs Brown Spot) | Operational |
| `rag/safety/rag_safety_gate.py` | `RagSafetyGate` | Independent CIBRC, PHI, Anthesis, Crop-Isolation gate | Needs decoupled architecture |
| `rag/api/rag_api.py` | `BhoomiRagEngine` | Core orchestration and Decision Contract assembler | Operational |
| `rag/shadow/shadow_runner.py` | `ShadowRunner` | Real-time / offline telemetry replay and shadow comparator | Operational |
| `rag/evaluation/evaluate_rag.py` | Benchmark Suite | 100 Golden + 50 Adversarial benchmark runner | Reporting bug identified |

---

## 3. Actual vs Documented Architecture

### Documented Architecture
The documented system presents a clean sequential pipeline:
Farmer Tamil Voice $\rightarrow$ ASR $\rightarrow$ Context Extraction $\rightarrow$ Tamil Expansion $\rightarrow$ Hybrid Retrieval $\rightarrow$ RRF $\rightarrow$ Agronomic Reranking $\rightarrow$ Diagnostic/ETL Resolution $\rightarrow$ Chemical Safety Gate $\rightarrow$ Structured Contract $\rightarrow$ TTS.

### Actual Audit Findings
1. **Safety Engine Placement**: In `rag_api.py`, safety checks were performed on parsed context before advisory assembly, but some safety-critical cases were coupled to whether retrieval returned results. Safety must be an **Independent Safety Policy Engine** running deterministically on decision candidates.
2. **Decision Contract States**: The schema only defined a small set of states (`DIRECT_ADVISORY`, `CONDITIONAL_ADVISORY`, `ASK_CLARIFYING_QUESTION`, `SAFETY_INTERVENTION_WARNING`, `REJECT_CROP_MISMATCH`, `SAFETY_REJECTION_MRL_HAZARD`, `ESCALATE_TO_KVK_OFFICER`). It lacked formal states for `INSUFFICIENT_EVIDENCE`, `EVIDENCE_CONFLICT`, `SAFETY_BLOCKED`, and `OUT_OF_SCOPE`.
3. **Source Conflict Resolution**: When multiple sources (e.g. CIBRC vs TNAU vs ICAR) provided varying recommendations, the system relied purely on RRF and heuristic multipliers rather than a dedicated, deterministic `SourceConflictResolver`.

---

## 4. Dependencies & Data Flow

### Upstream & Downstream Boundaries
- **Upstream**: Voice ASR & Dialect Normalizer (`services/api/app/ports/asr_tts.py`).
- **Downstream**: Structured Decision Contract consumed by Response Policy Engine $\rightarrow$ Multilingual Prompt Template $\rightarrow$ TTS.
- **Data Persistence**: Indexes serialized to `rag/indexes/` (JSON formats for zero external vector DB dependencies during development/staging, compatible with pgvector in production).

### Layered Flow
```
Farmer Query (Voice/Text)
       │
       ▼
QueryParser + QueryExpander (Preserves ambiguity)
       │
       ▼
Hybrid Retrieval: BM25 (0.35) + Dense Vector (0.35) + Structured (0.30)
       │
       ▼
Reciprocal Rank Fusion (k=60)
       │
       ▼
Agronomic Reranker (Authority 10->1.0, 9->0.95, 8->0.90)
       │
       ▼
Evidence Grounding & Source Conflict Resolver
       │
       ▼
Independent Safety Policy Engine (Deterministic Invariants)
       │
       ▼
RAG Decision Contract
```

---

## 5. Index Generation & Reproducibility Status

- **Source Corpus**: 16 authoritative markdown documents in `data/curated/Dataset_v4_validated/corpus/` + normalized evidence tables.
- **Index Files**:
  - `rag/indexes/evidence_objects_v4_2_0_validated.json` (59 canonical objects)
  - `rag/indexes/semantic_chunks_v4_2_0_validated.json` (118 semantic chunks)
  - `rag/indexes/vector_index_v4_2_0_validated.json` (128-dim dense semantic hash embeddings)
  - `rag/indexes/evidence_objects_v4_3_0_candidate.json` (64 canonical objects)
  - `rag/indexes/semantic_chunks_v4_3_0_candidate.json` (130 semantic chunks)
- **Determinism**: Chunking and hash embeddings are 100% deterministic with zero floating random seeds.

---

## 6. Technical Debt, Risks & Weaknesses

### 1. Evaluation Metric Flaw
- Conflation of entity matching with top-K evidence chunk retrieval in `evaluate_rag.py`.
- Hardcoded table pass status in generated markdown report.
- Lack of Evidence Grounding Accuracy metrics (Claim-to-evidence support, Citation completeness).

### 2. ASR Error Coupling
- Benchmark previously evaluated only clean transcripts. A voice-first advisory platform requires separate clean vs noisy ASR evaluation to measure degradation across dialects.

### 3. Ambiguous Vocabulary Protection
- *மட்ட பூச்சி* is successfully quarantined in `QueryExpander`, but needs explicit confirmation that zero candidate promote attempts bypass this quarantine.

### 4. Concurrency & Contamination
- Need automated concurrency stress testing (up to 100 concurrent workers) to ensure zero state mutation and zero cross-request evidence contamination.
- Need strict candidate-vs-production contamination tests ensuring `v4.3` candidate knowledge never leaks into `v4.2` production execution.

---

## 7. Audit Conclusion & Roadmap

The existing RAG core provides a solid foundation. With the evaluation bug remediation, source conflict resolution, independent safety policy enforcement, 500-case Tamil voice benchmark, 1,000-case real-world replay, concurrency testing, and 5,000-turn shadow evaluation, the system will achieve verifiable canary readiness.
