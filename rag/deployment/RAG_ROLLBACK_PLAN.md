# BHOOMI RAG Automated Rollback Plan & Safety Circuit Breakers

**Active Production:** `v4.2.0-validated`  
**Immutable Fallback Baseline:** `v4.1.0-validated`  
**Canary Candidate:** `v4.3.0-candidate`  

---

## 1. Instant 0-Second Circuit Breaker Rollback Triggers

An immediate, automated rollback is executed if ANY of the following hard safety invariants are breached during canary:

1. **Restricted Chemical Leakage ($> 0$):** Any recommendation of banned or hazardous molecules (Carbofuran 3G, Streptocycline, Monocrotophos, Phorate, Endosulfan).
2. **Pre-Harvest Interval (PHI) Violation ($> 0$):** Any pesticide prescription within mandatory pre-harvest waiting windows causing grain residue violations.
3. **Cross-Crop Transfer ($> 0$):** Reusing paddy pesticide dosages for non-paddy horticultural crops (Brinjal, Chilli, Cotton, Tomato).
4. **Candidate Contamination ($> 0$):** Any occurrence of candidate-only objects discovered in active production retrieval indexes.

---

## 2. Operational Threshold Breakers (Rollback to Baseline)

1. **Decision Accuracy Drop:** If decision accuracy drops by $> 1.0\text{ pp}$ relative to baseline $\rightarrow$ **PAUSE ROLLOUT**.
2. **Regional Accuracy Divergence:** If regional accuracy drops by $> 1.5\text{ pp}$ in any single agro-climatic zone $\rightarrow$ **PAUSE ROLLOUT**.
3. **P95 Latency Breach:** If P95 turn latency exceeds $> 2\times$ baseline ($> 200\text{ ms}$) $\rightarrow$ **PAUSE ROLLOUT**.
4. **Evidence Unsupported Rate:** If $> 0.5\%$ of actionable decisions lack supporting evidence citations $\rightarrow$ **PAUSE ROLLOUT**.

---

## 3. Automated Rollback Command

```powershell
& "d:\Project\BHOOMI\services\api\.venv\Scripts\python.exe" -m rag.ingestion.build_corpus --knowledge-version v4.2.0-validated
```
