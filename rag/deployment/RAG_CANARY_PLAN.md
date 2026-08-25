# BHOOMI RAG Multi-Stage Canary Deployment Plan

**Candidate Version:** `v4.3.0-candidate`  
**Current Gate Status:** `RAG_CANARY_BLOCKED` (Rollout will commence only upon unblocking)  
**Baseline Comparison:** `v4.2.0-validated`  

---

## 1. Staged Traffic Allocation Schedule

Upon unblocking of GATE-C retrieval targets:

| Stage | Traffic % | Audience Scope | Gate Requisites | Soak Duration |
|---|---|---|---|---|
| **Stage 1** | 1% | KVK Extension Officers & Internal Agronomists | 0 Safety Interventions, 0 Unhandled Exceptions | 24 Hours |
| **Stage 2** | 5% | Cauvery Delta Pilot Rice Farmers | 0 PHI/Chemical Complaints, P95 $< 100\text{ ms}$ | 48 Hours |
| **Stage 3** | 25% | Cauvery Delta + Western Agro-Ecological Zone | Decision Consistency $\ge 98.0\%$, Grounding 100% | 48 Hours |
| **Stage 4** | 50% | All 4 Agro-Ecological Zones in Tamil Nadu | Error Rate $< 0.01\%$, 0 Version Drift | 72 Hours |
| **Stage 5** | 100% | Full Production Release | Post-Canary Final Certification Sign-Off | Permanent |

---

## 2. Canary Telemetry & Observability

- **Real-Time Counters:** Decision state distribution, safety intervention frequency, KVK escalation rate.
- **Circuit Breakers:** Immediate fallback to `v4.2.0-validated` upon any safety violation.
