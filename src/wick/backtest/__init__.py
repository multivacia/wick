"""Backtest package (R3A)."""

from wick.backtest.engine import (
    HORIZONS,
    Bar,
    TradeResult,
    evaluate_horizons,
    evaluate_signal,
)

__all__ = [
    "HORIZONS",
    "Bar",
    "TradeResult",
    "evaluate_horizons",
    "evaluate_signal",
]
