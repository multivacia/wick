"""Context features computed only from candles <= t (no look-ahead)."""

from __future__ import annotations

import statistics
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from typing import Any

from wick.patterns.geometry import Geometry, compute_geometry
from wick.patterns.params import CONTEXT_VERSION, DetectorParams


@dataclass(frozen=True)
class OHLCV:
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(frozen=True)
class ContextFeatures:
    context_version: str
    trend_direction: str
    trend_strength: str
    sma_20: float | None
    sma_20_slope: float | None
    distance_from_sma_20: float | None
    return_5: float | None
    return_20: float | None
    atr_14: float | None
    normalized_atr: float | None
    volatility_regime: str
    volume_ratio_20: float | None
    volume_regime: str
    range_position_20: float | None
    range_position_bucket: str
    geometry: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return d


def _median(values: Sequence[float]) -> float | None:
    if not values:
        return None
    return float(statistics.median(values))


def _mean(values: Sequence[float]) -> float | None:
    if not values:
        return None
    return float(sum(values) / len(values))


def true_range(high: float, low: float, prev_close: float | None) -> float:
    if prev_close is None:
        return high - low
    return max(high - low, abs(high - prev_close), abs(low - prev_close))


def build_geometries(
    bars: Sequence[OHLCV],
    params: DetectorParams,
) -> list[Geometry]:
    """Build geometries with median_body from the previous ``median_body_window`` bodies."""
    out: list[Geometry] = []
    bodies: list[float] = []
    for i, bar in enumerate(bars):
        window = params.median_body_window
        med = _median(bodies[i - window : i]) if i >= window else None
        g = compute_geometry(
            open_=bar.open,
            high=bar.high,
            low=bar.low,
            close=bar.close,
            volume=bar.volume,
            params=params,
            median_body_14=med,
        )
        out.append(g)
        bodies.append(g.body)
    return out


def _normalized_atr_prefix(bars: Sequence[OHLCV], params: DetectorParams) -> list[float | None]:
    """Normalized ATR at each index using only bars <= i (None if undefined)."""
    n = len(bars)
    out: list[float | None] = [None] * n
    if n == 0:
        return out
    trs: list[float] = []
    for i in range(n):
        prev_c = bars[i - 1].close if i > 0 else None
        trs.append(true_range(bars[i].high, bars[i].low, prev_c))
        if i + 1 < params.atr_window:
            continue
        atr_i = _mean(trs[i - params.atr_window + 1 : i + 1])
        if atr_i is None or bars[i].close <= params.epsilon:
            continue
        out[i] = atr_i / bars[i].close
    return out


