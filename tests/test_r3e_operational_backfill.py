"""Tests for R3E operational historical backfill (isolated, non-scientific)."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path

import pytest

from wick.ingestion.providers.base import FetchResult, MarketDataProvider
from wick.ingestion.validators import RawCandle
from wick.r3e.future_unseen.protections import (
    FutureUnseenProtectionError,
    assert_strictly_after_cutoff,
)
from wick.r3e.operational_backfill import collect as collect_mod
from wick.r3e.operational_backfill import compatibility as compat_mod
from wick.r3e.operational_backfill import isolation as iso_mod
from wick.r3e.operational_backfill import paths as ob_paths
from wick.r3e.operational_backfill import reports as reports_mod
from wick.r3e.operational_backfill.config import (
    BACKFILL_END,
    BACKFILL_START,
    CLASSIFICATION,
    SERIES_UNIVERSE,
)
from wick.r3e.operational_backfill.policy import (
    HistoricalBackfillPolicyError,
    HistoricalOperationalBackfillPolicy,
)
from wick.r3e.operational_backfill.schema import (
    StructuralValidationError,
    is_structurally_compatible_with_future_unseen,
    validate_structural_record,
)
from wick.r3e.operational_backfill.store import store_batch


def _candle(ts: datetime, price: float = 100.0) -> RawCandle:
    return RawCandle(
        timestamp=ts,
        open=Decimal(str(price)),
        high=Decimal(str(price * 1.01)),
        low=Decimal(str(price * 0.99)),
        close=Decimal(str(price)),
        volume=Decimal("10"),
    )


def _rec(ts: datetime, **kwargs) -> dict:
    base = {
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "source": "binance",
        "market_ts": ts.isoformat(),
        "open": 100.0,
        "high": 101.0,
        "low": 99.0,
        "close": 100.5,
        "volume": 1.0,
        "revision": 1,
    }
    base.update(kwargs)
    return base


class FakeProvider(MarketDataProvider):
    name = "binance"
    asset_type = "crypto"

    def __init__(self, candles: list[RawCandle] | None = None, *, fail: bool = False):
        self._candles = candles or []
        self._fail = fail

    def fetch_ohlcv(self, symbol, timeframe, start, end) -> FetchResult:
        if self._fail:
            raise RuntimeError("provider down")
        return FetchResult(
            candles=list(self._candles),
            actual_start=start,
            actual_end=end,
        )


@pytest.fixture()
def ob_dirs(tmp_path, monkeypatch):
    root = tmp_path / "ob"
    reports = tmp_path / "reports"
    for d in (root / "raw", root / "validated", root / "manifests", reports):
        d.mkdir(parents=True)
    monkeypatch.setattr(ob_paths, "DEFAULT_OUTPUT_ROOT", root)
    monkeypatch.setattr(ob_paths, "REPORTS_DIR", reports)
    monkeypatch.setattr(collect_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(reports_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(compat_mod, "REPORTS_DIR", reports)
    return root


def test_historical_policy_accepts_window():
    pol = HistoricalOperationalBackfillPolicy()
    mid = BACKFILL_START + timedelta(days=10)
    assert pol.assert_eligible(mid) == mid


def test_historical_policy_rejects_before_start():
    pol = HistoricalOperationalBackfillPolicy()
    with pytest.raises(HistoricalBackfillPolicyError):
        pol.assert_eligible(BACKFILL_START - timedelta(seconds=1))


def test_historical_policy_rejects_after_cutoff():
    pol = HistoricalOperationalBackfillPolicy()
    with pytest.raises(HistoricalBackfillPolicyError):
        pol.assert_eligible(BACKFILL_END + timedelta(seconds=1))


def test_historical_policy_accepts_equal_cutoff():
    pol = HistoricalOperationalBackfillPolicy()
    assert pol.assert_eligible(BACKFILL_END) == BACKFILL_END


def test_future_unseen_policy_unchanged_rejects_historical():
    with pytest.raises(FutureUnseenProtectionError):
        assert_strictly_after_cutoff(BACKFILL_END)
    with pytest.raises(FutureUnseenProtectionError):
        assert_strictly_after_cutoff(BACKFILL_START + timedelta(days=1))


def test_ohlc_validation_rejects_bad_high():
    with pytest.raises(StructuralValidationError):
        validate_structural_record(
            _rec(BACKFILL_START + timedelta(hours=1), high=90.0, open=100.0, close=100.0)
        )


def test_timezone_naive_rejected():
    with pytest.raises((StructuralValidationError, FutureUnseenProtectionError, ValueError)):
        validate_structural_record(
            _rec(BACKFILL_START + timedelta(hours=1), market_ts="2026-05-01T00:00:00")
        )


def test_unknown_series_rejected():
    with pytest.raises(StructuralValidationError):
        validate_structural_record(
            _rec(BACKFILL_START + timedelta(hours=1), symbol="DOGE/USDT")
        )


def test_store_duplicate_and_revision(ob_dirs):
    ts = BACKFILL_START + timedelta(hours=2)
    r1 = store_batch([_rec(ts)], output=ob_dirs)
    assert r1.accepted == 1
    r2 = store_batch([_rec(ts)], output=ob_dirs)
    assert r2.accepted == 0
    assert r2.duplicates == 1
    r3 = store_batch(
        [_rec(ts, close=100.9, revision=2)],
        output=ob_dirs,
    )
    assert r3.accepted == 1
    assert r3.revisions == 1


def test_post_cutoff_bar_rejected_in_sandbox(ob_dirs):
    ts = BACKFILL_END + timedelta(hours=1)
    result = store_batch([_rec(ts)], output=ob_dirs)
    assert result.accepted == 0
    assert any("after FUTURE_UNSEEN_CUTOFF" in r.reason or "after backfill end" in r.reason for r in result.rejections)


def test_directory_isolation_assert():
    with pytest.raises(RuntimeError):
        ob_paths.assert_not_official_path("data/future_unseen/raw/x.jsonl")


def test_collect_isolates_and_continues_on_provider_failure(ob_dirs, monkeypatch):
    # Freeze universe to a tiny subset via monkeypatch on collect.UNIVERSE
    from wick.r3d.universe import SeriesSpec

    tiny = [
        SeriesSpec("binance", "BTC/USDT", "1h", BACKFILL_START, 0.1, "crypto"),
        SeriesSpec("binance", "ETH/USDT", "1h", BACKFILL_START, 0.1, "crypto"),
    ]
    monkeypatch.setattr(collect_mod, "UNIVERSE", tiny)

    ts = BACKFILL_START + timedelta(hours=5)
    # ensure closed relative to "now"
    now = BACKFILL_END + timedelta(days=1)

    def factory(name: str):
        if name != "binance":
            raise RuntimeError("bad")
        # First series ok via shared provider — both use same provider instance cache
        return FakeProvider([_candle(ts)], fail=False)

    # Make second series fail by patching collect_series after first call
    calls = {"n": 0}
    real = collect_mod.collect_series

    def wrapped(spec, **kwargs):
        calls["n"] += 1
        if spec.symbol == "ETH/USDT":
            return {
                "meta": {
                    "series_key": f"{spec.source}|{spec.symbol}|{spec.timeframe}",
                    "status": "PROVIDER_FAILURE",
                    "provider_error": "boom",
                    "n_accepted_candidate": 0,
                    "min_bars_operational": 1,
                },
                "records": [],
                "rejections": [],
                "gaps": [],
            }
        return real(spec, **kwargs)

    monkeypatch.setattr(collect_mod, "collect_series", wrapped)
    # Lower min bars for COMPLETE
    monkeypatch.setattr(collect_mod, "_min_bars", lambda spec: 1)

    out = collect_mod.run_collect(
        start=BACKFILL_START,
        end=BACKFILL_END,
        output=ob_dirs,
        provider_factory=factory,
        now_utc=now,
    )
    assert out["n_missing"] >= 1
    assert (ob_dirs / "manifests" / "run_manifest.json").is_file()
    # Must not write under official paths
    assert "future_unseen" not in out["output_root"]


def test_schema_compatibility_and_temporal_ineligible(ob_dirs):
    ts = BACKFILL_START + timedelta(days=3)
    store_batch([_rec(ts)], output=ob_dirs)
    report = compat_mod.build_schema_compatibility_report(output=ob_dirs)
    assert report["STRUCTURAL_SCHEMA_COMPATIBLE"] is True
    assert report["FUTURE_UNSEEN_TEMPORALLY_ELIGIBLE"] is False
    assert is_structurally_compatible_with_future_unseen(_rec(ts))


def test_official_reject_probe_temp_only(ob_dirs, monkeypatch):
    ts = BACKFILL_START + timedelta(days=2)
    store_batch([_rec(ts)], output=ob_dirs)
    probe = compat_mod.run_official_reject_probe(output=ob_dirs, sample_size=1)
    assert probe["OFFICIAL_FUTURE_INGEST_REJECTED_HISTORICAL_DATA"] is True
    assert probe["accepted"] == 0
    assert probe["persistent_official_dirs_used"] is False


def test_official_state_snapshot_compare_equal(monkeypatch, tmp_path):
    man = tmp_path / "man"
    man.mkdir()
    state = {
        "R3E_FUTURE_DATA_COLLECTION": "IN_PROGRESS",
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "R4_STATUS": "BLOCKED",
        "ECONOMIC_INTERPRETATION_ALLOWED": False,
        "validation_command_executed": False,
        "effect_peeking_performed": False,
    }
    (man / "collection_state.json").write_text(json.dumps(state), encoding="utf-8")
    (man / "cutoff_manifest.json").write_text("{}", encoding="utf-8")
    (man / "model_freeze.json").write_text("{}", encoding="utf-8")
    reports = tmp_path / "reports"
    reports.mkdir()
    ops = {
        "n_observations_total": 0,
        "series_received": [],
        "series_missing": ["x"],
        "formal_collection_state": "IN_PROGRESS",
    }
    (reports / "ops_collection_report.json").write_text(json.dumps(ops), encoding="utf-8")
    raw = tmp_path / "raw"
    val = tmp_path / "validated"
    raw.mkdir()
    val.mkdir()

    monkeypatch.setattr(iso_mod, "OFFICIAL_COLLECTION_STATE", man / "collection_state.json")
    monkeypatch.setattr(iso_mod, "OFFICIAL_CUTOFF_MANIFEST", man / "cutoff_manifest.json")
    monkeypatch.setattr(iso_mod, "OFFICIAL_MODEL_FREEZE", man / "model_freeze.json")
    monkeypatch.setattr(iso_mod, "OFFICIAL_OPS_REPORT", reports / "ops_collection_report.json")
    monkeypatch.setattr(iso_mod, "OFFICIAL_FU_RAW", raw)
    monkeypatch.setattr(iso_mod, "OFFICIAL_FU_VALIDATED", val)

    before = iso_mod.snapshot_official_state()
    after = iso_mod.snapshot_official_state()
    cmp = iso_mod.compare_snapshots(before, after)
    assert cmp["OFFICIAL_COLLECTION_STATE_UNCHANGED"] is True


def test_no_gate_import_in_operational_modules():
    import wick.r3e.operational_backfill.collect as c
    import wick.r3e.operational_backfill.reports as r
    import wick.r3e.operational_backfill.store as s

    for mod in (c, s, r):
        src = Path(mod.__file__).read_text(encoding="utf-8")
        assert "future_unseen.validate" not in src
        assert "decide_gate" not in src
        assert "run_r3e_on_series" not in src


def test_classification_labels_present():
    assert CLASSIFICATION["DATA_ORIGIN"] == "HISTORICAL_OPERATIONAL_BACKFILL"
    assert CLASSIFICATION["SCIENTIFIC_EVIDENCE_ELIGIBLE"] is False
    assert CLASSIFICATION["FUTURE_UNSEEN_ELIGIBLE"] is False
    assert CLASSIFICATION["GATE_IMPACT_ALLOWED"] is False


def test_universe_has_20_series():
    assert len(SERIES_UNIVERSE) == 20


def test_closed_candle_rejection_path(ob_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", BACKFILL_START, 0.1, "crypto")]
    monkeypatch.setattr(collect_mod, "UNIVERSE", tiny)
    monkeypatch.setattr(collect_mod, "_min_bars", lambda spec: 1)
    # Open candle: timestamp near "now"
    now = datetime(2026, 7, 18, 12, 0, tzinfo=UTC)
    open_ts = now - timedelta(minutes=10)
    factory = lambda name: FakeProvider([_candle(open_ts)])  # noqa: E731
    out = collect_mod.run_collect(
        start=BACKFILL_START,
        end=BACKFILL_END,
        output=ob_dirs,
        provider_factory=factory,
        now_utc=now,
    )
    assert out["accepted_total"] == 0
    assert any(r.get("reason") == "candle_not_closed" for r in out["rejections"])


def test_hash_tamper_detected(ob_dirs):
    ts = BACKFILL_START + timedelta(hours=3)
    result = store_batch([_rec(ts)], output=ob_dirs)
    path = Path(result.validated_path)
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    from wick.r3e.future_unseen.hashing import sha256_file

    assert sha256_file(path) != result.file_sha256


def test_reports_have_no_effect_keys(ob_dirs, monkeypatch):
    ts = BACKFILL_START + timedelta(days=1, hours=1)
    store_batch([_rec(ts)], output=ob_dirs)
    collect_result = {
        "run_manifest": {
            "R3E_OPERATIONAL_BACKFILL_RUN": "PARTIAL",
            "n_series_expected": 20,
            "provider_failures": [],
            "series": [],
        },
        "mapping": {"series": []},
        "series_results": [
            {
                "meta": {
                    "series_key": "binance|BTC/USDT|1h",
                    "status": "PARTIAL",
                    "min_bars_operational": 1800,
                }
            }
        ],
        "gaps": [],
        "rejections": [],
        "accepted_total": 1,
        "rejected_store": 0,
        "duplicates": 0,
        "hash_integrity_ok": True,
        "hash_errors": [],
    }
    paths = reports_mod.build_all_reports(
        collect_result,
        isolation_compare={"OFFICIAL_COLLECTION_STATE_UNCHANGED": True, "differences": {}},
        schema_compat={"STRUCTURAL_SCHEMA_COMPATIBLE": True},
        reject_probe={"OFFICIAL_FUTURE_INGEST_REJECTED_HISTORICAL_DATA": True},
        output=ob_dirs,
    )
    doc = json.loads(paths["collection_report"].read_text(encoding="utf-8"))
    assert doc["validate_executed"] is False
    assert doc["models_executed"] == []
    assert "delta_candle" not in doc
