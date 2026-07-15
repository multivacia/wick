"""Database session helpers."""

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from wick.config import Settings, get_settings

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def get_engine(settings: Settings | None = None) -> Engine:
    global _engine, _SessionLocal
    cfg = settings or get_settings()
    if _engine is None:
        _engine = create_engine(
            cfg.database_url,
            pool_pre_ping=True,
            future=True,
        )
        _SessionLocal = sessionmaker(
            bind=_engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            future=True,
        )
    return _engine


def reset_engine() -> None:
    """Reset cached engine (tests / config reload)."""
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None


@contextmanager
def session_scope(settings: Settings | None = None) -> Iterator[Session]:
    get_engine(settings)
    assert _SessionLocal is not None
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
