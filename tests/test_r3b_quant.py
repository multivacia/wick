"""R3B/R3C statistics and gate tests."""

from __future__ import annotations

from wick.backtest.engine import Bar
from wick.quant.baselines import paired_random_entry_returns, trend_only_returns
from wick.quant.experiments import (
    SignalEvent,
    apply_fdr_across_reports,
    run_strategy_validation,
    write_reports,
)
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
    assert report.mean_random_baseline is not None
    assert report.buy_and_hold_train is not None
    assert report.walk_forward_mean_oos is not None
    paths = write_reports([report], tmp_path)
    assert paths["technical"].exists()
    assert paths["executive"].exists()


def test_paired_random_baseline_uses_real_entries():
    bars = [Bar(100 + i * 0.05, 101, 99, 100.2 + i * 0.05) for i in range(120)]
    rets = paired_random_entry_returns(
        bars,
        n_signals=10,
        horizon=3,
        confirmation_used=False,
        cost_scenario="BASE",
        index_pool=range(0, 84),
        seed=11,
    )
    assert len(rets) == 10


def test_trend_only_baseline_produces_returns():
    bars = [Bar(100 + i * 0.2, 101 + i * 0.2, 99 + i * 0.2, 100.5 + i * 0.2) for i in range(100)]
    rets = trend_only_returns(
        bars,
        index_pool=range(0, 70),
        horizon=3,
        confirmation_used=False,
        cost_scenario="ZERO",
    )
    assert len(rets) > 0


def test_fdr_batch_across_strategies():
    bars = [Bar(100 + i * 0.1, 101 + i * 0.1, 99 + i * 0.1, 100.5 + i * 0.1) for i in range(200)]
    events = [
        SignalEvent(pattern_index=i, signal="bullish", pattern_type="HAMMER")
        for i in range(0, 150, 4)
    ]
    reports = [
        run_strategy_validation(
            bars,
            events,
            strategy_id=f"h{h}",
            description=f"N={h}",
            horizon=h,
            cost_scenario="BASE",
            n_resamples=200,
        )
        for h in (1, 3, 5)
    ]
    batched = apply_fdr_across_reports(reports)
    assert len(batched) == 3
    assert all("fdr_batched_across_strategies" in r.notes for r in batched)
