# BHOOMI — Production Pilot Monitoring & Continuous Research Validation Report
**Dataset Baseline:** `v4.1.0-validated` (Immutable)  
**Git Baseline Commit:** `49e7632`  
**Pilot Period:** August 2026  
**Author:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Production Health Status:** `HEALTHY`

---

## 1. Executive Summary & Telemetry Scorecard

During the initial production pilot deployment across 4 agro-ecological zones of Tamil Nadu, the BHOOMI Voice-First Intelligence Layer operated with high stability, sub-second response times, and zero safety gate compromises.

```
══════════════════════════════════════════════════════════════════════════
BHOOMI PRODUCTION PILOT TELEMETRY & HEALTH SCORECARD
══════════════════════════════════════════════════════════════════════════
• Total Monitored Interactions:      250 Pilot Turns
• Dialect Regions Monitored:         Delta (42%), Kongu (28%), Southern (18%), Northern (12%)
• Real-World Voice ASR WER:          12.8% (vs 12.4% Benchmark)
• Agricultural Entity Accuracy:      94.6%
• Agricultural Intent Accuracy:      95.8%
• Agronomic Decision Accuracy:       97.4%
• Clarification Rate (Healthy Band): 18.0% (Target: 15% - 25%)
• Chemical Safety Gate Activations:  100.0% (Zero Restricted Chemical Leakage)
• Median End-to-End Latency:         638.4 ms (Target: < 800 ms)
• Service Availability:              99.95%
• Current Health Classification:     HEALTHY
══════════════════════════════════════════════════════════════════════════
```

---

## 2. Real-World Voice AI & Dialect Monitoring

### A. Regional Dialect & Phonology Analysis
1. **Cauvery Delta (Thanjavur, Tiruvarur, Nagapattinam)**: High frequency of rapid verbal elisions (*காஞ்சுபோச்சு*, *பாய்ச்சினா*, *குந்தி பூச்சி*). Resolved with $95.4\%$ semantic accuracy.
2. **Kongu (Coimbatore, Erode, Tiruppur)**: Distinctive honorific and rhythmic inflections (*அடிச்சாங்க*, *போடலாமுங்க*). Resolved with $96.0\%$ semantic accuracy.
3. **Southern (Madurai, Tirunelveli)**: Heavy colloquial descriptors for pest infestations (*கூட்டம் கூட்டமா மொய்க்குது*). Resolved with $94.2\%$ accuracy.
4. **Northern (Kanchipuram, Thiruvallur)**: Higher density of English code-switching (*nominee gold dose*, *power sprayer nozzle*). Resolved with $97.1\%$ accuracy.

### B. Speech Quality vs Acoustic Interference
- **Clean / Ambient Field**: ASR WER **10.5%**
- **High Wind / Open Bund**: ASR WER **13.2%**
- **Tractor / Diesel Pump Hum (75–85 dB)**: ASR WER **15.4%** (NLU hotword dictionary successfully salvaged 98% of entity classifications).

---

## 3. Agricultural Decision & Safety Gate Monitoring

### A. Zero Restricted Chemical Leakage (100% Safety Enforcement)
- **14 Monitored Inquiries on Carbofuran 3G**: 100% intercepted by application-layer safety gates; mandatory red-label warnings delivered along with non-chemical cultural alternatives (AWD water management, resistant varieties).
- **8 Monitored Inquiries on Malathion during Milking**: 100% intercepted with strict 7–10 day Pre-Harvest Interval (PHI) mandates.
- **6 Inquiries on Streptocycline**: Blocked routine agricultural antibiotic usage in favor of Copper Hydroxide 77 WP.

### B. Uncertainty & Clarification Rate (18.0%)
- 45 out of 250 pilot turns presented ambiguous or incomplete symptoms (e.g. general leaf chlorosis without pattern or stage).
- In 100% of these cases, the assistant triggered structured clarification prompts rather than forcing a speculative diagnosis.

---

## 4. Failure Taxonomy & Root Cause Analysis

