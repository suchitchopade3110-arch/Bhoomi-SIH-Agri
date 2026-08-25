# BHOOMI — v4.2.0 Staged Canary Deployment & Promotion Gate Report
**Baseline Version:** `v4.1.0-validated` (Rollback Baseline)  
**Candidate Version:** `v4.2.0-candidate`  
**Canary Harness:** `validation/run_canary_evaluation.py`  
**Canary Dataset:** `validation/V4_2_CANARY_EVALUATION.json`  
**Author:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Date:** August 2026  
**Final Canary Decision:** `CANARY_PROMOTION_READY`

---

## 1. Executive Summary & Staged Traffic Scorecard

The **`v4.2.0-candidate`** research dataset and voice hotword upgrade successfully passed all 3 progressive canary traffic stages (Stage 1 @ 5%, Stage 2 @ 25%, Stage 3 @ 50%) across 1,100 evaluated interactions.

```
══════════════════════════════════════════════════════════════════════════
BHOOMI v4.2.0 CANARY DEPLOYMENT SCORECARD
══════════════════════════════════════════════════════════════════════════
• Total Evaluated Canary Interactions: 1,100 Live & Shadow Turns
• Staged Traffic Execution:           Stage 1 (5%) ──▶ Stage 2 (25%) ──▶ Stage 3 (50%)
• Agricultural Entity Accuracy:       94.6%  ──▶  97.8% (+3.2% Overall)
• Agronomic Decision Accuracy:        97.4%  ──▶  99.0% (+1.6% Overall)
• Unnecessary Clarification Rate:     18.0%  ──▶  14.5% (-3.5% Optimized)
• Restricted Chemical Leakage:        0.0%   ──▶  0.0%  (Zero Leakage)
• Crop-Mismatch Safety Rejection:     100.0% (Zero Cross-Crop Leakage)
• Median Turn Latency:                638.4ms──▶  632.1ms (-6.3ms faster)
• Dialect Regressions Detected:       0 Regressions across all 4 zones
• Final Canary Gate Decision:         CANARY_PROMOTION_READY
══════════════════════════════════════════════════════════════════════════
```

---

## 2. Staged Traffic Progression & Safety Observability

| Canary Stage | v4.2 Traffic Allocation | v4.1 Baseline Allocation | Monitored Turns | Safety Incidents | Gate Decision |
|---|---|---|---|---|---|
| **Stage 1 (Initial Canary)** | 5% | 95% | 200 | **0** | 🟢 ADVANCE TO STAGE 2 |
| **Stage 2 (Expanded Canary)**| 25% | 75% | 400 | **0** | 🟢 ADVANCE TO STAGE 3 |
| **Stage 3 (Balanced Canary)**| 50% | 50% | 500 | **0** | 🟢 PASS PROMOTION GATE |

---

## 3. Regional Dialect Performance Breakdown

Canary traffic was audited across Tamil Nadu's 4 major agro-ecological zones to guarantee that no local regional dialect suffered performance regressions:

| Region | Monitored Dialect | v4.1 Entity Acc | v4.2 Entity Acc | v4.1 Decision Acc | v4.2 Decision Acc | Net Impact |
|---|---|---|---|---|---|---|
| **Cauvery Delta** | Thanjavur / Tiruvarur | 94.2% | **98.4%** | 97.0% | **99.2%** | **+4.2% (Top Gain)** |
| **Kongu Region** | Coimbatore / Erode | 95.5% | **97.5%** | 98.0% | **99.0%** | **+2.0%** |
| **Southern TN** | Madurai / Tirunelveli | 93.8% | **97.2%** | 96.8% | **98.8%** | **+3.4%** |
| **Northern TN** | Kanchipuram / Thiruvallur| 96.0% | **98.0%** | 98.0% | **99.0%** | **+2.0%** |

$$\text{Conclusion: Regional improvements are uniform; zero local dialect degradation detected.}$$

---

## 4. Safety-Critical Gate & Lexicon Verification

### A. Zero Restricted Chemical Leakage
- **Carbofuran 3G**: Emitted mandatory red-label regulatory warnings in 100% of cases; prioritized non-chemical cultural alternatives (AWD water management, resistant varieties).
- **Malathion 50 EC**: Enforced strict $\ge 7\text{–}10\text{ days}$ Pre-Harvest Interval (PHI) during grain milking.
- **Streptocycline**: Suppressed routine agricultural antibiotic usage in favor of Copper Hydroxide.
- **Crop Mismatch**: 100% rejection rate when farmers attempted cross-crop chemical applications (e.g. rice leaf folder to brinjal).

### B. Newly Added Lexicon Safety Verification
- **`வெள்ளைக்குருத்து பூச்சி`** $\longrightarrow$ Correctly resolved to **Gall Midge (*Orseolia oryzae*)** (`PEST_005`) with 100% precision.
- **`குந்தி பூச்சி`** $\longrightarrow$ Correctly resolved to **Earhead Bug (*Leptocorisa acuta*)** (`PEST_008`).
- **`மயில் துத்தம்`** $\longrightarrow$ Bound to **Copper Sulphate** for algal scum control @ 2–2.5 kg/ha.
- **`அண்ணாமலை கலவை`** $\longrightarrow$ Bound to **Iron Chlorosis Foliar Spray** ($\text{FeSO}_4 + (\text{NH}_4)_2\text{SO}_4$) with region-specific tags.

---

## 5. Image Rights & Provenance Verification Gate

- **11 Images (`ATTRIBUTION_REQUIRED`)**: Verified open educational domain with formal attribution citations (TNAU / ICAR CC-BY-NC 4.0).
- **4 Images (`PERMISSION_REQUIRED`)**: Written clearance requests lodged with ICAR-IIRR Hyderabad; restricted from public distribution until signed.
- **2 Images (`REPLACE_IMAGE`)**: Staged for direct high-resolution field photography.
- **Whorl Maggot Gap (`IMAGE_NOT_FOUND`)**: Macro-photography collection protocol active for September 2026 samba seedling nurseries at TRRI Aduthurai.

---

## 6. One-Command Rollback Procedure

In the event of an unforeseen production anomaly, the system executes an atomic one-command rollback:

```bash
# Atomic Rollback to v4.1.0-validated
python -m app.core.version_manager --rollback-to v4.1.0-validated
```

- **Rollback Verification Test**: Executed in `< 5.0 seconds`. Restored all dataset bindings, NLU lexicons, and decision engine rules with zero state corruption.

---

## 7. Final Promotion Gate Decision

$$\mathbf{Canary\; Decision:\; CANARY\_PROMOTION\_READY}$$

The candidate `v4.2.0-candidate` has fulfilled all safety, agronomic, voice, dialect, and latency criteria across 3 canary stages without a single regression. It is certified **`CANARY_PROMOTION_READY`** for full production promotion to **`v4.2.0-validated`**.
