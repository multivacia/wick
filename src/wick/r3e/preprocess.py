"""Leakage-safe preprocessing: impute / one-hot / scale fit on train only."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass
class PreprocessFit:
    numeric_features: list[str]
    categorical_features: list[str]
    numeric_medians: dict[str, float]
    categorical_levels: dict[str, list[str]]
    scale_mean: np.ndarray
    scale_std: np.ndarray
    feature_names_: list[str] = field(default_factory=list)
    unknown_category_counts: dict[str, int] = field(default_factory=dict)


def _is_missing(v: Any) -> bool:
    if v is None:
        return True
    if isinstance(v, float) and (np.isnan(v) or np.isinf(v)):
        return True
    if isinstance(v, str) and v.upper() in {"", "UNKNOWN", "NONE", "NAN"}:
        return False  # UNKNOWN is explicit category, not numeric missing
    return False


def fit_preprocess(
    rows: list[dict[str, Any]],
    *,
    numeric_features: list[str],
    categorical_features: list[str],
) -> PreprocessFit:
    medians: dict[str, float] = {}
    for col in numeric_features:
        vals = [
            float(r[col]) for r in rows if r.get(col) is not None and not _num_missing(r.get(col))
        ]
        medians[col] = float(np.median(vals)) if vals else 0.0

    levels: dict[str, list[str]] = {}
    for col in categorical_features:
        seen: set[str] = set()
        for r in rows:
            v = r.get(col)
            if v is None:
                seen.add("UNKNOWN")
            else:
                seen.add(str(v))
        # UNKNOWN always available
        seen.add("UNKNOWN")
        levels[col] = sorted(seen)

    # Build train matrix to fit scaler
    x_raw = transform_raw(
        rows, numeric_features, categorical_features, medians, levels, track_unknown=None
    )
    mean = x_raw.mean(axis=0) if len(x_raw) else np.zeros(0)
    std = x_raw.std(axis=0) if len(x_raw) else np.ones(0)
    std = np.where(std < 1e-12, 1.0, std)
    names = _feature_names(numeric_features, categorical_features, levels)
    return PreprocessFit(
        numeric_features=list(numeric_features),
        categorical_features=list(categorical_features),
        numeric_medians=medians,
        categorical_levels=levels,
        scale_mean=mean,
        scale_std=std,
        feature_names_=names,
    )


def _num_missing(v: Any) -> bool:
    if v is None:
        return True
    try:
        f = float(v)
    except (TypeError, ValueError):
        return True
    return bool(np.isnan(f) or np.isinf(f))


def _feature_names(
    numeric_features: list[str],
    categorical_features: list[str],
    levels: dict[str, list[str]],
) -> list[str]:
    names = list(numeric_features)
    for col in categorical_features:
        for lvl in levels[col]:
            names.append(f"{col}={lvl}")
    return names


def transform_raw(
    rows: list[dict[str, Any]],
    numeric_features: list[str],
    categorical_features: list[str],
    medians: dict[str, float],
    levels: dict[str, list[str]],
    track_unknown: dict[str, int] | None,
) -> np.ndarray:
    out = np.zeros(
        (len(rows), len(numeric_features) + sum(len(levels[c]) for c in categorical_features))
    )
    for i, r in enumerate(rows):
        col_i = 0
        for col in numeric_features:
            v = r.get(col)
            if _num_missing(v):
                out[i, col_i] = medians[col]
            else:
                out[i, col_i] = float(v)
            col_i += 1
        for col in categorical_features:
            raw = r.get(col)
            key = "UNKNOWN" if raw is None else str(raw)
            if key not in levels[col]:
                if track_unknown is not None:
                    track_unknown[col] = track_unknown.get(col, 0) + 1
                key = "UNKNOWN"  # ignore unseen explicitly
            for lvl in levels[col]:
                out[i, col_i] = 1.0 if key == lvl else 0.0
                col_i += 1
    return out


def transform(fit: PreprocessFit, rows: list[dict[str, Any]]) -> tuple[np.ndarray, dict[str, int]]:
    unknown: dict[str, int] = {}
    raw = transform_raw(
        rows,
        fit.numeric_features,
        fit.categorical_features,
        fit.numeric_medians,
        fit.categorical_levels,
        track_unknown=unknown,
    )
    if raw.size == 0:
        return raw, unknown
    scaled = (raw - fit.scale_mean) / fit.scale_std
    fit.unknown_category_counts = unknown
    return scaled, unknown
