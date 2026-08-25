# BHOOMI RAG Knowledge Source Inventory

**Audit Date:** August 2026  
**Auditor:** Lead RAG Architect & Dataset Governance Engineer  
**Production Baseline Directory:** `data/curated/Dataset_v4_validated/` (Read-Only)  
**Candidate Staging Directory:** `data/curated/Dataset_v4_3_candidate/` (Isolated)  

---

## 1. Corpus Markdown Documents Inventory

| Document ID | File Name | Entity Name | Scientific / Pathogen Name | Source Authority | Validation Status |
|---|---|---|---|---|---|
| `DOC-PEST-001` | `corpus/rice_stem_borer.md` | Yellow Stem Borer | *Scirpophaga incertulas* | TNAU / ICAR-IIRR | **VALIDATED** |
| `DOC-PEST-002` | `corpus/rice_brown_planthopper.md` | Brown Planthopper (BPH) | *Nilaparvata lugens* | IRRI / TNAU | **VALIDATED** |
| `DOC-PEST-003` | `corpus/rice_leaf_folder.md` | Rice Leaf Folder | *Cnaphalocrocis medinalis* | TNAU / ICAR | **VALIDATED** |
| `DOC-PEST-004` | `corpus/rice_green_leafhopper.md` | Green Leafhopper (GLH) | *Nephotettix virescens* | ICAR-IIRR | **VALIDATED** |
| `DOC-PEST-005` | `corpus/rice_gall_midge.md` | Rice Gall Midge | *Orseolia oryzae* | TNAU / ICAR | **VALIDATED** |
| `DOC-PEST-006` | `corpus/rice_thrips.md` | Rice Thrips | *Stenchaetothrips biformis* | KVK / TNAU | **VALIDATED** |
| `DOC-PEST-007` | `corpus/rice_whorl_maggot.md` | Rice Whorl Maggot | *Hydrellia philippina* | TNAU | **VALIDATED** |
| `DOC-PEST-008` | `corpus/rice_earhead_bug.md` | Earhead Bug / Gundhi Bug | *Leptocorisa acuta* | ICAR-IIRR | **VALIDATED** |
| `DOC-DIS-001` | `corpus/rice_bacterial_leaf_blight.md`| Bacterial Leaf Blight (BLB) | *Xanthomonas oryzae pv. oryzae* | ICAR / IRRI / TNAU | **VALIDATED** |
| `DOC-DIS-002` | `corpus/rice_blast.md` | Rice Blast | *Magnaporthe oryzae* | ICAR / IRRI / TNAU | **VALIDATED** |
| `DOC-DIS-003` | `corpus/rice_sheath_blight.md` | Sheath Blight | *Rhizoctonia solani* | IRRI / TNAU | **VALIDATED** |
| `DOC-DIS-004` | `corpus/rice_tungro_virus.md` | Rice Tungro Virus (RTV) | RTBV & RTSV | IRRI / ICAR-IIRR | **VALIDATED** |
| `DOC-DIS-005` | `corpus/rice_false_smut.md` | Rice False Smut | *Ustilaginoidea virens* | ICAR-IIRR / TNAU | **VALIDATED (Candidate)** |
| `DOC-DIS-006` | `corpus/rice_stem_rot.md` | Rice Stem Rot | *Sclerotium oryzae* | TNAU / IRRI | **VALIDATED (Candidate)** |
| `DOC-DIS-007` | `corpus/rice_sheath_rot.md` | Sheath Rot | *Sarocladium oryzae* | TNAU / IRRI | **VALIDATED** |
| `DOC-DIS-008` | `corpus/rice_brown_spot.md` | Brown Spot | *Bipolaris oryzae* | ICAR / TNAU | **VALIDATED** |
| `DOC-DIS-009` | `corpus/rice_bacterial_leaf_streak.md`| Bacterial Leaf Streak | *Xanthomonas oryzae pv. oryzicola* | TNAU / ICAR | **VALIDATED** |

---

## 2. Quantitative Evidence Assets

