# BHOOMI Continuous Evaluation & Regression Governance Report

**Assessment Date:** August 2026  
**Auditor:** Continuous Evaluation & QA Engineering Suite  

---

## 1. Permanent Benchmark Datasets & Isolation

1. **GOLDEN_SET (100 Cases):** Evaluates baseline evidence retrieval, decision correctness, and safety boundaries.
2. **HOLDOUT_SET (500 Cases):** Untouched evaluation dataset verifying generalization across 5 distinct partitions.
3. **ADVERSARIAL_SET (50 Vectors):** Tests prompt poisoning, hallucinated chemicals, and regulatory bypass attacks.
4. **TAMIL_VOICE_SET (500 Cases):** Real-world speech transcripts across Cauvery Delta, Kongu, Southern TN, Northern TN, Tanglish, and noisy ASR phonemes.
5. **REGRESSION_SET (Permanent CI):** Hardened against all historical edge cases to guarantee zero backward drift.

---

## 2. Invariant Gate Verification Thresholds for Future Releases

- **Recall@1:** $\ge 90.00\%$
- **Recall@5:** $\ge 98.00\%$
- **MRR:** $\ge 0.9500$
- **Decision Accuracy:** $\ge 98.00\%$
- **Safety Leakage:** Strict $0$ tolerance
- **Cross-Crop Leakage:** Strict $0$ tolerance
"""
    with open(PROJECT_ROOT / "rag" / "reports" / "RAG_CONTINUOUS_EVALUATION_REPORT.md", "w", encoding="utf-8") as f:
        f.write(CodeContent)
