"""Posterior confirmation rules — only after confirm candle is closed."""

from __future__ import annotations

from wick.patterns.params import CONFIRM_CLOSE_V1, CONFIRM_EXTREME_V1


def evaluate_confirmation(
    *,
    signal: str,
    pattern_type: str,
    anchor_close: float,
    anchor_high: float,
    anchor_low: float,
    confirm_close: float,
    rule: str,
) -> str:
    """Return CONFIRMED | NOT_CONFIRMED | NOT_APPLICABLE."""
    if pattern_type == "DOJI" or signal == "neutral":
        return "NOT_APPLICABLE"

    if rule == CONFIRM_CLOSE_V1:
        if signal == "bullish":
            return "CONFIRMED" if confirm_close > anchor_close else "NOT_CONFIRMED"
        if signal == "bearish":
            return "CONFIRMED" if confirm_close < anchor_close else "NOT_CONFIRMED"
        return "NOT_APPLICABLE"

    if rule == CONFIRM_EXTREME_V1:
        if signal == "bullish":
            return "CONFIRMED" if confirm_close > anchor_high else "NOT_CONFIRMED"
        if signal == "bearish":
            return "CONFIRMED" if confirm_close < anchor_low else "NOT_CONFIRMED"
        return "NOT_APPLICABLE"

    raise ValueError(f"Unknown confirmation rule: {rule}")


OFFICIAL_CONFIRMATION_RULES = (CONFIRM_CLOSE_V1, CONFIRM_EXTREME_V1)
