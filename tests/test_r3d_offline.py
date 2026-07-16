"""R3D unit tests (offline; no live network)."""

from __future__ import annotations

from wick.r3d.manifest import build_variants
from wick.r3d.universe import UNIVERSE
from wick.r3d.vectorbt_compare import TradePoint, compare_trade_sets, vectorbt_net_returns


def test_universe_size():
    # 5 crypto × 2 tf + 5 stocks × 2 tf
    assert len(UNIVERSE) == 20


def test_variants_cover_patterns_horizons_costs():
    variants = build_variants()
    assert len(variants) == 8 * 4 * 2 * 3
    assert all(v.cost_scenario in {"OPTIMISTIC", "BASE", "STRESSED"} for v in variants)


def test_vectorbt_compare_exact_and_tolerances():
    opens = [100.0, 101.0, 102.0, 103.0]
    closes = [100.5, 101.5, 102.5, 103.5]
    entries = [0, 1]
    exits = [1, 2]
    cost = 0.0024
    vbt = vectorbt_net_returns(opens, closes, entries, exits, cost)
    own = [
        TradePoint(0, 1, "t0", "t1", vbt[0]),
        TradePoint(1, 2, "t1", "t2", vbt[1]),
    ]
    cmp = compare_trade_sets(
        own,
        vbt,
        vbt_entry_indices=entries,
        vbt_exit_indices=exits,
        vbt_entry_ts=["t0", "t1"],
        vbt_exit_ts=["t1", "t2"],
    )
    assert cmp.ok
    assert cmp.max_abs_trade_diff is not None
    assert cmp.max_abs_trade_diff < 1e-10
