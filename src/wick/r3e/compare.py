"""Paired model comparisons and DELTA_CANDLE = M5 - M4."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from wick.quant.stats import benjamini_hochberg, block_bootstrap_mean


@dataclass
class PairResult:
    left: str
    right: str
    n: int
    mean_left: float
    mean_right: float
    delta: float
    ci_low: float
    ci_high: float
    p_raw: float
    p_adj: float | None
    effect_size: float


def paired_delta(
    returns_left: list[float],
    returns_right: list[float],
    *,
    seed: int = 42,
    n_resamples: int = 1000,
) -> PairResult:
    """Compare two strategies on the same observation set (paired)."""
    a = np.asarray(returns_left, dtype=float)
    b = np.asarray(returns_right, dtype=float)
    if len(a) != len(b):
        raise ValueError("M4/M5 (or pair) must use identical observation counts")
    mask = np.isfinite(a) & np.isfinite(b)
    a = a[mask]
    b = b[mask]
    delta = a - b  # left - right; for M5 vs M4 call with left=M5, right=M4
    if len(delta) == 0:
        return PairResult("L", "R", 0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, None, 0.0)
    boot = block_bootstrap_mean(delta.tolist(), n_resamples=n_resamples, seed=seed)
    sd = float(np.std(delta, ddof=1)) if len(delta) > 1 else 0.0
    effect = float(np.mean(delta) / sd) if sd > 1e-12 else 0.0
    return PairResult(
        left="left",
        right="right",
        n=len(delta),
        mean_left=float(np.mean(a)),
        mean_right=float(np.mean(b)),
        delta=float(np.mean(delta)),
        ci_low=boot.ci_low,
        ci_high=boot.ci_high,
        p_raw=boot.p_value_raw,
        p_adj=None,
        effect_size=effect,
    )


def apply_family_fdr(results: list[PairResult], alpha: float = 0.05) -> list[PairResult]:
    _ = alpha
    raw = [r.p_raw for r in results]
    adj = benjamini_hochberg(raw)
    out: list[PairResult] = []
    for r, p in zip(results, adj, strict=True):
        out.append(
            PairResult(
                left=r.left,
                right=r.right,
                n=r.n,
                mean_left=r.mean_left,
                mean_right=r.mean_right,
                delta=r.delta,
                ci_low=r.ci_low,
                ci_high=r.ci_high,
                p_raw=r.p_raw,
                p_adj=p,
                effect_size=r.effect_size,
            )
        )
    return out
