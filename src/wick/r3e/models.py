"""M0–M5 model fitting — logistic L2 / Ridge / rule baselines."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from sklearn.linear_model import LogisticRegression, Ridge

from wick.r3e.config import LOGISTIC_GRID, RIDGE_GRID
from wick.r3e.preprocess import PreprocessFit, fit_preprocess, transform
from wick.r3e.scoring import mean_net, select_by_policy


@dataclass
class FittedModel:
    model_id: str
    kind: str  # random | rule_trend | logistic | ridge
    features: list[str]
    preprocess: PreprocessFit | None
    estimator: Any
    hyperparams: dict[str, Any]
    score_policy: str
    numeric_features: list[str]
    categorical_features: list[str]


def _split_feature_types(feature_names: list[str]) -> tuple[list[str], list[str]]:
    from wick.r3e.config import CANDLE_FEATURES, CATEGORICAL_FEATURES, NUMERIC_FEATURES

    cats = set(CATEGORICAL_FEATURES) | set(CANDLE_FEATURES)
    nums = set(NUMERIC_FEATURES)
    numeric = [f for f in feature_names if f in nums]
    categorical = [f for f in feature_names if f in cats]
    # any remaining treated as categorical (asset_id, timeframe already in cats)
    for f in feature_names:
        if f not in numeric and f not in categorical:
            categorical.append(f)
    return numeric, categorical


def fit_logistic(
    train_rows: list[dict[str, Any]],
    y_hit: np.ndarray,
    *,
    feature_names: list[str],
    C: float,
    class_weight: str | None,
    seed: int = 42,
) -> tuple[Any, PreprocessFit, list[str], list[str]]:
    numeric, categorical = _split_feature_types(feature_names)
    prep = fit_preprocess(train_rows, numeric_features=numeric, categorical_features=categorical)
    x, _ = transform(prep, train_rows)
    y = y_hit.astype(int)
    if len(np.unique(y)) < 2:
        # Single-class train fold: fall back to Ridge on constant-shifted labels proxy
        reg = Ridge(alpha=1.0)
        reg.fit(x, y.astype(float))
        return reg, prep, numeric, categorical
    clf = LogisticRegression(
        C=C,
        class_weight=class_weight,
        solver="lbfgs",
        max_iter=500,
        random_state=seed,
    )
    clf.fit(x, y)
    return clf, prep, numeric, categorical


def fit_ridge(
    train_rows: list[dict[str, Any]],
    y_ret: np.ndarray,
    *,
    feature_names: list[str],
    alpha: float,
) -> tuple[Any, PreprocessFit, list[str], list[str]]:
    numeric, categorical = _split_feature_types(feature_names)
    prep = fit_preprocess(train_rows, numeric_features=numeric, categorical_features=categorical)
    x, _ = transform(prep, train_rows)
    reg = Ridge(alpha=alpha)
    reg.fit(x, y_ret.astype(float))
    return reg, prep, numeric, categorical


def score_rows(fitted: FittedModel, rows: list[dict[str, Any]], *, seed: int = 42) -> np.ndarray:
    n = len(rows)
    if fitted.kind == "random":
        rng = np.random.default_rng(seed)
        return rng.random(n)
    if fitted.kind == "rule_trend":
        # Higher score when trend UP and strength not WEAK
        scores = np.zeros(n)
        for i, r in enumerate(rows):
            s = 0.0
            if r.get("trend_direction") == "UP":
                s += 0.6
            if r.get("trend_strength") in {"MODERATE", "STRONG"}:
                s += 0.3
            slope = r.get("sma_20_slope")
            if slope is not None and float(slope) > 0:
                s += min(float(slope) * 10.0, 0.1)
            scores[i] = s
        return scores
    assert fitted.preprocess is not None
    x, _ = transform(fitted.preprocess, rows)
    if fitted.kind == "logistic":
        est = fitted.estimator
        if hasattr(est, "predict_proba"):
            return est.predict_proba(x)[:, 1]
        # single-class fallback estimator (Ridge)
        return est.predict(x).astype(float)
    if fitted.kind == "ridge":
        pred = fitted.estimator.predict(x)
        return pred.astype(float)
    raise ValueError(fitted.kind)


def select_hyperparams_logistic(
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    y_train: np.ndarray,
    y_val_ret: np.ndarray,
    *,
    feature_names: list[str],
    policies: tuple[str, ...],
    seed: int = 42,
) -> tuple[dict[str, Any], str, float]:
    """Grid search with preprocess fit once on train (leakage-safe, same grid)."""
    best = {"C": 1.0, "class_weight": None}
    best_policy = policies[0]
    best_score = float("-inf")
    numeric, categorical = _split_feature_types(feature_names)
    prep = fit_preprocess(train_rows, numeric_features=numeric, categorical_features=categorical)
    x_tr, _ = transform(prep, train_rows)
    x_va, _ = transform(prep, val_rows)
    y = y_train.astype(int)
    single_class = len(np.unique(y)) < 2
    for C in LOGISTIC_GRID["C"]:
        for cw in LOGISTIC_GRID["class_weight"]:
            if single_class:
                est = Ridge(alpha=1.0)
                est.fit(x_tr, y.astype(float))
                scores = est.predict(x_va).astype(float)
            else:
                est = LogisticRegression(
                    C=C,
                    class_weight=cw,
                    solver="lbfgs",
                    max_iter=500,
                    random_state=seed,
                )
                est.fit(x_tr, y)
                scores = est.predict_proba(x_va)[:, 1]
            for pol in policies:
                mask = select_by_policy(scores, pol)
                m = mean_net(y_val_ret, mask)
                if np.isnan(m):
                    continue
                if m > best_score:
                    best_score = m
                    best = {"C": C, "class_weight": cw}
                    best_policy = pol
    return best, best_policy, best_score


def select_hyperparams_ridge(
    train_rows: list[dict[str, Any]],
    val_rows: list[dict[str, Any]],
    y_train_ret: np.ndarray,
    y_val_ret: np.ndarray,
    *,
    feature_names: list[str],
    policies: tuple[str, ...],
    seed: int = 42,
) -> tuple[dict[str, Any], str, float]:
    """Grid search with preprocess fit once on train (leakage-safe, same grid)."""
    _ = seed
    best = {"alpha": 1.0}
    best_policy = policies[0]
    best_score = float("-inf")
    numeric, categorical = _split_feature_types(feature_names)
    prep = fit_preprocess(train_rows, numeric_features=numeric, categorical_features=categorical)
    x_tr, _ = transform(prep, train_rows)
    x_va, _ = transform(prep, val_rows)
    y = y_train_ret.astype(float)
    for alpha in RIDGE_GRID["alpha"]:
        est = Ridge(alpha=alpha)
        est.fit(x_tr, y)
        scores = est.predict(x_va).astype(float)
        for pol in policies:
            # For ridge, PROBABILITY_* thresholds are not probability — skip those
            if pol.startswith("PROBABILITY_"):
                continue
            mask = select_by_policy(scores, pol)
            m = mean_net(y_val_ret, mask)
            if np.isnan(m):
                continue
            if m > best_score:
                best_score = m
                best = {"alpha": alpha}
                best_policy = pol
    return best, best_policy, best_score
