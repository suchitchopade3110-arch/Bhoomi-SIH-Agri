"""Case PDF payload builder (Phase 4 Objective 2).

Transforms a CaseSummary and associated farm/case metadata into a structured CasePDFPayload.
Guarantees strict superset mapping against Phase 3 CaseSummaryBundle with zero fabricated data sources.
"""

from typing import Any
from datetime import datetime
from app.schemas.case import CaseSummary, CaseSummaryBundle
from app.schemas.case_pdf import CasePDFPayload


def build_case_pdf_payload(
    case_summary: CaseSummary,
    assigned_kvk: str | None = None,
    share_url: str | None = None,
    prescribed_actions_summary: str | None = None,
) -> CasePDFPayload:
    """Build a structured CasePDFPayload from a compiled CaseSummary."""
    bundle = case_summary.bundle
    if bundle is None:
        from app.services.escalation.compiler import compile_case_summary_bundle
        bundle = compile_case_summary_bundle(
            crop=case_summary.crop or "Rice",
            region=f"{case_summary.village}, {case_summary.district}".strip(", "),
            growth_stage=case_summary.growth_stage or "Tillering",
            problem_history=[{"problem": case_summary.problem_summary, "severity": str(case_summary.severity)}],
            images=case_summary.latest_images or [],
            treatments_tried=[],
            followup_trend=None,
            current_advisory=case_summary.spoken_summary,
        )

    # Format summary headline
    crop_str = bundle.crop.replace("_", " ").title()
    prob_str = case_summary.problem_summary or "Crop Stress"
    sev_str = case_summary.severity.value if hasattr(case_summary.severity, "value") else str(case_summary.severity)
    stat_str = case_summary.status.value if hasattr(case_summary.status, "value") else str(case_summary.status)
    headline = f"{crop_str} — {prob_str} ({sev_str.title()})"

    return CasePDFPayload(
        case_id=case_summary.case_id,
        farm_id=case_summary.farm_id,
        farmer_name=case_summary.farmer_name or "Farmer",
        village=case_summary.village or "",
        district=case_summary.district or "",
        assigned_kvk=assigned_kvk or case_summary.escalated_to,
        severity=sev_str,
        status=stat_str,
        generated_at=datetime.utcnow(),
        bundle=bundle,
        summary_headline=headline,
        prescribed_actions_summary=prescribed_actions_summary,
        share_url=share_url or f"/cases/{case_summary.case_id}",
    )
