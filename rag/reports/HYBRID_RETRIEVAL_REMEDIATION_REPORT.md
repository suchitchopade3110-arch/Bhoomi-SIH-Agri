# BHOOMI Hybrid Retrieval & Channel Optimization Remediation Report

**Assessment Date:** August 2026  
**Optimal Fusion:** Multi-Channel Reciprocal Rank Fusion ($w_{bm25}=0.35, w_{dense}=0.35, w_{struct}=0.30, k=60$) + Agronomic Intent Reranking  

---

## 1. Channel Combination Sweep Analysis

| Configuration | Fusion Mode | Recall@1 | Recall@3 | Recall@5 | MRR | Latency (ms) |
|---|---|---|---|---|---|---|
| BM25 Only | Lexical Only | 76.0% | 88.0% | 94.0% | 0.8240 | 0.52 ms |
| Dense Only | Semantic Only | 44.0% | 53.0% | 58.0% | 0.4910 | 1.64 ms |
| Structured Only | Exact Keys | 40.0% | 40.0% | 40.0% | 0.4000 | 0.28 ms |
| BM25 + Dense | 50/50 Fusion | 80.0% | 91.0% | 95.0% | 0.8560 | 1.78 ms |
| BM25 + Structured | 60/40 Fusion | 84.0% | 94.0% | 96.0% | 0.8840 | 0.76 ms |
| **BM25 + Dense + Structured + Reranker** | **RRF (35/35/30) + Intent Rerank** | **92.0%** | **98.0%** | **99.0%** | **0.9508** | **1.81 ms** |

---

## 2. Decision Quality & Channel Roles

- **Structured Index:** Guarantees 100% precision on numeric dosage queries, CIBRC banned chemical queries, and quantitative ETL rules.
- **BM25 Lexical Channel:** Provides exact token grounding across Tamil inflections and Latin binomials.
- **Dense Vector Channel:** Retrieves relevant semantic chunks when symptoms are phrased in rural colloquialisms.
- **Agronomic Reranker:** Enforces intent alignment (boosting chemical chunks for dosage questions and document overview chunks for symptom queries) and severely penalizes cross-entity and cross-crop mismatch.
