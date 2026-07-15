"""Shared pytest fixtures — offline tests use PostgreSQL when available.

Schema for tests is created from SQLAlchemy metadata matching the Alembic models.
Application runtime must use Alembic only (see test_no_create_all).
After the test session, Alembic migrations are re-applied so the local DB remains usable.
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from wick.config import Settings
from wick.db.base import Base
from wick.ingestion.validators import RawCandle

DEFAULT_TEST_URL = os.environ.get(
    "TEST_DATABASE_URL",
    os.environ.get(
        "DATABASE_URL",
        "postgresql+psycopg://wick:wick@127.0.0.1:5432/wick",
    ),
)


@pytest.fixture(scope="session")
def database_url() -> str:
    return DEFAULT_TEST_URL


@pytest.fixture(scope="session")
def engine(database_url: str):
    eng = create_engine(database_url, pool_pre_ping=True, future=True)
    try:
        with eng.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"PostgreSQL not available for tests: {exc}")

    Base.metadata.drop_all(eng)
    with eng.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    with eng.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
    eng.dispose()

    # Restore official schema via Alembic for local/demo usage after tests
    cfg = Config("alembic.ini")
    os.environ["DATABASE_URL"] = database_url
    command.upgrade(cfg, "head")


@pytest.fixture
def session(engine) -> Iterator[Session]:
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection, autoflush=False, future=True)
    sess = SessionLocal()
    try:
        yield sess
    finally:
        sess.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def settings() -> Settings:
    return Settings(
        DATABASE_URL=DEFAULT_TEST_URL,
        CANDLE_CLOSE_SAFETY_DELAY_SECONDS=30,
    )


@pytest.fixture
def now_fixed() -> datetime:
    return datetime(2024, 6, 15, 12, 0, 0, tzinfo=UTC)


def make_candle(
    ts: datetime,
    *,
    o: str = "100",
    h: str = "110",
    low: str = "90",
    c: str = "105",
    v: str = "1000",
) -> RawCandle:
    return RawCandle(
        timestamp=ts,
        open=Decimal(o),
        high=Decimal(h),
        low=Decimal(low),
        close=Decimal(c),
        volume=Decimal(v),
    )


@pytest.fixture
def sample_closed_candles(now_fixed: datetime) -> list[RawCandle]:
    base = datetime(2024, 1, 1, tzinfo=UTC)
    return [make_candle(base + timedelta(days=i), c=str(100 + i)) for i in range(5)]
