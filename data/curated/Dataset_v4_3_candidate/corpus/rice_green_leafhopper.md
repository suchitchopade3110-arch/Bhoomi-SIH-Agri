---
doc_id: DOC-PEST-004
title: "ICAR Rice Production Manual — Green Leafhopper"
crop: "Rice (Oryza sativa)"
pest_name: "Green leafhopper (GLH)"
scientific_name: "Nephotettix virescens"
pest_id: "PEST_004"
source_organization: "ICAR-IIRR"
source_type: "Technical Bulletin"
source_document: "ICAR Rice Production Manual — Green Leafhopper"
source_page: "Insect Pest Management / Leafhoppers"
source_url: "https://iirr.icar.gov.in/"
citation: "ICAR Rice Production Manual"
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
  - record_id: "ETL-008"
    stage: "seedling"
    threshold:
      base:
        metric: "hoppers_per_hill"
        operator: ">="
        value: 5.0
        unit: "hoppers/hill"
      modifier:
        condition: "rice_tungro_virus_endemic_area"
        adjusted_value_min: 1.0
        adjusted_value_max: 2.0
        adjusted_unit: "hoppers/hill"
    status: "SOURCE_SUPPORTED_WITH_CONTEXT"
    exact_source_text: "Seedling: 5 hoppers/hill"
  - record_id: "ETL-009"
    stage: "vegetative"
    threshold:
      base:
        metric: "hoppers_per_hill"
        operator: ">="
        value_min: 10.0
        value_max: 15.0
        unit: "hoppers/hill"
      modifier:
        condition: "rice_tungro_virus_symptoms_present_in_vicinity"
        adjusted_value: 2.0
        adjusted_unit: "hoppers/hill"
    status: "SOURCE_SUPPORTED_WITH_CONTEXT"
    exact_source_text: "Vegetative: 10-15 hoppers/hill"
  - record_id: "ETL-010"
    stage: "reproductive"
    threshold:
      base:
        metric: "hoppers_per_hill"
        operator: ">="
        value: 20.0
        unit: "hoppers/hill"
      modifier:
        condition: "post_heading_diminished_virus_transmission_risk"
        adjusted_value: 20.0
        adjusted_unit: "hoppers/hill"
    status: "SOURCE_SUPPORTED_WITH_CONTEXT"
    exact_source_text: "Reproductive: 20 hoppers/hill"

chemical_prescriptions:
  - chemical: "Imidacloprid"
    formulation: "17.8 SL"
    dose: "100 ml/ha"
    regulatory_status: "VERIFIED_CURRENT"
    evidence_status: "SOURCE_SUPPORTED_CIBRC_ALIGNED"
    notes: "CIBRC approved for rice leafhoppers at 100-125 ml/ha in 500 L water. Suppresses vector population to prevent Tungro spread. PHI: 21 days."
---

# ICAR Rice Production Manual: Green Leafhopper (GLH)

## 1. Overview & Crop Stages Affected
Green leafhopper (*Nephotettix virescens*) infests paddy across all growth stages. Direct feeding causes foliage yellowing, but its primary economic significance lies in its role as the active vector transmitting Rice Tungro Virus (RTV), making early management in nursery and vegetative stages critical.

## 2. Distinguishing Field Identification Cues
- Slender, bright-green wedge-shaped insect with distinct black markings on the head and forewings.
- Extreme jumping and flying agility when disturbed in the canopy.
- Foliage yellowing beginning from leaf tips and extending downwards along margins.
- Stunted plant growth accompanied by orange-yellow leaf discoloration if Rice Tungro Virus is co-transmitted.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Seedling Stage**: 5 hoppers per hill (`SOURCE_SUPPORTED_WITH_CONTEXT`). *Context Modifier: In Rice Tungro Virus (RTV) endemic tracts, threshold drops to 1–2 hoppers per hill.*
- **Vegetative Stage**: 10 to 15 hoppers per hill (`SOURCE_SUPPORTED_WITH_CONTEXT`). *Context Modifier: Drops to 2 hoppers per hill if active virus infection is present in neighboring plots.*
- **Reproductive Stage**: 20 hoppers per hill (`SOURCE_SUPPORTED_WITH_CONTEXT`). *Context Modifier: Direct feeding threshold post-heading when virus transmission risk diminishes.*

## 4. Integrated Management & Control Practices
- **Cultural & Varietal Control**: Adopt resistant rice cultivars like CO 51. Remove collateral weed hosts (*Leersia hexandra*, *Cyperus*) along bunds and irrigation channels.
- **Preventive Management**: Apply neem-based insecticidal formulations (Azadirachtin) as preventive repellant.
- **Chemical Control (Validated)**: Apply Imidacloprid 17.8 SL @ 100–125 ml/ha (`VERIFIED_CURRENT`, PHI: 21 days) to suppress vector populations and prevent virus transmission.

## 5. Regulatory & Validation Status
- Chemical Advice Status: Imidacloprid 17.8 SL is **VERIFIED_CURRENT** (CIBRC approved on rice).
- ETL Validation Status: **SOURCE_SUPPORTED_WITH_CONTEXT** (virus vector modifier documented).
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
