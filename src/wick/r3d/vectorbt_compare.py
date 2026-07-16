"""Complementary vectorbt comparison with fixed absolute tolerances."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

import numpy as np

# Human-authorized tolerances (R3D)
TOL_TRADE_RETURN = 1e-10
TOL_AGGREGATE = 1e-8


@dataclass
class TradePoint:
    entry_index: int
    exit_index: int
    entry_ts: Any
    exit_ts: Any
    net_return: float


@dataclass
class CompareResult:
    ok: bool
    n_trades_own: int
    n_trades_vbt: int
    max_abs_trade_diff: float | None
    max_abs_agg_diff: float | None
    notes: list[str]


def compare_trade_sets(
    own: Sequence[TradePoint],
    vbt_returns: Sequence[float],
    *,
    vbt_entry_indices: Sequence[int],
    vbt_exit_indices: Sequence[int],
    vbt_entry_ts: Sequence[Any] | None = None,
    vbt_exit_ts: Sequence[Any] | None = None,
) -> CompareResult:
    notes: list[str] = []
    ok = True
    if len(own) != len(vbt_returns):
        ok = False
        notes.append(f"count mismatch own={len(own)} vbt={len(vbt_returns)}")
    if len(own) != len(vbt_entry_indices) or len(own) != len(vbt_exit_indices):
        ok = False
        notes.append("index count mismatch")

    n = min(len(own), len(vbt_returns), len(vbt_entry_indices), len(vbt_exit_indices))
    max_trade = 0.0
    for i in range(n):
        if own[i].entry_index != int(vbt_entry_indices[i]):
            ok = False
            notes.append(f"entry_index mismatch at {i}")
        if own[i].exit_index != int(vbt_exit_indices[i]):
            ok = False
            notes.append(f"exit_index mismatch at {i}")
        if vbt_entry_ts is not None and own[i].entry_ts != vbt_entry_ts[i]:
            ok = False
            notes.append(f"entry_ts mismatch at {i}")
        if vbt_exit_ts is not None and own[i].exit_ts != vbt_exit_ts[i]:
            ok = False
            notes.append(f"exit_ts mismatch at {i}")
        diff = abs(own[i].net_return - float(vbt_returns[i]))
        max_trade = max(max_trade, diff)
        if diff > TOL_TRADE_RETURN:
            ok = False
            notes.append(f"trade return diff {diff} > {TOL_TRADE_RETURN} at {i}")

    own_mean = float(np.mean([t.net_return for t in own])) if own else 0.0
    vbt_mean = float(np.mean(list(vbt_returns))) if vbt_returns else 0.0
    agg_diff = abs(own_mean - vbt_mean)
    if agg_diff > TOL_AGGREGATE:
        ok = False
        notes.append(f"aggregate mean diff {agg_diff} > {TOL_AGGREGATE}")

    return CompareResult(
        ok=ok,
        n_trades_own=len(own),
        n_trades_vbt=len(vbt_returns),
        max_abs_trade_diff=max_trade if n else None,
        max_abs_agg_diff=agg_diff,
        notes=notes[:50],
    )


def vectorbt_net_returns(
    opens: Sequence[float],
    closes: Sequence[float],
    entry_indices: Sequence[int],
    exit_indices: Sequence[int],
    total_cost: float,
) -> list[float]:
    """Independent path: gross = close[exit]/open[entry]-1; net = gross - total_cost.

    Named vectorbt_* because it is the complementary calculator; uses the same
    formula as the auditable engine without importing it (oracle separation).
    Optional vectorbt package may wrap this later without changing tolerances.
    """
    out: list[float] = []
    for e, x in zip(entry_indices, exit_indices, strict=True):
        entry = float(opens[e])
        exit_p = float(closes[x])
        if entry <= 0 or exit_p <= 0:
            continue
        gross = exit_p / entry - 1.0
        out.append(gross - total_cost)
    return out
