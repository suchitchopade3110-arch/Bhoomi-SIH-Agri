---
doc_id: DOC-PEST-002
title: "IRRI Rice Knowledge Bank — Brown Planthopper Management"
crop: "Rice (Oryza sativa)"
pest_name: "Brown planthopper (BPH)"
scientific_name: "Nilaparvata lugens"
pest_id: "PEST_002"
source_organization: "ICAR-IRRI"
source_type: "Research Paper"
source_document: "IRRI Rice Knowledge Bank — Brown Planthopper Management"
source_page: "Pest Management / Insect Pests / Brown Planthopper"
source_url: "https://www.knowledgebank.irri.org/training/fact-sheets/pest-management/insect-pests/item/brown-planthopper"
citation: "IRRI Rice Knowledge Bank - BPH Management"
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
  - record_id: "ETL-003"
    stage: "seedling"
    threshold:
      base:
        metric: "nymphs_per_hill"
        operator: ">="
        value_min: 1.0
        value_max: 2.0
        unit: "nymphs/hill"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Seedling: 1-2 nymphs/hill"
  - record_id: "ETL-004"
    stage: "vegetative"
    threshold:
      base:
        metric: "nymphs_per_hill"
        operator: ">="
        value_min: 5.0
        value_max: 10.0
        unit: "nymphs/hill"
      modifier:
        condition: "beneficial_predators_ge_1_per_hill (Cyrtorhinus mirid bugs / Lycosa spiders)"
        adjusted_value_min: 10.0
        adjusted_value_max: 15.0
        adjusted_unit: "nymphs/hill"
    status: "SOURCE_SUPPORTED_WITH_CONTEXT"
    exact_source_text: "Vegetative: 5-10 nymphs/hill"
  - record_id: "ETL-005"
    stage: "reproductive"
    threshold:
      base:
        metric: "nymphs_per_hill"
        operator: ">="
        value_min: 10.0
        value_max: 20.0
        unit: "nymphs/hill"
      modifier:
        condition: "high_natural_enemy_predator_density_intact"
        adjusted_value: 20.0
        adjusted_unit: "nymphs/hill"
    status: "SOURCE_SUPPORTED_WITH_CONTEXT"
    exact_source_text: "Reproductive: 10-20 nymphs/hill"

chemical_prescriptions:
  - chemical: "Buprofezin"
    formulation: "25 SC"
    dose: "400 ml/ha"
    regulatory_status: "VERIFIED_CURRENT"
    evidence_status: "SOURCE_SUPPORTED_DOSE_VARIATION_NOTED"
    notes: "CIBRC registered for rice BPH. Standard label dosage is 800 ml/ha in 500 L water (source quotes 400 ml/ha). Direct spray at plant base."
---

# IRRI Rice Knowledge Bank: Brown Planthopper (BPH) Management

## 1. Overview & Crop Stages Affected
Brown planthopper (*Nilaparvata lugens*) is a destructive sap-sucking pest affecting rice across Tamil Nadu and South India. It can infest crops at all growth stages, with damage peaking between the tillering and flowering stages.

Both nymphs and adults gather at the base of rice tillers near the water line, sucking plant sap. Heavy infestation leads to extensive yellowing and rapid drying of crops in characteristic circular patches, commonly referred to as "hopper burn."

## 2. Distinguishing Field Identification Cues
- Small brownish insect with distinct white bands across the mid-dorsal abdomen.
- Wings held roof-like over the body at rest; exists in both long-winged (macropterous) and short-winged (brachypterous) forms.
- Young nymphs possessing white waxy filaments gathering densely at the plant base.
- Circular scorched or dried-up patches of plants ("hopper burn") spreading rapidly across the field.
- Copious excretion of sticky honeydew at the base of tillers leading to black sooty mold growth.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Seedling Stage**: 1 to 2 nymphs per hill (`SOURCE_SUPPORTED`).
- **Vegetative Stage**: 5 to 10 nymphs per hill (`SOURCE_SUPPORTED_WITH_CONTEXT`). *Context Modifier: Threshold increases to 10–15 nymphs/hill if mirid bug predators (Cyrtorhinus) or wolf spiders are present at $\ge 1\text{ per hill}$.*
- **Reproductive Stage**: 10 to 20 nymphs per hill (`SOURCE_SUPPORTED_WITH_CONTEXT`). *Context Modifier: Upper limit (20/hill) applies when natural biological control is intact.*

## 4. Integrated Management & Control Practices
- **Cultural & Varietal Control**: Grow resistant paddy varieties such as ADT 36 and ASD 16. Avoid excessive application of nitrogenous fertilizers, especially late top-dressing. Maintain intermittent irrigation (AWD) with 2 to 5 cm water depth rather than continuous deep flooding.
- **Biological Control**: Conserve beneficial natural predators including the mirid bug (*Cyrtorhinus lividipennis*), predatory spiders (*Lycosa pseudoannulata*), and water striders.
- **Chemical Control (Validated)**: Apply Buprofezin 25 SC @ 400–800 ml/ha (`VERIFIED_CURRENT`), directing spray nozzle towards the base of tillers where hoppers congregate.

## 5. Regulatory & Validation Status
- Chemical Advice Status: Buprofezin 25 SC is **VERIFIED_CURRENT** (CIBRC approved for BPH/GLH on rice).
- ETL Validation Status: **SOURCE_SUPPORTED_WITH_CONTEXT** (predator-dependent modifier documented).
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
