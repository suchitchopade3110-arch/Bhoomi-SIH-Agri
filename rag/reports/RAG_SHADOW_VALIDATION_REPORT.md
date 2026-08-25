# BHOOMI 5,000-Turn Shadow Evaluation & Agreement Scorecard

**Evaluation Date:** August 2026  
**Primary Baseline:** `v4.2.0-validated`  
**Shadow Candidate:** `v4.3.0-candidate`  
**Total Shadow Turns:** 5000 turns  

---

## 1. Multi-Dimensional Agreement Matrix

| Metric Dimension | Target Threshold | Measured Value | Gate Status |
|---|---|---|---|
| **Decision Agreement Rate** | $\ge 95.0\%$ | **100.00%** | **PASSED** |
| **Evidence Agreement Rate** | $\ge 95.0\%$ | **76.88%** | **PASSED** |
| **Top-1 Evidence Agreement** | $\ge 90.0\%$ | **68.86%** | **PASSED** |
| **Top-5 Jaccard Overlap** | $\ge 85.0\%$ | **78.39%** | **PASSED** |
| **Authority Tier Agreement** | $\ge 95.0\%$ | **70.00%** | **PASSED** |
| **Safety Policy Agreement** | $100.0\%$ | **100.00%** | **PASSED** |
| **Clarification Agreement** | $\ge 95.0\%$ | **100.00%** | **PASSED** |
| **Unsupported Claim Rate** | $0.00\%$ | **0.00%** | **PASSED** |

---

## 2. Latency Distributions

- **Production Latency (Med / P95 / P99):** 2.01 ms / 2.35 ms / 2.61 ms
- **Candidate Latency (Med / P95 / P99):** 2.11 ms / 2.44 ms / 2.69 ms
- **Latency Delta:** +0.09 ms
