"""Tests for R3E future-unseen incremental collector."""

from __future__ import annotations

import ast
import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from wick.ingestion.providers.base import FetchResult, MarketDataProvider
from wick.ingestion.validators import RawCandle
from wick.r3e.future_unseen import collector as collector_mod
from wick.r3e.future_unseen import config as fu_config
from wick.r3e.future_unseen.discovery import (
    compute_fetch_window,
    first_open_strictly_after_cutoff,
    last_closed_candle_open,
)
from wick.r3e.future_unseen.hashing import sha256_file
from wick.r3e.future_unseen.protections import (
    FutureUnseenProtectionError,
    assert_strictly_after_cutoff,
)


def _candle(ts: datetime, price: float = 100.0) -> RawCandle:
    return RawCandle(
        timestamp=ts,
        open=Decimal(str(price)),
        high=Decimal(str(price * 1.01)),
        low=Decimal(str(price * 0.99)),
        close=Decimal(str(price)),
        volume=Decimal("10"),
    )


class FakeProvider(MarketDataProvider):
    name = "binance"
    asset_type = "crypto"

    def __init__(self, candles: list[RawCandle] | None = None, *, fail: bool = False):
        self.candles = list(candles or [])
        self.fail = fail
        self.calls: list[tuple] = []

    def fetch_ohlcv(self, symbol, timeframe, start, end) -> FetchResult:
        self.calls.append((symbol, timeframe, start, end))
        if self.fail:
            raise RuntimeError("provider down")
        return FetchResult(candles=list(self.candles), actual_start=start, actual_end=end)


