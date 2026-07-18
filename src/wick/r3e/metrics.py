"""Economic and stability metrics for R3E reports."""

from __future__ import annotations

import numpy as np


def hit_rate(returns: list[float]) -> float | None:
    if not returns:
        return None
    arr = np.asarray(returns, dtype=float)
    return float(np.mean(arr > 0))


def max_drawdown(returns: list[float]) -> float | None:
    if not returns:
        return None
    equity = np.cumprod(1.0 + np.asarray(returns, dtype=float))
    peak = np.maximum.accumulate(equity)
    dd = (equity - peak) / np.where(peak == 0, 1.0, peak)
    return float(dd.min())


def exposure_fraction(n_selected: int, n_eligible: int) -> float | None:
    if n_eligible <= 0:
        return None
    return float(n_selected / n_eligible)


def cumulative_return(returns: list[float]) -> float | None:
    if not returns:
        return None
    return float(np.prod(1.0 + np.asarray(returns, dtype=float)) - 1.0)