### 2.1 Normalized ETL Evidence (`evidence/ETL_EVIDENCE_NORMALIZED.jsonl`)
- **Total Records Ingested**: 19 normalized ETL threshold objects.
- **Directly Source-Supported**: 13 records (e.g. Stem borer 10% dead hearts, Gall midge 5% silver shoots, Thrips 5-10 thrips/seedling).
- **Context-Dependent Conditional Records**: 6 records (BPH predator ratios, GLH Tungro endemicity, Leaf folder flag leaf booting stage, Earhead bug panicle vs hill density).

### 2.2 Severity Evidence (`evidence/SEVERITY_EVIDENCE.jsonl`)
- **Total Records Ingested**: 14 records across 8 pests and 6 major diseases.
- **SES Scale Alignment**: Standard Evaluation System for Rice (IRRI/ICAR SES 1–9) with quantitative percentage damage cutoffs and qualitative symptom progression.

### 2.3 Chemical Regulatory Status Audit (`evidence/CHEMICAL_STATUS_AUDIT.jsonl`)
- **Total Chemicals Ingested**: 15 active ingredient records audited against CIBRC 2026:
  - `VERIFIED_CURRENT`: Chlorantraniliprole 18.5 SC, Buprofezin 25 SC, Imidacloprid 17.8 SL, Thiamethoxam 25 WG, Copper Hydroxide 77 WP, Tricyclazole 75 WP, Isoprothiolane 40 EC, Hexaconazole 5 EC, Validamycin 3 L, Azoxystrobin + Difenoconazole 29.6 SC, Propiconazole 25 EC, Pseudomonas fluorescens.
  - `RESTRICTED`: Carbofuran 3G (Class Ib red-label, state phased restrictions), Malathion 50 EC (Strict 7–10d PHI during grain milking), Streptocycline (AMR restriction).
  - `DRONE_ULV_APPROVED`: Chlorantraniliprole, Copper Hydroxide, Azoxystrobin + Difenoconazole with conditional 20–25 L/ha spray volume and drift buffers.

### 2.4 Diagnostic Decision Trees (`evidence/DIAGNOSTIC_DECISION_TREES.jsonl`)
- `DDT-001`: Multi-turn structured decision tree for physiological Zinc Deficiency (*Khaira*) vs fungal Brown Spot (*Bipolaris oryzae*).

---

## 3. Tamil Linguistic & Dialect Assets

### `tamil/TAMIL_PEST_LEXICON.csv`
- **Total Terms**: 24 terms spanning canonical names, symptom phrases, and colloquial dialect variants.
- **Active Production Aliases**:
  - `வெள்ளைக்குருத்து பூச்சி` $\rightarrow$ Gall Midge (*Orseolia oryzae*) — `VERIFIED`
  - `குந்தி பூச்சி` $\rightarrow$ Earhead Bug (*Leptocorisa acuta*) — `VERIFIED`
  - `மயில் துத்தம்` $\rightarrow$ Copper Sulphate ($CuSO_4$) — `VERIFIED`
  - `அண்ணாமலை கலவை` $\rightarrow$ Iron Chlorosis Foliar Mixture — `VERIFIED`
  - `வெங்காயத்தாள் புழு` $\rightarrow$ Gall Midge (*Orseolia oryzae*) — `VERIFIED (Candidate)`
- **Deferred / Quarantined Terms**:
  - `மட்ட பூச்சி` $\rightarrow$ Sheath Mite (*Steneotarsonemus spinki*) — `DEFERRED_RESEARCH` (Kept out of direct production entity resolution due to residual ambiguity).

---

## 4. Multi-Modal Visual Assets & Image Manifest

- **Total Reference Photos**: 17 images across 7 pest classes.
- **Licensing Status**: CC-BY-NC 4.0 compliant educational attribution to TNAU Agritech Expert System.
- **Known Gap**: Whorl Maggot (`IMG-0018`) preserved explicitly as `IMAGE_NOT_FOUND` (field collection planned for September 2026 Samba nursery).
