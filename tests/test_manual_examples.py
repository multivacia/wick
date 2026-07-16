"""Manual formula examples required by CLAUDE.md invariants."""

from datetime import UTC, datetime, timedelta

from wick.ingestion.validators import is_candle_closed


def test_manual_closed_candle_formula():
    """open_time + timeframe_duration <= now_utc - safety_delay

    Example:
      open_time = 2024-06-15T10:00:00Z
      timeframe = 1h  => duration = 1 hour
      safety_delay = 30s
      close_deadline = 2024-06-15T11:00:00Z
      eligible when now >= 2024-06-15T11:00:30Z
    """
    open_time = datetime(2024, 6, 15, 10, 0, 0, tzinfo=UTC)
    assert not is_candle_closed(
        open_time,
        "1h",
        now_utc=datetime(2024, 6, 15, 11, 0, 29, tzinfo=UTC),
        safety_delay_seconds=30,
    )
    assert is_candle_closed(
        open_time,
        "1h",
        now_utc=datetime(2024, 6, 15, 11, 0, 30, tzinfo=UTC),
        safety_delay_seconds=30,
    )


def test_manual_daily_formula():
    open_time = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
    # Eligible at 2024-01-02T00:00:30Z
    assert is_candle_closed(
        open_time,
        "1d",
        now_utc=open_time + timedelta(days=1, seconds=30),
        safety_delay_seconds=30,
    )
