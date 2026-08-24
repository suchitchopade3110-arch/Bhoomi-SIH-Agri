# BHOOMI Dataset v4 Curated Working Staging Report
**Location:** `data/curated/Dataset_v4_validated/`  
**Status:** `STAGING_VALIDATED_NORMALIZED — READY_FOR_REVIEW`  
**Curator:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Date:** August 2026

---

## 1. Executive Summary & Working Directory Structure

The curated working directory `data/curated/Dataset_v4_validated/` has been systematically upgraded with validated chemical regulatory findings and normalized ETL evidence structures. The original `data/external/Dataset_v4/` was preserved 100% read-only.

```
data/curated/Dataset_v4_validated/
├── CORPUS_MANIFEST.json             # Document and artifact manifest
├── SOURCE_REGISTRY.csv              # Authority source registry
├── DATASET_VALIDATION_STATUS.md     # Staging status report (this file)
├── corpus/                          # 8 Standardized Markdown RAG documents (Updated with structured ETLs)
│   ├── rice_stem_borer.md           # DOC-PEST-001 (2 ETLs, 2 chemicals)
│   ├── rice_brown_planthopper.md    # DOC-PEST-002 (3 ETLs, 1 chemical)
│   ├── rice_leaf_folder.md          # DOC-PEST-003 (2 ETLs, 1 chemical)
│   ├── rice_green_leafhopper.md     # DOC-PEST-004 (3 ETLs, 1 chemical)
│   ├── rice_gall_midge.md           # DOC-PEST-005 (1 ETL, 1 chemical)
│   ├── rice_thrips.md               # DOC-PEST-006 (2 ETLs, 1 chemical)
│   ├── rice_whorl_maggot.md         # DOC-PEST-007 (2 ETLs, 1 chemical)
│   └── rice_earhead_bug.md          # DOC-PEST-008 (2 ETLs, 1 chemical)
├── evidence/                        # Structured quantitative evidence
│   ├── ETL_EVIDENCE.jsonl           # 17 raw structured ETL records
│   └── ETL_EVIDENCE_NORMALIZED.jsonl # 17 normalized ETLs with base & modifier structures
├── tamil/                           # Tamil linguistic assets
│   └── TAMIL_PEST_LEXICON.csv       # 23 canonical names & dialectal variants
├── images/                          # 17 reference images preserved unchanged
│   ├── brown_planthopper/           # 3 images
│   ├── earhead_bug/                 # 2 images
│   ├── gall_midge/                  # 2 images
│   ├── green_leafhopper/            # 2 images
│   ├── leaf_folder/                 # 3 images
│   ├── stem_borer/                  # 3 images
│   ├── thrips/                      # 2 images
│   └── whorl_maggot/                # 0 images
├── manifests/                       # Schemas and registries
│   ├── CORPUS_MANIFEST.json
│   ├── SOURCE_REGISTRY.csv
│   ├── image_manifest.csv
│   ├── vision_label_schema.json
│   └── pest_corpus_collection_plan.csv
└── validation/                      # Completed validation results & analysis
    ├── PEST_VALIDATION_TRACKER.csv  # 8-pest readiness checklist
    ├── CHEMICAL_VALIDATION_REQUIRED.csv # Original chemical queue
    ├── CHEMICAL_VALIDATION_RESULTS.csv  # Audited regulatory results (5 verified, 4 restricted)
    ├── ETL_VALIDATION_RESULTS.csv   # Audited ETL results (11 supported, 6 context-dependent)
    └── ETL_CONFLICTS.md             # Detailed contextual interpretation notes
```

---

## 2. Updated Corpus & ETL Normalization Summary

- **8 Pest Markdown Documents Updated**: All 8 files in `corpus/` now carry structured `etl_evidence` arrays embedded directly in YAML frontmatter, capturing base values, measurement metrics, and contextual modifiers without collapsing nuance.
- **17 Normalized ETL Evidence Records**: Stored in `evidence/ETL_EVIDENCE_NORMALIZED.jsonl` with explicit `base` (value, unit) and `modifier` (condition, adjusted value) hierarchies.
- **11 Directly Source-Supported ETLs**: Verifiable numerical action thresholds from TNAU, ICAR-IIRR, IRRI, and KVK publications.
- **6 Context-Dependent ETLs**: Explicitly preserve environmental and biological conditions:
  - *BPH (Vegetative & Reproductive)*: Adjusted upwards when beneficial predators (Cyrtorhinus mirid bugs / wolf spiders) are $\ge 1\text{/hill}$.
  - *Leaf Folder (Reproductive)*: Tightened to 5–10% when flag leaf is emerging due to carbohydrate importance.
  - *GLH (Seedling, Vegetative, Reproductive)*: Adjusted to 1–2/hill in Rice Tungro Virus (RTV) endemic tracts due to vector transmission risks.
  - *Earhead Bug (Milking)*: Preserves dual representation between 10 bugs/100 panicles and 1–2 bugs/hill.

---

## 3. Chemical Regulatory Validation Status

All 9 chemical prescriptions in the corpus have been audited against the CIBRC 2026 registered list:
- **5 Verified Current (`VERIFIED_CURRENT`)**:
  - *Chlorantraniliprole 18.5 SC* (Stem borer, Leaf folder) — CIBRC approved, PHI 47 days.
  - *Buprofezin 25 SC* (BPH) — CIBRC approved IGR.
  - *Imidacloprid 17.8 SL* (GLH) — CIBRC approved, PHI 21 days.
  - *Thiamethoxam 25 WG* (Thrips) — CIBRC approved, PHI 14 days.
- **4 Restricted (`RESTRICTED`)**:
  - *Carbofuran 3G* (Stem borer, Gall midge, Whorl maggot) — Class Ib toxicant under phased state-level restrictions/bans; flagged for non-chemical cultural prioritization.
  - *Malathion 50 EC* (Earhead bug) — Mandatory minimum 7–10 days Pre-Harvest Interval (PHI) required to prevent grain residue violations during milking.

---

## 4. Unresolved Research Issues

1. **Pest Severity Cutoffs**: Discrete percentage damage and insect count cutoffs for the 3-tier severity framework (`early`, `moderate`, `severe_spreading`) remain unassigned (`severity_status: "MISSING_SOURCE_CUTOFFS"`).
2. **Whorl Maggot Image**: Dataset v4 package contains 0 reference images for Whorl maggot (7 of 8 classes populated).
3. **Dialectal Tamil Review**: 7 colloquial Tamil terms in `TAMIL_PEST_LEXICON.csv` remain marked as `NEEDS_REVIEW` pending field farmer validation.
