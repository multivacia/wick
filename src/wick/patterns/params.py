"""R2 detector parameters — official catalog from R2_PATTERN_SPECIFICATION.md.

Any change requires a new detector_version and parameters_hash.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass

DETECTOR_VERSION = "1.0.0"
CONTEXT_VERSION = "1.0.0"
CONFIRM_CLOSE_V1 = "CONFIRM_CLOSE_V1"
CONFIRM_EXTREME_V1 = "CONFIRM_EXTREME_V1"


@dataclass(frozen=True)
class DetectorParams:
    epsilon: float = 1.0e-12

    doji_body_ratio_max: float = 0.10

    small_body_vs_median_max: float = 0.75
    large_body_vs_median_min: float = 1.50

    median_body_window: int = 14
    atr_window: int = 14
    sma_window: int = 20
    volume_window: int = 20
    range_position_window: int = 20
    volatility_median_window: int = 100

    hammer_body_ratio_max: float = 0.35
    hammer_lower_wick_to_body_min: float = 2.0
    hammer_upper_wick_to_body_max: float = 0.5
    hammer_close_position_min: float = 0.60

    inverted_hammer_body_ratio_max: float = 0.35
    inverted_hammer_upper_wick_to_body_min: float = 2.0
    inverted_hammer_lower_wick_to_body_max: float = 0.5
    inverted_hammer_close_position_min: float = 0.40

    shooting_star_body_ratio_max: float = 0.35
    shooting_star_upper_wick_to_body_min: float = 2.0
    shooting_star_lower_wick_to_body_max: float = 0.5
    shooting_star_close_position_max: float = 0.40

    engulfing_body_min_factor: float = 1.0
    engulfing_allow_equal_boundaries: bool = True

    morning_star_middle_body_ratio_max: float = 0.30
    morning_star_recovery_min: float = 0.50

    evening_star_middle_body_ratio_max: float = 0.30
    evening_star_decline_min: float = 0.50

    trend_up_sma_slope_min: float = 0.001
    trend_up_return_20_min: float = 0.02
    trend_down_sma_slope_max: float = -0.001
    trend_down_return_20_max: float = -0.02

    def to_dict(self) -> dict:
        return asdict(self)

    def parameters_hash(self) -> str:
        payload = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


DEFAULT_PARAMS = DetectorParams()
