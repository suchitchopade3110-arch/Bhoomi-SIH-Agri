# BHOOMI — v4.3 Candidate Research, Agricultural Evidence & Dataset Governance Plan
**Document ID:** RES-PLAN-v4.3  
**Active Production Baseline:** `v4.2.0-validated` (Immutable)  
**Rollback Baseline:** `v4.1.0-validated` (Certified Snapshot)  
**Target Candidate Version:** `v4.3.0-candidate`  
**Author:** Tharun BL (Production Research, Agricultural Evidence, Voice Quality & Dataset Governance)  
**Date:** August 2026  
**Status:** `RESEARCH_PLAN_APPROVED — PENDING_EVIDENCE_GATHERING`  

---

## 1. Executive Intent & Architecture Governance

The objective of the BHOOMI v4.3 research cycle is to address verified production telemetry gaps through evidence-backed agricultural research, controlled voice model fine-tuning, and structured multi-modal data collection without perturbing the certified `v4.2.0-validated` production baseline.

### 1.1 Strict Version Governance Workflow
Under no circumstances shall production telemetry trigger direct edits to the active production corpus or runtime routing logic. All development must follow the staged governance pipeline:

```
┌─────────────────────────┐
│ REAL FARMER SIGNAL      │  (Production Voice Telemetry across 4 TN Agro-Zones)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ PRODUCTION TELEMETRY    │  (Anonymized Interaction Tracking in V4_2_PRODUCTION_ERROR_LOG)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ ERROR CLASSIFICATION    │  (16-Class Taxonomy: ASR, Entity, Data Gap, Safety, etc.)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ EVIDENCE GATHERING      │  (Authoritative ICAR-IIRR / TNAU / CIBRC 2026 Extraction)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ EXPERT PEER REVIEW      │  (Joint Sign-Off: Entomology, Pathology, Agronomy, Extension)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ REGRESSION TEST SUITE   │  (Golden Integration + V4_3_REGRESSION_ADDITIONS)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ V4.3 CANDIDATE BRANCH   │  (Isolated Dataset Staging: data/candidates/Dataset_v4.3/)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ CONTROLLED VALIDATION   │  (6-Gate Pre-Deployment Readiness Suite + Shadow Evaluation)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ STAGED CANARY (5%-50%)  │  (Multi-Turn Live Traffic Evaluation with Rollback SLA <5s)
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│ PRODUCTION PROMOTION    │  (v4.3.0-validated certified; v4.2.0 becomes Rollback Baseline)
└─────────────────────────┘
```

---

## 2. Agricultural Evidence Research Campaigns

### 2.1 Research Campaign A: High-Impact Pathological Expansions
1. **Rice False Smut (*Ustilaginoidea virens* / மஞ்சள் கதிர் பூஞ்சாணம்)**:
   - *Problem*: High occurrence during humid flowering stages in the Cauvery Delta (Late Samba season).
   - *Authoritative Evidence Sources*: ICAR-IIRR Rice Diseases Management Guide; TNAU Crop Production Guide 2020.
   - *Target Deliverable*: `DOC-DIS-005.md` with explicit preventive spray window (Boot-leaf stage, 5–7 days prior to panicle emergence).
   - *Approved Chemicals*: Copper Hydroxide 77 WP @ 1.25 kg/ha or Propiconazole 25 EC @ 500 ml/ha. Spraying during full anthesis is strictly prohibited to prevent florets blast and spikelet sterility.
2. **Rice Stem Rot (*Sclerotium oryzae* / தண்டு அழுகல் நோய்)**:
   - *Problem*: Lower stem sheath rotting in ill-drained delta soils causing catastrophic lodging at maturity.
   - *Authoritative Evidence Sources*: TNAU Agritech Pathology Portal; IRRI Rice Knowledge Bank.
   - *Target Deliverable*: `DOC-DIS-006.md` highlighting primary water drainage protocols (intermittent drying to aerate soil) and targeted basal stem fungicide application (Hexaconazole 5 EC @ 1000 ml/ha or Validamycin 3 L @ 1000 ml/ha).

### 2.2 Research Campaign B: Aerial Drone Spraying & ULV Calibration SOP
1. *Problem*: Rapidly increasing farmer adoption of agricultural drones in Northern and Delta Tamil Nadu without certified water dilution parameters.
2. *Authoritative Evidence Sources*: CIBRC Standard Operating Procedure (SOP) for Drone Application of Pesticides; TNAU Department of Farm Machinery Drone Advisory.
3. *Target Deliverable*: Drone-specific frontmatter attributes:
   - Water Volume: 20–25 Liters/hectare (8–10 Liters/acre).
   - Droplet Size: 100–150 microns (VMD).
   - Wind Speed Cutoff: $< 10\text{ km/h}$ (drift hazard limit).
   - Buffer Zone: Minimum 100-meter buffer from residential dwellings and water bodies.

### 2.3 Research Campaign C: Biological & Organic Input Compatibility
1. *Problem*: Farmers tank-mixing *Pseudomonas fluorescens* or *Trichoderma* with chemical fungicides.
2. *Authoritative Evidence Sources*: TNAU Bio-inoculant Formulation Manual; ICAR-NBAIR.
3. *Target Deliverable*: Strict chemical incompatibility gate rule mandating a **minimum 7-day window** between bio-control agent application and synthetic chemical fungicide sprays.

---

## 3. Tamil Voice Quality & Regional Dialect Acoustic Campaign

