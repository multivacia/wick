"""R3E gate classification — never auto-start R4."""

from __future__ import annotations


def classify_r3e(
    *,
    context_promising: bool,
    candle_adds_value: bool,
    candle_delta_positive_stable: bool,
    mean_net_m4: float | None,
    mean_net_m5: float | None,
    has_critical_findings: bool,
    fdr_reported: bool,
    exploratory: bool = True,
) -> str:
    """Classify development outcomes.

    Allowed labels for real-data development run:
    CONTEXT_HAS_NO_EDGE | CONTEXT_PROMISING | CANDLE_ADDS_NO_VALUE |
    CANDLE_ADDS_VALUE_EXPLORATORY | INCONCLUSIVE
    """
    if has_critical_findings or not fdr_reported:
        return "INCONCLUSIVE"
    if candle_adds_value and candle_delta_positive_stable and context_promising:
        return "CANDLE_ADDS_VALUE_EXPLORATORY" if exploratory else "CANDLE_ADDS_VALUE"
    if context_promising and not candle_adds_value:
        return "CANDLE_ADDS_NO_VALUE"
    if context_promising:
        return "CONTEXT_PROMISING"
    if mean_net_m4 is not None and mean_net_m4 <= 0 and (
        mean_net_m5 is None or mean_net_m5 <= 0
    ):
        return "CONTEXT_HAS_NO_EDGE"
    return "INCONCLUSIVE"


def final_gate_state(classification: str, *, real_data: bool = False) -> dict[str, str]:
    """Maximum allowed state — always pending future unseen data."""
    out = {
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
        "classification": classification,
    }
    if real_data:
        out.update(
            {
                "R3E_REAL_DATA_RUN": "COMPLETE",
                "R3E_REAL_DATA_AUDIT": "COMPLETE",
            }
        )
    else:
        out.update(
            {
                "R3E_IMPLEMENTATION": "COMPLETE",
                "R3E_AUDIT": "COMPLETE",
            }
        )
    return out