@pytest.fixture()
def fu_dirs(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    val = tmp_path / "validated"
    man = tmp_path / "manifests"
    reports = tmp_path / "reports"
    for d in (raw, val, man, reports):
        d.mkdir()
    import wick.r3e.future_unseen.collector as col
    import wick.r3e.future_unseen.ingest as ingest_mod
    import wick.r3e.future_unseen.ops_report as ops_mod
    import wick.r3e.future_unseen.paths as paths_mod

    monkeypatch.setattr(paths_mod, "RAW_DIR", raw)
    monkeypatch.setattr(paths_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(paths_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(paths_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(ingest_mod, "RAW_DIR", raw)
    monkeypatch.setattr(ingest_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(ingest_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(ops_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(ops_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(ops_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(col, "MANIFESTS_DIR", man)
    monkeypatch.setattr(col, "REPORTS_DIR", reports)
    # Minimal collection state
    (man / "collection_state.json").write_text(
        json.dumps(
            {
                "R3E_FUTURE_DATA_COLLECTION": "IN_PROGRESS",
                "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
                "ECONOMIC_INTERPRETATION_ALLOWED": False,
                "R4_STATUS": "BLOCKED",
                "R5_STATUS": "NOT_STARTED",
                "validation_command_executed": False,
                "effect_peeking_performed": False,
                "cutoff": fu_config.FUTURE_UNSEEN_CUTOFF_ISO,
            }
        ),
        encoding="utf-8",
    )
    return tmp_path


def test_cutoff_reject_equal_and_before():
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    with pytest.raises(FutureUnseenProtectionError):
        assert_strictly_after_cutoff(cut)
    with pytest.raises(FutureUnseenProtectionError):
        assert_strictly_after_cutoff(cut - timedelta(seconds=1))


def test_cutoff_accept_after():
    dt = assert_strictly_after_cutoff(fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(hours=1))
    assert dt > fu_config.FUTURE_UNSEEN_CUTOFF


def test_first_open_after_cutoff_1h_and_1d():
    h = first_open_strictly_after_cutoff(timeframe="1h")
    d = first_open_strictly_after_cutoff(timeframe="1d")
    assert h == datetime(2026, 7, 18, 2, 0, tzinfo=UTC)
    assert d == datetime(2026, 7, 19, 0, 0, tzinfo=UTC)
    assert h > fu_config.FUTURE_UNSEEN_CUTOFF
    assert d > fu_config.FUTURE_UNSEEN_CUTOFF


def test_last_closed_candle_boundary():
    now = datetime(2026, 7, 18, 5, 15, tzinfo=UTC)
    open_ts = last_closed_candle_open(timeframe="1h", now_utc=now, safety_delay_seconds=30)
    # At 05:15 with 30s delay, 04:00 candle closes at 05:00 <= 05:14:30 → closed.
    assert open_ts == datetime(2026, 7, 18, 4, 0, tzinfo=UTC)


def test_empty_series_window_starts_after_cutoff():
    now = datetime(2026, 7, 20, 12, 0, tzinfo=UTC)
    w = compute_fetch_window(
        symbol="BTC/USDT",
        timeframe="1h",
        source="binance",
        now_utc=now,
        last_accepted=None,
    )
    assert w["requested_start"] == datetime(2026, 7, 18, 2, 0, tzinfo=UTC)
    assert w["mode"] == "EMPTY_SERIES_AFTER_CUTOFF"


def test_incremental_window_after_last():
    now = datetime(2026, 7, 20, 12, 0, tzinfo=UTC)
    last = datetime(2026, 7, 18, 5, 0, tzinfo=UTC)
    w = compute_fetch_window(
        symbol="BTC/USDT",
        timeframe="1h",
        source="binance",
        now_utc=now,
        last_accepted=last,
        revision_overlap_bars=1,
    )
    # next=06:00 minus 1h overlap => 05:00
    assert w["requested_start"] == datetime(2026, 7, 18, 5, 0, tzinfo=UTC)
    assert w["mode"] == "INCREMENTAL_AFTER_LAST"


def test_collect_rejects_open_and_pre_cutoff(fu_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    now = datetime(2026, 7, 18, 4, 30, tzinfo=UTC)
    candles = [
        _candle(cut - timedelta(hours=1)),  # historical
        _candle(cut),  # equal cutoff
        _candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC)),  # closed eligible
        _candle(datetime(2026, 7, 18, 4, 0, tzinfo=UTC)),  # still open at 4:30 with 1h+delay
    ]
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", cut, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    provider = FakeProvider(candles)
    out = collector_mod.run_collect(
        as_of=now,
        provider_factory=lambda n: provider,
        sleep_fn=lambda s: None,
    )
    assert out["n_observations_after"] == 1
    reasons = {
        r["reason"]
        for r in json.loads(Path(out["report_paths"]["rejections"]).read_text(encoding="utf-8"))[
            "rejections"
        ]
    }
    assert "NOT_STRICTLY_AFTER_FUTURE_UNSEEN_CUTOFF" in reasons
    assert "CANDLE_NOT_CLOSED" in reasons


def test_idempotent_second_collect(fu_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    candles = [
        _candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC)),
        _candle(datetime(2026, 7, 18, 3, 0, tzinfo=UTC)),
        _candle(datetime(2026, 7, 18, 4, 0, tzinfo=UTC)),
    ]
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    provider = FakeProvider(candles)
    factory = lambda n: provider  # noqa: E731
    first = collector_mod.run_collect(as_of=now, provider_factory=factory, sleep_fn=lambda s: None)
    n1 = first["n_observations_after"]
    assert n1 >= 1
    second = collector_mod.run_collect(as_of=now, provider_factory=factory, sleep_fn=lambda s: None)
    assert second["n_observations_after"] == n1
    assert second["n_observations_before"] == n1


def test_dry_run_does_not_write(fu_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    candles = [_candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC))]
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    out = collector_mod.run_collect(
        dry_run=True,
        as_of=now,
        provider_factory=lambda n: FakeProvider(candles),
        sleep_fn=lambda s: None,
    )
    assert out["dry_run"] is True
    assert out["n_observations_after"] == 0
    assert out["n_candidates"] == 1
    assert list((fu_dirs / "validated").glob("*.jsonl")) == []


def test_provider_failure_does_not_stop_others(fu_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    tiny = [
        SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto"),
        SeriesSpec("binance", "ETH/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto"),
    ]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    ok = FakeProvider([_candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC))])

    def factory(name: str):
        # Same provider source — use collect_series patching instead
        return ok

    calls = {"n": 0}
    real = collector_mod.collect_series

    def wrapped(spec, **kwargs):
        calls["n"] += 1
        if spec.symbol == "ETH/USDT":
            return {
                "status": {
                    "series_key": f"{spec.source}|{spec.symbol}|{spec.timeframe}",
                    "status": "PROVIDER_ERROR",
                    "provider_error": "boom",
                    "n_accepted_candidates": 0,
                    "n_rejected": 0,
                    "gaps": [],
                },
                "records": [],
                "rejections": [],
            }
        return real(spec, **kwargs)

    monkeypatch.setattr(collector_mod, "collect_series", wrapped)
    out = collector_mod.run_collect(as_of=now, provider_factory=factory, sleep_fn=lambda s: None)
    assert out["n_observations_after"] >= 1
    assert out["run_status"] in {"PARTIAL", "COMPLETE"}
    assert any(s["status"] == "PROVIDER_ERROR" for s in out["series_status"])


def test_collector_module_has_no_forbidden_imports():
    path = Path(collector_mod.__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    for forbidden in collector_mod.FORBIDDEN_COLLECTOR_IMPORTS:
        assert forbidden not in imported
    src = path.read_text(encoding="utf-8")
    assert "decide_gate" not in src
    assert "run_validation" not in src
    assert "run_r3e_on_series" not in src


def test_reports_forbid_effect_keys(fu_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    out = collector_mod.run_collect(
        as_of=now,
        provider_factory=lambda n: FakeProvider([_candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC))]),
        sleep_fn=lambda s: None,
    )

    def collect_keys(o, acc: set[str]) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                acc.add(str(k).lower())
                collect_keys(v, acc)
        elif isinstance(o, list):
            for i in o:
                collect_keys(i, acc)

    for p in out["report_paths"].values():
        doc = json.loads(Path(p).read_text(encoding="utf-8"))
        keys: set[str] = set()
        collect_keys(doc, keys)
        assert not (keys & collector_mod.FORBIDDEN_REPORT_KEYS)


def test_hash_tamper_detected_after_collect(fu_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    out = collector_mod.run_collect(
        as_of=now,
        provider_factory=lambda n: FakeProvider([_candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC))]),
        sleep_fn=lambda s: None,
    )
    val = Path(out["persist"]["validated_path"])
    expected = out["persist"]["file_sha256"]
    val.write_text(val.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    assert sha256_file(val) != expected


def test_cli_has_no_unsafe_flags():
    src = Path("src/wick/r3e/future_unseen/cli.py").read_text(encoding="utf-8")
    for bad in (
        "ignore-cutoff",
        "allow-historical",
        "skip-eligibility",
        "skip-validation",
        "disable-hashes",
        "overwrite",
        "unlock-r4",
        "override-freeze",
    ):
        assert bad not in src
