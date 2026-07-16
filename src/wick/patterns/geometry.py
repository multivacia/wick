"""Per-candle geometric features (no look-ahead)."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from wick.patterns.params import DetectorParams

Number = float | Decimal


def _f(value: Number) -> float:
    return float(value)


@dataclass(frozen=True)
class Geometry:
    open: float
    high: float
    low: float
    close: float
    volume: float
    body: float
    candle_range: float
    upper_wick: float
    lower_wick: float
    mid_body: float
    is_bull: bool
    is_bear: bool
    is_degenerate: bool
    body_ratio: float | None
    upper_wick_ratio: float | None
    lower_wick_ratio: float | None
    close_position: float | None
    open_position: float | None
    upper_wick_to_body: float
    lower_wick_to_body: float
    is_doji: bool
    median_body_14: float | None = None
    body_vs_median_14: float | None = None
    is_small_body: bool | None = None
    is_large_body: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "body": self.body,
            "candle_range": self.candle_range,
            "upper_wick": self.upper_wick,
            "lower_wick": self.lower_wick,
            "body_ratio": self.body_ratio,
            "upper_wick_ratio": self.upper_wick_ratio,
            "lower_wick_ratio": self.lower_wick_ratio,
            "upper_wick_to_body": self.upper_wick_to_body,
            "lower_wick_to_body": self.lower_wick_to_body,
            "close_position": self.close_position,
            "open_position": self.open_position,
            "is_bull": self.is_bull,
            "is_bear": self.is_bear,
            "is_doji": self.is_doji,
            "is_degenerate": self.is_degenerate,
            "median_body_14": self.median_body_14,
            "body_vs_median_14": self.body_vs_median_14,
            "is_small_body": self.is_small_body,
            "is_large_body": self.is_large_body,
        }


def compute_geometry(
    *,
    open_: Number,
    high: Number,
    low: Number,
    close: Number,
    volume: Number = 0,
    params: DetectorParams | None = None,
    median_body_14: float | None = None,
) -> Geometry:
    p = params or DetectorParams()
    o, h, low_v, c, v = _f(open_), _f(high), _f(low), _f(close), _f(volume)
    body = abs(c - o)
    candle_range = h - low_v
    upper_wick = h - max(o, c)
    lower_wick = min(o, c) - low_v
    mid_body = (o + c) / 2.0
    is_bull = c > o
    is_bear = c < o
    is_degenerate = candle_range <= p.epsilon

    if is_degenerate:
        body_ratio = upper_wick_ratio = lower_wick_ratio = None
        close_position = open_position = None
        is_doji = False
    else:
        body_ratio = body / candle_range
        upper_wick_ratio = upper_wick / candle_range
        lower_wick_ratio = lower_wick / candle_range
        close_position = (c - low_v) / candle_range
        open_position = (o - low_v) / candle_range
        is_doji = body_ratio <= p.doji_body_ratio_max

    safe_body = max(body, p.epsilon)
    upper_wick_to_body = upper_wick / safe_body
    lower_wick_to_body = lower_wick / safe_body

    body_vs_median: float | None = None
    is_small: bool | None = None
    is_large: bool | None = None
    if median_body_14 is None or median_body_14 <= p.epsilon:
        body_vs_median = None
        is_small = None
        is_large = None
    else:
        body_vs_median = body / median_body_14
        is_small = body_vs_median <= p.small_body_vs_median_max
        is_large = body_vs_median >= p.large_body_vs_median_min

    return Geometry(
        open=o,
        high=h,
        low=low_v,
        close=c,
        volume=v,
        body=body,
        candle_range=candle_range,
        upper_wick=upper_wick,
        lower_wick=lower_wick,
        mid_body=mid_body,
        is_bull=is_bull,
        is_bear=is_bear,
        is_degenerate=is_degenerate,
        body_ratio=body_ratio,
        upper_wick_ratio=upper_wick_ratio,
        lower_wick_ratio=lower_wick_ratio,
        close_position=close_position,
        open_position=open_position,
        upper_wick_to_body=upper_wick_to_body,
        lower_wick_to_body=lower_wick_to_body,
        is_doji=is_doji,
        median_body_14=median_body_14,
        body_vs_median_14=body_vs_median,
        is_small_body=is_small,
        is_large_body=is_large,
    )