def compute_context_at(
    bars: Sequence[OHLCV],
    index: int,
    params: DetectorParams,
    geometries: list[Geometry] | None = None,
    *,
    normalized_atr_series: list[float | None] | None = None,
) -> ContextFeatures:
    """Context for candle ``index`` using only bars[0:index+1]."""
    if index < 0 or index >= len(bars):
        raise IndexError("index out of range")
    # No look-ahead: never read bars/geoms beyond ``index``.
    geoms = geometries if geometries is not None else build_geometries(bars[: index + 1], params)
    if len(geoms) <= index:
        raise IndexError("geometries shorter than index")
    g = geoms[index]
    t = index

    # ATR 14 — simple mean of last 14 TRs ending at t
    atr: float | None = None
    if t + 1 >= params.atr_window:
        trs: list[float] = []
        for i in range(t - params.atr_window + 1, t + 1):
            prev_c = bars[i - 1].close if i > 0 else None
            trs.append(true_range(bars[i].high, bars[i].low, prev_c))
        atr = _mean(trs)

    # SMA 20 including current
    sma: float | None = None
    slope: float | None = None
    distance: float | None = None
    w = params.sma_window
    if t + 1 >= w:
        sma = _mean([bars[i].close for i in range(t - w + 1, t + 1)])
        if t >= w:
            sma_prev = _mean([bars[i].close for i in range(t - w, t)])
            if sma is not None and sma_prev is not None and abs(sma_prev) > params.epsilon:
                slope = (sma - sma_prev) / sma_prev
        if sma is not None and abs(sma) > params.epsilon:
            distance = bars[t].close / sma - 1.0

    ret5 = bars[t].close / bars[t - 5].close - 1.0 if t >= 5 else None
    ret20 = bars[t].close / bars[t - 20].close - 1.0 if t >= 20 else None

    # Trend
    if slope is None or ret20 is None:
        trend_direction = "UNKNOWN"
    elif slope >= params.trend_up_sma_slope_min and ret20 >= params.trend_up_return_20_min:
        trend_direction = "UP"
    elif slope <= params.trend_down_sma_slope_max and ret20 <= params.trend_down_return_20_max:
        trend_direction = "DOWN"
    else:
        trend_direction = "SIDEWAYS"

    # Trend strength
    close = bars[t].close
    if atr is None or close <= params.epsilon or ret20 is None:
        trend_strength = "UNKNOWN"
    else:
        score = abs(ret20) / max(atr / close, params.epsilon)
        if score < 2:
            trend_strength = "WEAK"
        elif score < 4:
            trend_strength = "MODERATE"
        else:
            trend_strength = "STRONG"

    # Volume ratio 20 (mean includes current)
    vol_ratio: float | None = None
    volume_regime = "UNKNOWN"
    vw = params.volume_window
    if t + 1 >= vw:
        vols = [bars[i].volume for i in range(t - vw + 1, t + 1)]
        mean_vol = _mean(vols)
        cur_vol = bars[t].volume
        if mean_vol is None or mean_vol <= params.epsilon or cur_vol <= params.epsilon:
            vol_ratio = None
            volume_regime = "UNKNOWN"
        else:
            vol_ratio = cur_vol / mean_vol
            if vol_ratio < 0.75:
                volume_regime = "LOW"
            elif vol_ratio < 1.50:
                volume_regime = "NORMAL"
            elif vol_ratio < 2.50:
                volume_regime = "HIGH"
            else:
                volume_regime = "EXTREME"

    # Volatility regime — median of last 100 normalized ATR values ending at t
    normalized_atr = (atr / close) if atr is not None and close > params.epsilon else None
    volatility_regime = "UNKNOWN"
    if normalized_atr is not None:
        series = normalized_atr_series or _normalized_atr_prefix(bars[: t + 1], params)
        norms = [x for x in series[: t + 1] if x is not None]
        if len(norms) >= params.volatility_median_window:
            med = _median(norms[-params.volatility_median_window :])
        else:
            med = None  # insufficient for official 100-window → UNKNOWN
        if med is not None and med > params.epsilon:
            vratio = normalized_atr / med
            if vratio < 0.75:
                volatility_regime = "LOW"
            elif vratio < 1.50:
                volatility_regime = "NORMAL"
            else:
                volatility_regime = "HIGH"

    # Range position 20
    rw = params.range_position_window
    range_pos: float | None = None
    range_bucket = "UNKNOWN"
    if t + 1 >= rw:
        window_bars = bars[t - rw + 1 : t + 1]
        rh = max(b.high for b in window_bars)
        rl = min(b.low for b in window_bars)
        denom = rh - rl
        if denom <= params.epsilon:
            range_pos = None
            range_bucket = "UNKNOWN"
        else:
            range_pos = (bars[t].close - rl) / denom
            if range_pos <= 0.25:
                range_bucket = "BOTTOM"
            elif range_pos >= 0.75:
                range_bucket = "TOP"
            else:
                range_bucket = "MIDDLE"

    return ContextFeatures(
        context_version=CONTEXT_VERSION,
        trend_direction=trend_direction,
        trend_strength=trend_strength,
        sma_20=sma,
        sma_20_slope=slope,
        distance_from_sma_20=distance,
        return_5=ret5,
        return_20=ret20,
        atr_14=atr,
        normalized_atr=normalized_atr,
        volatility_regime=volatility_regime,
        volume_ratio_20=vol_ratio,
        volume_regime=volume_regime,
        range_position_20=range_pos,
        range_position_bucket=range_bucket,
        geometry=g.to_dict(),
    )


def compute_all_contexts(
    bars: Sequence[OHLCV],
    params: DetectorParams,
    geometries: list[Geometry] | None = None,
) -> list[ContextFeatures]:
    """O(n) context series — identical results to per-index ``compute_context_at``."""
    geoms = geometries if geometries is not None else build_geometries(bars, params)
    natr = _normalized_atr_prefix(bars, params)
    return [
        compute_context_at(bars, i, params, geoms, normalized_atr_series=natr)
        for i in range(len(bars))
    ]
