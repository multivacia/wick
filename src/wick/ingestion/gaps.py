"""Gap detection for crypto (24/7) and stocks (partial without calendar)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta

from wick.timeframes import timeframe_duration


@dataclass(frozen=True)
class Gap:
    asset_symbol: str
    timeframe: str
    gap_start: datetime
    gap_end: datetime
    expected_bars: int
    asset_type: str
    severity: str  # alert|info
    note: str


def detect_gaps(
    timestamps: list[datetime],
    *,
    asset_symbol: str,
    timeframe: str,
    asset_type: str,
) -> list[Gap]:
    """Detect missing intervals between sorted closed candles.

    Crypto: any missing interval is an alert.
    Stock: without an exchange calendar, weekend/overnight gaps are not treated
    as true gaps; only unusually large multi-day holes are flagged as info,
    and the check is marked partial.
    """
    if len(timestamps) < 2:
        return []

    duration = timeframe_duration(timeframe)
    ordered = sorted(ensure_aware(t) for t in timestamps)
    gaps: list[Gap] = []

    for prev, curr in zip(ordered, ordered[1:], strict=False):
        expected_next = prev + duration
        if curr <= expected_next:
            continue
        missing = int((curr - expected_next) / duration)
        if missing <= 0:
            continue

        if asset_type == "crypto":
            gaps.append(
                Gap(
                    asset_symbol=asset_symbol,
                    timeframe=timeframe,
                    gap_start=expected_next,
                    gap_end=curr,
                    expected_bars=missing,
                    asset_type=asset_type,
                    severity="alert",
                    note="Missing interval in 24/7 crypto series",
                )
            )
        else:
            # Stocks: without a trading calendar this check is partial.
            # Skip gaps that look like weekend/overnight for daily+; for intraday
            # flag only large holes (>= 24h of missing bars relative to duration).
            if _looks_like_session_break(prev, curr, timeframe):
                continue
            gaps.append(
                Gap(
                    asset_symbol=asset_symbol,
                    timeframe=timeframe,
                    gap_start=expected_next,
                    gap_end=curr,
                    expected_bars=missing,
                    asset_type=asset_type,
                    severity="info",
                    note=(
                        "Potential gap; trading calendar not implemented — "
                        "stock gap check is partial"
                    ),
                )
            )
    return gaps


def ensure_aware(ts: datetime) -> datetime:
    if ts.tzinfo is None:
        return ts.replace(tzinfo=UTC)
    return ts.astimezone(UTC)


def _looks_like_session_break(prev: datetime, curr: datetime, timeframe: str) -> bool:
    delta = curr - prev
    if timeframe in {"1d", "1w"}:
        # Weekend / holiday style gaps up to ~5 calendar days
        return delta <= timedelta(days=5)
    # Intraday: treat overnight/weekend as session breaks (< 3.5 days)
    return delta <= timedelta(days=3, hours=12)


def gaps_to_json(gaps: list[Gap]) -> list[dict]:
    out: list[dict] = []
    for g in gaps:
        d = asdict(g)
        d["gap_start"] = g.gap_start.isoformat()
        d["gap_end"] = g.gap_end.isoformat()
        out.append(d)
    return out
