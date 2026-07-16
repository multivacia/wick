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


def compute_context_at(
    bars: Sequence[OHLCV],
    index: int,
    params: DetectorParams,
    geometries: list[Geometry] | None = None,
) -> ContextFeatures:
    """Context for candle ``index`` using only bars[0:index+1]."""
    if index < 0 or index >= len(bars):
        raise IndexError("index out of range")
    # Enforce no look-ahead by slicing.
    hist = list(bars[: index + 1])
    geoms = geometries[: index + 1] if geometries is not None else build_geometries(hist, params)
    g = geoms[index]
    t = index

    # ATR 14 — simple mean of last 14 TRs ending at t
    atr: float | None = None
    if t + 1 >= params.atr_window:
        trs: list[float] = []
        for i in range(t - params.atr_window + 1, t + 1):
            prev_c = hist[i - 1].close if i > 0 else None
            trs.append(true_range(hist[i].high, hist[i].low, prev_c))
        atr = _mean(trs)

    # SMA 20 including current
    sma: float | None = None
    sma_prev: float | None = None
    slope: float | None = None
    distance: float | None = None
    w = params.sma_window
    if t + 1 >= w:
        closes = [b.close for b in hist]
        sma = _mean(closes[t - w + 1 : t + 1])
        if t >= w:
            sma_prev = _mean(closes[t - w : t])
            if sma is not None and sma_prev is not None and abs(sma_prev) > params.epsilon:
                slope = (sma - sma_prev) / sma_prev
        if sma is not None and abs(sma) > params.epsilon:
            distance = hist[t].close / sma - 1.0

    ret5 = hist[t].close / hist[t - 5].close - 1.0 if t >= 5 else None
    ret20 = hist[t].close / hist[t - 20].close - 1.0 if t >= 20 else None

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
    close = hist[t].close
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
        vols = [b.volume for b in hist[t - vw + 1 : t + 1]]
        mean_vol = _mean(vols)
        cur_vol = hist[t].volume
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

    # Volatility regime — median of last 100 normalized ATR values at each prior point
    normalized_atr = (atr / close) if atr is not None and close > params.epsilon else None
    volatility_regime = "UNKNOWN"
    if normalized_atr is not None:
        norms: list[float] = []
        # Recompute historical normalized ATRs up to t (expensive but correct / no look-ahead)
        for i in range(len(hist)):
            if i + 1 < params.atr_window:
                continue
            trs_i = []
            for j in range(i - params.atr_window + 1, i + 1):
                prev_c = hist[j - 1].close if j > 0 else None
                trs_i.append(true_range(hist[j].high, hist[j].low, prev_c))
            atr_i = _mean(trs_i)
            if atr_i is None or hist[i].close <= params.epsilon:
                continue
            norms.append(atr_i / hist[i].close)
        if len(norms) >= params.volatility_median_window:
            med = _median(norms[-params.volatility_median_window :])
        elif norms:
            med = None  # insufficient for official 100-window → UNKNOWN
        else:
            med = None
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
        window_bars = hist[t - rw + 1 : t + 1]
        rh = max(b.high for b in window_bars)
        rl = min(b.low for b in window_bars)
        denom = rh - rl
        if denom <= params.epsilon:
            range_pos = None
            range_bucket = "UNKNOWN"
        else:
            range_pos = (hist[t].close - rl) / denom
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
