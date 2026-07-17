"""R3E golden / adversarial tests — assume leakage until proven otherwise."""

from __future__ import annotations

import numpy as np

from wick.backtest.engine import Bar
from wick.r3e.dataset import build_observations, filter_development
from wick.r3e.manifest import build_manifest, freeze_manifest
from wick.r3e.nested_wf import assert_no_future_in_train, development_cutoff, nested_walk_forward
from wick.r3e.preprocess import fit_preprocess, transform
from wick.r3e.scoring import select_by_policy


def _bars(n: int = 200) -> list[Bar]:
    return [Bar(100 + i * 0.1, 101 + i * 0.1, 99 + i * 0.1, 100.5 + i * 0.1) for i in range(n)]


def test_development_cutoff_excludes_r3d_holdout():
    assert development_cutoff(100, 0.30) == 70


def test_nested_wf_temporal_no_leakage():
    folds = nested_walk_forward(200, outer_min_train=80, outer_test_size=40)
    assert folds
    for nf in folds:
        assert_no_future_in_train(nf.outer)
        for inn in nf.inner_folds:
            assert_no_future_in_train(inn)
            assert max(inn.train_idx) < min(inn.test_idx)


def test_scaler_fit_train_only_changes_with_train():
    rows_a = [{"x": float(i), "cat": "A" if i % 2 == 0 else "B"} for i in range(50)]
    rows_b = [{"x": float(i + 1000), "cat": "A" if i % 2 == 0 else "B"} for i in range(50)]
    fit_a = fit_preprocess(rows_a, numeric_features=["x"], categorical_features=["cat"])
    fit_b = fit_preprocess(rows_b, numeric_features=["x"], categorical_features=["cat"])
    assert fit_a.numeric_medians["x"] != fit_b.numeric_medians["x"]
    xa, _ = transform(fit_a, rows_a)
    # Transforming B with A's scaler must not refit
    xb, unk = transform(fit_a, [{"x": None, "cat": "Z"}])
    assert unk.get("cat", 0) >= 1
    assert xa.shape[1] == xb.shape[1]


def test_unknown_category_audited_not_silent_error():
    train = [{"x": 1.0, "cat": "A"}, {"x": 2.0, "cat": "B"}]
    fit = fit_preprocess(train, numeric_features=["x"], categorical_features=["cat"])
    _, unk = transform(fit, [{"x": 1.5, "cat": "NEVER_SEEN"}])
    assert unk["cat"] == 1


def test_m4_m5_same_observation_universe():
    bars = _bars(250)
    vols = [1000.0] * 250
    patterns = {
        i: {"pattern_type": "HAMMER", "signal": "bullish", "confirmation_variant": "raw"}
        for i in range(100, 200, 5)
    }
    obs = build_observations(bars, vols, asset_id="BTC", timeframe="1d", pattern_at_index=patterns)
    dev = filter_development(obs)
    # M4/M5 share rows; candle features differ but length equal
    assert all(not o.in_r3d_holdout for o in dev)
    assert any(o.in_r3d_holdout for o in obs)
    assert len(dev) < len(obs)


def test_threshold_policies_deterministic():
    scores = np.linspace(0, 1, 100)
    m10 = select_by_policy(scores, "TOP_10_PERCENT")
    m20 = select_by_policy(scores, "TOP_20_PERCENT")
    assert m10.sum() == 10
    assert m20.sum() == 20
    assert select_by_policy(scores, "PROBABILITY_060").sum() == (scores >= 0.60).sum()


def test_manifest_freeze_once(tmp_path):
    m = build_manifest(
        data_snapshot_hash="abc",
        train_windows=[],
        test_windows=[],
        selected_hyperparameters={},
        score_policy={},
    )
    path = tmp_path / "m.json"
    freeze_manifest(path, m)
    try:
        freeze_manifest(path, {**m, "frozen_at": None})
        raise AssertionError("should not refreeze")
    except RuntimeError:
        pass


def test_bearish_not_short_in_dataset_defaults():
    bars = _bars(150)
    obs = build_observations(
        bars,
        [1.0] * 150,
        asset_id="X",
        timeframe="1h",
        pattern_at_index={
            120: {
                "pattern_type": "SHOOTING_STAR",
                "signal": "bearish",
                "confirmation_variant": "raw",
            }
        },
    )
    row = next(o for o in obs if o.index == 120)
    assert row.signal == "bearish"
    # executable path in pipeline always evaluates as bullish long simulation for net_return
    # bearish remains a feature, not a short position
