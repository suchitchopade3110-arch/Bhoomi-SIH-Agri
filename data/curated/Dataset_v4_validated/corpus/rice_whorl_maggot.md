---
doc_id: DOC-PEST-007
title: "TNAU Whorl Maggot Management in Rice"
crop: "Rice (Oryza sativa)"
pest_name: "Whorl maggot"
scientific_name: "Hydrellia philippina"
pest_id: "PEST_007"
source_organization: "TNAU"
source_type: "Extension Bulletin"
source_document: "TNAU Whorl Maggot Management in Rice"
source_page: "Crop Protection / Rice Pest / Whorl Maggot"
source_url: "https://agritech.tnau.ac.in/crop_protection/rice_pest.html"
citation: "TNAU Whorl Maggot Management"
authority_level: "High"
source_date: "NOT EXPOSED IN SOURCE"
publication_date: null
publication_date_status: "not_exposed"
last_reviewed: 2026-08-24
verification_date: 2026-08-24
review_due: 2027-02-24
validation_status: "SOURCE_DERIVED_VALIDATED"
etl_validation_status: "SOURCE_SUPPORTED"
severity_status: "MISSING_SOURCE_CUTOFFS"

etl_evidence:
  - record_id: "ETL-014"
    stage: "seedling"
    threshold:
      base:
        metric: "maggots_per_seedling"
        operator: ">="
        value_min: 1.0
        value_max: 2.0
        unit: "maggots/seedling"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Seedling: 1-2 maggots/seedling"
  - record_id: "ETL-015"
    stage: "vegetative"
    threshold:
      base:
        metric: "damaged_leaves_pct"
        operator: ">="
        value: 10.0
        unit: "percent"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Vegetative: 10% damaged leaves"

chemical_prescriptions:
  - chemical: "Carbofuran"
    formulation: "3G"
    dose: "33 kg/ha"
    regulatory_status: "RESTRICTED"
    evidence_status: "SOURCE_DOCUMENTED_RESTRICTED"
    notes: "Carbofuran is under regulatory restriction in flooded rice ecosystems due to runoff toxicity; cultural water management (AWD drainage) and neem cake incorporation are safer verified alternatives."
---

# TNAU Whorl Maggot Management in Rice

## 1. Overview & Crop Stages Affected
Rice whorl maggot (*Hydrellia philippina*) attacks seedlings in nursery beds and newly transplanted rice up to 30 days after transplanting (early vegetative phase).

The maggot enters the unexpanded central leaf whorl and feeds on the inner margin of the developing leaf. When the leaf expands, the damaged portions appear as conspicuous yellowish-white streaks and ragged, serrated leaf margins.

## 2. Distinguishing Field Identification Cues
- White to yellowish feeding marks and ragged, broken margins on newly unfolded leaves.
- Presence of tiny, translucent whitish-yellow maggots inside the central leaf whorl.
- Small greyish-black flies with smoky wings skimming over standing water surfaces in flooded fields.
- Tiny elongated white eggs laid singly on the leaf surface close to the water level.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Seedling / Nursery Stage**: 1 to 2 maggots per seedling (`SOURCE_SUPPORTED`).
- **Vegetative Stage**: 10% damaged leaves within 30 days after transplanting (`SOURCE_SUPPORTED`).

*(Note: Severity cutoffs separating Early from Moderate/Severe infestations must be derived from vetted field evidence and are currently pending agronomist sign-off).*

## 4. Integrated Management & Control Practices
- **Cultural Control**: Drain standing water from the field periodically for 2 to 3 days to expose maggots and eggs to sunlight and natural predators. Avoid continuous deep flooding during the first month after transplanting.
- **Organic Amendments**: Incorporate neem cake @ 250 kg/ha in the nursery bed at sowing.
- **Chemical Control (Validated)**:
  - *Carbofuran 3G* @ 33 kg/ha (`RESTRICTED` — high environmental risk in aquatic paddy; non-chemical cultural drainage preferred).

## 5. Regulatory & Validation Status
- Chemical Advice Status: Carbofuran 3G is **RESTRICTED**.
- ETL Validation Status: **SOURCE_SUPPORTED** (direct TNAU guideline).
- Image Coverage Note: No downloaded image available in Dataset v4 package; reference field image required.
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
