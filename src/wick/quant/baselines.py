"""R3B baselines required by QUANT_METHODOLOGY.

1. Paired random entries (same count, same horizon/costs, valid indices)
2. Trend-only strategy (SMA20 slope / close>SMA)
3. Asset return on the same holding windows as strategy signals
4. Buy-and-hold over the evaluation window (context)
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from wick.backtest.engine import Bar, evaluate_signal


def _sma(closes: Sequence[float], window: int, end_inclusive: int) -> float | None:
    if end_inclusive + 1 < window:
        return None
    start = end_inclusive + 1 - window
    chunk = closes[start : end_inclusive + 1]
    return float(sum(chunk) / window)


def buy_and_hold_return(bars: Sequence[Bar], indices: range) -> float | None:
    """Context baseline: first open to last close inside ``indices``."""
    idxs = list(indices)
    if len(idxs) < 2:
        return None
    entry = float(bars[idxs[0]].open)
    exit_p = float(bars[idxs[-1]].close)
    if entry <= 0 or exit_p <= 0:
        return None
    return exit_p / entry - 1.0


def same_window_asset_returns(
    bars: Sequence[Bar],
    pattern_indices: Sequence[int],
    *,
    horizon: int,
    confirmation_used: bool,
) -> list[float]:
    """Gross asset path over each strategy holding window (no costs)."""
    out: list[float] = []
    for t in pattern_indices:
        r = evaluate_signal(
            bars,
            pattern_index=t,
            signal="bullish",
            pattern_type="ASSET_WINDOW",
            horizon=horizon,
            confirmation_used=confirmation_used,
            cost_scenario="ZERO",
        )
        if r.status == "OK" and r.gross_return is not None:
            out.append(r.gross_return)
    return out


def paired_random_entry_returns(
    bars: Sequence[Bar],
    *,
    n_signals: int,
    horizon: int,
    confirmation_used: bool,
    cost_scenario: str,
    index_pool: range,
    seed: int,
) -> list[float]:
    """Random pattern anchors with identical timing rules and costs."""
    if n_signals <= 0:
        return []
    offset = 2 if confirmation_used else 1
    max_pattern = len(bars) - offset - horizon
    candidates = [i for i in index_pool if i <= max_pattern]
    if not candidates:
        return []
    rng = np.random.default_rng(seed)
    # Sample with replacement if pool is smaller than n_signals
    picks = rng.choice(candidates, size=n_signals, replace=len(candidates) < n_signals)
    out: list[float] = []
    for t in picks:
        r = evaluate_signal(
            bars,
            pattern_index=int(t),
            signal="bullish",
            pattern_type="RANDOM_BASELINE",
            horizon=horizon,
            confirmation_used=confirmation_used,
            cost_scenario=cost_scenario,
        )
        if r.status == "OK" and r.net_return is not None:
            out.append(r.net_return)
    return out


def trend_only_returns(
    bars: Sequence[Bar],
    *,
    index_pool: range,
    horizon: int,
    confirmation_used: bool,
    cost_scenario: str,
    sma_window: int = 20,
) -> list[float]:
    """Long when close[t] > SMA20[t]; same entry/exit rules as pattern strategies."""
    closes = [float(b.close) for b in bars]
    offset = 2 if confirmation_used else 1
    max_pattern = len(bars) - offset - horizon
    out: list[float] = []
    for t in index_pool:
        if t > max_pattern or t < sma_window - 1:
            continue
        sma = _sma(closes, sma_window, t)
        if sma is None or closes[t] <= sma:
            continue
        r = evaluate_signal(
            bars,
            pattern_index=t,
            signal="bullish",
            pattern_type="TREND_ONLY",
            horizon=horizon,
            confirmation_used=confirmation_used,
            cost_scenario=cost_scenario,
        )
        if r.status == "OK" and r.net_return is not None:
            out.append(r.net_return)
    return out


def mean_or_none(xs: Sequence[float]) -> float | None:
    if not xs:
        return None
    return float(sum(xs) / len(xs))
