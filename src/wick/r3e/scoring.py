"""Frozen score policies — selection only on train/inner validation."""

from __future__ import annotations

import numpy as np


def select_by_policy(scores: np.ndarray, policy: str) -> np.ndarray:
    """Return boolean mask of selected observations."""
    n = len(scores)
    if n == 0:
        return np.zeros(0, dtype=bool)
    if policy == "TOP_10_PERCENT":
        k = max(1, int(np.ceil(0.10 * n)))
        order = np.argsort(scores)[::-1]
        mask = np.zeros(n, dtype=bool)
        mask[order[:k]] = True
        return mask
    if policy == "TOP_20_PERCENT":
        k = max(1, int(np.ceil(0.20 * n)))
        order = np.argsort(scores)[::-1]
        mask = np.zeros(n, dtype=bool)
        mask[order[:k]] = True
        return mask
    if policy == "PROBABILITY_055":
        return scores >= 0.55
    if policy == "PROBABILITY_060":
        return scores >= 0.60
    raise ValueError(f"Unknown score policy: {policy}")


def mean_net(returns: np.ndarray, mask: np.ndarray) -> float:
    if mask.sum() == 0:
        return float("nan")
    return float(np.mean(returns[mask]))
