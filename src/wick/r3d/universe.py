"""R3D universe and coverage targets (frozen for this validation run)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True)
class SeriesSpec:
    source: str
    symbol: str
    timeframe: str
    target_start: datetime
    min_years: float
    asset_class: str


def _utc(year: int, month: int, day: int) -> datetime:
    return datetime(year, month, day, tzinfo=UTC)


# Anchor "today" for planned windows (execution may clamp to provider limits).
_END = datetime(2026, 7, 16, tzinfo=UTC)

CRYPTO_SYMBOLS = ("BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT")
STOCK_SYMBOLS = ("PETR4.SA", "VALE3.SA", "ITUB4.SA", "AAPL", "MSFT")

# Coverage policy from human authorization (R3D).
COVERAGE_TARGETS = {
    ("crypto", "1h"): {"years": 2.0, "start": _END - timedelta(days=365 * 2)},
    ("crypto", "1d"): {"years": 4.0, "start": _END - timedelta(days=365 * 4)},
    ("stock", "1d"): {"years": 5.0, "start": _END - timedelta(days=365 * 5)},
    ("stock", "1h"): {"years": 2.0, "start": _END - timedelta(days=730)},  # Yahoo ~max
}

# For crypto 1d request max available history (provider may return less).
CRYPTO_1D_REQUEST_START = _utc(2018, 1, 1)


def build_universe() -> list[SeriesSpec]:
    out: list[SeriesSpec] = []
    for sym in CRYPTO_SYMBOLS:
        out.append(
            SeriesSpec(
                "binance",
                sym,
                "1h",
                COVERAGE_TARGETS[("crypto", "1h")]["start"],
                2.0,
                "crypto",
            )
        )
        out.append(
            SeriesSpec(
                "binance",
                sym,
                "1d",
                CRYPTO_1D_REQUEST_START,
                4.0,
                "crypto",
            )
        )
    for sym in STOCK_SYMBOLS:
        out.append(
            SeriesSpec(
                "yahoo",
                sym,
                "1d",
                COVERAGE_TARGETS[("stock", "1d")]["start"],
                5.0,
                "stock",
            )
        )
        out.append(
            SeriesSpec(
                "yahoo",
                sym,
                "1h",
                COVERAGE_TARGETS[("stock", "1h")]["start"],
                1.5,  # Yahoo intraday often < 2y; mark PARTIAL below min_years
                "stock",
            )
        )
    return out


UNIVERSE = build_universe()

# Official bullish/bearish pattern catalog (R2) — no extras.
PATTERN_TYPES = (
    "DOJI",
    "HAMMER",
    "INVERTED_HAMMER",
    "SHOOTING_STAR",
    "BULLISH_ENGULFING",
    "BEARISH_ENGULFING",
    "MORNING_STAR",
    "EVENING_STAR",
)

HORIZONS = (1, 3, 5, 10)
COST_SCENARIOS = ("OPTIMISTIC", "BASE", "STRESSED")
CONFIRMATION_VARIANTS = (False, True)  # raw signal vs confirmed
SEED = 42
N_BOOTSTRAP = 1000
TREND_BASELINE_V1 = "close > SMA20"
COST_MODEL_VERSION = "1.0.0-provisional"
