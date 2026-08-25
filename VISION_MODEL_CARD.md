# BHOOMI VISION MODEL CARD: 16-CLASS PADDY PATHOLOGY & ENTOMOLOGY CLASSIFIER

**Model Identifier:** `bhoomi-mobilenetv3-large-16cls`  
**Model Version:** `1.0.0`  
**Date Created:** 2026-08-25  
**Model Type:** Lightweight Convolutional Neural Network (MobileNetV3-Large Transfer Learning)  
**License:** CC-BY 4.0 (Model weights derivative of open-access research benchmarks)

---

## 1. Model Overview & Intended Use

`bhoomi-mobilenetv3-large-16cls` is a production-calibrated agricultural vision classifier designed specifically for the BHOOMI Voice-First Agricultural Advisory Platform (SIH25076).

- **Primary Task:** Automated identification of 16 canonical rice foliar diseases and insect pests from field-captured smartphone photographs.
- **Intended Deployment:** Edge mobile devices and containerized FastAPI advisory microservices.
- **Output Interface:** Emits `canonical_id` (`PEST_001..008`, `DISEASE_001..008`) and a calibrated probability `confidence` $\in [0.0, 1.0]$.
- **Out-of-Scope Use:** The model is **strictly prohibited** from outputting direct chemical dosages or pesticide formulations. All chemical advisories must be synthesized by the downstream RAG and CIBRC safety-certified layers.

---

## 2. Dataset & Provenance Summary

- **Total Training Dataset:** 11,161 verified canonical images.
- **Canonical Classes:** 16 (8 Diseases, 8 Insect Pests), each with $\ge 500$ unique images.
- **Data Provenance:** Paddy Doctor (`SRC-DS-01`), Roboflow Universe Open Rice (`SRC-DS-04`), ICAR-IIRR Repository (`SRC-DS-05`), Mendeley Data (`SRC-DS-07`), Zenodo Pathology (`SRC-DS-08`).
- **Data Isolation:** 17 TNAU exemplars isolated as `DIAGNOSTIC_REFERENCE_ONLY`; 13,237 quarantined records excluded.
- **Split Configuration:** 70% Train (7,813) / 15% Validation (1,674) / 15% Test (1,674) with random seed `42` and 0 SHA-256 partition leakage.

---

## 3. Quantitative Evaluation Summary (Untouched Test Set)

- **Overall Top-1 Accuracy:** **92.47%**
- **Overall Top-3 Accuracy:** **99.94%**
- **Macro Precision:** **92.54%**
- **Macro Recall:** **93.16%**
- **Macro F1-Score:** **92.79%**
- **Weighted F1-Score:** **92.48%**

---

## 4. Confidence Gate Policy

The model enforces BHOOMI's architectural confidence gate:
- $\ge 0.70$: High confidence $ightarrow$ Proceed to Severity Calculation and RAG Advisory Retrieval.
- $< 0.70$: Ambiguous / Low confidence $ightarrow$ Emit `ESCALATE_TO_KVK_OFFICER` with no unverified advice.

**Validation Gate Metrics:**
- **Coverage:** **49.70%**
- **Accuracy Above 0.70:** **99.40%**
- **Rejection/Escalation Rate:** **50.30%**

---

## 5. Known Limitations & Weaknesses

1. **Morphologically Similar Classes:** Early symptoms of Bacterial Leaf Blight vs Bacterial Leaf Streak and Rice Blast vs Brown Spot exhibit slight cross-confusion during early lesion emergence.
2. **Extreme Occlusion & Soil Clutter:** Severe background clutter may degrade accuracy by up to 8.2%; farmers are instructed through voice prompts to capture close-up images with leaves filling $\ge 60\%$ of the frame.
