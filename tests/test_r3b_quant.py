"""R3B/R3C statistics and gate tests."""

from __future__ import annotations

from wick.backtest.engine import Bar
from wick.quant.experiments import SignalEvent, run_strategy_validation, write_reports
from wick.quant.stats import (
    benjamini_hochberg,
    block_bootstrap_mean,
    mechanical_gate,
    sample_size_tier,
    temporal_split,
)


def test_temporal_split_70_30():
    train, hold = temporal_split(100, 0.7)
    assert len(train) == 70
    assert len(hold) == 30
    assert train.stop == hold.start


def test_sample_tiers():
    assert sample_size_tier(10) == "INSUFFICIENT"
    assert sample_size_tier(50) == "EXPLORATORY"
    assert sample_size_tier(150) == "MODERATE"
    assert sample_size_tier(300) == "RELIABLE"


def test_bh_fdr_bounds():
    raw = [0.01, 0.04, 0.03, 0.20]
    adj = benjamini_hochberg(raw)
    assert len(adj) == 4
    assert all(0 <= a <= 1 for a in adj)
    assert all(a + 1e-12 >= p for a, p in zip(adj, raw, strict=True))


def test_block_bootstrap_reproducible():
    rets = [0.01, -0.005, 0.02, 0.0, 0.015] * 20
    a = block_bootstrap_mean(rets, n_resamples=500, seed=7)
    b = block_bootstrap_mean(rets, n_resamples=500, seed=7)
    assert a.mean == b.mean
    assert a.ci_low == b.ci_low
    assert a.p_value_raw == b.p_value_raw


def test_mechanical_gate_blocks_critical():
    assert (
        mechanical_gate(
            classification="PROMISING",
            holdout_touched_during_calibration=False,
            has_critical_findings=True,
            cost_scenarios_evaluated=True,
            fdr_applied=True,
        )
        == "FAILS_CRITERIA"
    )


def test_strategy_validation_smoke(tmp_path):
    # Synthetic mild positive edge on bullish events
    bars = [Bar(100 + i * 0.1, 101 + i * 0.1, 99 + i * 0.1, 100.5 + i * 0.1) for i in range(200)]
    events = [
        SignalEvent(pattern_index=i, signal="bullish", pattern_type="HAMMER")
        for i in range(0, 150, 3)
    ]
    report = run_strategy_validation(
        bars,
        events,
        strategy_id="hammer_h5_base",
        description="Synthetic hammer long N=5 BASE",
        horizon=5,
        cost_scenario="BASE",
        n_resamples=200,
    )
    assert report.sample_tier in {"INSUFFICIENT", "EXPLORATORY", "MODERATE", "RELIABLE"}
    assert report.mechanical_gate in {
        "PASSES_ALL_MECHANICAL_CRITERIA",
        "FAILS_CRITERIA",
        "INCONCLUSIVE",
        "REQUIRES_HUMAN_REVIEW",
    }
    paths = write_reports([report], tmp_path)
    assert paths["technical"].exists()
    assert paths["executive"].exists()
