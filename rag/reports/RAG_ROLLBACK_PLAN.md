# BHOOMI RAG Automated Rollback Plan & Safety Circuit Breakers

**Active Production:** `v4.2.0-validated`  
**Immutable Fallback Target:** `v4.1.0-validated`  

---

## 1. Automatic Circuit Breaker Triggers (Instant 0-Second Rollback)

1. **Safety Leakage:** Any occurrence ($>0$) of restricted chemicals (Carbofuran, Streptocycline, Monocrotophos, Phorate) recommended to farmers $\rightarrow$ **INSTANT ROLLBACK**.
2. **Pre-Harvest Violation:** Any recommendation violating CIBRC Pre-Harvest Intervals (PHI) $\rightarrow$ **INSTANT ROLLBACK**.
3. **Cross-Crop Transfer:** Any paddy pesticide recommendation emitted for non-paddy horticultural crops $\rightarrow$ **INSTANT ROLLBACK**.
4. **Candidate Contamination:** Any occurrence of candidate-only objects discovered in active production retrieval index $\rightarrow$ **INSTANT ROLLBACK**.

## 2. Operational Threshold Breakers (Pause & Revert to v4.2.0)

1. **Decision Accuracy Drop:** If decision accuracy drops by $> 1.0\text{ pp}$ relative to baseline $\rightarrow$ **PAUSE ROLLOUT**.
2. **Regional Accuracy Divergence:** If regional accuracy drops by $> 1.5\text{ pp}$ in any single agro-climatic zone $\rightarrow$ **PAUSE ROLLOUT**.
3. **Latency Degradation:** If P95 turn latency exceeds $> 2\times$ baseline ($> 200\text{ ms}$) $\rightarrow$ **PAUSE ROLLOUT**.
4. **Evidence Unsupported Rate:** If $> 0.5\%$ of actionable decisions lack supporting evidence citations $\rightarrow$ **PAUSE ROLLOUT**.

## 3. Rollback Procedure

```powershell
# Automated 1-step rollback command
& "d:\Project\BHOOMI\services\api\.venv\Scripts\python.exe" -m rag.ingestion.build_corpus --knowledge-version v4.2.0-validated
```
