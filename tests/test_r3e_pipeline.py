"""R3E pipeline smoke tests on synthetic series."""

from __future__ import annotations

from wick.backtest.engine import Bar
from wick.r3e.dataset import build_observations
from wick.r3e.pipeline import run_r3e_experiment, run_r3e_on_series


def _series(n: int = 320, asset: str = "SYN"):
    # Oscillating path so directional hits are not single-class
    bars = []
    price = 100.0
    for i in range(n):
        price = price * (1.0 + (0.01 if (i // 5) % 2 == 0 else -0.008))
        bars.append(Bar(price, price * 1.01, price * 0.99, price * 1.001))
    vols = [1000 + (i % 7) * 10.0 for i in range(n)]
    patterns = {
        i: {"pattern_type": "HAMMER", "signal": "bullish", "confirmation_variant": "raw"}
        for i in range(110, n - 20, 6)
    }
    obs = build_observations(
        bars, vols, asset_id=asset, timeframe="1d", pattern_at_index=patterns, warmup=100
    )
    return {
        "bars": bars,
        "volumes": vols,
        "observations": obs,
        "asset_id": asset,
        "timeframe": "1d",
    }


def test_run_r3e_on_series_smoke():
    s = _series()
    res = run_r3e_on_series(s["bars"], s["observations"], horizon=5, cost_scenario="BASE")
    assert set(res["models"]) == {"M0", "M1", "M2", "M3", "M4", "M5"}
    assert res["gate"]["R3E_GATE"] == "PENDING_FUTURE_UNSEEN_DATA"
    assert res["gate"]["R4_STATUS"] == "BLOCKED"
    assert res.get("delta_candle") is not None or res["models"]["M5"]["n_oos_trades"] == 0


def test_experiment_writes_reports(tmp_path):
    series = [_series(300, "A"), _series(300, "B")]
    # Narrow run via monkeypatching would be heavy; call with defaults but series small
    executive = run_r3e_experiment(
        series,
        tmp_path,
        horizons=(5,),
        cost_scenarios=("BASE",),
    )
    assert (tmp_path / "experiment_manifest.json").exists()
    assert (tmp_path / "executive_report.json").exists()
    assert (tmp_path / "technical_report.json").exists()
    assert executive["R3E_GATE"] == "PENDING_FUTURE_UNSEEN_DATA"
    assert executive["r3d_holdout_reused"] is False
    assert executive["paper_trading_started"] is False
