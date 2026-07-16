"""Adversarial R2 audit — try to prove look-ahead / open candle / formula bugs."""

from __future__ import annotations

from wick.features.context import OHLCV, compute_context_at
from wick.patterns.detectors import detect_all_at_anchor
from wick.patterns.geometry import compute_geometry
from wick.patterns.params import DEFAULT_PARAMS


def test_context_ignores_future_bars_in_list():
    """Passing longer list must not change context at index t if we slice correctly."""
    bars = [OHLCV(float(i), float(i) + 1, float(i) - 1, float(i) + 0.2, 100) for i in range(1, 50)]
    ctx_a = compute_context_at(bars[:30], 29, DEFAULT_PARAMS)
    # Append crazy future
    future = bars[:30] + [OHLCV(9999, 10000, 9998, 9999.5, 1e9) for _ in range(20)]
    ctx_b = compute_context_at(future, 29, DEFAULT_PARAMS)
    assert ctx_a.sma_20 == ctx_b.sma_20
    assert ctx_a.atr_14 == ctx_b.atr_14
    assert ctx_a.return_5 == ctx_b.return_5
    assert ctx_a.trend_direction == ctx_b.trend_direction


def test_detection_at_t_ignores_future_geometry():
    g0 = compute_geometry(open_=10, high=10.6, low=8, close=10.5, volume=1)
    future = compute_geometry(open_=1, high=1000, low=0.1, close=999, volume=1)
    a = {h.pattern_type for h in detect_all_at_anchor([g0], 0, DEFAULT_PARAMS)}
    b = {h.pattern_type for h in detect_all_at_anchor([g0, future], 0, DEFAULT_PARAMS)}
    assert a == b


def test_insufficient_median_blocks_morning_star_large_body():
    """is_large_body must be strictly True; NULL/False must not detect morning star."""
    c1 = compute_geometry(open_=12, high=12.1, low=9, close=9.2, volume=1, median_body_14=None)
    c2 = compute_geometry(open_=9.2, high=9.5, low=9.0, close=9.25, volume=1, median_body_14=1.0)
    c3 = compute_geometry(open_=9.3, high=12.0, low=9.2, close=11.5, volume=1, median_body_14=1.0)
    assert c1.is_large_body is None
    hits = detect_all_at_anchor([c1, c2, c3], 2, DEFAULT_PARAMS)
    assert all(h.pattern_type != "MORNING_STAR" for h in hits)


def test_no_return_fields_in_r2_modules():
    """R2 must not compute trade returns / backtest artifacts."""
    from pathlib import Path

    root = Path("src/wick")
    banned = ("gross_return", "net_return", "backtest", "entry_price", "exit_price")
    offenders = []
    for path in root.rglob("*.py"):
        if "ingestion" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        # allow comments mentioning backtest prohibition in docs strings carefully
        for token in banned:
            if token in text and path.name not in {"__init__.py"}:
                # detection/service may mention nothing; patterns shouldn't
                if any(p in path.parts for p in ("patterns", "features", "detection")):
                    offenders.append(f"{path}:{token}")
    assert offenders == [], offenders
