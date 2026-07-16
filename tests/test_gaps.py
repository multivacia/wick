"""Gap detection tests."""

from datetime import UTC, datetime, timedelta

from wick.ingestion.gaps import detect_gaps


def test_crypto_gap_alerted():
    base = datetime(2024, 1, 1, tzinfo=UTC)
    timestamps = [base, base + timedelta(days=1), base + timedelta(days=3)]
    gaps = detect_gaps(timestamps, asset_symbol="BTC/USDT", timeframe="1d", asset_type="crypto")
    assert len(gaps) == 1
    assert gaps[0].severity == "alert"
    assert gaps[0].expected_bars == 1


def test_stock_weekend_not_treated_as_gap():
    # Fri -> Mon for daily stocks
    friday = datetime(2024, 1, 5, tzinfo=UTC)  # Friday
    monday = datetime(2024, 1, 8, tzinfo=UTC)  # Monday
    gaps = detect_gaps([friday, monday], asset_symbol="AAPL", timeframe="1d", asset_type="stock")
    assert gaps == []


def test_stock_large_hole_flagged_as_partial_info():
    a = datetime(2024, 1, 1, tzinfo=UTC)
    b = datetime(2024, 1, 20, tzinfo=UTC)
    gaps = detect_gaps([a, b], asset_symbol="PETR4", timeframe="1d", asset_type="stock")
    assert len(gaps) == 1
    assert gaps[0].severity == "info"
    assert "partial" in gaps[0].note.lower()
