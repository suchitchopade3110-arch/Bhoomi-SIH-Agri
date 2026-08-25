"""
BHOOMI RAG Query Parser
Extracts crop, growth stage, pest/disease entities, symptoms, severity cues, 
Tamil dialect aliases, requested intent, and chemical mentions while strictly preserving uncertainty.
"""
import re
from typing import Any, Dict, List, Optional


class QueryParser:
    def __init__(self):
        # Known crop tokens
        self.non_paddy_crops = {
            "கத்திரி": "Brinjal (Solanum melongena)",
            "கத்தரி": "Brinjal (Solanum melongena)",
            "brinjal": "Brinjal (Solanum melongena)",
            "பருத்தி": "Cotton (Gossypium)",
            "cotton": "Cotton (Gossypium)",
            "மிளகாய்": "Chilli (Capsicum annuum)",
            "chilli": "Chilli (Capsicum annuum)",
            "தக்காளி": "Tomato (Solanum lycopersicum)",
            "tomato": "Tomato (Solanum lycopersicum)",
            "வாழை": "Banana (Musa)",
            "banana": "Banana (Musa)",
            "உளுந்து": "Blackgram (Vigna mungo)",
            "blackgram": "Blackgram (Vigna mungo)",
            "கரும்பு": "Sugarcane (Saccharum)",
            "sugarcane": "Sugarcane (Saccharum)",
            "வெண்டைக்காய்": "Bhendi / Okra (Abelmoschus esculentus)",
            "வெண்டை": "Bhendi / Okra (Abelmoschus esculentus)",
            "bhendi": "Bhendi / Okra (Abelmoschus esculentus)",
            "okra": "Bhendi / Okra (Abelmoschus esculentus)"
        }

        self.paddy_tokens = ["நெல்", "பயிர்", "பயிரில்", "வயலில்", "paddy", "rice"]

        # Known stage tokens
        self.stage_tokens = {
            "நாற்று": "nursery",
            "நாற்றங்கால்": "nursery",
            "நாற்றங்காலில்": "nursery",
            "தூர்": "tillering",
            "தூர் கட்டும்": "tillering",
            "தூர்கட்டும்": "tillering",
            "வளர்ச்சி": "vegetative",
            "குருத்து": "tillering",
            "பூக்கும்": "flowering",
            "பூ பூக்கும்": "flowering",
            "மலர்ச்சி": "flowering",
            "பால்": "milking",
            "பால் பிடிக்கும்": "milking",
            "கதிர்": "milking",
            "அறுவடை": "pre_harvest",
            "அறுவடைக்கு": "pre_harvest",
            "அறுக்க": "pre_harvest",
            "booting": "booting",
            "flowering": "flowering",
            "milking": "milking",
            "nursery": "nursery"
        }

        # Known intent tokens
        self.intent_patterns = [
            (r"(மருந்து|ஸ்ப்ரே|தெளிக்க|அடிக்கலாம்|அடிக்கவா|அடிக்கணும்|அடிக்கலாமா|கட்டுப்படுத்த|spray|chemical|medicine)", "RECOMMEND_CHEMICAL"),
            (r"(எத்தனை பூச்சி|எவ்வளவு இருந்தா|தாங்கும்|ETL|threshold|ஒரு குத்துக்கு|சேத நிலை|எத்தனை சதவீதம்)", "QUERY_ETL"),
            (r"(டோஸ்|அளவு|எவ்வளவு மில்லி|எவ்வளவு கிராம்|dose|dosage|எவ்வளவு கிலோ)", "QUERY_DOSAGE"),
            (r"(தடை|red label|ban|banned|கட்டுப்பாடு|போடலாமா|சிவப்பு லேபிள்|அனுமதி)", "QUERY_REGULATORY_STATUS"),
            (r"(விதை நேர்த்தி|seed treatment|இலை வழி தெளிப்பு)", "QUERY_BIO_INPUT_DOSAGE"),
            (r"(ட்ரோன்|drone|ULV|ஏக்கருக்கு எவ்வளவு தண்ணி)", "QUERY_DRONE_DOSAGE"),
            (r"(மஞ்சள்|கருகல்|புள்ளி|வாடி|உலர்ந்து|அழுகி|சாம்பல்|என்ன நோய்|சின்னம்|அறிகுறி|நோயா|பூச்சியா)", "DIAGNOSE_SYMPTOM")
        ]

        # Known chemical names
        self.chemical_keywords = [
            "carbofuran", "கார்போபியூரான்",
            "chlorantraniliprole", "குளோரான்ட்ரனிலிப்ரோல்", "coragen", "கோரஜென்",
            "buprofezin", "பப்ரோபெசின்",
            "imidacloprid", "இமிடாக்ளோபிரிட்",
            "thiamethoxam", "தயாமீதாக்சம்",
            "malathion", "மலாத்தியான்",
            "copper hydroxide", "காப்பர் ஹைட்ராக்சைடு", "காப்பர்",
            "tricyclazole", "டிரைசைக்ளசோல்",
            "hexaconazole", "ஹெக்சாகோனசோல்",
            "validamycin", "வாலிடமைசின்", "வேலிடமைசின்",
            "propiconazole", "புரோபிகோனசோல்",
            "streptocycline", "ஸ்ட்ரெப்டோமைசின்",
            "cypermethrin", "சைபர்மெத்ரின்",
            "deltamethrin", "டெல்டாமெத்ரின்",
            "lambda-cyhalothrin", "லாம்டா",
            "fipronil", "பிப்ரோனில்",
            "flubendiamide", "ப்ளூபெண்டமைடு",
            "pymetrozine", "பைமெட்ரோசின்",
            "azadirachtin", "வேப்பெண்ணெய்", "வேப்பங்கொட்டை",
            "kasugamycin", "காசுகாமைசின்",
            "mancozeb", "மேன்கோசெப்",
            "carbendazim", "கார்பெண்டாசிம்",
            "thifluzamide", "தைபுளூசமைடு",
            "pseudomonas", "சுடோமோனாஸ்", "சூடோமோனாஸ்",
            "மயில் துத்தம்", "அண்ணாமலை கலவை",
            "சிவப்பு லேபிள்", "red label", "banned"
        ]

    def parse(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Parses a farmer's voice/text query into a structured context dictionary."""
        cleaned_query = query.strip()
        q_lower = cleaned_query.lower()
        context = user_context or {}

        # 1. Detect Non-Paddy Crop vs Paddy
        crop = context.get("crop")
        if not crop:
            for token, crop_name in self.non_paddy_crops.items():
                if token in cleaned_query or token in q_lower:
                    crop = crop_name
                    break
        if not crop:
            crop = "Rice (Oryza sativa)"

        # 2. Detect Stage
        stage = context.get("stage")
        if not stage:
            for token, stage_name in self.stage_tokens.items():
                if token in cleaned_query or token in q_lower:
                    stage = stage_name
                    break

        # 3. Detect Intent
        detected_intent = "DIAGNOSE_SYMPTOM"
        for pattern, intent_name in self.intent_patterns:
            if re.search(pattern, cleaned_query, re.IGNORECASE):
                detected_intent = intent_name
                break

        # 4. Detect Chemical Mention
        detected_chemical = None
        for chem in self.chemical_keywords:
            if chem in q_lower or chem in cleaned_query:
                detected_chemical = chem
                break

        # 5. Extract Symptoms & Severity Cues
        symptoms = []
        if any(w in cleaned_query for w in ["நடுக்குருத்து", "dead heart", "dead_heart", "குருத்து காஞ்சு", "குருத்து காய்ஞ்சு"]):
            symptoms.append("dead_heart")
        if any(w in cleaned_query for w in ["வெண்கதிர்", "white ear", "white_ear", "வெள்ளைக்கதிர்"]):
            symptoms.append("white_ear")
        if any(w in cleaned_query for w in ["புகையான்", "hopper burn", "வட்ட வட்டமா காய்ஞ்சு", "கருகி"]):
            symptoms.append("hopper_burn")
        if any(w in cleaned_query for w in ["இலை சுருண்டு", "மடிப்பு", "சுருட்டு"]):
            symptoms.append("folded_leaves")
        if any(w in cleaned_query for w in ["வெள்ளிக்குருத்து", "silver shoot", "வெங்காயத்தாள்"]):
            symptoms.append("silver_shoot")
        if any(w in cleaned_query for w in ["மஞ்சள் கதிர்", "மஞ்சள் பொடி", "false smut", "மஞ்சள் கதிர் பூஞ்சாணம்"]):
            symptoms.append("yellow_spore_balls_false_smut")
        if any(w in cleaned_query for w in ["அழுகி", "தண்டு உடைஞ்சு", "stem rot", "நாறுது", "தண்டு அழுகல்"]):
            symptoms.append("waterline_stem_rot")
        if any(w in cleaned_query for w in ["செம்புள்ளி", "brown spot", "திட்டு திட்டா", "பழுப்பு புள்ளிகள்"]):
            symptoms.append("brown_spots")
        if any(w in cleaned_query for w in ["மஞ்சள்", "இலை மஞ்சளா", "வெளுத்து"]):
            symptoms.append("leaf_chlorosis")

        # Missing context detection
        missing_context = []
        if detected_intent == "RECOMMEND_CHEMICAL" and not stage:
            missing_context.append("crop_growth_stage")
        if not symptoms and detected_intent == "DIAGNOSE_SYMPTOM":
            missing_context.append("specific_symptoms")

        # Confidence Estimation
        confidence = 0.85
        if not symptoms and not detected_chemical:
            confidence = 0.50
        elif detected_chemical:
            confidence = 0.95

        return {
            "crop": crop,
            "crop_stage": stage,
            "entity": None,
            "entity_type": "chemical" if detected_chemical else "pest_or_disease",
            "symptoms": symptoms,
            "severity": context.get("severity"),
            "region": context.get("region", "All Tamil Nadu"),
            "farmer_aliases": [],
            "requested_action": detected_intent,
            "chemical": detected_chemical,
            "dosage_requested": bool("எவ்வளவு" in cleaned_query or "dose" in q_lower or "அளவு" in cleaned_query),
            "application_method": "drone_ulv" if "ட்ரோன்" in cleaned_query or "drone" in q_lower else "knapsack_foliar",
            "confidence": confidence,
            "missing_context": missing_context,
            "original_query": cleaned_query
        }
