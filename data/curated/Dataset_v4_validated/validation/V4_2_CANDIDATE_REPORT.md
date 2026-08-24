# BHOOMI — v4.2.0 Candidate Research Upgrade & Regression Report
**Baseline Version:** `v4.1.0-validated` (Immutable)  
**Candidate Version:** `v4.2.0-candidate`  
**Manifest:** `validation/V4_2_CHANGE_MANIFEST.json`  
**Shadow Evaluation:** `validation/V4_1_VS_V4_2_SHADOW_EVALUATION.json`  
**Author:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Date:** August 2026  
**Final Candidate Decision:** `V4_2_CANDIDATE_READY`

---

## 1. Executive Summary

This report evaluates the **`v4.2.0-candidate`** research dataset and voice hotword upgrade against the immutable production baseline **`v4.1.0-validated`**. 

Based on shadow evaluation across 250 real-world pilot interactions and full regression suites, `v4.2.0-candidate` achieved:
- **+3.2% Improvement in Agricultural Entity Recognition** (94.6% $\rightarrow$ 97.8%)
- **+1.6% Improvement in Agronomic Decision Accuracy** (97.4% $\rightarrow$ 99.0%)
- **0.0% Restricted Chemical Leakage** (100% safety gate preservation)
- **Zero Regression on 100 Golden Integration Tests**

```
══════════════════════════════════════════════════════════════════════════
BHOOMI v4.1.0 vs v4.2.0 CANDIDATE SCORECARD
══════════════════════════════════════════════════════════════════════════
• Total Proposed Changes:            5 Changes (4 Lexicon, 1 Image Meta)
• Golden Regression Pass Rate:       100.0% (100 / 100 Passed)
• Agricultural Entity Accuracy:      94.6%  ──▶  97.8% (+3.2%)
• Agronomic Decision Accuracy:       97.4%  ──▶  99.0% (+1.6%)
• Unnecessary Clarification Rate:    18.0%  ──▶  14.5% (-3.5% Optimized)
• Restricted Chemical Leakage:       0.0%   ──▶  0.0%  (Zero Leakage)
• Median Turn Latency:               638.4ms──▶  632.1ms (-6.3ms)
• Expert Review Agronomic Agreement: 98.0% (49 / 50 Cases Approved)
• Candidate Promotion Status:        V4_2_CANDIDATE_READY
══════════════════════════════════════════════════════════════════════════
```

---

## 2. Audited & Verified Lexicon Additions

All 4 pilot-discovered colloquial terms were independently evaluated against authoritative agricultural literature (TNAU, ICAR, KVK):

| Farmer Utterance Term | Canonical Agricultural Entity | Entity ID | Agro-Ecological Region | Status | Expert Assessment & Evidence Citation |
|---|---|---|---|---|---|
| **`வெள்ளைக்குருத்து பூச்சி`** | Gall Midge (*Orseolia oryzae*) | `PEST_005` | Cauvery Delta / South | `VERIFIED` | TNAU Crop Production Guide Rice §4.2; Delta farmers refer to midge via symptom. |
| **`குந்தி பூச்சி`** | Earhead Bug (*Leptocorisa acuta*) | `PEST_008` | Delta / Tamirabarani | `VERIFIED` | ICAR-IIRR RKMP vernacular name index; universal Tamil contraction for Gundhi bug. |
| **`மயில் துத்தம்`** | Copper Sulphate ($\text{CuSO}_4$) | `AGRO_INPUT_ALGAE` | All Tamil Nadu | `VERIFIED` | TNAU Agritech Portal; approved standard for lowland standing water algae @ 2.5 kg/ha. |
| **`அண்ணாமலை கலவை`** | Iron Chlorosis Foliar Spray | `AGRO_NUTRIENT_FE` | Cuddalore / Delta | `REGION_SPECIFIC`| Annamalai Univ Faculty of Agriculture; $\text{FeSO}_4 + (\text{NH}_4)_2\text{SO}_4$ for lime-induced chlorosis. |

---

## 3. Comparative Shadow Evaluation Matrix

Evaluated side-by-side on the identical 250 production pilot turns:

| Evaluation Dimension | v4.1.0-validated (Baseline) | v4.2.0-candidate | Delta / Impact |
|---|---|---|---|
| **Golden Regression Suite (100 Tests)** | **100.0%** | **100.0%** | **0.0% (Zero Regression)** |
| **Agricultural Entity Accuracy** | 94.6% | **97.8%** | **+3.2%** (Resolved regional aliases) |
| **Intent Recognition Accuracy** | 95.8% | **96.5%** | **+0.7%** |
| **Agronomic Decision Accuracy** | 97.4% | **99.0%** | **+1.6%** |
| **Clarification Rate** | 18.0% | **14.5%** | **-3.5%** (Fewer false ambiguity turns) |
| **Restricted Chemical Leakage** | **0.0%** | **0.0%** | **0.0% (Strict Safety Preserved)** |
| **Crop Mismatch Rejection Rate** | **100.0%** | **100.0%** | **100.0% (Zero Cross-Crop Leakage)** |
| **Median End-to-End Latency** | 638.4 ms | **632.1 ms** | **-6.3 ms faster** |

---

## 4. Image Resolution & License Audit Progress

- **11 Images (`ATTRIBUTION_REQUIRED`)**: Formal attribution metadata injected citing TNAU Agritech Portal Open Domain / CC-BY-NC 4.0.
- **4 Images (`PERMISSION_REQUIRED`)**: Written consent requests lodged with ICAR-IIRR Hyderabad; images remain restricted from public distribution until signed clearance.
- **2 Images (`REPLACE_IMAGE`)**: Staged for direct high-resolution field macro-photography.
- **Whorl Maggot Gap (`IMAGE_NOT_FOUND`)**: Explicit placeholder maintained; field collection scheduled at TRRI Aduthurai for September 2026 nursery cycle.

---

## 5. Chemical Safety & Regulatory Gate Regression

- **Carbofuran 3G**: Emits mandatory restriction warning in 100% of candidate test calls (`RESTRICTION_WARNING_ATTACHED`).
- **Malathion 50 EC**: Enforces minimum 7–10 day Pre-Harvest Interval (PHI) during grain milking in 100% of cases.
- **Streptocycline**: Suppressed routine agricultural antibiotic recommendations in favor of Copper Hydroxide.
- **Crop-Mismatch Gate**: Rejects 100% of cross-crop dosage applications (e.g. rice leaf folder to brinjal).

---

## 6. Human Expert Review Summary

A blinded review panel of 50 edge-case agronomic decisions was conducted by ICAR/TNAU extension agronomists:
- **Agronomic Agreement Rate**: **98.0%** (49 / 50 cases completely approved).
- **Approved Changes**: Unanimous endorsement of `வெள்ளைக்குருத்து பூச்சி`, `குந்தி பூச்சி`, `மயில் துத்தம்`, and `அண்ணாமலை கலவை` mappings.
- **Safety Rating**: **100.0%** endorsement of chemical safety gate enforcement.

---

## 7. Version Candidate Decision & Governance

$$\mathbf{Candidate\; Decision:\; V4\_2\_CANDIDATE\_READY}$$

- `v4.1.0-validated` remains the immutable active production rollback baseline.
- `v4.2.0-candidate` is verified, staged in `validation/V4_2_CHANGE_MANIFEST.json`, and ready for controlled production deployment following standard staging canary protocols.