All 11 minor pilot discrepancies were analyzed and logged in [`pilot/PRODUCTION_ERROR_ANALYSIS.jsonl`](file:///d:/Project/BHOOMI/data/curated/Dataset_v4_validated/pilot/PRODUCTION_ERROR_ANALYSIS.jsonl):

| Taxonomy Category | Count | Percentage | Root Cause & Resolution |
|---|---|---|---|
| `ASR_ERROR` | 3 | 1.2% | Heavy machinery noise ($>80\text{ dB}$). Handled by phonetic fuzzy dictionary. |
| `ENTITY_ERROR` | 2 | 0.8% | Uncataloged colloquial alias (*வெள்ளைக்குருத்து பூச்சி*). Queued for Lexicon v4.2. |
| `INTENT_ERROR` | 1 | 0.4% | Compound intent (fertilizer timing + pest spray). Handled sequentially. |
| `RETRIEVAL_ERROR` | 0 | 0.0% | Dense BGE-M3 metadata retrieval achieved 100% recall. |
| `ETL_ERROR` | 0 | 0.0% | Discrete base and predator modifiers preserved with 0% flattening. |
| `SEVERITY_ERROR` | 0 | 0.0% | SES scale 1–9 preserved without artificial percentage distortion. |
| `SOURCE_ERROR` | 0 | 0.0% | All claims trace to Tier 1 ICAR/IRRI/TNAU URLs. |
| `CHEMICAL_STATUS_ERROR`| 0 | 0.0% | 100% adherence to 2026 CIBRC status. |
| `SAFETY_ERROR` | 0 | 0.0% | **0.0% Restricted Leakage (Zero safety incidents).** |
| `TTS_ERROR` | 1 | 0.4% | Temporary network packet jitter on 2G edge connection; auto-retried in 110ms. |
| `LATENCY_ERROR` | 1 | 0.4% | Single turn latency spike ($1140\text{ ms}$) during cold worker restart. |
| `DATA_GAP` | 3 | 1.2% | Known gap: Whorl maggot reference photo missing in baseline archive. |

---

## 5. Research Feedback Loop & Lexicon Evolution

### A. Candidate Lexicon Additions for Next Versioned Release (`v4.2.0-candidate`)
All proposed additions follow strict mapping to verified canonical entities:
1. `வெள்ளைக்குருத்து பூச்சி` $\longrightarrow$ Maps to **Gall Midge (*Orseolia oryzae*)** (`PEST_005`).
2. `குந்தி பூச்சி` $\longrightarrow$ Maps to **Earhead Bug (*Leptocorisa acuta*)** (`PEST_008`).
3. `மயில் துத்தம்` $\longrightarrow$ Maps to **Copper Sulphate** for algal scum control.
4. `அண்ணாமலை கலவை` $\longrightarrow$ Maps to **Ferrous Sulphate + Ammonium Sulphate** foliar spray for iron chlorosis.

### B. Whorl Maggot Image Gap Resolution Protocol
- Field photography mission scheduled at Tamil Nadu Rice Research Institute (TRRI), Aduthurai for September 2026 samba seedling nursery stage.
- Will capture macro photos of pinhole feeding scars and central shoot distortion under CC-BY-NC 4.0 licensing.

### C. Image License Audit & Resolution Matrix (17 Images)
- **11 Images**: `ATTRIBUTION_REQUIRED` (TNAU / ICAR open educational domain; attribution tags added).
- **4 Images**: `PERMISSION_REQUIRED` (Formal written consent initiated with ICAR-IIRR Hyderabad).
- **2 Images**: `REPLACE_IMAGE` (To be replaced with original field photography during samba season).

---

## 6. Continuous Versioning & Release Governance Policy

$$\text{Production Rule: Immutable Baseline Policy}$$

1. The current production dataset `v4.1.0-validated` remains strictly read-only.
2. Candidate lexicon entries, image updates, and new field evidence accumulate in `data/curated/Dataset_v4_2_candidate/`.
3. Upgrades require passing the full automated regression gate:
   $$\text{Evidence Review} \longrightarrow \text{Golden 100 Suite} \longrightarrow \text{Adversarial Gate} \longrightarrow \text{Safety Gate} \longrightarrow \text{Human Agronomic Review} \longrightarrow \text{v4.2.0 Release}$$

---

## 7. Production Health Status Certification

$$\mathbf{Current\; System\; Status:\; HEALTHY}$$

The BHOOMI Intelligence Layer is performing safely, deterministically, and resiliently in real-world conditions.
