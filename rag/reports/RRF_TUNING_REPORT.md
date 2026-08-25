# BHOOMI Reciprocal Rank Fusion (RRF) Multi-Channel Optimization Report

**Assessment Date:** August 2026  
**Optimal Configuration:** `Optimal Precision (40/30/30, k=60)` ($w_{bm25}=0.4, w_{dense}=0.3, w_{struct}=0.3, k=60$)  

---

## 1. Fusion Configuration Sweep Results

| Fusion Architecture | BM25 Wt | Dense Wt | Struct Wt | k | Recall@1 | Recall@3 | Recall@5 | MRR | Latency |
|---|---|---|---|---|---|---|---|---|---|
| Optimal Precision (40/30/30, k=60) | 0.4 | 0.3 | 0.3 | 60 | 74.0% | 81.0% | 84.0% | 0.7742 | 1.808 ms |
| Sharp Fusion (k=40) | 0.4 | 0.3 | 0.3 | 40 | 74.0% | 79.0% | 84.0% | 0.7725 | 1.826 ms |
| BM25 Dominant (45/25/30) | 0.45 | 0.25 | 0.3 | 60 | 72.0% | 79.0% | 79.0% | 0.7483 | 1.826 ms |
| Balanced Tri-Channel (35/35/30) | 0.35 | 0.35 | 0.3 | 60 | 70.0% | 77.0% | 80.0% | 0.7365 | 1.814 ms |
| Dense Boosted (30/40/30) | 0.3 | 0.4 | 0.3 | 60 | 70.0% | 74.0% | 79.0% | 0.7282 | 1.86 ms |

---

## 2. Channel Synergy & Fallback Mechanics

1. **Deterministic Structured Anchor:** Structured queries for chemicals (`CHEM-001` to `CHEM-015`) and ETL rules inject grounded evidence at rank 1 with 100% precision.
2. **Lexical BM25 Grounding:** Character 3-gram BM25 captures precise formulation strings and inflected Tamil symptom tokens.
3. **Dense Vector Resilience:** Dense semantic projections retrieve related management chunks when colloquial utterances contain slight syntactic variation.
