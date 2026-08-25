---
doc_id: DOC-PEST-003
title: "TNAU Rice Pest Management Guide — Leaf Folder"
crop: "Rice (Oryza sativa)"
pest_name: "Leaf folder"
scientific_name: "Cnaphalocrocis medinalis"
pest_id: "PEST_003"
source_organization: "TNAU"
source_type: "Extension Bulletin"
source_document: "TNAU Rice Pest Management Guide — Leaf Folder"
source_page: "Crop Protection / Rice Pest / Leaf Folder"
source_url: "https://agritech.tnau.ac.in/crop_protection/rice_pest.html"
citation: "TNAU Rice Pest Management Guide"
authority_level: "High"
source_date: "NOT EXPOSED IN SOURCE"
publication_date: null
publication_date_status: "not_exposed"
last_reviewed: 2026-08-24
verification_date: 2026-08-24
review_due: 2027-02-24
validation_status: "SOURCE_DERIVED_VALIDATED"
etl_validation_status: "SOURCE_SUPPORTED_WITH_CONTEXT"
severity_status: "MISSING_SOURCE_CUTOFFS"

etl_evidence:
  - record_id: "ETL-006"
    stage: "vegetative"
    threshold:
      base:
        primary_metric: "larvae_per_hill"
        operator: ">="
        value: 1.0
        unit: "larva/hill"
        alternative_metric: "folded_leaves_pct"
        alternative_operator: ">="
        alternative_value: 10.0
        alternative_unit: "percent"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Vegetative: 1 larva/hill or 10% folded leaves"
  - record_id: "ETL-007"
    stage: "reproductive"
    threshold:
      base:
        primary_metric: "larvae_per_hill"
        operator: ">="
        value: 2.0
        unit: "larva/hill"
        alternative_metric: "folded_leaves_pct"
        alternative_operator: ">="
        alternative_value: 20.0
        alternative_unit: "percent"
      modifier:
        condition: "flag_leaf_emergence_booting_stage"
        adjusted_value_min: 5.0
        adjusted_value_max: 10.0
        adjusted_unit: "percent_damaged_flag_leaves"
    status: "SOURCE_SUPPORTED_WITH_CONTEXT"
    exact_source_text: "Reproductive: 2 larvae/hill or 20% folded leaves"

chemical_prescriptions:
  - chemical: "Chlorantraniliprole"
    formulation: "18.5 SC"
    dose: "150 ml/ha"
    regulatory_status: "VERIFIED_CURRENT"
    evidence_status: "SOURCE_SUPPORTED_CIBRC_ALIGNED"
    notes: "CIBRC approved label claim for Leaf folder in rice. Dilution: 150 ml in 500 L water/ha. PHI: 47 days."
---

# TNAU Rice Pest Management Guide: Leaf Folder

## 1. Overview & Crop Stages Affected
Rice leaf folder (*Cnaphalocrocis medinalis*) is a widespread foliage feeder of paddy across Tamil Nadu. It damages crops primarily from the vegetative stage through the boot leaf and panicle emergence stages.

The larva folds the leaf blade longitudinally using silken threads and feeds on the green mesophyll tissue from within the protective roll, leaving transparent white streaks and significantly impairing photosynthesis.

## 2. Distinguishing Field Identification Cues
- Leaves folded lengthwise with fine silken threads holding the margins together.
- Greenish-translucent caterpillar found actively feeding inside the folded leaf blade.
- Longitudinal white, papery streaks on damaged leaves where chlorophyll has been scraped.
- Adult moth exhibiting golden-yellow wings with distinct wavy dark borders.
- Severely infested fields exhibit a whitish, scorched appearance from a distance.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Vegetative Stage**: 1 larva per hill OR 10% folded leaves (`SOURCE_SUPPORTED`).
- **Reproductive Stage**: 2 larvae per hill OR 20% folded leaves (`SOURCE_SUPPORTED_WITH_CONTEXT`). *Context Modifier: During flag leaf emergence and booting stage, threshold tightens to 5–10% damaged flag leaves due to its critical role in grain carbohydrate supply.*

## 4. Integrated Management & Control Practices
- **Cultural Control**: Avoid excessively close planting; maintain wider row spacing to facilitate light penetration. Clear grassy weeds (*Echinochloa*, *Leersia*) from field bunds as they serve as alternate hosts.
- **Physical & Biological Control**: Install light traps in the field to monitor and trap adult moths. Conserve natural egg parasitoids such as *Trichogramma chilonis*.
- **Chemical Control (Validated)**: Apply Chlorantraniliprole 18.5 SC @ 150 ml/ha (`VERIFIED_CURRENT`, PHI: 47 days) when pest threshold is crossed.

## 5. Regulatory & Validation Status
- Chemical Advice Status: Chlorantraniliprole 18.5 SC is **VERIFIED_CURRENT** (CIBRC registered on rice).
- ETL Validation Status: **SOURCE_SUPPORTED_WITH_CONTEXT** (flag leaf booting modifier documented).
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
