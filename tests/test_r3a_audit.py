"""Adversarial R3A — prove confirmation never uses open[t+1], no short labeling."""

from __future__ import annotations

from wick.backtest.engine import Bar, evaluate_signal


def test_adversarial_confirmation_never_uses_open_t1():
    bars = [
        Bar(50, 51, 49, 50),
        Bar(999, 1000, 998, 999),  # if wrongly used as entry, obvious
        Bar(100, 105, 99, 103),
    ]
    r = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bullish",
        pattern_type="HAMMER",
        horizon=1,
        confirmation_used=True,
        cost_scenario="ZERO",
    )
    assert r.entry_price == 100
    assert r.entry_price != 999


def test_adversarial_no_short_fields_on_bearish():
    bars = [Bar(10, 11, 9, 10), Bar(10, 10, 7, 7)]
    r = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bearish",
        pattern_type="SHOOTING_STAR",
        horizon=1,
        confirmation_used=False,
        cost_scenario="BASE",
    )
    assert r.net_return is None
    assert r.gross_return is None
    assert r.executable_long is False
    d = r.to_dict()
    assert "short_pnl" not in d
