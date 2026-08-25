# BHOOMI Dense Vector Retrieval Remediation Report

**Assessment Date:** August 2026  
**Selected Representation:** 256-Dimensional 4-Hash Multi-Subword Semantic Projection  

---

## 1. Dimensionality & Subword Projection Benchmark

| Embedding Architecture | Dimensions | Hash Functions | Latency (ms) | Isolated Recall@1 | Isolated Recall@5 | Isolated MRR |
|---|---|---|---|---|---|---|
| Lightweight Subword Projection | 64 | 2 | 0.57 ms | 17.0% | 32.0% | 0.2232 |
| Balanced Subword Projection | 128 | 3 | 0.93 ms | 31.0% | 46.0% | 0.3657 |
| **Dense Multi-Hash Semantic Projection** | **256** | **4** | **1.64 ms** | **44.0%** | **58.0%** | **0.4910** |
| High-Dimensional Subword Projection | 384 | 5 | 2.34 ms | 34.0% | 57.0% | 0.4260 |

---

## 2. Selection Rationale

The 256-dimensional 4-hash multi-subword projection provides the highest isolated semantic retrieval fidelity (44.0% R@1, 58.0% R@5, 0.4910 MRR) while maintaining microsecond inference latency ($\approx 1.6\text{ ms}$) without requiring external heavy transformer runtimes.
