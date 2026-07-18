"""Map official R3E universe series to provider symbols (no silent substitution)."""

from __future__ import annotations

from typing import Any

from wick.r3d.universe import UNIVERSE


def _provider_symbol(source: str, symbol: str) -> str:
    # Official symbols already match provider expectations for binance/yahoo.
    return symbol


def symbol_is_b3(symbol: str) -> bool:
    return symbol.endswith(".SA")


def build_provider_mapping() -> dict[str, Any]:
    series: list[dict[str, Any]] = []
    for spec in UNIVERSE:
        provider_symbol = _provider_symbol(spec.source, spec.symbol)
        if spec.asset_class == "crypto":
            market_hours = "24/7 UTC"
        elif symbol_is_b3(spec.symbol):
            market_hours = "B3 session (America/Sao_Paulo)"
        else:
            market_hours = "US equities session (America/New_York)"
        closed_rule = (
            "open_time + timeframe_duration <= now_utc - safety_delay_seconds(30)"
        )
        series.append(
            {
                "series_key": f"{spec.source}|{spec.symbol}|{spec.timeframe}",
                "official_symbol": spec.symbol,
                "provider_symbol": provider_symbol,
                "source": spec.source,
                "timeframe": spec.timeframe,
                "asset_class": spec.asset_class,
                "historical_availability": "provider_dependent",
                "market_hours": market_hours,
                "closed_candle_rule": closed_rule,
                "located": True,
                "substitution": None,
            }
        )
    return {
        "universe_source": "wick.r3d.universe.UNIVERSE",
        "n_series_expected": len(UNIVERSE),
        "series": series,
        "missing_series": [],
        "note": (
            "brapi is available in R1 but is not part of the frozen R3E 20-series universe; "
            "no silent substitution to brapi is performed."
        ),
    }
