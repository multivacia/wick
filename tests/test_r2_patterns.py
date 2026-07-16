"""R2 detector, context, confirmation, and golden dataset tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from wick.features.context import OHLCV, compute_context_at
from wick.patterns.confirmation import CONFIRM_CLOSE_V1, CONFIRM_EXTREME_V1, evaluate_confirmation
from wick.patterns.detectors import detect_all_at_anchor
from wick.patterns.geometry import compute_geometry
from wick.patterns.params import DEFAULT_PARAMS, DetectorParams

GOLDEN = Path(__file__).parent / "golden" / "r2" / "patterns_catalog.json"


def _g(o, h, low, c, *, median=None, params=None):
    return compute_geometry(
        open_=o,
        high=h,
        low=low,
        close=c,
        volume=1,
        params=params or DEFAULT_PARAMS,
        median_body_14=median,
    )


def test_golden_catalog_patterns():
    data = json.loads(GOLDEN.read_text(encoding="utf-8"))
    params = DEFAULT_PARAMS
    for case in data["cases"]:
        bars = [OHLCV(**c) for c in case["candles"]]
        # For multi-candle, provide large median so large_body can be true when needed
        geoms = []
        for i, b in enumerate(bars):
            med = 1.0 if len(bars) >= 3 and i == 0 else None
            # For engulfing / stars needing relative size on first of 3:
            if len(bars) == 3 and i == 0:
                med = 0.5  # body will be large vs median
            geoms.append(
                compute_geometry(
                    open_=b.open,
                    high=b.high,
                    low=b.low,
                    close=b.close,
                    volume=b.volume,
                    params=params,
                    median_body_14=med,
                )
            )
        idx = len(geoms) - 1
        hits = {h.pattern_type for h in detect_all_at_anchor(geoms, idx, params)}
        for pattern, expected in case["expected"].items():
            assert (pattern in hits) is expected, f"{case['case_id']} {pattern}: hits={hits}"


def test_hammer_boundary_and_scale_translation():
    params = DEFAULT_PARAMS
    base = _g(10.0, 10.6, 8.0, 10.5)
    assert detect_all_at_anchor([base], 0, params)
    scaled = _g(100.0, 106.0, 80.0, 105.0)
    shifted = _g(1010.0, 1010.6, 1008.0, 1010.5)

    def types(g):
        return {h.pattern_type for h in detect_all_at_anchor([g], 0, params)}

    assert "HAMMER" in types(base)
    assert types(base) == types(scaled) == types(shifted)


def test_future_candle_does_not_change_detection():
    params = DEFAULT_PARAMS
    g0 = _g(10.0, 10.6, 8.0, 10.5)
    hits1 = detect_all_at_anchor([g0], 0, params)
    future = _g(1, 100, 0.1, 50)
    hits2 = detect_all_at_anchor([g0, future], 0, params)
    assert {h.pattern_type for h in hits1} == {h.pattern_type for h in hits2}


def test_doji_exact_boundary():
    g = _g(100, 110, 90, 102)  # body 2 / range 20 = 0.10
    assert g.body_ratio == pytest.approx(0.10)
    hits = detect_all_at_anchor([g], 0, DEFAULT_PARAMS)
    assert any(h.pattern_type == "DOJI" for h in hits)


def test_degenerate_not_doji():
    g = _g(100, 100, 100, 100)
    assert g.is_degenerate
    assert not g.is_doji
    assert detect_all_at_anchor([g], 0, DEFAULT_PARAMS) == []


def test_morning_star_requires_large_first_body():
    params = DEFAULT_PARAMS
    # c1 large bear, c2 small, c3 bull recovery
    c1 = _g(12, 12.1, 9, 9.2, median=0.5)  # body 2.8 >> 0.5
    c2 = _g(9.2, 9.5, 9.0, 9.25, median=1.0)
    c3 = _g(9.3, 12.0, 9.2, 11.5, median=1.0)
    assert c1.is_large_body is True
    hits = detect_all_at_anchor([c1, c2, c3], 2, params)
    assert any(h.pattern_type == "MORNING_STAR" for h in hits)


def test_evening_star_positive():
    params = DEFAULT_PARAMS
    c1 = _g(9, 12.1, 8.9, 12, median=0.5)
    c2 = _g(12.0, 12.3, 11.8, 12.1, median=1.0)
    c3 = _g(12.0, 12.1, 9.0, 9.5, median=1.0)
    hits = detect_all_at_anchor([c1, c2, c3], 2, params)
    assert any(h.pattern_type == "EVENING_STAR" for h in hits)


def test_confirmation_rules():
    assert (
        evaluate_confirmation(
            signal="bullish",
            pattern_type="HAMMER",
            anchor_close=10,
            anchor_high=11,
            anchor_low=8,
            confirm_close=10.5,
            rule=CONFIRM_CLOSE_V1,
        )
        == "CONFIRMED"
    )
    assert (
        evaluate_confirmation(
            signal="bullish",
            pattern_type="HAMMER",
            anchor_close=10,
            anchor_high=11,
            anchor_low=8,
            confirm_close=10.5,
            rule=CONFIRM_EXTREME_V1,
        )
        == "NOT_CONFIRMED"
    )
    assert (
        evaluate_confirmation(
            signal="neutral",
            pattern_type="DOJI",
            anchor_close=10,
            anchor_high=11,
            anchor_low=8,
            confirm_close=12,
            rule=CONFIRM_CLOSE_V1,
        )
        == "NOT_APPLICABLE"
    )


def test_context_no_lookahead_insufficient_is_unknown():
    bars = [OHLCV(10, 11, 9, 10.5, 100) for _ in range(5)]
    ctx = compute_context_at(bars, 4, DEFAULT_PARAMS)
    assert ctx.trend_direction == "UNKNOWN"
    assert ctx.atr_14 is None
    assert ctx.return_20 is None


def test_context_atr_sma_with_enough_history():
    # trending up series
    bars = [OHLCV(i, i + 1, i - 1, i + 0.5, 100 + i) for i in range(1, 40)]
    ctx = compute_context_at(bars, 38, DEFAULT_PARAMS)
    assert ctx.atr_14 is not None
    assert ctx.sma_20 is not None
    assert ctx.return_5 is not None
    assert ctx.return_20 is not None
    assert ctx.trend_direction in {"UP", "DOWN", "SIDEWAYS"}


def test_parameters_hash_stable():
    a = DetectorParams().parameters_hash()
    b = DetectorParams().parameters_hash()
    assert a == b
    c = DetectorParams(doji_body_ratio_max=0.11).parameters_hash()
    assert a != c


def test_overlap_allowed_hammer_not_doji():
    g = _g(10.0, 10.6, 8.0, 10.5)
    hits = detect_all_at_anchor([g], 0, DEFAULT_PARAMS)
    types = {h.pattern_type for h in hits}
    assert "HAMMER" in types
    assert "DOJI" not in types
