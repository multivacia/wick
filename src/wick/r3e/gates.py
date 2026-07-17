"""R3E gate classification — never auto-start R4."""

from __future__ import annotations


def classify_r3e(
    *,
    context_promising: bool,
    candle_adds_value: bool,
    candle_delta_positive_stable: bool,
    mean_net_m5: float | None,
    has_critical_findings: bool,
    fdr_reported: bool,
) -> str:
    if has_critical_findings or not fdr_reported:
        return "REQUIRES_FUTURE_VALIDATION"
    if mean_net_m5 is not None and mean_net_m5 < 0 and not context_promising:
        return "NEGATIVE"
    if candle_adds_value and candle_delta_positive_stable and context_promising:
        return "CANDLE_ADDS_VALUE"
    if context_promising and not candle_adds_value:
        return "CANDLE_ADDS_NO_VALUE"
    if context_promising:
        return "CONTEXT_PROMISING"
    return "INCONCLUSIVE"


def final_gate_state(classification: str) -> dict[str, str]:
    """Maximum allowed state — always pending future unseen data."""
    _ = classification
    return {
        "R3E_IMPLEMENTATION": "COMPLETE",
        "R3E_AUDIT": "COMPLETE",
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
        "classification": classification,
    }
