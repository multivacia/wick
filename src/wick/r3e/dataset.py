"""Build R3E observations from OHLCV + context + optional patterns.

Observations are closed bars with warmup; M4 and M5 share the exact same rows.
R3D holdout indices (final 30%) are flagged and excluded from R3E development.
"""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from typing import Any

from wick.backtest.costs import get_scenario
from wick.backtest.engine import Bar, evaluate_signal
from wick.features.context import OHLCV, build_geometries, compute_all_contexts
from wick.patterns.params import DEFAULT_PARAMS
from wick.r3e.config import R3D_HOLDOUT_FRAC
from wick.r3e.nested_wf import development_cutoff


@dataclass
class Observation:
    index: int
    timestamp: str | None
    asset_id: str
    timeframe: str
    # features
    trend_direction: str
    trend_strength: str
    sma_20_slope: float | None
    distance_from_sma_20: float | None
    return_5: float | None
    return_20: float | None
    volume_ratio_20: float | None
    volume_regime: str
    atr_14: float | None
    normalized_atr: float | None
    volatility_regime: str
    range_position_20: float | None
    range_position_bucket: str
    pattern_type: str
    signal: str
    confirmation_variant: str
    # targets per horizon/cost filled externally or in builder helpers
    in_r3d_holdout: bool

    def feature_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d.pop("index")
        d.pop("timestamp")
        d.pop("in_r3d_holdout")
        return d


def data_snapshot_hash(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def build_observations(
    bars: list[Bar],
    volumes: list[float],
    *,
    asset_id: str,
    timeframe: str,
    pattern_at_index: dict[int, dict[str, str]] | None = None,
    timestamps: list[str] | None = None,
    warmup: int = 100,
) -> list[Observation]:
    """Build one observation per closed bar after warmup.

    pattern_at_index maps bar index -> {pattern_type, signal, confirmation_variant}.
    Missing patterns become UNKNOWN (preserved explicitly).
    """
    ohlcv = [
        OHLCV(b.open, b.high, b.low, b.close, float(volumes[i] if i < len(volumes) else 0.0))
        for i, b in enumerate(bars)
    ]
    geoms = build_geometries(ohlcv, DEFAULT_PARAMS)
    ctxs = compute_all_contexts(ohlcv, DEFAULT_PARAMS, geoms)
    n = len(bars)
    cut = development_cutoff(n, R3D_HOLDOUT_FRAC)
    pattern_at_index = pattern_at_index or {}
    out: list[Observation] = []
    for i in range(warmup, n):
        ctx = ctxs[i]
        pat = pattern_at_index.get(i, {})
        out.append(
            Observation(
                index=i,
                timestamp=timestamps[i] if timestamps else None,
                asset_id=asset_id,
                timeframe=timeframe,
                trend_direction=ctx.trend_direction,
                trend_strength=ctx.trend_strength,
                sma_20_slope=ctx.sma_20_slope,
                distance_from_sma_20=ctx.distance_from_sma_20,
                return_5=ctx.return_5,
                return_20=ctx.return_20,
                volume_ratio_20=ctx.volume_ratio_20,
                volume_regime=ctx.volume_regime,
                atr_14=ctx.atr_14,
                normalized_atr=ctx.normalized_atr,
                volatility_regime=ctx.volatility_regime,
                range_position_20=ctx.range_position_20,
                range_position_bucket=ctx.range_position_bucket,
                pattern_type=pat.get("pattern_type", "UNKNOWN"),
                signal=pat.get("signal", "UNKNOWN"),
                confirmation_variant=pat.get("confirmation_variant", "UNKNOWN"),
                in_r3d_holdout=i >= cut,
            )
        )
    return out


def compute_targets(
    bars: list[Bar],
    observations: list[Observation],
    *,
    horizon: int,
    cost_scenario: str,
) -> tuple[list[float], list[int]]:
    """net_return (long from open[t+1]) and directional_hit (close[exit]>entry)."""
    _ = get_scenario  # cost scenario validated via evaluate_signal
    nets: list[float] = []
    hits: list[int] = []
    for obs in observations:
        # pattern index = bar index t; entry t+1 (context available after close t)
        r = evaluate_signal(
            bars,
            pattern_index=obs.index,
            signal="bullish",
            pattern_type=obs.pattern_type if obs.pattern_type != "UNKNOWN" else "CONTEXT",
            horizon=horizon,
            confirmation_used=False,
            cost_scenario=cost_scenario,
        )
        if r.status != "OK" or r.net_return is None:
            nets.append(float("nan"))
            hits.append(0)
        else:
            nets.append(float(r.net_return))
            hits.append(1 if (r.gross_return or 0.0) > 0 else 0)
    return nets, hits


def filter_development(observations: list[Observation]) -> list[Observation]:
    """Exclude R3D holdout from R3E development/evaluation."""
    return [o for o in observations if not o.in_r3d_holdout]


def non_overlapping_mask(
    observations: list[Observation],
    selected: list[bool],
    *,
    horizon: int,
) -> list[bool]:
    """Greedy non-overlapping long-only positions (entry=t+1, exit=entry+N-1)."""
    out = [False] * len(observations)
    last_exit = -1
    order = sorted(range(len(observations)), key=lambda i: observations[i].index)
    for i in order:
        if not selected[i]:
            continue
        entry = observations[i].index + 1
        exit_i = entry + horizon - 1
        if entry <= last_exit:
            continue
        out[i] = True
        last_exit = exit_i
    return out
