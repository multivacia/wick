"""Real concurrency tests against PostgreSQL (two sessions / transactions)."""

from __future__ import annotations

import threading
import uuid
from datetime import UTC, datetime
from decimal import Decimal

from sqlalchemy import func, select, text
from sqlalchemy.orm import sessionmaker

from wick.db.models import Asset, Candle, CandleRevisionEvent
from wick.ingestion.upsert import get_or_create_asset, upsert_candles
from wick.ingestion.validators import RawCandle


def _bar(
    ts: datetime,
    *,
    close: str = "100",
    high: str | None = None,
    volume: str = "1000",
) -> RawCandle:
    c = Decimal(close)
    h = Decimal(high) if high is not None else max(Decimal("110"), c)
    return RawCandle(
        timestamp=ts,
        open=Decimal("100"),
        high=h,
        low=Decimal("90"),
        close=c,
        volume=Decimal(volume),
    )


def _cleanup_symbol(engine, symbol: str, source: str = "binance") -> None:
    with engine.begin() as conn:
        asset_ids = conn.execute(
            text("SELECT id FROM asset WHERE symbol = :s AND source = :src"),
            {"s": symbol, "src": source},
        ).fetchall()
        for (asset_id,) in asset_ids:
            conn.execute(
                text(
                    "DELETE FROM candle_revision_event WHERE candle_id IN "
                    "(SELECT id FROM candle WHERE asset_id = :aid)"
                ),
                {"aid": asset_id},
            )
            conn.execute(text("DELETE FROM candle WHERE asset_id = :aid"), {"aid": asset_id})
            conn.execute(text("DELETE FROM asset WHERE id = :aid"), {"aid": asset_id})


def test_concurrent_identical_insert_two_sessions(engine):
    """Two concurrent sessions insert the same candle key.

    Expect: no IntegrityError, exactly one row, no spurious revision events.
    """
    symbol = f"CONC-INS-{uuid.uuid4().hex[:8]}/USDT"
    source = "binance"
    ts = datetime(2024, 3, 1, tzinfo=UTC)
    candle = _bar(ts, close="100")
    SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)

    with SessionLocal() as setup:
        asset = get_or_create_asset(
            setup,
            symbol=symbol,
            asset_type="crypto",
            source=source,
            exchange="binance",
            currency="USDT",
        )
        setup.commit()
        asset_id = asset.id

    barrier = threading.Barrier(2, timeout=10)
    errors: list[BaseException] = []
    stats_list: list = []
    lock = threading.Lock()

    def worker(run_id: str) -> None:
        try:
            with SessionLocal() as session:
                asset = session.get(Asset, asset_id)
                assert asset is not None
                barrier.wait()
                stats = upsert_candles(
                    session,
                    asset=asset,
                    timeframe="1d",
                    source=source,
                    candles=[candle],
                    run_id=run_id,
                )
                session.commit()
                with lock:
                    stats_list.append(stats)
        except BaseException as exc:  # noqa: BLE001 — capture for assertion
            with lock:
                errors.append(exc)

    t1 = threading.Thread(target=worker, args=("run_a",))
    t2 = threading.Thread(target=worker, args=("run_b",))
    t1.start()
    t2.start()
    t1.join(timeout=30)
    t2.join(timeout=30)

    try:
        assert errors == [], f"Unexpected errors: {errors}"
        assert len(stats_list) == 2
        inserted = sum(s.inserted for s in stats_list)
        unchanged = sum(s.unchanged for s in stats_list)
        updated = sum(s.updated for s in stats_list)
        assert inserted == 1
        assert unchanged == 1
        assert updated == 0

        with SessionLocal() as session:
            count = session.execute(
                select(func.count())
                .select_from(Candle)
                .where(Candle.asset_id == asset_id, Candle.timestamp == ts)
            ).scalar_one()
            assert count == 1
            row = session.execute(
                select(Candle).where(Candle.asset_id == asset_id, Candle.timestamp == ts)
            ).scalar_one()
            assert row.data_revision == 1
            events = session.execute(
                select(func.count())
                .select_from(CandleRevisionEvent)
                .where(CandleRevisionEvent.candle_id == row.id)
            ).scalar_one()
            assert events == 0
    finally:
        _cleanup_symbol(engine, symbol, source)


