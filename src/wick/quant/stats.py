"""R3B statistical helpers — block bootstrap, FDR, temporal split."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np


def temporal_split(n: int, train_frac: float = 0.70) -> tuple[range, range]:
    if not 0 < train_frac < 1:
        raise ValueError("train_frac must be in (0,1)")
    cut = int(math.floor(n * train_frac))
    return range(0, cut), range(cut, n)


def sample_size_tier(n: int) -> str:
    if n < 30:
        return "INSUFFICIENT"
    if n < 100:
        return "EXPLORATORY"
    if n < 300:
        return "MODERATE"
    return "RELIABLE"


def benjamini_hochberg(p_values: Sequence[float], alpha: float = 0.05) -> list[float]:
    """BH-adjusted p-values; ``alpha`` reserved for callers applying rejection."""
    _ = alpha
    m = len(p_values)
    if m == 0:
        return []
    order = sorted(range(m), key=lambda i: p_values[i])
    adjusted = [0.0] * m
    running = 1.0
    # Traverse from largest p to smallest
    for k in range(m, 0, -1):
        idx = order[k - 1]
        running = min(running, p_values[idx] * m / k)
        adjusted[idx] = min(running, 1.0)
    return adjusted


@dataclass(frozen=True)
class BootstrapResult:
    mean: float
    ci_low: float
    ci_high: float
    p_value_raw: float
    n_resamples: int
    seed: int


def block_bootstrap_mean(
    returns: Sequence[float],
    *,
    block_size: int = 5,
    n_resamples: int = 1000,
    seed: int = 42,
    alternative: str = "greater",
) -> BootstrapResult:
    rng = np.random.default_rng(seed)
    x = np.asarray(list(returns), dtype=float)
    n = len(x)
    if n == 0:
        return BootstrapResult(0.0, 0.0, 0.0, 1.0, n_resamples, seed)
    if block_size < 1:
        raise ValueError("block_size must be >= 1")

    means = np.empty(n_resamples, dtype=float)
    n_blocks = int(math.ceil(n / block_size))
    max_start = max(n - block_size + 1, 1)
    for i in range(n_resamples):
        pieces = []
        for _ in range(n_blocks):
            start = int(rng.integers(0, max_start))
            pieces.append(x[start : start + block_size])
        sample = np.concatenate(pieces)[:n]
        means[i] = float(sample.mean())

    obs = float(x.mean())
    ci_low, ci_high = np.quantile(means, [0.025, 0.975])
    if alternative == "greater":
        p_raw = float(np.mean(means <= 0.0))
    else:
        p_raw = float(np.mean(means >= 0.0))
    p_raw = min(max(p_raw, 1.0 / (n_resamples + 1)), 1.0)
    return BootstrapResult(obs, float(ci_low), float(ci_high), p_raw, n_resamples, seed)


def paired_random_baseline(
    returns: Sequence[float],
    *,
    seed: int = 42,
) -> list[float]:
    rng = np.random.default_rng(seed)
    arr = np.asarray(list(returns), dtype=float).copy()
    rng.shuffle(arr)
    return arr.tolist()


def walk_forward_slices(
    n_train: int,
    *,
    min_train: int = 50,
    step: int = 20,
) -> list[tuple[range, range]]:
    folds: list[tuple[range, range]] = []
    cut = min_train
    while cut < n_train:
        test_end = min(cut + step, n_train)
        if test_end <= cut:
            break
        folds.append((range(0, cut), range(cut, test_end)))
        cut = test_end
    return folds


def classify_result(
    *,
    n: int,
    mean_net: float,
    p_adj: float,
    beats_baseline: bool,
    alpha: float = 0.05,
) -> str:
    tier = sample_size_tier(n)
    if tier == "INSUFFICIENT":
        return "INCONCLUSIVE"
    if mean_net <= 0:
        return "NEGATIVE"
    if p_adj <= alpha and beats_baseline and tier in {"MODERATE", "RELIABLE"}:
        return "PROMISING"
    if p_adj <= alpha and beats_baseline:
        return "INCONCLUSIVE"
    if mean_net > 0 and p_adj > alpha:
        return "INCONCLUSIVE"
    return "NO_EDGE"


def mechanical_gate(
    *,
    classification: str,
    holdout_touched_during_calibration: bool,
    has_critical_findings: bool,
    cost_scenarios_evaluated: bool,
    fdr_applied: bool,
) -> str:
    if has_critical_findings or holdout_touched_during_calibration:
        return "FAILS_CRITERIA"
    if not cost_scenarios_evaluated or not fdr_applied:
        return "REQUIRES_HUMAN_REVIEW"
    if classification == "PROMISING":
        return "PASSES_ALL_MECHANICAL_CRITERIA"
    if classification in {"INCONCLUSIVE", "NO_EDGE"}:
        return "INCONCLUSIVE"
    return "FAILS_CRITERIA"
