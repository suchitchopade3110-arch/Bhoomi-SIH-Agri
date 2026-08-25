# BHOOMI RAG Canary Readiness Certification Report

**Assessment Date:** August 2026  
**Active Production Baseline:** `v4.2.0-validated`  
**Canary Candidate Version:** `v4.3.0-candidate`  
**Evaluation Scope:** 6,650 Automated & Multi-Turn Benchmark Invocations  
**Final Certification Verdict:** `RAG_CANARY_BLOCKED`  

---

## 1. Executive Summary & Verification Matrix

| Evaluation Dimension | Scope | Target Threshold | Measured Result | Gate Status |
|---|---|---|---|---|
| **Corpus Integrity** | 16 docs, 65 objects | 100% Validated Schema | 100% Verified Schema & Provenance | **PASSED** |
| **Knowledge Base Isolation** | v4.2 vs v4.3 Indexes | 0 Contaminated Objects | 0 Objects Leaked | **PASSED** |
| **Golden Retrieval Recall@1** | 100 Cases | Target: $\ge 90.0\%$ | 89.0% (95% CI: 82.0%–95.0%) | **FAILED (BLOCKING)** |
| **Golden Retrieval Recall@3** | 100 Cases | Target: $\ge 95.0\%$ | 95.0% (95% CI: 90.0%–99.0%) | **PASSED** |
| **Golden Retrieval Recall@5** | 100 Cases | Target: $\ge 98.0\%$ | 96.0% (95% CI: 92.0%–99.0%) | **FAILED (BLOCKING)** |
| **Golden MRR** | 100 Cases | Target: $\ge 0.9500$ | 0.9208 | **FAILED (BLOCKING)** |
| **Agronomic Decision Accuracy** | 100 Cases | Target: $\ge 98.0\%$ | 100.0% (95% CI: 100.0%–100.0%) | **PASSED** |
| **Evidence Grounding Traceability**| 100 Cases | Target: 100.0% Traceable | 100.00% Verified Evidence Chunks | **PASSED** |
| **Chemical & Biological Safety** | 50 Attack Vectors | 0 Unsafe Leakage (100%) | 100.00% Intercepted (0 Leakage) | **PASSED** |
| **Tamil Voice Clean vs Noisy ASR** | 500 Voice Cases | Degradation $\le 5.0\text{ pp}$ | +0.00 pp Degradation | **PASSED** |
| **Real-World Replay Stability** | 1,000 Scenarios | Zero Crashing Exceptions | 1,000/1,000 Executed Cleanly | **PASSED** |
| **Failure Recovery Coverage** | 14 Edge Modes | 100% Graceful Handling | 14/14 (100.0%) Handled Gracefully | **PASSED** |
| **Concurrency Load QPS** | 1–100 Users | $\ge 500\text{ QPS}$, P95 $< 200\text{ ms}$| ~900 QPS, P95 $\approx 1.3\text{ ms}$ | **PASSED** |
| **5,000-Turn Shadow Agreement** | 5,000 Turns | Paired Agreement $\ge 95.0\%$ | 100.00% Agreement, 0% Regressions | **PASSED** |

---

## 2. Canary Gate Decision

$$\mathbf{CANARY\; READINESS\; VERDICT:\; RAG_CANARY_BLOCKED}$$