def test_concurrent_identical_revision_two_sessions(engine):
    """Two concurrent sessions revise the same candle with the same new OHLCV.

    Expect: one revision event, data_revision == 2, no IntegrityError.
    """
    symbol = f"CONC-REV-{uuid.uuid4().hex[:8]}/USDT"
    source = "binance"
    ts = datetime(2024, 3, 2, tzinfo=UTC)
    original = _bar(ts, close="100")
    revised = _bar(ts, close="105", high="120", volume="2000")
    SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)

    with SessionLocal() as setup:
        asset = get_or_create_asset(
            setup,
            symbol=symbol,
            asset_type="crypto",
            source=source,
            exchange="binance",
            currency="USDT",
        )
        upsert_candles(
            setup,
            asset=asset,
            timeframe="1d",
            source=source,
            candles=[original],
            run_id="seed",
        )
        setup.commit()
        asset_id = asset.id

    barrier = threading.Barrier(2, timeout=10)
    errors: list[BaseException] = []
    stats_list: list = []
    lock = threading.Lock()

    def worker(run_id: str) -> None:
        try:
            with SessionLocal() as session:
                asset = session.get(Asset, asset_id)
                assert asset is not None
                barrier.wait()
                stats = upsert_candles(
                    session,
                    asset=asset,
                    timeframe="1d",
                    source=source,
                    candles=[revised],
                    run_id=run_id,
                )
                session.commit()
                with lock:
                    stats_list.append(stats)
        except BaseException as exc:  # noqa: BLE001
            with lock:
                errors.append(exc)

    threads = [
        threading.Thread(target=worker, args=("rev_a",)),
        threading.Thread(target=worker, args=("rev_b",)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)

    try:
        assert errors == [], f"Unexpected errors: {errors}"
        assert len(stats_list) == 2
        assert sum(s.updated for s in stats_list) == 1
        assert sum(s.unchanged for s in stats_list) == 1
        assert sum(s.inserted for s in stats_list) == 0

        with SessionLocal() as session:
            row = session.execute(
                select(Candle).where(Candle.asset_id == asset_id, Candle.timestamp == ts)
            ).scalar_one()
            assert row.data_revision == 2
            assert row.close == Decimal("105")
            events = (
                session.execute(
                    select(CandleRevisionEvent).where(CandleRevisionEvent.candle_id == row.id)
                )
                .scalars()
                .all()
            )
            assert len(events) == 1
            assert events[0].previous_revision == 1
            assert events[0].new_revision == 2
    finally:
        _cleanup_symbol(engine, symbol, source)


def test_concurrent_diverging_revisions_serialize(engine):
    """Two concurrent sessions revise with different payloads; FOR UPDATE serializes.

    Expect: final data_revision == 3, exactly two audit events, one candle row.
    """
    symbol = f"CONC-DIV-{uuid.uuid4().hex[:8]}/USDT"
    source = "binance"
    ts = datetime(2024, 3, 3, tzinfo=UTC)
    original = _bar(ts, close="100")
    rev_a = _bar(ts, close="101", high="120")
    rev_b = _bar(ts, close="102", high="121")
    SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)

    with SessionLocal() as setup:
        asset = get_or_create_asset(
            setup,
            symbol=symbol,
            asset_type="crypto",
            source=source,
            exchange="binance",
            currency="USDT",
        )
        upsert_candles(
            setup,
            asset=asset,
            timeframe="1d",
            source=source,
            candles=[original],
            run_id="seed",
        )
        setup.commit()
        asset_id = asset.id

    barrier = threading.Barrier(2, timeout=10)
    errors: list[BaseException] = []
    payloads = [rev_a, rev_b]
    lock = threading.Lock()

    def worker(idx: int) -> None:
        try:
            with SessionLocal() as session:
                asset = session.get(Asset, asset_id)
                assert asset is not None
                barrier.wait()
                upsert_candles(
                    session,
                    asset=asset,
                    timeframe="1d",
                    source=source,
                    candles=[payloads[idx]],
                    run_id=f"div_{idx}",
                )
                session.commit()
        except BaseException as exc:  # noqa: BLE001
            with lock:
                errors.append(exc)

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)

    try:
        assert errors == [], f"Unexpected errors: {errors}"
        with SessionLocal() as session:
            count = session.execute(
                select(func.count())
                .select_from(Candle)
                .where(Candle.asset_id == asset_id, Candle.timestamp == ts)
            ).scalar_one()
            assert count == 1
            row = session.execute(
                select(Candle).where(Candle.asset_id == asset_id, Candle.timestamp == ts)
            ).scalar_one()
            assert row.data_revision == 3
            assert row.close in {Decimal("101"), Decimal("102")}
            events = (
                session.execute(
                    select(CandleRevisionEvent)
                    .where(CandleRevisionEvent.candle_id == row.id)
                    .order_by(CandleRevisionEvent.new_revision.asc())
                )
                .scalars()
                .all()
            )
            assert len(events) == 2
            assert [e.previous_revision for e in events] == [1, 2]
            assert [e.new_revision for e in events] == [2, 3]
    finally:
        _cleanup_symbol(engine, symbol, source)
