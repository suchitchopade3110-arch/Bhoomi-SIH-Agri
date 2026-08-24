"""
BHOOMI RAG Query Expander
Expands parsed farmer queries with verified Tamil aliases, canonical names, scientific binomials,
and regional hotwords while safeguarding against ambiguous terms (e.g. 'மட்ட பூச்சி').
"""
from typing import Any, Dict, List, Set, Tuple


class QueryExpander:
    def __init__(self, knowledge_version: str = "v4.2.0-validated"):
        self.knowledge_version = knowledge_version

        # Verified Production Aliases and Entities
        self.alias_mappings = {
            # Gall Midge
            "வெள்ளைக்குருத்து பூச்சி": {"entity_id": "PEST_005", "canonical_name": "Gall midge", "scientific_name": "Orseolia oryzae", "tamil_canonical": "ஆணைக்கொம்பன்"},
            "வெள்ளைக்குருத்து": {"entity_id": "PEST_005", "canonical_name": "Gall midge", "scientific_name": "Orseolia oryzae", "tamil_canonical": "ஆணைக்கொம்பன்"},
            "வெள்ளிக்குருத்து": {"entity_id": "PEST_005", "canonical_name": "Gall midge", "scientific_name": "Orseolia oryzae", "tamil_canonical": "ஆணைக்கொம்பன்"},
            "ஆணைக்கொம்பன்": {"entity_id": "PEST_005", "canonical_name": "Gall midge", "scientific_name": "Orseolia oryzae", "tamil_canonical": "ஆணைக்கொம்பன்"},
            "gall midge": {"entity_id": "PEST_005", "canonical_name": "Gall midge", "scientific_name": "Orseolia oryzae", "tamil_canonical": "ஆணைக்கொம்பன்"},

            # Earhead Bug
            "குந்தி பூச்சி": {"entity_id": "PEST_008", "canonical_name": "Earhead bug", "scientific_name": "Leptocorisa acuta", "tamil_canonical": "கதிர் நாவாய்ப்பூச்சி"},
            "கதிர் நாவாய்ப்பூச்சி": {"entity_id": "PEST_008", "canonical_name": "Earhead bug", "scientific_name": "Leptocorisa acuta", "tamil_canonical": "கதிர் நாவாய்ப்பூச்சி"},
            "நாவாய்ப்பூச்சி": {"entity_id": "PEST_008", "canonical_name": "Earhead bug", "scientific_name": "Leptocorisa acuta", "tamil_canonical": "கதிர் நாவாய்ப்பூச்சி"},
            "சாற்றுப்பூச்சி": {"entity_id": "PEST_008", "canonical_name": "Earhead bug", "scientific_name": "Leptocorisa acuta", "tamil_canonical": "கதிர் நாவாய்ப்பூச்சி"},
            "earhead bug": {"entity_id": "PEST_008", "canonical_name": "Earhead bug", "scientific_name": "Leptocorisa acuta", "tamil_canonical": "கதிர் நாவாய்ப்பூச்சி"},
            "gundhi bug": {"entity_id": "PEST_008", "canonical_name": "Earhead bug", "scientific_name": "Leptocorisa acuta", "tamil_canonical": "கதிர் நாவாய்ப்பூச்சி"},

            # Stem Borer
            "தண்டு துளைப்பான்": {"entity_id": "PEST_001", "canonical_name": "Stem borer", "scientific_name": "Scirpophaga incertulas", "tamil_canonical": "தண்டு துளைப்பான்"},
            "குருத்துப் பூச்சி": {"entity_id": "PEST_001", "canonical_name": "Stem borer", "scientific_name": "Scirpophaga incertulas", "tamil_canonical": "தண்டு துளைப்பான்"},
            "நடுக்குருத்து": {"entity_id": "PEST_001", "canonical_name": "Stem borer", "scientific_name": "Scirpophaga incertulas", "tamil_canonical": "தண்டு துளைப்பான்"},
            "வெண்கதிர்": {"entity_id": "PEST_001", "canonical_name": "Stem borer", "scientific_name": "Scirpophaga incertulas", "tamil_canonical": "தண்டு துளைப்பான்"},
            "வெள்ளைக்கதிர்": {"entity_id": "PEST_001", "canonical_name": "Stem borer", "scientific_name": "Scirpophaga incertulas", "tamil_canonical": "தண்டு துளைப்பான்"},
            "stem borer": {"entity_id": "PEST_001", "canonical_name": "Stem borer", "scientific_name": "Scirpophaga incertulas", "tamil_canonical": "தண்டு துளைப்பான்"},

            # BPH
            "புகையான்": {"entity_id": "PEST_002", "canonical_name": "Brown planthopper (BPH)", "scientific_name": "Nilaparvata lugens", "tamil_canonical": "புகையான்"},
            "பழுப்பு தத்துப்பூச்சி": {"entity_id": "PEST_002", "canonical_name": "Brown planthopper (BPH)", "scientific_name": "Nilaparvata lugens", "tamil_canonical": "புகையான்"},
            "bph": {"entity_id": "PEST_002", "canonical_name": "Brown planthopper (BPH)", "scientific_name": "Nilaparvata lugens", "tamil_canonical": "புகையான்"},
            "brown planthopper": {"entity_id": "PEST_002", "canonical_name": "Brown planthopper (BPH)", "scientific_name": "Nilaparvata lugens", "tamil_canonical": "புகையான்"},
            "hopper burn": {"entity_id": "PEST_002", "canonical_name": "Brown planthopper (BPH)", "scientific_name": "Nilaparvata lugens", "tamil_canonical": "புகையான்"},

            # Leaf Folder
            "இலை சுருட்டு புழு": {"entity_id": "PEST_003", "canonical_name": "Leaf folder", "scientific_name": "Cnaphalocrocis medinalis", "tamil_canonical": "இலை சுருட்டு புழு"},
            "சுருட்டுப் புழு": {"entity_id": "PEST_003", "canonical_name": "Leaf folder", "scientific_name": "Cnaphalocrocis medinalis", "tamil_canonical": "இலை சுருட்டு புழு"},
            "இலை சுருட்டு": {"entity_id": "PEST_003", "canonical_name": "Leaf folder", "scientific_name": "Cnaphalocrocis medinalis", "tamil_canonical": "இலை சுருட்டு புழு"},
            "leaf folder": {"entity_id": "PEST_003", "canonical_name": "Leaf folder", "scientific_name": "Cnaphalocrocis medinalis", "tamil_canonical": "இலை சுருட்டு புழு"},

            # GLH
            "பச்சை தத்துப்பூச்சி": {"entity_id": "PEST_004", "canonical_name": "Green leafhopper (GLH)", "scientific_name": "Nephotettix virescens", "tamil_canonical": "பச்சை தத்துப்பூச்சி"},
            "glh": {"entity_id": "PEST_004", "canonical_name": "Green leafhopper (GLH)", "scientific_name": "Nephotettix virescens", "tamil_canonical": "பச்சை தத்துப்பூச்சி"},
            "green leafhopper": {"entity_id": "PEST_004", "canonical_name": "Green leafhopper (GLH)", "scientific_name": "Nephotettix virescens", "tamil_canonical": "பச்சை தத்துப்பூச்சி"},

            # Thrips
            "இலைப்பேன்": {"entity_id": "PEST_006", "canonical_name": "Thrips", "scientific_name": "Stenchaetothrips biformis", "tamil_canonical": "இலைப்பேன்"},
            "சுருள் பேன்": {"entity_id": "PEST_006", "canonical_name": "Thrips", "scientific_name": "Stenchaetothrips biformis", "tamil_canonical": "இலைப்பேன்"},
            "thrips": {"entity_id": "PEST_006", "canonical_name": "Thrips", "scientific_name": "Stenchaetothrips biformis", "tamil_canonical": "இலைப்பேன்"},

            # Whorl Maggot
            "வோர்ல் மேகட்": {"entity_id": "PEST_007", "canonical_name": "Whorl maggot", "scientific_name": "Hydrellia philippina", "tamil_canonical": "குருத்து ஈ"},
            "குருத்து ஈ": {"entity_id": "PEST_007", "canonical_name": "Whorl maggot", "scientific_name": "Hydrellia philippina", "tamil_canonical": "குருத்து ஈ"},
            "whorl maggot": {"entity_id": "PEST_007", "canonical_name": "Whorl maggot", "scientific_name": "Hydrellia philippina", "tamil_canonical": "குருத்து ஈ"},

            # Diseases
            "பாக்டீரியா இலைக்கருகல்": {"entity_id": "DIS_001", "canonical_name": "Bacterial Leaf Blight", "scientific_name": "Xanthomonas oryzae pv. oryzae", "tamil_canonical": "பாக்டீரியா இலைக்கருகல்"},
            "blb": {"entity_id": "DIS_001", "canonical_name": "Bacterial Leaf Blight", "scientific_name": "Xanthomonas oryzae pv. oryzae", "tamil_canonical": "பாக்டீரியா இலைக்கருகல்"},
            "குலை நோய்": {"entity_id": "DIS_002", "canonical_name": "Rice Blast", "scientific_name": "Magnaporthe oryzae", "tamil_canonical": "குலை நோய்"},
            "blast": {"entity_id": "DIS_002", "canonical_name": "Rice Blast", "scientific_name": "Magnaporthe oryzae", "tamil_canonical": "குலை நோய்"},
            "கழுத்து குலை": {"entity_id": "DIS_002", "canonical_name": "Rice Blast", "scientific_name": "Magnaporthe oryzae", "tamil_canonical": "குலை நோய்"},
            "neck blast": {"entity_id": "DIS_002", "canonical_name": "Rice Blast", "scientific_name": "Magnaporthe oryzae", "tamil_canonical": "குலை நோய்"},
            "மடல்கருகல்": {"entity_id": "DIS_003", "canonical_name": "Sheath Blight", "scientific_name": "Rhizoctonia solani", "tamil_canonical": "மடல்கருகல்"},
            "மடல் கருகல்": {"entity_id": "DIS_003", "canonical_name": "Sheath Blight", "scientific_name": "Rhizoctonia solani", "tamil_canonical": "மடல்கருகல்"},
            "sheath blight": {"entity_id": "DIS_003", "canonical_name": "Sheath Blight", "scientific_name": "Rhizoctonia solani", "tamil_canonical": "மடல்கருகல்"},
            "துங்ரோ": {"entity_id": "DIS_004", "canonical_name": "Rice Tungro Virus", "scientific_name": "RTBV & RTSV", "tamil_canonical": "துங்ரோ வைரஸ் நோய்"},
            "tungro": {"entity_id": "DIS_004", "canonical_name": "Rice Tungro Virus", "scientific_name": "RTBV & RTSV", "tamil_canonical": "துங்ரோ வைரஸ் நோய்"},
            "மஞ்சள் கதிர் பூஞ்சாணம்": {"entity_id": "DIS_007", "canonical_name": "Rice False Smut", "scientific_name": "Ustilaginoidea virens", "tamil_canonical": "மஞ்சள் கதிர் பூஞ்சாணம்"},
            "false smut": {"entity_id": "DIS_007", "canonical_name": "Rice False Smut", "scientific_name": "Ustilaginoidea virens", "tamil_canonical": "மஞ்சள் கதிர் பூஞ்சாணம்"},
            "மஞ்சள் கதிர்": {"entity_id": "DIS_007", "canonical_name": "Rice False Smut", "scientific_name": "Ustilaginoidea virens", "tamil_canonical": "மஞ்சள் கதிர் பூஞ்சாணம்"},
            "தண்டு அழுகல்": {"entity_id": "DIS_006", "canonical_name": "Rice Stem Rot", "scientific_name": "Sclerotium oryzae", "tamil_canonical": "தண்டு அழுகல்"},
            "stem rot": {"entity_id": "DIS_006", "canonical_name": "Rice Stem Rot", "scientific_name": "Sclerotium oryzae", "tamil_canonical": "தண்டு அழுகல்"},
            "மடல் அழுகல்": {"entity_id": "DIS_007", "canonical_name": "Sheath Rot", "scientific_name": "Sarocladium oryzae", "tamil_canonical": "மடல் அழுகல்"},
            "sheath rot": {"entity_id": "DIS_007", "canonical_name": "Sheath Rot", "scientific_name": "Sarocladium oryzae", "tamil_canonical": "மடல் அழுகல்"},
            "செம்புள்ளி": {"entity_id": "DIS_008", "canonical_name": "Brown Spot", "scientific_name": "Bipolaris oryzae", "tamil_canonical": "செம்புள்ளி நோய்"},
            "brown spot": {"entity_id": "DIS_008", "canonical_name": "Brown Spot", "scientific_name": "Bipolaris oryzae", "tamil_canonical": "செம்புள்ளி நோய்"},
            "இலைக்கோடு": {"entity_id": "DIS_009", "canonical_name": "Bacterial Leaf Streak", "scientific_name": "Xanthomonas oryzae pv. oryzicola", "tamil_canonical": "பாக்டீரியா இலைக்கோடு"},
            "bls": {"entity_id": "DIS_009", "canonical_name": "Bacterial Leaf Streak", "scientific_name": "Xanthomonas oryzae pv. oryzicola", "tamil_canonical": "பாக்டீரியா இலைக்கோடு"},

            # Traditional Inputs & Chemicals
            "மயில் துத்தம்": {"entity_id": "AGRO_INPUT_COPPER_SULPHATE", "canonical_name": "Copper Sulphate (CuSO4)", "scientific_name": "CuSO4", "tamil_canonical": "மயில் துத்தம்"},
            "அண்ணாமலை கலவை": {"entity_id": "AGRO_NUTRITION_IRON_CHLOROSIS", "canonical_name": "Iron Chlorosis Foliar Mixture", "scientific_name": "FeSO4 + (NH4)2SO4", "tamil_canonical": "அண்ணாமலை கலவை"},
            "சுடோமோனாஸ்": {"entity_id": "CHEM_CHEM-015", "canonical_name": "Pseudomonas fluorescens", "scientific_name": "Pseudomonas fluorescens", "tamil_canonical": "சுடோமோனாஸ்"},
            "சூடோமோனாஸ்": {"entity_id": "CHEM_CHEM-015", "canonical_name": "Pseudomonas fluorescens", "scientific_name": "Pseudomonas fluorescens", "tamil_canonical": "சுடோமோனாஸ்"},
            "pseudomonas": {"entity_id": "CHEM_CHEM-015", "canonical_name": "Pseudomonas fluorescens", "scientific_name": "Pseudomonas fluorescens", "tamil_canonical": "சுடோமோனாஸ்"},
            "chlorantraniliprole": {"entity_id": "CHEM_CHEM-001", "canonical_name": "Chlorantraniliprole 18.5 SC", "scientific_name": "Chlorantraniliprole", "tamil_canonical": "குளோரான்ட்ரனிலிப்ரோல்"},
            "coragen": {"entity_id": "CHEM_CHEM-001", "canonical_name": "Chlorantraniliprole 18.5 SC", "scientific_name": "Chlorantraniliprole", "tamil_canonical": "கோரஜென்"},
            "கோரஜென்": {"entity_id": "CHEM_CHEM-001", "canonical_name": "Chlorantraniliprole 18.5 SC", "scientific_name": "Chlorantraniliprole", "tamil_canonical": "கோரஜென்"},
            "buprofezin": {"entity_id": "CHEM_CHEM-002", "canonical_name": "Buprofezin 25 SC", "scientific_name": "Buprofezin", "tamil_canonical": "பப்ரோபெசின்"},
            "பப்ரோபெசின்": {"entity_id": "CHEM_CHEM-002", "canonical_name": "Buprofezin 25 SC", "scientific_name": "Buprofezin", "tamil_canonical": "பப்ரோபெசின்"},
            "thiamethoxam": {"entity_id": "CHEM_CHEM-004", "canonical_name": "Thiamethoxam 25 WG", "scientific_name": "Thiamethoxam", "tamil_canonical": "தயாமீதாக்சம்"},
            "தயாமீதாக்சம்": {"entity_id": "CHEM_CHEM-004", "canonical_name": "Thiamethoxam 25 WG", "scientific_name": "Thiamethoxam", "tamil_canonical": "தயாமீதாக்சம்"},
            "copper hydroxide": {"entity_id": "CHEM_CHEM-007", "canonical_name": "Copper Hydroxide 77 WP", "scientific_name": "Copper Hydroxide", "tamil_canonical": "காப்பர் ஹைட்ராக்சைடு"},
            "காப்பர் ஹைட்ராக்சைடு": {"entity_id": "CHEM_CHEM-007", "canonical_name": "Copper Hydroxide 77 WP", "scientific_name": "Copper Hydroxide", "tamil_canonical": "காப்பர் ஹைட்ராக்சைடு"},
            "tricyclazole": {"entity_id": "CHEM_CHEM-008", "canonical_name": "Tricyclazole 75 WP", "scientific_name": "Tricyclazole", "tamil_canonical": "டிரைசைக்ளசோல்"},
            "டிரைசைக்ளசோல்": {"entity_id": "CHEM_CHEM-008", "canonical_name": "Tricyclazole 75 WP", "scientific_name": "Tricyclazole", "tamil_canonical": "டிரைசைக்ளசோல்"}
        }

        # Candidate alias
        if knowledge_version == "v4.3.0-candidate":
            self.alias_mappings["வெங்காயத்தாள் புழு"] = {"entity_id": "PEST_005", "canonical_name": "Gall midge", "scientific_name": "Orseolia oryzae", "tamil_canonical": "ஆணைக்கொம்பன்"}

        # Ambiguous aliases (must route to clarification)
        self.ambiguous_terms = {
            "மட்ட பூச்சி": "Ambiguous Kongu dialect term (used for sheath mites or general sheath pests); requires symptom clarification"
        }

    def expand(self, parsed_context: Dict[str, Any]) -> Dict[str, Any]:
        """Expands the query context with canonical entities, scientific terms, and hotwords."""
        query_text = parsed_context.get("original_query", "")
        q_lower = query_text.lower()
        detected_aliases = []
        canonical_entities = []
        scientific_names = []
        entity_ids = []
        expanded_keywords: Set[str] = set()
        is_ambiguous_alias = False
        ambiguity_reason = None

        # 1. Check for ambiguous terms
        for ambig_term, reason in self.ambiguous_terms.items():
            if ambig_term in query_text:
                is_ambiguous_alias = True
                ambiguity_reason = reason
                detected_aliases.append(ambig_term)

        # 2. Check for verified aliases & terms
        for alias_term, data in self.alias_mappings.items():
            if alias_term in query_text or alias_term in q_lower:
                detected_aliases.append(alias_term)
                if data.get("canonical_name"):
                    canonical_entities.append(data["canonical_name"])
                    expanded_keywords.add(data["canonical_name"].lower())
                if data.get("scientific_name"):
                    scientific_names.append(data["scientific_name"])
                    expanded_keywords.add(data["scientific_name"].lower())
                if data.get("tamil_canonical"):
                    expanded_keywords.add(data["tamil_canonical"])
                if data.get("entity_id"):
                    entity_ids.append(data["entity_id"])

        # Add symptom expansions
        for sym in parsed_context.get("symptoms", []):
            if sym == "dead_heart":
                expanded_keywords.update(["dead heart", "நடுக்குருத்து", "stem borer", "scirpophaga incertulas", "PEST_001"])
            elif sym == "hopper_burn":
                expanded_keywords.update(["hopper burn", "புகையான்", "bph", "nilaparvata lugens", "PEST_002"])
            elif sym == "silver_shoot":
                expanded_keywords.update(["silver shoot", "வெள்ளிக்குருத்து", "gall midge", "orseolia oryzae", "PEST_005"])
            elif sym == "folded_leaves":
                expanded_keywords.update(["folded leaves", "இலை சுருட்டு", "cnaphalocrocis medinalis", "PEST_003"])
            elif sym == "yellow_spore_balls_false_smut":
                expanded_keywords.update(["false smut", "ustilaginoidea virens", "மஞ்சள் கதிர் பூஞ்சாணம்", "DIS_007"])
            elif sym == "waterline_stem_rot":
                expanded_keywords.update(["stem rot", "sclerotium oryzae", "தண்டு அழுகல்", "DIS_006"])

        # Add chemical expansions
        if parsed_context.get("chemical"):
            expanded_keywords.add(parsed_context["chemical"].lower())

        # Construct expanded query string
        expanded_query_terms = list(expanded_keywords)
        expanded_search_query = f"{query_text} " + " ".join(expanded_query_terms)

        result = dict(parsed_context)
        result["farmer_aliases"] = detected_aliases
        result["expanded_canonical_entities"] = canonical_entities
        result["expanded_scientific_names"] = scientific_names
        result["expanded_entity_ids"] = entity_ids
        result["expanded_keywords"] = expanded_query_terms
        result["expanded_search_query"] = expanded_search_query.strip()
        result["is_ambiguous_alias"] = is_ambiguous_alias
        result["ambiguity_reason"] = ambiguity_reason

        return result
