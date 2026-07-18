"""Tests for R3E future-unseen readiness gate (B2 / R3E-READINESS-001)."""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from typer.testing import CliRunner

from wick.r3e.future_unseen import config as fu_config
from wick.r3e.future_unseen.cli import app
from wick.r3e.future_unseen.hashing import sha256_file
from wick.r3e.future_unseen.readiness import (
    EXIT_BLOCKED,
    EXIT_NOT_READY,
    EXIT_READY,
    STATUS_BLOCKED,
    STATUS_NOT_READY,
    STATUS_READY,
    evaluate_readiness,
    exit_code_for_status,
)


@pytest.fixture()
def ready_dirs(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    val = tmp_path / "validated"
    man = tmp_path / "manifests"
    reports = tmp_path / "reports"
    for d in (raw, val, man, reports):
        d.mkdir()
    import wick.r3e.future_unseen.paths as paths_mod
    import wick.r3e.future_unseen.readiness as readiness_mod

    monkeypatch.setattr(paths_mod, "RAW_DIR", raw)
    monkeypatch.setattr(paths_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(paths_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(paths_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(paths_mod, "COLLECTION_STATE_PATH", man / "collection_state.json")
    monkeypatch.setattr(readiness_mod, "RAW_DIR", raw)
    monkeypatch.setattr(readiness_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(readiness_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(readiness_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(readiness_mod, "COLLECTION_STATE_PATH", man / "collection_state.json")
    return {"raw": raw, "val": val, "man": man, "reports": reports, "root": tmp_path}


def _write_state(man: Path, **overrides):
    state = {
        "R3E_FUTURE_DATA_COLLECTION": "IN_PROGRESS",
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "ECONOMIC_INTERPRETATION_ALLOWED": False,
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
        "validation_command_executed": False,
        "effect_peeking_performed": False,
        "cutoff": fu_config.FUTURE_UNSEEN_CUTOFF_ISO,
    }
    state.update(overrides)
    (man / "collection_state.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def _bar(symbol: str, source: str, timeframe: str, ts: datetime, price: float = 100.0) -> dict:
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source": source,
        "market_ts": ts.astimezone(UTC).isoformat(),
        "open": price,
        "high": price * 1.01,
        "low": price * 0.99,
        "close": price * 1.001,
        "volume": 1000.0,
        "revision": 1,
        "origin": "future-unseen-test",
    }


def _seed_complete_store(ready_dirs, *, as_of: datetime, n_series: int = 16, bars: int = 200):
    man = ready_dirs["man"]
    val = ready_dirs["val"]
    _write_state(man, R3E_FUTURE_DATA_COLLECTION="COMPLETE")
    universe = list(fu_config.SERIES_UNIVERSE)[:n_series]
    start = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(hours=1)
    lines: list[str] = []
    for sym, tf, src in universe:
        for i in range(bars):
            # keep all bars <= as_of
            ts = start + timedelta(hours=i)
            if ts > as_of:
                break
            lines.append(json.dumps(_bar(sym, src, tf, ts)))
    path = val / "batch_ready.jsonl"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    digest = sha256_file(path)
    meta = {
        "batch_id": "batch_ready",
        "validated_path": str(path),
        "file_sha256": digest,
        "origin": "future-unseen-test",
        "gaps_detected": [],
        "rejections": [],
    }
    (man / "batch_ready.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return path


def test_window_under_90_days_not_ready(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=10)
    _seed_complete_store(ready_dirs, as_of=as_of, n_series=16, bars=200)
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_NOT_READY
    assert report["window_days"] < 90
    assert any(r["code"] == "WINDOW_DAYS_INSUFFICIENT" for r in report["not_ready_reasons"])


def test_ready_when_criteria_met(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _seed_complete_store(ready_dirs, as_of=as_of, n_series=16, bars=200)
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_READY
    assert report["series_with_min_bars"] >= 16
    assert report["hash_status"] == "OK"
    assert report["scientific_safety"]["VALIDATE_AUTHORIZED"] is False
    assert report["scientific_safety"]["R4_STATUS"] == "BLOCKED"
    assert report["scientific_safety"]["R5_STATUS"] == "NOT_STARTED"
    assert exit_code_for_status(report["readiness_status"]) == EXIT_READY


def test_insufficient_series_not_ready(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _seed_complete_store(ready_dirs, as_of=as_of, n_series=5, bars=200)
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_NOT_READY
    assert any(r["code"] == "SERIES_INSUFFICIENT" for r in report["not_ready_reasons"])


def test_insufficient_bars_not_ready(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _seed_complete_store(ready_dirs, as_of=as_of, n_series=16, bars=50)
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_NOT_READY
    assert any(
        r["code"] in {"SERIES_INSUFFICIENT", "BARS_INSUFFICIENT"}
        for r in report["not_ready_reasons"]
    )


def test_invalid_hash_blocked(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    path = _seed_complete_store(ready_dirs, as_of=as_of)
    man = ready_dirs["man"] / "batch_ready.json"
    meta = json.loads(man.read_text(encoding="utf-8"))
    meta["file_sha256"] = "0" * 64
    man.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_BLOCKED
    assert report["hash_status"] == "INVALID"
    assert exit_code_for_status(report["readiness_status"]) == EXIT_BLOCKED
    assert path.is_file()


def test_pre_cutoff_data_blocked(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _write_state(ready_dirs["man"])
    bad_ts = fu_config.FUTURE_UNSEEN_CUTOFF  # equal → blocked
    path = ready_dirs["val"] / "bad.jsonl"
    path.write_text(
        json.dumps(_bar("BTC/USDT", "binance", "1h", bad_ts)) + "\n",
        encoding="utf-8",
    )
    meta = {
        "batch_id": "bad",
        "validated_path": str(path),
        "file_sha256": sha256_file(path),
        "origin": "future-unseen-test",
        "gaps_detected": [],
        "rejections": [],
    }
    (ready_dirs["man"] / "batch_bad.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_BLOCKED
    assert any(b["code"] == "PRE_OR_AT_CUTOFF_DATA" for b in report["blockers"])


def test_open_candle_not_ready(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _write_state(ready_dirs["man"])
    future = as_of + timedelta(hours=5)
    path = ready_dirs["val"] / "open.jsonl"
    path.write_text(
        json.dumps(_bar("BTC/USDT", "binance", "1h", future)) + "\n",
        encoding="utf-8",
    )
    meta = {
        "batch_id": "open",
        "validated_path": str(path),
        "file_sha256": sha256_file(path),
        "origin": "future-unseen-test",
        "gaps_detected": [],
        "rejections": [],
    }
    (ready_dirs["man"] / "batch_open.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    report = evaluate_readiness(as_of=as_of, strict=False)
    assert report["readiness_status"] == STATUS_NOT_READY
    assert any(r["code"] == "OPEN_OR_FUTURE_CANDLE" for r in report["not_ready_reasons"])


def test_duplicate_blocked(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _write_state(ready_dirs["man"])
    ts = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(hours=2)
    rec = json.dumps(_bar("BTC/USDT", "binance", "1h", ts))
    path = ready_dirs["val"] / "dup.jsonl"
    path.write_text(rec + "\n" + rec + "\n", encoding="utf-8")
    meta = {
        "batch_id": "dup",
        "validated_path": str(path),
        "file_sha256": sha256_file(path),
        "origin": "future-unseen-test",
        "gaps_detected": [],
        "rejections": [],
    }
    (ready_dirs["man"] / "batch_dup.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_BLOCKED
    assert any(b["code"] == "DUPLICATES_PRESENT" for b in report["blockers"])


def test_informational_gap_does_not_block(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    path = _seed_complete_store(ready_dirs, as_of=as_of)
    man = ready_dirs["man"] / "batch_ready.json"
    meta = json.loads(man.read_text(encoding="utf-8"))
    meta["gaps_detected"] = [{"kind": "hole", "classification": "UNEXPLAINED_GAP"}]
    man.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    # refresh hash unchanged for validated file
    assert path.is_file()
    report = evaluate_readiness(as_of=as_of)
    assert report["gap_status"]["counts"]["INFORMATIONAL"] >= 1
    assert report["readiness_status"] == STATUS_READY


def test_critical_gap_blocked(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _seed_complete_store(ready_dirs, as_of=as_of)
    man = ready_dirs["man"] / "batch_ready.json"
    meta = json.loads(man.read_text(encoding="utf-8"))
    meta["gaps_detected"] = [{"kind": "non_monotonic"}]
    man.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_BLOCKED
    assert any(b["code"] == "CRITICAL_GAP" for b in report["blockers"])


def test_backfill_mix_blocked(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    path = _seed_complete_store(ready_dirs, as_of=as_of)
    man = ready_dirs["man"] / "batch_ready.json"
    meta = json.loads(man.read_text(encoding="utf-8"))
    meta["origin"] = "operational_backfill/sandbox"
    man.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    assert path.is_file()
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_BLOCKED
    assert any(b["code"] == "BACKFILL_OR_FORBIDDEN_MIX" for b in report["blockers"])


def test_manifest_inconsistency_blocked(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _write_state(ready_dirs["man"])
    (ready_dirs["man"] / "batch_broken.json").write_text(
        json.dumps({"batch_id": "broken", "origin": "x"}) + "\n",
        encoding="utf-8",
    )
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] == STATUS_BLOCKED
    assert report["manifest_status"] == "INCONSISTENT"


def test_idempotent_rerun(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _seed_complete_store(ready_dirs, as_of=as_of)
    a = evaluate_readiness(as_of=as_of)
    b = evaluate_readiness(as_of=as_of)
    for key in (
        "readiness_status",
        "readiness_reason",
        "series_with_min_bars",
        "hash_status",
        "manifest_status",
        "n_observations_total",
    ):
        assert a[key] == b[key]


def test_read_only_no_store_mutation(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=10)
    _seed_complete_store(ready_dirs, as_of=as_of, n_series=2, bars=10)
    before = {
        p: p.read_bytes()
        for p in list(ready_dirs["val"].glob("*")) + list(ready_dirs["man"].glob("*"))
    }
    evaluate_readiness(as_of=as_of)
    after = {
        p: p.read_bytes()
        for p in list(ready_dirs["val"].glob("*")) + list(ready_dirs["man"].glob("*"))
    }
    assert before == after


def test_does_not_call_validate(ready_dirs, monkeypatch):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=10)
    _seed_complete_store(ready_dirs, as_of=as_of, n_series=2, bars=10)

    def boom(*_a, **_k):
        raise AssertionError("validate must not be imported/called")

    monkeypatch.setattr("wick.r3e.future_unseen.validate.run_validation", boom)
    report = evaluate_readiness(as_of=as_of)
    assert report["readiness_status"] in {STATUS_NOT_READY, STATUS_BLOCKED, STATUS_READY}


def test_no_science_keys_in_output(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _seed_complete_store(ready_dirs, as_of=as_of)
    report = evaluate_readiness(as_of=as_of)
    blob = json.dumps(report).lower()
    for key in ("delta_candle", "p_value", "fdr", "mean_net", "m5_minus_m4"):
        assert key not in blob


def test_r4_r5_unchanged_in_report(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _seed_complete_store(ready_dirs, as_of=as_of)
    report = evaluate_readiness(as_of=as_of)
    assert report["scientific_safety"]["R4_STATUS"] == "BLOCKED"
    assert report["scientific_safety"]["R5_STATUS"] == "NOT_STARTED"


def test_json_stable_and_exit_codes(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=10)
    _seed_complete_store(ready_dirs, as_of=as_of, n_series=2, bars=10)
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "readiness",
            "--as-of",
            as_of.isoformat(),
            "--output-report",
            str(ready_dirs["reports"] / "r.json"),
            "--json",
        ],
    )
    assert result.exit_code == EXIT_NOT_READY
    payload = json.loads(result.stdout)
    assert payload["readiness_status"] == STATUS_NOT_READY
    assert "readiness_reason" in payload
    assert (ready_dirs["reports"] / "r.json").is_file()


def test_timezone_ordering(ready_dirs):
    as_of = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(days=91)
    _write_state(ready_dirs["man"])
    t1 = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(hours=1)
    t2 = fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(hours=3)
    path = ready_dirs["val"] / "order.jsonl"
    # intentionally reverse write order
    path.write_text(
        json.dumps(_bar("BTC/USDT", "binance", "1h", t2))
        + "\n"
        + json.dumps(_bar("BTC/USDT", "binance", "1h", t1))
        + "\n",
        encoding="utf-8",
    )
    meta = {
        "batch_id": "order",
        "validated_path": str(path),
        "file_sha256": sha256_file(path),
        "origin": "future-unseen-test",
        "gaps_detected": [{"kind": "non_monotonic"}],
        "rejections": [],
    }
    (ready_dirs["man"] / "batch_order.json").write_text(json.dumps(meta) + "\n", encoding="utf-8")
    report = evaluate_readiness(as_of=as_of)
    sk = "binance|BTC/USDT|1h"
    assert report["series_counts"].get(sk, 0) == 2
    # temporal first/last normalized
    assert report["readiness_status"] == STATUS_BLOCKED  # critical gap
    assert any(b["code"] == "CRITICAL_GAP" for b in report["blockers"])
