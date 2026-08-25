---
pest_name: "Thrips"
crop: "Rice (Oryza sativa)"
scientific_name: "Stenchaetothrips biformis"
category: "Insect Pest"
tamil_name: "இலைப்பேன்"
aliases:
  - "Rice thrips"
  - "சுருள் பேன்"
  - "Paddy thrips"
  - "Nursery thrips"
source_organization: "KVK / TNAU"
source_title: "KVK Rice Nursery Management — Thrips Control"
source_url: "https://kvk.icar.gov.in/"
review_date: "2026-08-24"
authority_level: "Medium-High (ICAR Krishi Vigyan Kendra Advisory - Authority Tier 7)"
---

# KVK Rice Nursery Management: Thrips Control

## 1. Identification
Rice thrips (*Stenchaetothrips biformis*) is a tiny, highly destructive lacerating and sucking insect pest of rice seedlings in nursery beds and newly transplanted fields across Tamil Nadu, particularly under dry weather and water deficit stress.

Farmers and nursery managers can identify the pest through the following features:
- **Adult Thrips**: Minute, slender, elongated insect (1.0 to 1.5 mm long) with a dark brown to blackish body. Adults possess two pairs of narrow, strap-like wings fringed with long, fine hairs ("fringed wings").
- **Nymphs**: Very tiny, wingless, soft-bodied, translucent-white to pale yellow insects found actively crawling on the inner surface of folded leaves.
- **Eggs**: Microscopic, bean-shaped, pale yellow eggs inserted individually into the leaf tissue of tender seedlings.

## 2. Distinguishing Cues
Thrips damage is distinguished from drought stress, mite feeding, and other sucking pests by the following diagnostic signs:
- **Silvery Streaks & Inward Leaf Curling**: Lacerated leaf tissues exhibit distinct yellowish to silvery-white longitudinal streaks on the upper surface. The leaf margins curl inward from the sides toward the midrib, forming tightly rolled needle-like tubes.
- **Withered Burnt Tips**: Leaf tips turn brown, dry up, and curl into tight corkscrews, giving the nursery bed a dry, reddish-brown or scorched appearance.
- **Water Submersion Response**: Unlike true drought stress which affects the entire plant uniformly, floating curled leaves on water or submerging them reveals tiny yellow nymphs crawling out within seconds.

## 3. Symptoms and Field Signs
- **Epidermal Laceration & Sap Desiccation**: Both nymphs and adults use their asymmetrical piercing-rasping mouthparts to lacerate the epidermal cells of tender leaves and imbibe the exuding sap.
- **Stunted Seedling Growth**: Affected seedlings in nursery beds stop growing, fail to tiller normally, and become severely stunted, delaying transplanting operations.
- **Burnt Nursery Patches (இலைப்பேன் கருகல்)**: Infested nursery beds develop dry, scorched, yellowish-brown patches that can lead to total seedling mortality if unmanaged during dry spells.

## 4. Life-Cycle and Relevant Biology
- **Oviposition**: A female thrips lays 30 to 50 eggs inside leaf epidermal tissues over 10 to 15 days. Incubation takes 3 to 5 days.
- **Nymphal Stages**: Nymphs develop through 2 feeding larval instars over 7 to 10 days, followed by non-feeding prepupal and pupal stages on the leaf or soil surface lasting 2 to 3 days.
- **Total Generation Time**: Entire life cycle is completed in 13 to 19 days, allowing rapid population buildup under hot, dry conditions ($>30^\circ\text{C}$ with low rainfall).
- **Water Sensitivity**: Thrips are highly sensitive to standing water and drowning; rainfall or continuous nursery flooding naturally knocks down populations.

## 5. Vulnerable Growth Stages
Thrips attack rice exclusively during the early stages of crop establishment:
- **Nursery / Seedling Stage (1 to 20 Days After Sowing)**: Peak danger zone; young succulent seedling leaves are highly prone to rolling and death.
- **Early Vegetative Stage (Up to 25 Days After Transplanting)**: Vulnerable during dry spells and moisture stress; recovers rapidly once tillering accelerates.
- **Reproductive & Maturing Stages**: Not susceptible; foliage is too tough for thrips feeding.

## 6. Economic Threshold Level (ETL)
Chemical intervention should be initiated when nursery or field scouting reaches the following source-quoted action thresholds:
- **ETL Classification**: `NUMERIC_ETL`
- **Seedling / Nursery Stage**: $\ge 5\text{ thrips per seedling}$ (`SOURCE_SUPPORTED`).
- **Vegetative (Tillering) Stage**: $\ge 25\text{ thrips per hill}$ (`SOURCE_SUPPORTED`).
- *Distinction from Severity*: ETL sets the actionable boundary for flooding or foliar application. Severity tracks the percentage of leaf roll drying and seedling stand mortality.

