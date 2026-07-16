"""R3A manual formula tests — independent of production wiring."""

from __future__ import annotations

import pytest

from wick.backtest.costs import get_scenario
from wick.backtest.engine import (
    Bar,
    directional_return_bearish,
    entry_index_for,
    evaluate_signal,
    exit_index_for,
    gross_return_long,
)


def test_manual_example_100_to_103_base_cost():
    """entry=100 exit=103 gross=0.03 total_cost BASE=0.0024 net=0.0276"""
    bars = [Bar(100, 101, 99, 100)]  # t=0 unused pattern
    # entry at index 1 open=100, exit N=1 close=103 → need bars[1]
    bars = [
        Bar(99, 100, 98, 99),  # t pattern
        Bar(100, 104, 99, 103),  # t+1 entry open 100, for N=1 exit close 103
    ]
    base = get_scenario("BASE")
    assert base.total_cost == pytest.approx(0.0024)
    gross = gross_return_long(100, 103)
    assert gross == pytest.approx(0.03)
    net = gross - base.total_cost
    assert net == pytest.approx(0.0276)

    result = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bullish",
        pattern_type="HAMMER",
        horizon=1,
        confirmation_used=False,
        cost_scenario="BASE",
    )
    assert result.status == "OK"
    assert result.entry_index == 1
    assert result.exit_index == 1
    assert result.entry_price == 100
    assert result.exit_price == 103
    assert result.gross_return == pytest.approx(0.03)
    assert result.net_return == pytest.approx(0.0276)
    assert result.executable_long is True


@pytest.mark.parametrize("n,exit_i", [(1, 1), (3, 3), (5, 5), (10, 10)])
def test_horizons_exit_index(n, exit_i):
    assert exit_index_for(entry_index=1, horizon=n) == exit_i


def test_confirmation_enters_at_t_plus_2_not_t_plus_1():
    # bars: 0=pattern, 1=confirm candle, 2=entry open, ...
    bars = [
        Bar(10, 11, 9, 10),  # t
        Bar(10, 12, 10, 11),  # t+1 confirmation close=11 > close[t]
        Bar(20, 21, 19, 20.5),  # t+2 entry open MUST be used
        Bar(20.5, 22, 20, 21),  # t+3
    ]
    assert entry_index_for(pattern_index=0, confirmation_used=True) == 2
    assert entry_index_for(pattern_index=0, confirmation_used=False) == 1
    r = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bullish",
        pattern_type="HAMMER",
        horizon=1,
        confirmation_used=True,
        cost_scenario="ZERO",
    )
    assert r.entry_index == 2
    assert r.entry_price == 20
    assert r.entry_price != bars[1].open


def test_insufficient_future_data():
    bars = [Bar(1, 2, 0.5, 1.5), Bar(1.5, 2, 1, 1.8)]
    r = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bullish",
        pattern_type="HAMMER",
        horizon=5,
        confirmation_used=False,
    )
    assert r.status == "NOT_EVALUABLE_INSUFFICIENT_FUTURE_DATA"
    assert r.net_return is None


def test_bearish_is_directional_not_short_pnl():
    bars = [
        Bar(10, 11, 9, 10),
        Bar(10, 10.5, 8, 8.5),  # entry open 10, exit close 8.5 for N=1
    ]
    r = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bearish",
        pattern_type="SHOOTING_STAR",
        horizon=1,
        confirmation_used=False,
        cost_scenario="BASE",
    )
    assert r.executable_long is False
    assert r.gross_return is None
    assert r.net_return is None
    assert r.directional_return == pytest.approx(directional_return_bearish(10, 8.5))
    assert r.directional_hit is True


def test_zero_and_stressed_costs():
    bars = [Bar(1, 1, 1, 1), Bar(100, 110, 99, 103)]
    z = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bullish",
        pattern_type="HAMMER",
        horizon=1,
        confirmation_used=False,
        cost_scenario="ZERO",
    )
    s = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bullish",
        pattern_type="HAMMER",
        horizon=1,
        confirmation_used=False,
        cost_scenario="STRESSED",
    )
    assert z.net_return == pytest.approx(0.03)
    assert s.net_return == pytest.approx(0.03 - get_scenario("STRESSED").total_cost)


def test_invalid_zero_price():
    bars = [Bar(1, 1, 1, 1), Bar(0, 1, 0, 1)]
    r = evaluate_signal(
        bars,
        pattern_index=0,
        signal="bullish",
        pattern_type="HAMMER",
        horizon=1,
        confirmation_used=False,
    )
    assert r.status == "INVALID_PRICE"
