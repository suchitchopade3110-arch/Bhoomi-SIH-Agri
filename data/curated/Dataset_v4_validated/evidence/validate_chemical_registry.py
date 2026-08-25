"""
BHOOMI Chemical Regulatory & Safety Registry Validator
Validates all 26 registered chemical recommendations across pest and disease corpora against CIBRC/DPPQS regulatory standards.

Outputs:
data/curated/Dataset_v4_validated/evidence/CHEMICAL_REGULATORY_VALIDATION.json
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

EVIDENCE_DIR = Path(__file__).resolve().parent
REGISTRY_FILE = EVIDENCE_DIR / "CHEMICAL_REGULATORY_REGISTRY.json"
OUTPUT_FILE = EVIDENCE_DIR / "CHEMICAL_REGULATORY_VALIDATION.json"

sys.stdout.reconfigure(encoding="utf-8")

ALLOWED_STATUSES = [
    "VERIFIED_CURRENT",
    "HISTORICAL",
    "RESTRICTED",
    "PROHIBITED",
    "UNVERIFIED",
    "CONFLICTING",
    "NOT_APPLICABLE"
]


def validate_chemical_registry():
    print("================================================================================")
    print("RUNNING BHOOMI CHEMICAL REGULATORY & SAFETY REGISTRY VALIDATOR")
    print("================================================================================")

    if not REGISTRY_FILE.exists():
        print(f"[-] MISSING REGISTRY FILE: {REGISTRY_FILE}")
        sys.exit(1)

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    chemicals = data.get("chemicals", [])
    report = {
        "report_title": "BHOOMI Chemical Regulatory & Safety Validation Report",
        "total_chemicals_audited": len(chemicals),
        "status_breakdown": {
            "VERIFIED_CURRENT": 0,
            "RESTRICTED": 0,
            "PROHIBITED": 0,
            "HISTORICAL": 0,
            "UNVERIFIED": 0,
            "CONFLICTING": 0,
            "NOT_APPLICABLE": 0
        },
        "missing_safety_metadata_count": 0,
        "overall_status": "READY",
        "results": []
    }

    for chem in chemicals:
        cid = chem.get("chemical_id")
        ai = chem.get("active_ingredient")
        formulation = chem.get("formulation")
        status = chem.get("regulatory_status")
        phi = chem.get("phi")
        dose = chem.get("dose")
        evidence = chem.get("evidence", [])
        warnings = chem.get("warnings", [])
        farmer_action = chem.get("farmer_action_allowed")

        # Track status count
        if status in report["status_breakdown"]:
            report["status_breakdown"][status] += 1

        missing_fields = []
        if not ai:
            missing_fields.append("active_ingredient")
        if not formulation:
            missing_fields.append("formulation")
        if not status or status not in ALLOWED_STATUSES:
            missing_fields.append("valid_regulatory_status")
        if status == "VERIFIED_CURRENT" and (not phi or phi == "N/A"):
            missing_fields.append("phi")
        if status == "VERIFIED_CURRENT" and (not dose or dose == "N/A"):
            missing_fields.append("dose")
        if len(evidence) == 0:
            missing_fields.append("evidence")

        if missing_fields:
            report["missing_safety_metadata_count"] += 1

        # Action consistency check
        action_inconsistent = False
        if status in ["PROHIBITED", "RESTRICTED", "HISTORICAL", "UNVERIFIED"] and farmer_action is True:
            action_inconsistent = True
            missing_fields.append("farmer_action_allowed_must_be_false_for_non_verified_status")

        entry_status = "VALID"
        if missing_fields or action_inconsistent:
            entry_status = "INVALID"
            report["overall_status"] = "BLOCKED"
        elif warnings:
            entry_status = "VALID_WITH_WARNINGS"

        entry = {
            "chemical_id": cid,
            "active_ingredient": ai,
            "formulation": formulation,
            "regulatory_status": status,
            "phi": phi,
            "dose": dose,
            "evidence_count": len(evidence),
            "warnings_count": len(warnings),
            "warnings": warnings,
            "farmer_action_allowed": farmer_action,
            "missing_fields": missing_fields,
            "validation_status": entry_status
        }
        report["results"].append(entry)

        print(f"  * [{entry_status:<19}] {cid:<8} | {ai[:26]:<26} | Status: {status:<18} | Farmer Action: {str(farmer_action):<5} | Warn: {len(warnings)}")

    if report["overall_status"] == "READY" and any(r["validation_status"] == "VALID_WITH_WARNINGS" for r in report["results"]):
        report["overall_status"] = "READY_WITH_WARNINGS"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\n================================================================================")
    print(f"VALIDATION REPORT GENERATED: {OUTPUT_FILE}")
    print(f"TOTAL AUDITED: {report['total_chemicals_audited']}")
    print(f"STATUS BREAKDOWN: {report['status_breakdown']}")
    print(f"OVERALL STATUS: {report['overall_status']}")
    print("================================================================================")


if __name__ == "__main__":
    validate_chemical_registry()
