#!/usr/bin/env python3
"""Run R3E nested-WF development experiment on synthetic multi-asset panel.

Labeled synthetic — not a substitute for future unseen real validation.
R3D holdout semantics are still applied (final 30% excluded).
"""

from __future__ import annotations

from pathlib import Path

from wick.backtest.engine import Bar
from wick.r3e.dataset import build_observations
from wick.r3e.pipeline import run_r3e_experiment


def make_series(asset: str, timeframe: str, n: int = 360, seed: int = 0) -> dict:
    bars: list[Bar] = []
    price = 100.0 + seed
    vols = []
    for i in range(n):
        drift = 0.012 if ((i + seed) // 6) % 2 == 0 else -0.01
        price = max(1.0, price * (1.0 + drift + ((i % 11) - 5) * 0.0005))
        bars.append(Bar(price, price * 1.01, price * 0.99, price * (1.0 + drift * 0.2)))
        vols.append(1000.0 + (i % 9) * 25.0)
    patterns = {
        i: {
            "pattern_type": "HAMMER" if i % 12 else "BULLISH_ENGULFING",
            "signal": "bullish",
            "confirmation_variant": "raw" if i % 2 == 0 else "confirmed",
        }
        for i in range(110, n - 15, 5)
    }
    obs = build_observations(
        bars,
        vols,
        asset_id=asset,
        timeframe=timeframe,
        pattern_at_index=patterns,
        warmup=100,
    )
    return {
        "bars": bars,
        "volumes": vols,
        "observations": obs,
        "asset_id": asset,
        "timeframe": timeframe,
    }


def main() -> None:
    assets = [
        ("BTC/USDT", "1h"),
        ("ETH/USDT", "1d"),
        ("PETR4.SA", "1d"),
        ("AAPL", "1h"),
        ("MSFT", "1d"),
    ]
    series = [make_series(a, tf, n=360, seed=i * 3) for i, (a, tf) in enumerate(assets)]
    out = Path("reports/r3e")
    executive = run_r3e_experiment(
        series,
        out,
        horizons=(1, 5),
        cost_scenarios=("BASE", "OPTIMISTIC", "STRESSED"),
    )
    print(executive)


if __name__ == "__main__":
    main()
