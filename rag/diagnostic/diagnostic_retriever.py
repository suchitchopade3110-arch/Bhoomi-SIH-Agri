"""
BHOOMI Diagnostic Decision Retriever
Retrieves competing diagnoses, distinguishing features, and multi-turn decision trees
for ambiguous foliar symptoms (e.g. Zinc Deficiency vs Brown Spot, general chlorosis, kresek vs dead heart).
"""
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class DiagnosticRetriever:
    def __init__(self, knowledge_version: str = "v4.2.0-validated"):
        self.knowledge_version = knowledge_version
        self.indexes_dir = PROJECT_ROOT / "rag" / "indexes"
        
        v_tag = knowledge_version.replace("-", "_").replace(".", "_")
        self.obj_file = self.indexes_dir / f"evidence_objects_{v_tag}.json"
        
        self.decision_trees: List[Dict[str, Any]] = []
        self._load_trees()

    def _load_trees(self):
        """Loads structured decision trees from evidence objects."""
        if not self.obj_file.exists():
            return
        with open(self.obj_file, "r", encoding="utf-8") as f:
            objects = json.load(f)
            for obj in objects:
                if obj.get("chunk_type") == "DECISION_TREE" or obj.get("diagnostic_features"):
                    self.decision_trees.append(obj)

    def evaluate_diagnostic_query(self, parsed_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates whether a symptom query requires a multi-turn diagnostic decision tree or clarification."""
        symptoms = parsed_context.get("symptoms", [])
        original_query = parsed_context.get("original_query", "").lower()
        has_resolved_entity = bool(parsed_context.get("expanded_entity_ids") or parsed_context.get("expanded_canonical_entities"))

        # Check for Zinc vs Brown spot differential trigger
        if "செம்புள்ளி" in original_query and ("துத்தநாக" in original_query or "zinc" in original_query or "ஜிங்க்" in original_query or "நோயா" in original_query or "குறைபாடா" in original_query):
            tree_id = self.decision_trees[0].get("evidence_id") if self.decision_trees else "DDT-001"
            return {
                "diagnostic_mode": "ACTIVE_DECISION_TREE",
                "tree_id": tree_id,
                "name": "Zinc Deficiency vs Brown Spot Decision Tree",
                "clarification_required": True,
                "clarifying_question_tamil": "பயிரின் பருவம் என்ன? நட்டு எத்தனை நாட்கள் ஆகிறது? புள்ளிகள் இலை நரம்பின் நடுப்பகுதியில் செம்பழுப்பு நிறமாக உள்ளதா அல்லது இலை முழுக்க முட்டை வடிவில் உள்ளதா?",
                "competing_hypotheses": [
                    {"entity": "Zinc Deficiency (Khaira)", "treatment": "Foliar 0.5% ZnSO4 + 1% Urea"},
                    {"entity": "Brown Spot (Bipolaris oryzae)", "treatment": "Mancozeb 75 WP @ 1 kg/ha"}
                ]
            }

        # If entity is already identified (e.g. Gall midge, Leaf folder, Blast, etc.), do NOT ask generic clarification!
        if has_resolved_entity:
            return {
                "diagnostic_mode": "DIRECT_DIAGNOSIS_POSSIBLE",
                "clarification_required": False,
                "clarifying_question_tamil": None,
                "competing_hypotheses": []
            }

        # Check for generic ambiguous yellowing without resolved entity
        if "leaf_chlorosis" in symptoms or ("மஞ்சள்" in original_query and not any(k in original_query for k in ["மஞ்சள் கதிர்", "false smut"])):
            return {
                "diagnostic_mode": "AMBIGUOUS_SYMPTOM_CLARIFICATION",
                "clarification_required": True,
                "clarifying_question_tamil": "இலை மஞ்சளாதல் பல காரணங்களால் ஏற்படலாம். மஞ்சள் நிறம் இலை விளிம்பில் அலை அலையாக உள்ளதா அல்லது நடுப்பகுதியில் உள்ளதா? பயிரின் பருவம் என்ன என்று கூற முடியுமா?",
                "competing_hypotheses": [
                    {"entity": "Bacterial Leaf Blight (BLB)", "cue": "wavy margins with bacterial ooze"},
                    {"entity": "Green Leafhopper / Tungro", "cue": "orange-yellow discoloration from tip"},
                    {"entity": "Nitrogen / Zinc Deficiency", "cue": "uniform lower leaf chlorosis or midrib bronze"}
                ]
            }

        # Check for vague queries like "ஏதோ பூச்சி பறக்குது"
        if any(w in original_query for w in ["ஏதோ பூச்சி", "ஏதோ ஒரு புது பூச்சி", "காரணமும் தெரியல", "புது பூச்சி"]):
            return {
                "diagnostic_mode": "INSUFFICIENT_SYMPTOM_INFORMATION",
                "clarification_required": True,
                "clarifying_question_tamil": "வயலில் என்ன வகையான பாதிப்பு அல்லது பூச்சி காணப்படுகிறது என்று விவரிக்க முடியுமா?",
                "competing_hypotheses": []
            }

        return {
            "diagnostic_mode": "DIRECT_DIAGNOSIS_POSSIBLE",
            "clarification_required": False,
            "clarifying_question_tamil": None,
            "competing_hypotheses": []
        }
