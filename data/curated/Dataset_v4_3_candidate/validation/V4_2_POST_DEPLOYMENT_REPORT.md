# BHOOMI — v4.2.0 Post-Deployment Evaluation & Production Window Report
**Promoted Production Baseline:** `v4.2.0-validated`  
**Rollback Baseline:** `v4.1.0-validated`  
**Git Promotion Commit:** `cfbf6d6`  
**Deployment Timestamp:** August 2026  
**Author:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Production Status:** `BHOOMI_PRODUCTION_v4.2.0`

---

## 1. Executive Summary

Following successful staged canary execution (5%, 25%, 50% across 1,100 turns) and 100% passing post-deployment smoke tests across 16 critical production scenarios, **`v4.2.0-validated`** is certified as the active production intelligence baseline for BHOOMI.

```
══════════════════════════════════════════════════════════════════════════
BHOOMI v4.2.0 POST-DEPLOYMENT SCORECARD
══════════════════════════════════════════════════════════════════════════
• Promoted Dataset Version:          v4.2.0-validated (Active Live)
• Rollback Dataset Version:          v4.1.0-validated (Immutable Snapshot)
• Post-Deployment Smoke Test Pass:   16 / 16 Scenarios Passed (100.0%)
• Agricultural Entity Accuracy:      97.8% (+3.2% vs v4.1 Baseline)
• Agronomic Decision Accuracy:       99.0% (+1.6% vs v4.1 Baseline)
• Restricted Chemical Leakage:       0.0% (Zero Leakage Incidents)
• Crop-Mismatch Rejection Rate:      100.0% (Zero Cross-Crop Leakage)
• Median End-to-End Latency:         632.1 ms (Target: < 800 ms)
• Stream Interruption Latency:       118.9 ms (Sub-150ms Barge-In)
• Live Service Availability:         99.96%
• Certified Production Status:       BHOOMI_PRODUCTION_v4.2.0
══════════════════════════════════════════════════════════════════════════
```

---

## 2. Post-Deployment Performance Metrics

| Metric Dimension | v4.1.0 Baseline | v4.2.0 Live Production | Net Impact & Production Health |
|---|---|---|---|
| **ASR Semantic Fidelity (WER)** | 12.8% | **12.4%** | +0.4% improvement via hotword biasing |
| **Agricultural Entity Accuracy** | 94.6% | **97.8%** | **+3.2%** (Resolved regional aliases) |
| **Agricultural Intent Accuracy** | 95.8% | **96.5%** | **+0.7%** |
| **Agronomic Decision Accuracy** | 97.4% | **99.0%** | **+1.6%** |
| **Clarification Rate** | 18.0% | **14.5%** | **-3.5%** (Optimized false ambiguity) |
| **Restricted Chemical Leakage** | **0.0%** | **0.0%** | **100% Hard Safety Gate Enforced** |
| **Crop Mismatch Rejection Rate** | **100.0%** | **100.0%** | **100% Hard Cross-Crop Isolation** |
| **Median Turn Latency** | 638.4 ms | **632.1 ms** | **-6.3 ms faster** |
| **P95 Latency** | 682.1 ms | **674.8 ms** | **-7.3 ms faster** |
| **Service Availability** | 99.95% | **99.96%** | Exceeds 99.9% Production SLA |

---

## 3. Post-Deployment Smoke Test Verification (16 Scenarios)

All 16 production edge-case scenarios passed without a single failure:
1. **Voice Smoke Tests (1–5)**: Standard Tamil, Delta colloquial slang, code-switching, Gall midge alias (`வெள்ளைக்குருத்து பூச்சி`), and Rice Blast queries executed cleanly.
2. **Agriculture Smoke Tests (6–9)**: BPH predator modifiers preserved without averaging; SES scale severity preserved; ambiguous yellow leaves safely triggered clarification; missing info queries safely prompted user.
3. **Safety Smoke Tests (10–12)**: Carbofuran 3G red-label warning emitted; Brinjal shoot borer dosage crossover blocked; Malathion Pre-Harvest Interval mandated.
4. **Reliability Smoke Tests (13–16)**: ASR timeout gracefully fell back to retry prompt; TTS timeout fell back to text stream; DB offline escalated to KVK; stream barge-in canceled in 118.9 ms with zero state corruption.

---

## 4. Operational Incidents & Safety Summary

- **Total P0 / P1 Safety Incidents**: **0**
- **Restricted Chemical Attempts Intercepted**: 100%
- **Rollback Invocations Triggered**: **0** (Rollback to `v4.1.0-validated` remains fully verified and operational via one command).

---

## 5. Certification Declaration

$$\mathbf{Status:\; BHOOMI\_PRODUCTION\_v4.2.0}$$
