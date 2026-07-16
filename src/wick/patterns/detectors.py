"""Official R2 pattern detectors (shape only; no trend requirement)."""

from __future__ import annotations

from dataclasses import dataclass

from wick.patterns.geometry import Geometry
from wick.patterns.params import DETECTOR_VERSION, DetectorParams


@dataclass(frozen=True)
class PatternHit:
    pattern_type: str
    signal: str  # bullish|bearish|neutral
    length: int
    version: str = DETECTOR_VERSION


def detect_doji(g: Geometry, params: DetectorParams) -> PatternHit | None:
    if g.is_degenerate or g.body_ratio is None:
        return None
    if g.body_ratio <= params.doji_body_ratio_max:
        return PatternHit("DOJI", "neutral", 1)
    return None


def detect_hammer(g: Geometry, params: DetectorParams) -> PatternHit | None:
    if g.is_degenerate or g.body_ratio is None or g.close_position is None:
        return None
    if g.is_doji:
        return None
    if (
        g.body_ratio <= params.hammer_body_ratio_max
        and g.lower_wick_to_body >= params.hammer_lower_wick_to_body_min
        and g.upper_wick_to_body <= params.hammer_upper_wick_to_body_max
        and g.close_position >= params.hammer_close_position_min
    ):
        return PatternHit("HAMMER", "bullish", 1)
    return None


def detect_inverted_hammer(g: Geometry, params: DetectorParams) -> PatternHit | None:
    if g.is_degenerate or g.body_ratio is None or g.close_position is None:
        return None
    if g.is_doji:
        return None
    if (
        g.body_ratio <= params.inverted_hammer_body_ratio_max
        and g.upper_wick_to_body >= params.inverted_hammer_upper_wick_to_body_min
        and g.lower_wick_to_body <= params.inverted_hammer_lower_wick_to_body_max
        and g.close_position >= params.inverted_hammer_close_position_min
    ):
        return PatternHit("INVERTED_HAMMER", "bullish", 1)
    return None


def detect_shooting_star(g: Geometry, params: DetectorParams) -> PatternHit | None:
    if g.is_degenerate or g.body_ratio is None or g.close_position is None:
        return None
    if g.is_doji:
        return None
    if (
        g.body_ratio <= params.shooting_star_body_ratio_max
        and g.upper_wick_to_body >= params.shooting_star_upper_wick_to_body_min
        and g.lower_wick_to_body <= params.shooting_star_lower_wick_to_body_max
        and g.close_position <= params.shooting_star_close_position_max
    ):
        return PatternHit("SHOOTING_STAR", "bearish", 1)
    return None


def detect_bullish_engulfing(
    prev: Geometry, curr: Geometry, params: DetectorParams
) -> PatternHit | None:
    if prev.is_doji or curr.is_doji:
        return None
    if not (prev.is_bear and curr.is_bull):
        return None
    if params.engulfing_allow_equal_boundaries:
        open_ok = curr.open <= prev.close
        close_ok = curr.close >= prev.open
    else:
        open_ok = curr.open < prev.close
        close_ok = curr.close > prev.open
    if not (open_ok and close_ok):
        return None
    if curr.body < prev.body * params.engulfing_body_min_factor:
        return None
    return PatternHit("BULLISH_ENGULFING", "bullish", 2)


def detect_bearish_engulfing(
    prev: Geometry, curr: Geometry, params: DetectorParams
) -> PatternHit | None:
    if prev.is_doji or curr.is_doji:
        return None
    if not (prev.is_bull and curr.is_bear):
        return None
    if params.engulfing_allow_equal_boundaries:
        open_ok = curr.open >= prev.close
        close_ok = curr.close <= prev.open
    else:
        open_ok = curr.open > prev.close
        close_ok = curr.close < prev.open
    if not (open_ok and close_ok):
        return None
    if curr.body < prev.body * params.engulfing_body_min_factor:
        return None
    return PatternHit("BEARISH_ENGULFING", "bearish", 2)


def detect_morning_star(
    c1: Geometry, c2: Geometry, c3: Geometry, params: DetectorParams
) -> PatternHit | None:
    if c1.is_doji or c3.is_doji:
        return None
    if not c1.is_bear:
        return None
    if c1.is_large_body is not True:
        return None
    if c2.body_ratio is None or c2.body_ratio > params.morning_star_middle_body_ratio_max:
        return None
    if not c3.is_bull:
        return None
    recovery = c1.close + (c1.open - c1.close) * params.morning_star_recovery_min
    if c3.close < recovery:
        return None
    return PatternHit("MORNING_STAR", "bullish", 3)


def detect_evening_star(
    c1: Geometry, c2: Geometry, c3: Geometry, params: DetectorParams
) -> PatternHit | None:
    if c1.is_doji or c3.is_doji:
        return None
    if not c1.is_bull:
        return None
    if c1.is_large_body is not True:
        return None
    if c2.body_ratio is None or c2.body_ratio > params.evening_star_middle_body_ratio_max:
        return None
    if not c3.is_bear:
        return None
    decline = c1.close - (c1.close - c1.open) * params.evening_star_decline_min
    if c3.close > decline:
        return None
    return PatternHit("EVENING_STAR", "bearish", 3)


def detect_all_at_anchor(
    geoms: list[Geometry],
    index: int,
    params: DetectorParams,
) -> list[PatternHit]:
    """Detect all patterns whose anchor is ``geoms[index]`` (no future candles)."""
    hits: list[PatternHit] = []
    curr = geoms[index]
    for fn in (detect_doji, detect_hammer, detect_inverted_hammer, detect_shooting_star):
        hit = fn(curr, params)
        if hit is not None:
            hits.append(hit)
    if index >= 1:
        prev = geoms[index - 1]
        for fn in (detect_bullish_engulfing, detect_bearish_engulfing):
            hit = fn(prev, curr, params)
            if hit is not None:
                hits.append(hit)
    if index >= 2:
        c1, c2, c3 = geoms[index - 2], geoms[index - 1], curr
        for fn in (detect_morning_star, detect_evening_star):
            hit = fn(c1, c2, c3, params)
            if hit is not None:
                hits.append(hit)
    return hits
