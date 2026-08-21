"""Named constants for the confidence gate (PRD §5.6, §5.7).

Thresholds themselves are NOT constants here — they come from config
(``CONFIDENCE_GATE``, ``RAG_RELEVANCE_THRESHOLD``) and are injected into
``decide()`` by the caller, per the execution plan. This module only names
the fixed, non-configurable pieces: the escalation reason codes and their
mapping onto the contract's stable machine error codes.
"""

# Domain-level escalation reasons. Distinct from the contract's machine error
# codes below because "out of scope" isn't its own code in the contract — see
# GATE_REASON_TO_ERROR_CODE.
GATE_REASON_BELOW_IMAGE_CONFIDENCE = "below_image_confidence_gate"
GATE_REASON_OUT_OF_SCOPE = "out_of_scope"
GATE_REASON_BELOW_RETRIEVAL_RELEVANCE = "no_relevant_source"

# Maps each domain reason onto the contract's stable error envelope code
# (contract §2.1). The contract has no dedicated "out of scope" code — PRD
# §5.6 and contract §2.10 both fold out-of-scope crop/disease submissions
# into the same escalation branch as below-gate confidence, so it maps to
# BELOW_CONFIDENCE_GATE too. Assumption, flagged: if a future contract
# revision adds a dedicated code, only this mapping needs to change.
GATE_REASON_TO_ERROR_CODE: dict[str, str] = {
    GATE_REASON_BELOW_IMAGE_CONFIDENCE: "BELOW_CONFIDENCE_GATE",
    GATE_REASON_OUT_OF_SCOPE: "BELOW_CONFIDENCE_GATE",
    GATE_REASON_BELOW_RETRIEVAL_RELEVANCE: "NO_RELEVANT_SOURCE",
}
