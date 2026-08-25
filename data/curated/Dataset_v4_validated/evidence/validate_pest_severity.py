"""
BHOOMI Pest Severity & Decision Threshold Validator
Validates structured 3-tier severity data for all 8 rice pests:
1. Stem Borer
2. Brown Planthopper
3. Leaf Folder
4. Green Leafhopper
5. Gall Midge
6. Thrips
7. Whorl Maggot
8. Earhead Bug

Outputs:
data/curated/Dataset_v4_validated/evidence/PEST_SEVERITY_VALIDATION.json
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

EVIDENCE_DIR = Path(__file__).resolve().parent
SEVERITY_FILE = EVIDENCE_DIR / "PEST_SEVERITY.json"
OUTPUT_FILE = EVIDENCE_DIR / "PEST_SEVERITY_VALIDATION.json"

sys.stdout.reconfigure(encoding="utf-8")


def validate_pest_severity():
    print("================================================================================")
    print("RUNNING BHOOMI PEST SEVERITY & DECISION THRESHOLD VALIDATOR")
    print("================================================================================")

    if not SEVERITY_FILE.exists():
        print(f"[-] MISSING SEVERITY FILE: {SEVERITY_FILE}")
        sys.exit(1)

    with open(SEVERITY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    records = data.get("pest_severity_records", [])
    report = {
        "report_title": "BHOOMI Pest Severity & Decision Threshold Validation Report",
        "total_pests_expected": 8,
        "total_pests_validated": len(records),
        "overall_status": "READY",
        "results": []
    }

    restricted_chemicals_map = {
        "PEST_001": ["Carbofuran 3G (RESTRICTED)"],
        "PEST_005": ["Carbofuran 3G (RESTRICTED)"],
        "PEST_007": ["Carbofuran 3G (RESTRICTED)"],
        "PEST_008": ["Malathion 50 EC (RESTRICTED_PHI_MANDATORY)"]
    }

    for rec in records:
        pid = rec.get("pest_id")
        pname = rec.get("pest_name")
        early = rec.get("early", {})
        moderate = rec.get("moderate", {})
        severe = rec.get("severe", {})
        etl = rec.get("etl", {})
        penalty = rec.get("penalty", {})

        # Check completeness
        early_status = early.get("threshold_status", "NOT_ESTABLISHED")
        mod_status = moderate.get("threshold_status", "NOT_ESTABLISHED")
        sev_status = severe.get("threshold_status", "NOT_ESTABLISHED")
        etl_status = etl.get("classification", "NOT_ESTABLISHED")

        early_cues = len(early.get("observable_cues", [])) > 0
        mod_cues = len(moderate.get("observable_cues", [])) > 0
        sev_cues = len(severe.get("observable_cues", [])) > 0

        severity_complete = bool(early_cues and mod_cues and sev_cues)

        ev_count = len(early.get("evidence", [])) + len(moderate.get("evidence", [])) + len(severe.get("evidence", [])) + len(etl.get("evidence", []))

        quant_thresh_present = bool(
            early.get("quantitative_thresholds") and
            moderate.get("quantitative_thresholds") and
            severe.get("quantitative_thresholds")
        )

        unsupported_claims = []
        project_derived_rules = []
        if penalty.get("rule_type") == "PROJECT_DERIVED_RULE":
            project_derived_rules.append(f"Penalty mapping (Early: {penalty.get('early')}, Mod: {penalty.get('moderate')}, Sev: {penalty.get('severe')}) is a PROJECT_DERIVED_RULE for Active Problem Load computation.")

        reg_warnings = restricted_chemicals_map.get(pid, [])

        # Determine individual status
        if not severity_complete or not etl_status:
            status = "BLOCKED"
            report["overall_status"] = "BLOCKED"
        elif reg_warnings:
            status = "READY_WITH_WARNINGS"
        else:
            status = "READY"

        entry = {
            "pest_id": pid,
            "pest_name": pname,
            "severity_complete": severity_complete,
            "early_status": early_status,
            "moderate_status": mod_status,
            "severe_status": sev_status,
            "etl_status": etl_status,
            "evidence_count": ev_count,
            "quantitative_thresholds_present": quant_thresh_present,
            "unsupported_claims": unsupported_claims,
            "project_derived_rules": project_derived_rules,
            "regulatory_warnings": reg_warnings,
            "status": status
        }

        report["results"].append(entry)
        print(f"  * [{status:<19}] {pid} | {pname:<20} | ETL: {etl_status:<12} | SES Scale: {sev_status:<30} | Ev: {ev_count}")

    if report["overall_status"] == "READY" and any(r["status"] == "READY_WITH_WARNINGS" for r in report["results"]):
        report["overall_status"] = "READY_WITH_WARNINGS"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n================================================================================")
    print(f"VALIDATION REPORT GENERATED: {OUTPUT_FILE}")
    print(f"OVERALL STATUS: {report['overall_status']}")
    print("================================================================================")


if __name__ == "__main__":
    validate_pest_severity()
