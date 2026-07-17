"""R3E orchestration: nested WF on development set, M0–M5, M5 vs M4."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from wick.backtest.engine import Bar
from wick.quant.stats import block_bootstrap_mean
from wick.r3e.compare import PairResult, apply_family_fdr, paired_delta
from wick.r3e.config import (
    FEATURE_SETS,
    HORIZONS,
    INNER_VAL_FRAC,
    N_BOOTSTRAP,
    OUTER_MIN_TRAIN,
    OUTER_TEST_SIZE,
    RANDOM_SEED,
    SCORE_POLICIES,
)
from wick.r3e.dataset import (
    Observation,
    compute_targets,
    data_snapshot_hash,
    filter_development,
    non_overlapping_mask,
)
from wick.r3e.gates import classify_r3e, final_gate_state
from wick.r3e.manifest import build_manifest, freeze_manifest
from wick.r3e.models import (
    FittedModel,
    fit_logistic,
    fit_ridge,
    score_rows,
    select_hyperparams_logistic,
    select_hyperparams_ridge,
)
from wick.r3e.nested_wf import assert_no_future_in_train, nested_walk_forward
from wick.r3e.scoring import mean_net, select_by_policy


def _rows(obs: list[Observation]) -> list[dict[str, Any]]:
    return [o.feature_dict() for o in obs]


def _finite(returns: list[float], mask: np.ndarray) -> list[float]:
    out = []
    for i, m in enumerate(mask):
        if m and np.isfinite(returns[i]):
            out.append(float(returns[i]))
    return out


def run_model_nested(
    model_id: str,
    observations: list[Observation],
    nets: list[float],
    hits: list[int],
    *,
    horizon: int,
    overlap_policy: str,
    seed: int = RANDOM_SEED,
) -> dict[str, Any]:
    """Run nested WF for one model; returns OOS selected returns and metadata."""
    n = len(observations)
    nested = nested_walk_forward(
        n,
        outer_min_train=min(OUTER_MIN_TRAIN, max(40, n // 3)),
        outer_test_size=min(OUTER_TEST_SIZE, max(20, n // 8)),
        inner_val_frac=INNER_VAL_FRAC,
    )
    oos_returns: list[float] = []
    selected_hyper: dict[str, Any] = {}
    selected_policy = "TOP_20_PERCENT"
    train_windows = []
    test_windows = []

    for fold_i, nf in enumerate(nested):
        assert_no_future_in_train(nf.outer)
        for inn in nf.inner_folds:
            assert_no_future_in_train(inn)

        tr = nf.outer.train_idx
        te = nf.outer.test_idx
        inner = nf.inner_folds[0]
        train_rows = _rows([observations[i] for i in inner.train_idx])
        val_rows = _rows([observations[i] for i in inner.test_idx])
        y_tr_hit = np.asarray([hits[i] for i in inner.train_idx], dtype=int)
        y_tr_ret = np.asarray([nets[i] for i in inner.train_idx], dtype=float)
        y_va_ret = np.asarray([nets[i] for i in inner.test_idx], dtype=float)

        # Replace nan targets in train with 0 for fitting only (masked separately for economics)
        y_tr_hit = np.nan_to_num(y_tr_hit, nan=0.0).astype(int)
        y_tr_ret = np.nan_to_num(y_tr_ret, nan=0.0)

        if model_id == "M0":
            fitted = FittedModel(
                model_id="M0",
                kind="random",
                features=[],
                preprocess=None,
                estimator=None,
                hyperparams={},
                score_policy="TOP_20_PERCENT",
                numeric_features=[],
                categorical_features=[],
            )
            selected_policy = "TOP_20_PERCENT"
            selected_hyper = {}
        elif model_id == "M1":
            feats = list(FEATURE_SETS["M1"])
            # rule trend — no sklearn hyperparams; policy selected on inner val
            fitted = FittedModel(
                model_id="M1",
                kind="rule_trend",
                features=feats,
                preprocess=None,
                estimator=None,
                hyperparams={},
                score_policy="TOP_20_PERCENT",
                numeric_features=[],
                categorical_features=[],
            )
            scores_val = score_rows(fitted, val_rows, seed=seed + fold_i)
            best_pol, best_s = "TOP_20_PERCENT", float("-inf")
            for pol in SCORE_POLICIES:
                if pol.startswith("PROBABILITY_"):
                    continue
                m = mean_net(y_va_ret, select_by_policy(scores_val, pol))
                if np.isfinite(m) and m > best_s:
                    best_s, best_pol = m, pol
            selected_policy = best_pol
            fitted.score_policy = best_pol
            selected_hyper = {"kind": "rule_trend"}
            # refit concept N/A — score on full outer train then test
            train_rows_full = _rows([observations[i] for i in tr])
            _ = train_rows_full
        else:
            feats = list(FEATURE_SETS[model_id])
            # Use logistic for hit + policy; primary economic score from selected trades
            hp, pol, _ = select_hyperparams_logistic(
                train_rows,
                val_rows,
                y_tr_hit,
                y_va_ret,
                feature_names=feats,
                policies=SCORE_POLICIES,
                seed=seed + fold_i,
            )
            # Also consider ridge for return; keep logistic as official classifier path
            hp_r, pol_r, s_r = select_hyperparams_ridge(
                train_rows,
                val_rows,
                y_tr_ret,
                y_va_ret,
                feature_names=feats,
                policies=SCORE_POLICIES,
                seed=seed + fold_i,
            )
            # Choose better inner economic score between logistic and ridge
            # Recompute logistic best score
            est_l, prep_l, num_l, cat_l = fit_logistic(
                train_rows,
                y_tr_hit,
                feature_names=feats,
                C=hp["C"],
                class_weight=hp["class_weight"],
                seed=seed,
            )
            tmp_l = FittedModel("tmp", "logistic", feats, prep_l, est_l, hp, pol, num_l, cat_l)
            s_l = mean_net(y_va_ret, select_by_policy(score_rows(tmp_l, val_rows, seed=seed), pol))
            if np.isfinite(s_r) and (not np.isfinite(s_l) or s_r > s_l):
                est, prep, num, cat = fit_ridge(
                    _rows([observations[i] for i in tr]),
                    np.nan_to_num(np.asarray([nets[i] for i in tr], dtype=float), nan=0.0),
                    feature_names=feats,
                    alpha=hp_r["alpha"],
                )
                fitted = FittedModel(model_id, "ridge", feats, prep, est, hp_r, pol_r, num, cat)
                selected_policy = pol_r
                selected_hyper = {"kind": "ridge", **hp_r}
            else:
                est, prep, num, cat = fit_logistic(
                    _rows([observations[i] for i in tr]),
                    np.nan_to_num(np.asarray([hits[i] for i in tr], dtype=float), nan=0.0).astype(
                        int
                    ),
                    feature_names=feats,
                    C=hp["C"],
                    class_weight=hp["class_weight"],
                    seed=seed,
                )
                fitted = FittedModel(model_id, "logistic", feats, prep, est, hp, pol, num, cat)
                selected_policy = pol
                selected_hyper = {"kind": "logistic", **hp}

        # Outer test once
        if model_id == "M1":
            fitted = FittedModel(
                model_id="M1",
                kind="rule_trend",
                features=list(FEATURE_SETS["M1"]),
                preprocess=None,
                estimator=None,
                hyperparams={},
                score_policy=selected_policy,
                numeric_features=[],
                categorical_features=[],
            )
        test_rows = _rows([observations[i] for i in te])
        scores = score_rows(fitted, test_rows, seed=seed + 1000 + fold_i)
        mask = select_by_policy(scores, selected_policy)
        if overlap_policy == "NON_OVERLAPPING_LONG_ONLY":
            obs_te = [observations[i] for i in te]
            mask_list = non_overlapping_mask(obs_te, mask.tolist(), horizon=horizon)
            mask = np.asarray(mask_list, dtype=bool)
        rets = [nets[i] for i in te]
        oos_returns.extend(_finite(rets, mask))
        train_windows.append({"fold": fold_i, "train": [min(tr), max(tr)], "n": len(tr)})
        test_windows.append({"fold": fold_i, "test": [min(te), max(te)], "n": len(te)})

    boot = (
        block_bootstrap_mean(oos_returns, n_resamples=N_BOOTSTRAP, seed=seed)
        if oos_returns
        else None
    )
    return {
        "model_id": model_id,
        "n_oos_trades": len(oos_returns),
        "mean_net": float(np.mean(oos_returns)) if oos_returns else None,
        "ci95": [boot.ci_low, boot.ci_high] if boot else None,
        "p_raw": boot.p_value_raw if boot else None,
        "selected_hyperparameters": selected_hyper,
        "score_policy": selected_policy,
        "oos_returns": oos_returns,
        "train_windows": train_windows,
        "test_windows": test_windows,
        "overlap_policy": overlap_policy,
    }


def run_r3e_on_series(
    bars: list[Bar],
    observations: list[Observation],
    *,
    horizon: int = 5,
    cost_scenario: str = "BASE",
    overlap_policy: str = "NON_OVERLAPPING_LONG_ONLY",
) -> dict[str, Any]:
    dev = filter_development(observations)
    # Keep only observations with evaluable future
    nets_all, hits_all = compute_targets(bars, dev, horizon=horizon, cost_scenario=cost_scenario)
    keep = [i for i, v in enumerate(nets_all) if np.isfinite(v)]
    dev = [dev[i] for i in keep]
    nets = [nets_all[i] for i in keep]
    hits = [hits_all[i] for i in keep]

    results = {}
    for mid in ("M0", "M1", "M2", "M3", "M4", "M5"):
        results[mid] = run_model_nested(
            mid, dev, nets, hits, horizon=horizon, overlap_policy=overlap_policy
        )

    # Paired comparisons on available OOS trade returns — align by truncating to min length
    pairs_spec = [("M1", "M0"), ("M2", "M1"), ("M3", "M2"), ("M4", "M3"), ("M5", "M4")]
    pair_results: list[PairResult] = []
    for left, right in pairs_spec:
        a = results[left]["oos_returns"]
        b = results[right]["oos_returns"]
        n = min(len(a), len(b))
        if n == 0:
            continue
        pr = paired_delta(a[:n], b[:n], seed=RANDOM_SEED, n_resamples=N_BOOTSTRAP)
        pr.left, pr.right = left, right
        pair_results.append(pr)
    pair_results = apply_family_fdr(pair_results)

    m5_vs_m4 = next((p for p in pair_results if p.left == "M5" and p.right == "M4"), None)
    m4 = results["M4"]
    context_promising = (
        m4["mean_net"] is not None
        and m4["mean_net"] > 0
        and m4["p_raw"] is not None
        and m4["p_raw"] <= 0.05
        and m4["n_oos_trades"] >= 30
    )
    candle_adds = (
        m5_vs_m4 is not None
        and m5_vs_m4.delta > 0
        and m5_vs_m4.p_adj is not None
        and m5_vs_m4.p_adj <= 0.05
        and m5_vs_m4.ci_low > 0
    )
    classification = classify_r3e(
        context_promising=bool(context_promising),
        candle_adds_value=bool(candle_adds),
        candle_delta_positive_stable=bool(
            candle_adds and m5_vs_m4 is not None and m5_vs_m4.effect_size > 0
        ),
        mean_net_m5=results["M5"]["mean_net"],
        has_critical_findings=False,
        fdr_reported=True,
    )
    return {
        "horizon": horizon,
        "cost_scenario": cost_scenario,
        "overlap_policy": overlap_policy,
        "n_dev_observations": len(dev),
        "models": {
            k: {kk: vv for kk, vv in v.items() if kk != "oos_returns"}
            | {"oos_returns_n": len(v["oos_returns"])}
            for k, v in results.items()
        },
        "pairs": [asdict(p) for p in pair_results],
        "delta_candle": asdict(m5_vs_m4) if m5_vs_m4 else None,
        "classification": classification,
        "gate": final_gate_state(classification),
        "_oos": {k: v["oos_returns"] for k, v in results.items()},
    }


def run_r3e_experiment(
    series: list[dict[str, Any]],
    out_dir: Path,
    *,
    horizons: tuple[int, ...] = HORIZONS,
    cost_scenarios: tuple[str, ...] = ("BASE", "OPTIMISTIC", "STRESSED"),
) -> dict[str, Any]:
    """series items: {bars, volumes, observations, asset_id, timeframe}"""
    out_dir.mkdir(parents=True, exist_ok=True)
    snap = data_snapshot_hash(
        "|".join(f"{s['asset_id']}:{s['timeframe']}:{len(s['bars'])}" for s in series)
    )

    # Freeze manifesto before evaluating (declare windows policy + grids)
    manifest = build_manifest(
        data_snapshot_hash=snap,
        train_windows=[{"policy": "nested_walk_forward_expanding"}],
        test_windows=[{"policy": "outer_test_once_per_window"}],
        selected_hyperparameters={"note": "selected per fold on inner validation only"},
        score_policy={"allowed": list(SCORE_POLICIES)},
        extra={"n_series": len(series)},
    )
    freeze_manifest(out_dir / "experiment_manifest.json", manifest)

    all_results = []
    concentration_asset: Counter[str] = Counter()
    for s in series:
        for h in horizons:
            for cost in cost_scenarios:
                for overlap in ("ALL_SIGNALS", "NON_OVERLAPPING_LONG_ONLY"):
                    # Limit cost×horizon×overlap explosion for ALL_SIGNALS primary BASE
                    if cost != "BASE" and overlap != "NON_OVERLAPPING_LONG_ONLY":
                        continue
                    if h not in (1, 5) and not (
                        cost == "BASE" and overlap == "NON_OVERLAPPING_LONG_ONLY"
                    ):
                        continue
                    res = run_r3e_on_series(
                        s["bars"],
                        s["observations"],
                        horizon=h,
                        cost_scenario=cost,
                        overlap_policy=overlap,
                    )
                    res["asset_id"] = s["asset_id"]
                    res["timeframe"] = s["timeframe"]
                    concentration_asset[s["asset_id"]] += 1
                    # drop bulky
                    res.pop("_oos", None)
                    all_results.append(res)

    # Aggregate M5-M4 across BASE/h5/non-overlap
    deltas = [
        r["delta_candle"]
        for r in all_results
        if r.get("delta_candle")
        and r["cost_scenario"] == "BASE"
        and r["horizon"] == 5
        and r["overlap_policy"] == "NON_OVERLAPPING_LONG_ONLY"
    ]
    classifications = Counter(r["classification"] for r in all_results)

    executive = {
        **final_gate_state(
            "CANDLE_ADDS_VALUE"
            if classifications.get("CANDLE_ADDS_VALUE", 0) > 0
            else (
                "CONTEXT_PROMISING"
                if classifications.get("CONTEXT_PROMISING", 0) > 0
                else (
                    "NEGATIVE"
                    if classifications.get("NEGATIVE", 0) >= classifications.get("INCONCLUSIVE", 0)
                    else "INCONCLUSIVE"
                )
            )
        ),
        "experiment_id": manifest["experiment_id"],
        "parent_experiment_id": manifest["parent_experiment_id"],
        "data_snapshot_hash": snap,
        "n_series": len(series),
        "n_result_rows": len(all_results),
        "classification_counts": dict(classifications),
        "delta_candle_base_h5_nonoverlap": deltas,
        "concentration_by_asset": dict(concentration_asset),
        "r3d_holdout_reused": False,
        "paper_trading_started": False,
        "limitations": [
            "R3E_GATE remains PENDING_FUTURE_UNSEEN_DATA even if promising",
            "COST_MODEL_VERSION=1.0.0-provisional unchanged",
            "R3D holdout excluded; not used as final validation",
        ],
    }
    # Override gate always
    executive["R3E_GATE"] = "PENDING_FUTURE_UNSEEN_DATA"
    executive["R4_STATUS"] = "BLOCKED"
    executive["R5_STATUS"] = "NOT_STARTED"

    technical = {
        "manifest_ref": "experiment_manifest.json",
        "results": all_results,
        "executive": executive,
    }
    (out_dir / "technical_report.json").write_text(
        json.dumps(technical, indent=2, default=str) + "\n", encoding="utf-8"
    )
    (out_dir / "executive_report.json").write_text(
        json.dumps(executive, indent=2) + "\n", encoding="utf-8"
    )
    return executive
