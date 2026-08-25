# BHOOMI Dense Embedding & Semantic Vector Retrieval Benchmark Report

**Assessment Date:** August 2026  
**Corpus Chunks:** 140 Semantic Chunks  
**Selected Production Architecture:** `Production 128-dim (3-hash)` (Optimal latency/recall tradeoff)  

---

## 1. Dimensionality Comparison Matrix

| Architecture | Dim | Hashes | Recall@1 | Recall@3 | Recall@5 | MRR | Latency | Index Size |
|---|---|---|---|---|---|---|---|---|
| Lightweight 64-dim (2-hash) | 64 | 2 | 17.0% | 27.0% | 32.0% | 0.2232 | 0.572 ms | 35.0 KB |
| Production 128-dim (3-hash) | 128 | 3 | 31.0% | 42.0% | 46.0% | 0.3657 | 0.933 ms | 70.0 KB |
| Dense 256-dim (4-hash) | 256 | 4 | 44.0% | 53.0% | 58.0% | 0.4910 | 1.642 ms | 140.0 KB |
| High-Res 384-dim (5-hash) | 384 | 5 | 34.0% | 50.0% | 57.0% | 0.4260 | 2.336 ms | 210.0 KB |

---

## 2. Multi-Script & Linguistic Capabilities

- **Subword Agglutination Encoding:** Character 3-gram hashing captures Tamil stem semantics even under phonetic spelling variations.
- **Tanglish Code-Switching:** English and Tamil terms mapped simultaneously into orthogonal projection buckets.
- **Deterministic Zero-Dependency Indexing:** Vector calculations are 100% deterministic with zero external model server dependency, eliminating cold-start latency and inference non-determinism.
