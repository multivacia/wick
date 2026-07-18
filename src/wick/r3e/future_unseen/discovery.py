"""Incremental window discovery for future-unseen collection."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from wick.r3e.future_unseen.config import FUTURE_UNSEEN_CUTOFF
from wick.r3e.future_unseen.ingest import load_all_validated_records
from wick.timeframes import timeframe_duration


def floor_to_timeframe(ts: datetime, timeframe: str) -> datetime:
    """Floor UTC timestamp to timeframe open boundary (epoch-aligned UTC)."""
    dur = timeframe_duration(timeframe)
    epoch = datetime(1970, 1, 1, tzinfo=UTC)
    ts_utc = ts.astimezone(UTC)
    seconds = int((ts_utc - epoch).total_seconds())
    dur_s = int(dur.total_seconds())
    floored = epoch + timedelta(seconds=(seconds // dur_s) * dur_s)
    return floored


def first_open_strictly_after_cutoff(
    *,
    timeframe: str,
    cutoff: datetime | None = None,
) -> datetime:
    """First UTC-aligned open strictly after FUTURE_UNSEEN_CUTOFF.

    market_ts convention: candle open time (matches Binance/Yahoo ingest).
    """
    cut = cutoff or FUTURE_UNSEEN_CUTOFF
    dur = timeframe_duration(timeframe)
    candidate = floor_to_timeframe(cut, timeframe)
    while candidate <= cut:
        candidate += dur
    return candidate


def last_closed_candle_open(
    *,
    timeframe: str,
    now_utc: datetime,
    safety_delay_seconds: int = 30,
) -> datetime | None:
    """Latest open_time whose candle is closed at now_utc with safety delay."""
    dur = timeframe_duration(timeframe)
    deadline = now_utc.astimezone(UTC) - timedelta(seconds=safety_delay_seconds) - dur
    if deadline.tzinfo is None:
        raise ValueError("now_utc must be timezone-aware")
    open_ts = floor_to_timeframe(deadline, timeframe)
    # Ensure closed under the same rule
    if open_ts + dur > now_utc.astimezone(UTC) - timedelta(seconds=safety_delay_seconds):
        open_ts -= dur
    return open_ts


def last_accepted_by_series(
    records: list[dict[str, Any]] | None = None,
) -> dict[str, datetime]:
    """Map series_key -> last accepted market_ts."""
    rows = records if records is not None else load_all_validated_records()
    out: dict[str, datetime] = {}
    for rec in rows:
        sk = f"{rec['source']}|{rec['symbol']}|{rec['timeframe']}"
        ts = datetime.fromisoformat(rec["market_ts"].replace("Z", "+00:00")).astimezone(UTC)
        prev = out.get(sk)
        if prev is None or ts > prev:
            out[sk] = ts
    return out


def compute_fetch_window(
    *,
    symbol: str,
    timeframe: str,
    source: str,
    now_utc: datetime,
    last_accepted: datetime | None,
    safety_delay_seconds: int = 30,
    revision_overlap_bars: int = 1,
) -> dict[str, Any]:
    """Compute provider fetch [start, end] for one series.

    Empty series: start = first open after cutoff.
    Existing: start = next open after last accepted, minus optional overlap bars.
    End: last closed candle open (inclusive request upper bound via now).
    """
    series_key = f"{source}|{symbol}|{timeframe}"
    dur = timeframe_duration(timeframe)
    end_open = last_closed_candle_open(
        timeframe=timeframe,
        now_utc=now_utc,
        safety_delay_seconds=safety_delay_seconds,
    )
    if last_accepted is None:
        start = first_open_strictly_after_cutoff(timeframe=timeframe)
        mode = "EMPTY_SERIES_AFTER_CUTOFF"
    else:
        next_open = last_accepted + dur
        # Small overlap for revision detection (pre-defined, non-duplicating via store).
        overlap = max(0, int(revision_overlap_bars))
        start = next_open - (dur * overlap) if overlap else next_open
        # Never request at/before cutoff
        floor_start = first_open_strictly_after_cutoff(timeframe=timeframe)
        if start < floor_start:
            start = floor_start
        mode = "INCREMENTAL_AFTER_LAST"
    # Provider end: use now (filter closed later); record decision boundary
    return {
        "series_key": series_key,
        "mode": mode,
        "requested_start": start,
        "requested_end": now_utc.astimezone(UTC),
        "last_accepted": last_accepted.isoformat() if last_accepted else None,
        "last_closed_candle_boundary": end_open.isoformat() if end_open else None,
        "revision_overlap_bars": revision_overlap_bars,
        "decision_rule": (
            "fetch until now_utc; accept only closed candles with "
            "market_ts > FUTURE_UNSEEN_CUTOFF; open-time market_ts convention"
        ),
        "no_new_closed_possible": bool(
            end_open is not None and last_accepted is not None and end_open <= last_accepted
        ),
    }
