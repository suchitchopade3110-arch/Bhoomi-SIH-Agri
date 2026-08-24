"""
BHOOMI Tamil Voice & Multi-Dialect Retrieval Benchmark Dataset Generator
Generates exactly 500 structured test queries covering:
- Standard Tamil (75)
- Cauvery Delta Tamil (75)
- Kongu Tamil (75)
- Southern Tamil Nadu (75)
- Northern Tamil Nadu (75)
- Tanglish & Tamil-English Code Switching (50)
- Noisy ASR Transcripts & Phonetic Elisions (50)
- Ambiguous Rural Slang & Edge Cases (25)
Total: 500 test cases
"""
import json
import random
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def generate_500_tamil_voice_cases() -> List[Dict[str, Any]]:
    cases = []
    case_idx = 1

    # Base entity definitions
    entities = [
        ("PEST_001", "DOC-PEST-001", "Stem borer", "தண்டு துளைப்பான்", "Scirpophaga incertulas", ["நடுக்குருத்து", "வெண்கதிர்", "குருத்துப் பூச்சி", "dead heart"]),
        ("PEST_002", "DOC-PEST-002", "Brown planthopper (BPH)", "புகையான்", "Nilaparvata lugens", ["புகையான்", "வட்ட கருகல்", "hopper burn", "சாற்றுப்பூச்சி"]),
        ("PEST_003", "DOC-PEST-003", "Leaf folder", "இலை சுருட்டு புழு", "Cnaphalocrocis medinalis", ["இலை சுருட்டு", "மடிப்பு புழு", "சுருட்டுப் புழு", "folded leaf"]),
        ("PEST_004", "DOC-PEST-004", "Green leafhopper (GLH)", "பச்சை தத்துப்பூச்சி", "Nephotettix virescens", ["பச்சை தத்துப்பூச்சி", "துங்ரோ பரப்புது", "glh"]),
        ("PEST_005", "DOC-PEST-005", "Gall midge", "Gall midge", "Orseolia oryzae", ["ஆணைக்கொம்பன்", "வெள்ளைக்குருத்து பூச்சி", "வெள்ளிக்குருத்து", "வெங்காயத்தாள்"]),
        ("PEST_006", "DOC-PEST-006", "Thrips", "இலைப்பேன்", "Stenchaetothrips biformis", ["இலைப்பேன்", "சுருள் பேன்", "ஊசி இலை"]),
        ("PEST_007", "DOC-PEST-007", "Whorl maggot", "Whorl maggot", "Hydrellia philippina", ["குருத்து ஈ", "வோர்ல் மேகட்", "இலை விளிம்பு அறுபட்டது"]),
        ("PEST_008", "DOC-PEST-008", "Earhead bug", "Earhead bug", "Leptocorisa acuta", ["குந்தி பூச்சி", "கதிர் நாவாய்ப்பூச்சி", "சாற்றுப்பூச்சி", "துர்நாற்றம்"]),
        ("DIS_001", "DOC-DIS-001", "Bacterial Leaf Blight", "பாக்டீரியா இலைக்கருகல்", "Xanthomonas oryzae", ["அலை அலையான மஞ்சள் கருகல்", "பாக்டீரியா கருகல்", "blb"]),
        ("DIS_002", "DOC-DIS-002", "Rice Blast", "குலை நோய்", "Magnaporthe oryzae", ["கண் வடிவ புள்ளி", "கழுத்து குலை", "blast"]),
        ("DIS_003", "DOC-DIS-003", "Sheath Blight", "மடல்கருகல்", "Rhizoctonia solani", ["தண்டு மட்டை சாம்பல் திட்டு", "மடல் கருகல்", "sheath blight"]),
        ("DIS_004", "DOC-DIS-004", "Rice Tungro Virus", "துங்ரோ வைரஸ்", "RTBV / RTSV", ["இலை ஆரஞ்சு நிறம்", "பயிர் குட்டை"]),
        ("DIS_007", "DOC-DIS-007", "Rice False Smut", "மஞ்சள் கதிர் பூஞ்சாணம்", "Ustilaginoidea virens", ["மஞ்சள் பொடி உருண்டை", "false smut"]),
        ("DIS_006", "DOC-DIS-006", "Rice Stem Rot", "தண்டு அழுகல்", "Sclerotium oryzae", ["தண்டு அழுகி நாறுது", "stem rot"]),
        ("DIS_005", "DOC-DIS-005", "Brown Spot", "செம்புள்ளி நோய்", "Bipolaris oryzae", ["வட்ட பழுப்பு புள்ளிகள்", "brown spot"]),
        ("DIS_008", "DOC-DIS-008", "Bacterial Leaf Streak", "பாக்டீரியா இலைக்கோடு", "Xanthomonas oryzicola", ["ஒளி ஊடுருவும் கோடுகள்", "bls"])
    ]

    # 1. Standard Tamil (75 cases)
    for i in range(75):
        ent = entities[i % len(entities)]
        query_templates = [
            f"நெற்பயிரில் {ent[3]} தாக்குதல் அறிகுறி என்ன?",
            f"{ent[3]} கட்டுப்படுத்த CIBRC பரிந்துரைத்த மருந்து என்ன?",
            f"{ent[3]} பொருளாதார சேத நிலை (ETL) அளவு என்ன?",
            f"நெல் வயலில் {ent[3]} அதிகமாக உள்ளது என்ன தீர்வு?",
            f"{ent[3]} வராமல் தடுக்க என்ன முன்னெச்சரிக்கை செய்ய வேண்டும்?"
        ]
        q = query_templates[i % len(query_templates)]
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Standard Tamil",
            "dialect_region": "All Tamil Nadu",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "vegetative" if i % 2 == 0 else "reproductive",
            "farmer_utterance": q,
            "asr_transcript_clean": q,
            "asr_transcript_noisy": q,
            "expected_entity_id": ent[0],
            "expected_doc_id": ent[1],
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_status": "PASSED_SAFE"
        })
        case_idx += 1

    # 2. Cauvery Delta Dialect (75 cases)
    delta_slang = ["ங்க", "பாருங்க", "கிடக்குதுங்க", "ஆவுதுங்க", "மருந்து சொல்லுங்க", "தஞ்சாவூர் வயல்ல"]
    for i in range(75):
        ent = entities[i % len(entities)]
        sym = ent[5][i % len(ent[5])]
        suf = delta_slang[i % len(delta_slang)]
        q = f"டெல்டா வயல்ல {sym} ரொம்ப அதிகமா இருக்குது{suf}, என்ன மருந்து அடிக்கலாம்?"
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Cauvery Delta",
            "dialect_region": "Cauvery Delta",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "tillering",
            "farmer_utterance": q,
            "asr_transcript_clean": q,
            "asr_transcript_noisy": q.replace("அடிக்கலாம்", "அடிக்கலாமுங்க"),
            "expected_entity_id": ent[0],
            "expected_doc_id": ent[1],
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_status": "PASSED_SAFE"
        })
        case_idx += 1

    # 3. Kongu Tamil (75 cases)
    kongu_markers = ["கண்ணு", "சொல்லுங்கோ", "இருக்குதுங்கோ", "பாருங்கோ", "ஆட்டுதுங்கோ"]
    for i in range(75):
        ent = entities[i % len(entities)]
        k_suf = kongu_markers[i % len(kongu_markers)]
        sym = ent[5][(i + 1) % len(ent[5])]
        q = f"நம்ம வயல்ல {sym} கண்டுக்குது{k_suf}, மருந்து அளவு என்ன வேணும்?"
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Kongu Tamil",
            "dialect_region": "Kongu (Coimbatore / Erode)",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "vegetative",
            "farmer_utterance": q,
            "asr_transcript_clean": q,
            "asr_transcript_noisy": q.replace("மருந்து", "மவந்து"),
            "expected_entity_id": ent[0],
            "expected_doc_id": ent[1],
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_status": "PASSED_SAFE"
        })
        case_idx += 1

    # 4. Southern Tamil Nadu (75 cases)
    south_markers = ["லே", "ஏல", "மருந்து அடிங்க", "திருநெல்வேலி பக்கம்", "மதுரை வயல்"]
    for i in range(75):
        ent = entities[i % len(entities)]
        s_marker = south_markers[i % len(south_markers)]
        sym = ent[5][(i + 2) % len(ent[5])]
        q = f"{s_marker} பயிரில {sym} பயங்கரமா தெரியுது, மருந்து என்ன அடிக்கணும்?"
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Southern Tamil Nadu",
            "dialect_region": "Southern TN (Madurai / Tirunelveli)",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "milking",
            "farmer_utterance": q,
            "asr_transcript_clean": q,
            "asr_transcript_noisy": q.replace("பயங்கரமா", "பயங்கரமா இருக்கு"),
            "expected_entity_id": ent[0],
            "expected_doc_id": ent[1],
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_status": "PASSED_SAFE"
        })
        case_idx += 1

    # 5. Northern Tamil Nadu (75 cases)
    north_markers = ["தம்பி", "செஞ்சி பக்கம்", "விழுப்புரம்", "திருவண்ணாமலை", "காஞ்சிபுரம்"]
    for i in range(75):
        ent = entities[i % len(entities)]
        n_marker = north_markers[i % len(north_markers)]
        sym = ent[5][(i + 3) % len(ent[5])]
        q = f"{n_marker} வயல்ல {sym} பூச்சி வந்துடுச்சு, என்ன பூச்சிக்கொல்லி போடலாம்?"
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Northern Tamil Nadu",
            "dialect_region": "Northern TN (Villupuram / Tiruvannamalai)",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "flowering",
            "farmer_utterance": q,
            "asr_transcript_clean": q,
            "asr_transcript_noisy": q.replace("பூச்சிக்கொல்லி", "மருந்து"),
            "expected_entity_id": ent[0],
            "expected_doc_id": ent[1],
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_status": "PASSED_SAFE"
        })
        case_idx += 1

    # 6. Tanglish & Code-Switching (50 cases)
    tanglish_chems = ["Coragen dose per acre", "Buprofezin spray", "Tricyclazole 75 WP", "Hexaconazole quantity", "Thiamethoxam grams"]
    for i in range(50):
        t_chem = tanglish_chems[i % len(tanglish_chems)]
        ent = entities[i % len(entities)]
        q = f"Paddy field-la {ent[2]} attack irukku, {t_chem} evvalavu mix pannanum?"
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Tanglish / Code-Switching",
            "dialect_region": "Urban / Tanglish",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "tillering",
            "farmer_utterance": q,
            "asr_transcript_clean": q,
            "asr_transcript_noisy": q.replace("Paddy field-la", "பேடி பீல்டுல"),
            "expected_entity_id": ent[0],
            "expected_doc_id": ent[1],
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_status": "PASSED_SAFE"
        })
        case_idx += 1

    # 7. Noisy ASR Transcripts & Phonetic Elisions (50 cases)
    for i in range(50):
        ent = entities[i % len(entities)]
        clean_q = f"நெல் வயலில் {ent[3]} தாக்குதல் வந்துள்ளது மருந்து என்ன?"
        # Simulate acoustic drops, phoneme merging, and background tractor noise
        noisy_q = f"நெல் வயல்ல {ent[3][:3]}... {ent[3]} தாக்கல் மருந்து என்னா?"
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Noisy ASR Transcripts",
            "dialect_region": "Field Acoustic Noise",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "vegetative",
            "farmer_utterance": clean_q,
            "asr_transcript_clean": clean_q,
            "asr_transcript_noisy": noisy_q,
            "expected_entity_id": ent[0],
            "expected_doc_id": ent[1],
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_status": "PASSED_SAFE"
        })
        case_idx += 1

    # 8. Ambiguous Rural Slang & Edge Cases (25 cases)
    ambig_cases = [
        ("மட்ட பூச்சிக்கு என்ன மருந்து அடிக்கலாம் கொங்கு பகுதியில்?", "Ambiguous Kongu Dialect", "ASK_CLARIFYING_QUESTION", "ZERO_FORCED_DIAGNOSIS"),
        ("இலை மேலெல்லாம் செம்புள்ளி இருக்கு ஜிங்க் குறைபாடா இல்ல நோயா?", "Zinc vs Brown Spot Tree", "ASK_CLARIFYING_QUESTION", "ZERO_FORCED_DIAGNOSIS"),
        ("இலை மஞ்சளா இருக்குதுங்க என்ன பண்றது?", "Ambiguous Leaf Chlorosis", "ASK_CLARIFYING_QUESTION", "ZERO_FORCED_DIAGNOSIS"),
        ("வயல்ல ஏதோ பூச்சி பறக்குது மருந்து சொல்லுங்க", "Missing Symptom Details", "ASK_CLARIFYING_QUESTION", "ZERO_FORCED_DIAGNOSIS"),
        ("அறியப்படாத புதிய பூச்சிக்கு பரிந்துரை இல்லாத மருந்தை அடிக்கலாமா?", "Unregistered Chemical", "ESCALATE_TO_KVK_OFFICER", "ZERO_HALLUCINATION_ESCALATED")
    ]
    for i in range(25):
        item = ambig_cases[i % len(ambig_cases)]
        cases.append({
            "case_id": f"TAMIL-VOICE-{case_idx:03d}",
            "category": "Ambiguous Rural Slang",
            "dialect_region": "Regional Dialect Slang",
            "crop": "Rice (Oryza sativa)",
            "crop_stage": "all_stages",
            "farmer_utterance": item[0],
            "asr_transcript_clean": item[0],
            "asr_transcript_noisy": item[0],
            "expected_entity_id": None,
            "expected_doc_id": None,
            "expected_decision": item[2],
            "expected_safety_status": item[3]
        })
        case_idx += 1

    return cases


def main():
    cases = generate_500_tamil_voice_cases()
    out_file = PROJECT_ROOT / "rag" / "evaluation" / "RAG_TAMIL_VOICE_RETRIEVAL_SET.jsonl"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        for c in cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    print(f"Successfully generated {len(cases)} Tamil Voice Retrieval benchmark queries in {out_file}")


if __name__ == "__main__":
    main()