## 7. Severity Indicators
- **A. Observable Severity Indicators**:
  - *Early Severity*: Minute silvery spots on upper leaf surfaces; mild inward rolling of leaf tips ($1\text{–}4\text{ thrips/seedling}$ in nursery).
  - *Moderate Severity*: Conspicuous needle-like leaf rolling; tips drying and yellowing ($5\text{–}10\text{ thrips/seedling}$ in nursery or $10\text{–}25/\text{hill}$ at tillering).
  - *Severe Severity*: Extensive leaf curling and drying across seedling bed ($>25\text{ thrips/hill}$, $>50\%$ rolled leaves); scorched appearance of nursery.
  - *Catastrophic*: Complete nursery seedling mortality or field-wide dry-out with total loss of transplantable stand.
- **B. Quantitative Severity Thresholds**:
  - *KVK / TNAU Nursery Damage Scale*:
    - SES 1–3 (Early): $1\text{–}4\text{ thrips/seedling}$ in nursery (`SOURCE_SUPPORTED`).
    - SES 5 (Moderate): $5\text{–}10\text{ thrips/seedling}$ (nursery) or $10\text{–}25\text{ thrips/hill}$ (tillering) (`SOURCE_SUPPORTED`).
    - SES 7 (Severe): $>25\text{ thrips/hill}$, $>50\%$ rolled leaves (`SOURCE_SUPPORTED`).
    - SES 9 (Catastrophic): Complete nursery seedling collapse (`SOURCE_SUPPORTED`).
  - *Threshold Status*: `SOURCE_SUPPORTED` (KVK Extension Advisory).
  - *Internal Engine Penalty Mapping*: Early = 30, Moderate = 55, Severe = 80 (`PROJECT_DERIVED_RULE` for Farm Health Score sub-index).

## 8. Cultural and Mechanical Management
- **Nursery Submersion (Flooding)**: Completely submerge nursery beds under water for 24 to 48 hours to drown nymphs and adults, dislodging them from the leaves.
- **Adequate Irrigation**: Avoid allowing nursery beds or newly transplanted fields to dry out during the first 3 weeks.
- **Wet Nursery Method**: Adopt wet nursery sowing rather than dry nursery beds in thrips-prone tracts.
- **Neem Seed Kernel Extract (NSKE 5%)**: Spray NSKE 5% or neem oil @ 3 ml/L water as a preventive repellent at 10 days after sowing.

## 9. Biological Management
- **Predatory Spiders & Anthocorid Bugs**: Conserve minute pirate bugs (*Orius* spp.) and small linyphiid spiders, which consume thrips nymphs voraciously.
- **Ladybird Beetles & Mirid Bugs**: Protect predatory coccinellids and mirid bugs inhabiting the nursery margins.

## 10. Chemical Management
When thrips populations cross the Economic Threshold Level in nursery or main field, apply approved systemic insecticides in adequate spray volume (100 L water per 10 cents nursery, or 500 L/ha for main field):
- **Thiamethoxam 25 WG** @ 100 g/ha (40 g/acre) in 500 L water (`VERIFIED_CURRENT`). Highly systemic neonicotinoid; provides rapid translaminar protection to newly emerging leaf whorls; Pre-Harvest Interval (PHI): 14 days.
- **Imidacloprid 17.8 SL** @ 100 ml/ha (20 ml/acre) in 500 L water (`VERIFIED_CURRENT`). Rapid knockdown; PHI: 21 days.

## 11. Monitoring Guidance
- **Wet Palm Test (ஈர உள்ளங்கை முறை)**: Pass a wet palm across 10 to 15 seedlings in the nursery bed; count the number of tiny dark thrips adhering to the wet palm.
- **Blue Sticky Traps**: Set up blue sticky traps @ 2 per 10 cents nursery bed to monitor adult thrips population surges.
- **Visual Seedling Counting**: Inspect 10 seedlings chosen randomly from 5 distinct spots in the nursery.

## 12. Escalation and Decision Cues
Escalate immediately to the KVK Extension Officer or Block Agricultural Officer if:
- **Extensive Nursery Scorching**: Over 30% of seedlings in nursery beds show complete leaf drying and tip scorching.
- **Post-Flooding Survival**: Thrips remain active despite 48-hour continuous nursery submersion.
- **Transplanting Delay**: Seedling growth is delayed beyond 30 days due to unchecked thrips injury.

## 13. Source Citations
- **Primary Source**: ICAR Krishi Vigyan Kendra (KVK) Extension Advisory on Rice Nursery Protection and Thrips Management (`https://kvk.icar.gov.in/`).
- **Secondary Source**: TNAU Agritech Portal — Paddy Nursery Protection Guide.
- **Authority Level**: Tier 7 (ICAR KVK / Extension Protocol).

## 14. Review Metadata
- **Last Review Date**: 2026-08-24
- **Verification Date**: 2026-08-24
- **Next Scheduled Review**: 2027-02-24 (6-Month Cycle)
- **Publication Date**: Not exposed in source web portal (marked `not_exposed`).
- **Validation Status**: `SOURCE_DERIVED_VALIDATED`
