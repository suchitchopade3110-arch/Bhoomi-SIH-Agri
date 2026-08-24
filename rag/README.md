# BHOOMI Evidence-First Agricultural RAG System

**Version:** 1.0.0-production  
**Target Architecture:** Agricultural Evidence-Grounded Hybrid RAG & Decision Layer  
**Knowledge Baseline (Active Production):** `v4.2.0-validated`  
**Candidate Knowledge Staging:** `v4.3.0-candidate`  
**Rollback Knowledge Baseline:** `v4.1.0-validated`  
**Operating Mode:** Evidence Retrieval, Structured Decisioning & Strict Regulatory Safety Gate  

---

## 1. Core Philosophy: Agricultural Evidence vs Generic Chatbot

Generic RAG systems rely on LLM parameters to synthesize answers from loose semantic chunks. In crop protection and farmer advisory, this creates catastrophic hallucination risks (e.g. recommending restricted chemicals, fabricating economic threshold percentages, cross-crop pesticide transfer, or advising chemical sprays during full flowering).

**BHOOMI RAG strictly separates Retrieval, Decisioning, Safety, and Explanation:**

```
FARMER TAMIL VOICE
        │
        ▼ (ASR / Normalization)
PARSED QUERY CONTEXT (Crop, Stage, Symptoms, Region, Aliases)
        │
        ▼ (Query Expansion with Tamil Lexicon)
HYBRID RETRIEVAL (Dense Vector + BM25 Lexical + Structured Index + Alias Index)
        │
        ▼ (Reciprocal Rank Fusion & Authority Scoring)
AGRONOMIC EVIDENCE RERANKING
        │
        ▼ (Base ETL + Contextual Modifier Resolution)
DIAGNOSTIC & ETL RESOLUTION LAYER
        │
        ▼ (CIBRC Regulatory Check, PHI, Crop Match, Restricted Molecules)
CHEMICAL SAFETY GATE
        │
        ▼ (Structured Decision Contract)
RAG DECISION CONTRACT (Zero-Hallucination Grounded State)
        │
        ▼ (Tamil Response Generation / Multi-lingual Prompt)
EXPLANATION GENERATION & TTS
```

---

## 2. Directory Structure

```
rag/
├── README.md                                # System overview & operational guide
├── architecture/
│   ├── RAG_ARCHITECTURE.md                 # Detailed architecture & dataflow specifications
│   └── RAG_SOURCE_INVENTORY.md             # Complete audit of ingested knowledge sources
├── schema/
│   ├── RAG_EVIDENCE_SCHEMA.json            # Canonical schema for evidence objects & chunks
│   └── RAG_DECISION_CONTRACT.json          # Schema for RAG output passed to generation/TTS
├── ingestion/
│   ├── build_corpus.py                     # Ingestion, parsing, normalization & chunking pipeline
│   └── validate_corpus.py                  # Schema compliance & provenance verification harness
├── query/
│   ├── query_parser.py                     # Query intent, entity, crop, stage & symptom extractor
│   └── query_expander.py                   # Multi-dialect Tamil alias & scientific query expander
├── retrieval/
│   ├── hybrid_retriever.py                 # Hybrid RRF orchestrator across dense, BM25 & structured
│   ├── bm25_retriever.py                   # Lexical Okapi BM25 engine with Tamil unicode tokenization
│   ├── vector_retriever.py                 # Dense vector semantic retrieval engine
│   ├── structured_retriever.py             # Rule, ETL, severity & chemical structured query engine
│   └── reranker.py                         # Agronomic authority & context-aware reranker
├── diagnostic/
│   └── diagnostic_retriever.py             # Multi-turn diagnostic decision tree retriever
├── safety/
│   └── rag_safety_gate.py                  # Hard chemical safety, PHI, crop-isolation & drone gate
├── api/
│   └── rag_api.py                          # High-performance FastAPI retrieval & decision endpoints
├── shadow/
│   ├── shadow_runner.py                    # Shadow RAG evaluation harness against live telemetry
│   └── shadow_comparator.py                # Telemetry delta comparator & regression detector
├── observability/
│   └── RAG_RETRIEVAL_LOG_SCHEMA.json       # Structured observability & telemetry logging schema
├── evaluation/
│   ├── RAG_GOLDEN_SET.jsonl                # 100 verified golden retrieval benchmark queries
│   ├── RAG_ADVERSARIAL_SET.jsonl           # 50 adversarial attack & edge-case test queries
│   └── evaluate_rag.py                     # Automated RAG evaluation benchmark harness
├── indexes/                                # Serialized BM25, vector, and structured indexes
└── reports/
    ├── EMBEDDING_MODEL_SELECTION.md        # Embedding benchmark & architectural selection report
    ├── RAG_INITIAL_VALIDATION_REPORT.md    # Complete RAG validation & metrics scorecard
    ├── RAG_ADVERSARIAL_REPORT.md           # Adversarial stress test & safety leakage report
    └── RAG_SHADOW_EVALUATION_REPORT.md     # 2,000-turn shadow evaluation vs production report
```

---

## 3. Quick Start & Execution

```powershell
# 1. Build and index the knowledge corpus
python -m rag.ingestion.build_corpus --knowledge-version v4.2.0-validated

# 2. Validate corpus integrity & provenance
python -m rag.ingestion.validate_corpus

# 3. Run complete evaluation benchmark
python -m rag.evaluation.evaluate_rag

# 4. Run shadow evaluation harness
python -m rag.shadow.shadow_runner --turns 2000
```
