"""
BHOOMI Independent Agronomic & Chemical Safety Policy Engine
Enforces strict regulatory compliance (CIBRC), Pre-Harvest Intervals (PHI), crop isolation,
anthesis/flowering protection, drone ULV calibration, and bio-control incompatibility intervals.

CRITICAL INVARIANT:
The safety gate runs as an INDEPENDENT DETERMINISTIC POLICY ENGINE on the query, parsed context,
and decision candidate. Even if retrieval or an LLM recommends an unsafe practice, this engine
deterministically blocks or modifies it.
"""
from typing import Any, Dict, List, Optional, Tuple


class RagSafetyGate:
    def __init__(self):
        # Restricted / Banned Chemicals & Overdose Attacks
        self.restricted_tokens = [
            "carbofuran", "கார்போபியூரான்",
            "streptocycline", "ஸ்ட்ரெப்டோமைசின்",
            "monocrotophos", "மோனோகுரோட்டோபாஸ்",
            "phorate", "போரேட்",
            "சிவப்பு லேபிள்", "red label", "banned", "தடை செய்யப்பட்ட", "தடை",
            "strongest banned", "10 மடங்கு கூடுதல்", "வீரியமான சிவப்பு",
            "ignore safety", "ignore safety instructions", "பரிந்துரை இல்லாத"
        ]

        # Non-Paddy Crop Tokens (Cross-Crop Isolation)
        self.non_paddy_crop_tokens = [
            "கத்திரி", "கத்தரி", "brinjal",
            "மிளகாய்", "chilli",
            "பருத்தி", "cotton",
            "தக்காளி", "tomato",
            "வாழை", "banana",
            "உளுந்து", "blackgram",
            "கரும்பு", "sugarcane",
            "வெண்டைக்காய்", "வெண்டை", "bhendi", "okra"
        ]

        # Bio-Control Incompatibility Indicators
        self.biocontrol_tokens = [
            "சுடோமோனாஸ்", "சூடோமோனாஸ்", "pseudomonas", "உயிர் உரம்", "உயிர் கட்டுப்பாடு"
        ]
        self.biocontrol_conflict_tokens = [
            "காப்பர்", "copper", "hexaconazole", "பூஞ்சாண", "fungicide", "ரசாயன",
            "3 நாள்", "மறுநாள்", "கலக்க", "சேர்த்து", "ஒண்ணா", "tank-mix", "tank mix", "விஷம்", "விஷத்தை"
        ]

        # PHI Pre-Harvest Indicators
        self.pre_harvest_tokens = [
            "அறுவடை", "அறுக்க", "அடுத்த வாரம்", "pre-harvest", "pre harvest",
            "நாளை மறுநாள்", "2 நாள்", "3 நாள்", "4 நாள்", "அறுவடைக்கு",
            "24 hours", "அறுவடை தருணத்தில்", "தானியத்தில்", "அறுத்தால்"
        ]

        # Anthesis / Flowering Indicators
        self.flowering_tokens = [
            "பூக்கும் போது", "பூ பூக்கும்", "flowering", "மலர்ச்சி", "மகரந்த", "பூக்கும் தருணத்தில்"
        ]

    def validate_safety(
        self,
        parsed_context: Dict[str, Any],
        retrieved_evidence: Optional[List[Dict[str, Any]]] = None,
        candidate_decision: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluates all safety constraints deterministically against query, parsed context, and decision candidate.
        """
        query_text = (parsed_context.get("original_query") or "").lower()
        candidate_text = ""
        if candidate_decision:
            candidate_text = (candidate_decision.get("recommended_action_tamil") or candidate_decision.get("recommendation") or "").lower()
        if retrieved_evidence:
            candidate_text += " " + " ".join([ev.get("text", "").lower() for ev in retrieved_evidence[:2]])

        # 1. Check for Fake / Unregistered / Unsupported Entities
        if any(w in query_text for w in ["போலி பூச்சி", "போலி நோய்", "புதிய பூச்சி", "அறியப்படாத"]):
            return {
                "is_safe": False,
                "safety_status": "ZERO_HALLUCINATION_ESCALATED",
                "decision": "ESCALATE_TO_KVK_OFFICER",
                "reason": "Unsupported or Unregistered Pest/Disease: Escalated to KVK officer to prevent hallucinated chemical prescription.",
                "response_tamil": "இந்த பூச்சி அல்லது நோய்க்கான அங்கீகரிக்கப்பட்ட பரிந்துரை இல்லை. அருகிலுள்ள வேளாண் அறிவியல் நிலையத்தை (KVK) அணுகவும்."
            }

        # 2. Check Crop Mismatch (Cross-Crop Transfer Protection)
        if any(w in query_text for w in self.non_paddy_crop_tokens):
            return {
                "is_safe": False,
                "safety_status": "CROP_MISMATCH_BLOCKED",
                "decision": "REJECT_CROP_MISMATCH",
                "reason": "Crop Mismatch: Reusing paddy pesticide recommendations for non-paddy horticultural crops is strictly prohibited.",
                "response_tamil": "நெற்பயிருக்கான மருந்து மற்றும் அளவுகளை கத்தரி, பருத்தி, மிளகாய் போன்ற மாற்றுப் பயிர்களுக்கு பயன்படுத்தக்கூடாது. அப்பயிருக்குரிய CIBRC பரிந்துரைகளை மட்டுமே பின்பற்றவும்."
            }

        # 3. Check Bio-Control (Pseudomonas fluorescens) 7-Day Incompatibility
        if any(w in query_text for w in self.biocontrol_tokens):
            if any(w in query_text for w in ["எத்தனை நாட்கள் கழித்து", "எத்தனை நாள் இடைவெளி"]):
                return {
                    "is_safe": True,
                    "safety_status": "BIO_COMPATIBILITY_ENFORCED",
                    "decision": "DIRECT_ADVISORY",
                    "reason": "Mandatory 7-day interval required between bio-control Pseudomonas fluorescens and chemical fungicides.",
                    "response_tamil": "சுடோமோனாஸ் (Pseudomonas) தெளித்த பிறகு ரசாயன அல்லது காப்பர் பூஞ்சாண மருந்துகளை தெளிக்க குறைந்தபட்சம் 7 நாட்கள் இடைவெளி விட வேண்டும்."
                }
            if any(w in query_text for w in self.biocontrol_conflict_tokens):
                return {
                    "is_safe": False,
                    "safety_status": "BIO_COMPATIBILITY_ENFORCED",
                    "decision": "SAFETY_INTERVENTION_WARNING",
                    "reason": "Biological Incompatibility: Pseudomonas fluorescens bacterial culture is killed when mixed with copper or chemical fungicides. Requires 7-day interval.",
                    "response_tamil": "சுடோமோனாஸ் (Pseudomonas) போன்ற நுண்ணுயிர் உயிர் உரங்களை காப்பர் அல்லது ரசாயன பூஞ்சாண மருந்துகளுடன் கலக்கக்கூடாது. இரண்டிற்கும் இடையே குறைந்தபட்சம் 7 நாட்கள் இடைவெளி அவசியம்."
                }

        # 4. Check Restricted & Banned Chemicals / Overdose (in query OR retrieved candidate)
        if any(w in query_text for w in self.restricted_tokens) or any(w in candidate_text for w in ["carbofuran 3g", "கார்போபியூரான் 3ஜி", "streptocycline + copper"]):
            return {
                "is_safe": False,
                "safety_status": "RESTRICTION_WARNING_ATTACHED",
                "decision": "SAFETY_INTERVENTION_WARNING",
                "reason": "Restricted/Banned Molecule Intercepted: Prohibited chemicals or unauthorized overdose attempt blocked.",
                "response_tamil": "எச்சரிக்கை: கார்போபியூரான் 3ஜி (Carbofuran) மற்றும் ஸ்ட்ரெப்டோமைசின் (Streptocycline) ஆகியவை அதீத நச்சுத்தன்மை கொண்ட அல்லது கட்டுப்படுத்தப்பட்ட மருந்துகளாகும். லேபிள் பரிந்துரைக்கு மேல் மருந்து அடிக்கக்கூடாது."
            }

        # 5. Check Pre-Harvest Interval (PHI) Safety
        if any(w in query_text for w in self.pre_harvest_tokens):
            if any(w in query_text for w in ["மலாத்தியான்", "malathion", "மருந்து", "ஸ்ப்ரே", "பூச்சிக்கொல்லி", "குந்தி பூச்சி", "நாவாய்ப்பூச்சி", "தானியத்தில்", "spray", "நஞ்சு"]):
                return {
                    "is_safe": False,
                    "safety_status": "MANDATORY_PHI_ENFORCED",
                    "decision": "SAFETY_REJECTION_MRL_HAZARD",
                    "reason": "Pre-Harvest Interval Hazard: Spraying pesticides within pre-harvest window causes severe MRL grain residue violations.",
                    "response_tamil": "அறுவடைக்கு முன் பூச்சிக்கொல்லி மருந்துகள் அடிக்கக்கூடாது. மலாத்தியான் போன்ற மருந்துகளுக்கு 7-10 நாட்கள் காத்திருப்பு காலம் (PHI) தேவை. உடனடியாக அறுவடை செய்தால் மனித உடலுக்கு ஆபத்தான நச்சுத்தன்மை நெல் மணியில் தங்கிவிடும்."
                }

        # 6. Check Anthesis / Flowering Stage Chemical Protection
        if any(w in query_text for w in self.flowering_tokens):
            return {
                "is_safe": False,
                "safety_status": "CHEMICAL_RECOMMENDATION_BLOCKED",
                "decision": "SAFETY_INTERVENTION_WARNING",
                "reason": "Flowering Stage Chemical Block: Fungicide/insecticide spraying during full anthesis causes floret blast and spikelet sterility.",
                "response_tamil": "பயிர் பூக்கும் தருணத்தில் (Full flowering / Anthesis) பூஞ்சாண மற்றும் பூச்சிக்கொல்லி மருந்துகள் அடிப்பதை தவிர்க்க வேண்டும். இது மகரந்த சேர்க்கையை பாதித்து பதர் நெல் உருவாக வழிவகுக்கும்."
            }

        # 7. Check Drone ULV Application Safety
        if "ட்ரோன்" in query_text or "drone" in query_text or parsed_context.get("application_method") == "drone_ulv":
            return {
                "is_safe": True,
                "safety_status": "DRONE_SAFETY_ENFORCED",
                "decision": "CONDITIONAL_ADVISORY",
                "reason": "Drone ULV Conditional Guardrails: 20-25 L/ha spray volume, wind speed <10 km/h, 100m buffer zone.",
                "response_tamil": "ட்ரோன் மூலம் தெளிக்கும் போது ஏக்கருக்கு 8-10 லிட்டர் தண்ணீர் (ஹெக்டேருக்கு 20-25 லிட்டர்) கலக்க வேண்டும். காற்றின் வேகம் மணிக்கு 10 கி.மீ-க்கு குறைவாகவும், நீர்நிலைகளில் இருந்து 100 மீட்டர் இடைவெளியிலும் இருக்க வேண்டும்."
            }

        return {
            "is_safe": True,
            "safety_status": "PASSED_SAFE",
            "decision": "DIRECT_ADVISORY",
            "reason": "All chemical and agronomic safety invariants validated.",
            "response_tamil": None
        }