### 3.1 Field Dialect Lexicon Validation
The following terms logged in `TAMIL_PEST_LEXICON.csv` will undergo formal multi-district extension review:

| Term (Tamil) | Proposed Canonical Entity | Focus Zone | Field Validation Center | Target Status in v4.3 |
|---|---|---|---|---|
| **வெங்காயத்தாள் புழு** | Gall midge (*Orseolia oryzae*) | Southern TN | AC&RI Madurai / KVK Ambasamudram | `VERIFIED` |
| **மட்ட பூச்சி** | Sheath mite (*Steneotarsonemus spinki*) | Kongu | TNAU Coimbatore / KVK Sandhiyur | `VERIFIED` |
| **துங்ரோ பூச்சி** | Green leafhopper (*Nephotettix virescens*) | Cauvery Delta | TRRI Aduthurai / KVK Needamangalam | `VERIFIED` |
| **சாற்றுப்பூச்சி** | Earhead bug (*Leptocorisa acuta*) | Coastal Delta | KVK Sikkal, Nagapattinam | `VERIFIED` |

### 3.2 Acoustic Noise Injection & Fine-Tuning
1. *Acoustic Interference Profiles*: Record 50 hours of authentic agricultural field background audio:
   - 80 dB Diesel Pump Shed noise.
   - 85 dB Power Tiller / Tractor field operations.
   - 70 dB Open Canal wind shear.
   - Heavy monsoon rainfall on tin shed roofs.
2. *Training Objective*: Fine-tune the IndicConformer ASR acoustic model with 20% synthetic agricultural noise injection, reducing high-noise WER from **14.8% to $< 11.5\%$**.

---

## 4. Visual Evidence & Multi-Modal Dataset Governance

### 4.1 Whorl Maggot (*Hydrellia philippina*) Field Collection
- **Field Site**: Tamil Nadu Rice Research Institute (TRRI), Aduthurai.
- **Timing**: September 2026 Samba nursery and early transplanting cycle (15–30 DAT).
- **Target Images**: Minimum 4 verified high-resolution RAW photographs capturing:
  1. Characteristic ragged, serrated leaf margins on unfurled central leaves.
  2. Pinpoint feeding streaks on leaf whorl.
  3. Close-up macro of puparium at base of leaf blade.
  4. Wide-angle view showing stunted seedling patch.
- **Verification Schema**: Entomologist signed verification certificate, GPS coordinates, timestamp, camera EXIF, and SHA-256 integrity hash recorded in `manifests/image_manifest.csv`.

### 4.2 Image Rights & Legal Licensing Audit
- Formalize institutional open-access educational attribution documentation with TNAU Directorate of Extension Education.
- Maintain CC-BY-NC 4.0 compliant attribution manifests for all 17 baseline reference photos.

---

## 5. Candidate Multi-Gate Verification Criteria

Before any candidate dataset is considered for v4.3 promotion, it must pass all 6 validation gates with 100% compliance:

```
══════════════════════════════════════════════════════════════════════════════
BHOOMI v4.3 CANDIDATE PROMOTION VERIFICATION CRITERIA
══════════════════════════════════════════════════════════════════════════════
1. GOLDEN REGRESSION GATE:
   • 100% pass on 100-test Golden Regression Suite
   • 100% pass on V4_3_REGRESSION_ADDITIONS (All 8 newly added cases)

2. CHEMICAL SAFETY & REGULATORY GATE:
   • 0.0% Restricted chemical emission (Hard Safety Boundary)
   • 100% Pre-Harvest Interval (PHI) compliance on pre-harvest queries
   • 100% Crop-mismatch isolation (Zero cross-crop leakage)

3. ADVERSARIAL DISAMBIGUATION GATE:
   • 100% Clarification triggered on ambiguous symptoms (Zero forced diagnosis)
   • 100% Honest escalation on out-of-corpus queries (Zero LLM fabrication)

4. LATENCY & CONCURRENCY BENCHMARK:
   • Median Latency: < 650 ms (Normal warm state)
   • P95 Latency: < 750 ms
   • Stress 50-Concurrent Latency: Median < 850 ms, Timeouts 0.0%

5. VOICE BARGE-IN & INTERRUPTION TEST:
   • Median Audio Cancellation Latency: < 120 ms
   • Context State Preservation: 100.0% (Zero session corruption)

6. STAGED CANARY VALIDATION:
   • 5% Canary (200 turns) -> 25% Canary (500 turns) -> 50% Canary (1000 turns)
   • Zero P0/P1 Safety Incidents across entire canary execution window
══════════════════════════════════════════════════════════════════════════════
```

---

## 6. Rollback Assurance & SLA Guardrails

- **Rollback Target Version**: `v4.2.0-validated` (Current production) / `v4.1.0-validated` (Cold baseline).
- **Rollback SLA**: $< 5\text{ seconds}$ via automated symlink switch and hot cache eviction.
- **Rollback Triggers**:
  - Any confirmed restricted chemical leakage ($> 0.0\%$).
  - Any cross-crop dosage recommendation failure.
  - End-to-end P95 latency $> 950\text{ ms}$ over a 5-minute rolling window.
  - Live service error rate $> 0.5\%$.

---

## 7. Plan Summary & Next Steps

This research plan establishes a rigorous, evidence-based roadmap for BHOOMI v4.3 development. The active `v4.2.0-validated` production baseline remains locked and fully operational while research proceeds in isolated staging.
