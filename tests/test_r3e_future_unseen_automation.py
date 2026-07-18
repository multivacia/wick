"""Tests for R3E future-unseen collection automation (B4)."""

from __future__ import annotations

import ast
import json
import os
import time
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

import pytest
from typer.testing import CliRunner

from wick.ingestion.providers.base import FetchResult, MarketDataProvider
from wick.ingestion.validators import RawCandle
from wick.r3e.future_unseen import automation as automation_mod
from wick.r3e.future_unseen import collector as collector_mod
from wick.r3e.future_unseen import config as fu_config
from wick.r3e.future_unseen.automation import (
    EXIT_BLOCKED,
    EXIT_FAILED,
    EXIT_OK,
    EXIT_SKIPPED_LOCKED,
    FORBIDDEN_AUTOMATION_IMPORTS,
    STATUS_BLOCKED,
    STATUS_COMPLETE,
    STATUS_FAILED,
    STATUS_NO_NEW_DATA,
    STATUS_PARTIAL,
    STATUS_SKIPPED_LOCKED,
    AutomationLock,
    exit_code_for_cycle_status,
    run_cycle,
)
from wick.r3e.future_unseen.cli import app


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
        self.calls = 0

    def fetch_ohlcv(self, symbol, timeframe, start, end) -> FetchResult:
        self.calls += 1
        if self.fail:
            raise RuntimeError("provider down")
        return FetchResult(candles=list(self.candles), actual_start=start, actual_end=end)


@pytest.fixture()
def auto_dirs(tmp_path, monkeypatch):
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
    import wick.r3e.future_unseen.readiness as readiness_mod

    monkeypatch.setattr(paths_mod, "RAW_DIR", raw)
    monkeypatch.setattr(paths_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(paths_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(paths_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(paths_mod, "COLLECTION_STATE_PATH", man / "collection_state.json")
    monkeypatch.setattr(ingest_mod, "RAW_DIR", raw)
    monkeypatch.setattr(ingest_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(ingest_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(ops_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(ops_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(ops_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(col, "MANIFESTS_DIR", man)
    monkeypatch.setattr(col, "REPORTS_DIR", reports)
    monkeypatch.setattr(readiness_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(readiness_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(readiness_mod, "RAW_DIR", raw)
    monkeypatch.setattr(readiness_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(readiness_mod, "COLLECTION_STATE_PATH", man / "collection_state.json")
    monkeypatch.setattr(automation_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(automation_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(automation_mod, "COLLECTION_STATE_PATH", man / "collection_state.json")

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
    return {
        "root": tmp_path,
        "raw": raw,
        "val": val,
        "man": man,
        "reports": reports,
        "lock": reports / "automation.lock",
        "state": reports / "automation_state.json",
        "runs": reports / "automation_runs",
        "events": reports / "automation_events.jsonl",
    }


def _base_collect_result(**overrides):
    doc = {
        "collection_run_id": "fu_collect_test",
        "run_status": "COMPLETE",
        "dry_run": False,
        "n_observations_before": 10,
        "n_observations_after": 12,
        "n_candidates": 2,
        "persist": {"n_store_rejected": 0, "n_accepted": 2},
        "series_status": [
            {
                "series_key": "binance|BTC/USDT|1h",
                "status": "SUCCESS",
                "n_accepted_candidates": 2,
                "n_rejected": 0,
            }
        ],
        "ops": {"n_observations_total": 12, "hash_integrity_ok": True},
    }
    doc.update(overrides)
    return doc


def _ready_report(status: str = "NOT_READY", reason: str = "WINDOW_DAYS_INSUFFICIENT"):
    return {
        "readiness_status": status,
        "readiness_reason": reason,
        "window_days": 0.7,
        "eligible_series": 5,
        "series_with_min_bars": 0,
        "required_series": 16,
        "required_min_bars": 200,
        "hash_status": "OK" if status != "BLOCKED" else "INVALID",
        "manifest_status": "OK" if status != "BLOCKED" else "INCONSISTENT",
        "gap_status": {"counts": {}},
        "collector_status": "IN_PROGRESS",
        "scientific_safety": {
            "validation_command_executed": False,
            "effect_peeking_performed": False,
            "VALIDATE_AUTHORIZED": False,
            "R4_STATUS": "BLOCKED",
            "R5_STATUS": "NOT_STARTED",
        },
    }


def test_full_cycle_with_real_collect(auto_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    candles = [
        _candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC)),
        _candle(datetime(2026, 7, 18, 3, 0, tzinfo=UTC)),
    ]
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    provider = FakeProvider(candles)

    def collect_fn(**kwargs):
        return collector_mod.run_collect(
            provider_factory=lambda _n: provider,
            sleep_fn=lambda _s: None,
            **kwargs,
        )

    out = run_cycle(
        as_of=now,
        collect_fn=collect_fn,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] in {STATUS_COMPLETE, STATUS_PARTIAL, STATUS_NO_NEW_DATA}
    assert out["observations_accepted"] >= 1
    assert out["idempotency_status"] == "PASS"
    assert out["readiness_status"] in {"NOT_READY", "READY", "BLOCKED"}
    assert out["validation_command_executed"] is False
    assert (Path(out["run_dir"]) / "cycle_report.json").is_file()
    assert auto_dirs["state"].is_file()
    assert not auto_dirs["lock"].exists()


def test_cycle_no_new_data(auto_dirs):
    calls: list[bool] = []

    def collect_fn(**kwargs):
        calls.append(bool(kwargs.get("dry_run")))
        before = 20
        return _base_collect_result(
            dry_run=bool(kwargs.get("dry_run")),
            n_observations_before=before,
            n_observations_after=before,
            n_candidates=0,
            persist={"n_accepted": 0, "n_store_rejected": 0},
        )

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 20},
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] == STATUS_NO_NEW_DATA
    assert out["observations_accepted"] == 0
    assert exit_code_for_cycle_status(out["status"]) == EXIT_OK
    assert calls.count(False) >= 2  # live + idempotency


def test_partial_provider_failure(auto_dirs):
    def collect_fn(**kwargs):
        if kwargs.get("dry_run"):
            return _base_collect_result(dry_run=True, n_candidates=1)
        return _base_collect_result(
            run_status="PARTIAL",
            n_observations_before=10,
            n_observations_after=11,
            series_status=[
                {
                    "series_key": "binance|BTC/USDT|1h",
                    "status": "SUCCESS",
                    "n_accepted_candidates": 1,
                    "n_rejected": 0,
                },
                {
                    "series_key": "binance|ETH/USDT|1h",
                    "status": "PROVIDER_ERROR",
                    "n_accepted_candidates": 0,
                    "n_rejected": 0,
                },
            ],
        )

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 11},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] == STATUS_PARTIAL
    assert out["provider_failures"] == 1
    assert out["observations_accepted"] == 1


def test_retry_limit_passed_to_collect(auto_dirs):
    seen: list[int] = []

    def collect_fn(**kwargs):
        seen.append(int(kwargs["max_retries"]))
        return _base_collect_result(
            dry_run=bool(kwargs.get("dry_run")),
            n_observations_before=5,
            n_observations_after=5 if kwargs.get("dry_run") else 6,
        )

    run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 6},
        max_retries=0,
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert seen
    assert all(v == 0 for v in seen)


def test_timeout(auto_dirs):
    def collect_fn(**kwargs):
        time.sleep(0.25)
        return _base_collect_result(dry_run=bool(kwargs.get("dry_run")))

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        timeout_seconds=1,
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    # dry-run sleeps 0.25; live sleeps 0.25; then timeout before/around readiness depending on clock
    assert out["status"] in {STATUS_FAILED, STATUS_COMPLETE, STATUS_PARTIAL, STATUS_NO_NEW_DATA}
    if out["timed_out"]:
        assert out["status"] == STATUS_FAILED
        assert exit_code_for_cycle_status(out["status"]) == EXIT_FAILED


def test_timeout_forced(auto_dirs, monkeypatch):
    mono = {"t": 1000.0}

    def fake_mono():
        return mono["t"]

    monkeypatch.setattr(automation_mod.time, "monotonic", fake_mono)

    def collect_fn(**kwargs):
        mono["t"] += 50
        return _base_collect_result(dry_run=bool(kwargs.get("dry_run")))

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        timeout_seconds=10,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["timed_out"] is True
    assert out["status"] == STATUS_FAILED


def test_active_lock_skipped(auto_dirs):
    lock = AutomationLock(auto_dirs["lock"], run_id="other", ttl_seconds=600)
    ok, reason = lock.acquire()
    assert ok
    assert reason == "acquired"

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **_k: _base_collect_result(),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True},
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] == STATUS_SKIPPED_LOCKED
    assert exit_code_for_cycle_status(out["status"]) == EXIT_SKIPPED_LOCKED
    assert auto_dirs["lock"].exists()


def test_stale_lock_recovered(auto_dirs):
    stale = {
        "run_id": "stale",
        "pid": 999999,
        "acquired_at": "2020-01-01T00:00:00+00:00",
        "expires_at": "2020-01-01T01:00:00+00:00",
        "owner": "dead:999999",
    }
    auto_dirs["lock"].write_text(json.dumps(stale), encoding="utf-8")

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] in {STATUS_COMPLETE, STATUS_PARTIAL, STATUS_NO_NEW_DATA}
    assert not auto_dirs["lock"].exists()


def test_interrupt_after_collect_before_readiness(auto_dirs):
    store = {"n": 10}

    def collect_fn(**kwargs):
        dry = bool(kwargs.get("dry_run"))
        before = store["n"]
        if not dry:
            store["n"] = before + 2
        return _base_collect_result(
            dry_run=dry,
            n_observations_before=before,
            n_observations_after=store["n"] if not dry else before,
        )

    def boom_readiness(**_k):
        raise RuntimeError("simulated interrupt before readiness")

    first = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=boom_readiness,
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": store["n"]},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert first["status"] == STATUS_FAILED
    assert store["n"] == 12
    assert not auto_dirs["lock"].exists()

    second = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": store["n"]},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert second["status"] in {STATUS_COMPLETE, STATUS_NO_NEW_DATA, STATUS_PARTIAL}
    assert second["readiness_status"] == "NOT_READY"


def test_safe_rerun_and_idempotency(auto_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    candles = [_candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC))]
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    provider = FakeProvider(candles)

    def collect_fn(**kwargs):
        return collector_mod.run_collect(
            provider_factory=lambda _n: provider,
            sleep_fn=lambda _s: None,
            **kwargs,
        )

    first = run_cycle(
        as_of=now,
        collect_fn=collect_fn,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    n_after = first["store_after"]
    second = run_cycle(
        as_of=now,
        collect_fn=collect_fn,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert first["idempotency_status"] == "PASS"
    assert second["status"] == STATUS_NO_NEW_DATA
    assert second["store_after"] == n_after
    assert second["idempotency_status"] == "PASS"


def test_immutable_history_and_derivable_state(auto_dirs):
    out1 = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    path1 = Path(out1["run_dir"]) / "cycle_report.json"
    snap1 = path1.read_text(encoding="utf-8")

    out2 = run_cycle(
        as_of=datetime(2026, 7, 18, 7, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(
            dry_run=bool(kwargs.get("dry_run")),
            n_observations_before=12,
            n_observations_after=14,
        ),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 14},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert path1.read_text(encoding="utf-8") == snap1
    assert out1["run_id"] != out2["run_id"]
    state = json.loads(auto_dirs["state"].read_text(encoding="utf-8"))
    assert state["last_run_id"] == out2["run_id"]
    assert state["derived_from_run"] == out2["run_id"]
    assert state["VALIDATE_AUTHORIZED"] is False


def test_transition_not_ready_to_ready(auto_dirs):
    auto_dirs["state"].write_text(
        json.dumps({"last_readiness_status": "NOT_READY", "last_run_id": "prev"}),
        encoding="utf-8",
    )
    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report("READY", "COMPLETE"),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["readiness_status"] == "READY"
    assert out["readiness_transition"] == "NOT_READY->READY"
    assert out["HUMAN_AUTHORIZATION_REQUIRED"] is True
    assert out["VALIDATE_AUTHORIZED"] is False
    events = auto_dirs["events"].read_text(encoding="utf-8")
    assert "READINESS_BECAME_READY" in events
    assert 'VALIDATE_AUTHORIZED": false' in events or '"VALIDATE_AUTHORIZED": false' in events


def test_transition_not_ready_to_blocked(auto_dirs):
    auto_dirs["state"].write_text(
        json.dumps({"last_readiness_status": "NOT_READY"}),
        encoding="utf-8",
    )
    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report("BLOCKED", "HASH_INVALID"),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] == STATUS_BLOCKED
    assert out["readiness_transition"] == "NOT_READY->BLOCKED"
    assert exit_code_for_cycle_status(out["status"]) == EXIT_BLOCKED
    assert "READINESS_OR_CYCLE_BLOCKED" in auto_dirs["events"].read_text(encoding="utf-8")


def test_preflight_hash_blocked(auto_dirs):
    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **_k: (_ for _ in ()).throw(AssertionError("collect must not run")),
        readiness_fn=lambda **_k: _ready_report("BLOCKED", "HASH_INVALID"),
        ops_fn=lambda **_k: {"hash_integrity_ok": False, "n_observations_total": 0},
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] == STATUS_BLOCKED
    assert out["preflight"]["reason"] == "HASH_INTEGRITY_FAILED"


def test_does_not_call_validate(auto_dirs, monkeypatch):
    def boom(*_a, **_k):
        raise AssertionError("validate must not be imported/called")

    monkeypatch.setattr("wick.r3e.future_unseen.validate.run_validation", boom)
    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["validation_command_executed"] is False
    assert out["effect_peeking_performed"] is False


def test_no_forbidden_science_imports_or_keys(auto_dirs):
    path = Path(automation_mod.__file__)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    for forbidden in FORBIDDEN_AUTOMATION_IMPORTS:
        assert forbidden not in imported

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    blob = json.dumps(out).lower()
    for bad in ("delta_candle", "p_value", "fdr", "sharpe", "mean_net", "m5_minus_m4"):
        assert bad not in blob


def test_no_store_mutation_on_dry_run_only(auto_dirs, monkeypatch):
    from wick.r3d.universe import SeriesSpec

    now = datetime(2026, 7, 18, 6, 0, tzinfo=UTC)
    tiny = [SeriesSpec("binance", "BTC/USDT", "1h", fu_config.FUTURE_UNSEEN_CUTOFF, 0.1, "crypto")]
    monkeypatch.setattr(collector_mod, "UNIVERSE", tiny)
    provider = FakeProvider([_candle(datetime(2026, 7, 18, 2, 0, tzinfo=UTC))])

    def collect_fn(**kwargs):
        return collector_mod.run_collect(
            provider_factory=lambda _n: provider,
            sleep_fn=lambda _s: None,
            **kwargs,
        )

    before = list(auto_dirs["val"].glob("*.jsonl"))
    out = run_cycle(
        as_of=now,
        dry_run_only=True,
        collect_fn=collect_fn,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] == STATUS_COMPLETE
    assert list(auto_dirs["val"].glob("*.jsonl")) == before


def test_no_credentials_in_logs(auto_dirs):
    secret = "SUPER_SECRET_API_KEY_DO_NOT_LEAK"

    def collect_fn(**kwargs):
        return _base_collect_result(
            dry_run=bool(kwargs.get("dry_run")),
            provider_debug={"api_key": secret, "token": secret},
        )

    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=collect_fn,
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    report_text = (Path(out["run_dir"]) / "cycle_report.json").read_text(encoding="utf-8")
    assert secret not in report_text
    assert secret not in json.dumps(out)


def test_json_stable_and_exit_codes(auto_dirs, monkeypatch):
    monkeypatch.setattr(
        "wick.r3e.future_unseen.cli.run_cycle",
        lambda **_k: {
            "run_id": "fu_auto_test",
            "status": STATUS_NO_NEW_DATA,
            "as_of": "2026-07-18T06:00:00+00:00",
            "dry_run_candidates": 0,
            "observations_accepted": 0,
            "store_before": 10,
            "store_after": 10,
            "idempotency_status": "PASS",
            "readiness_status": "NOT_READY",
            "readiness_reason": "WINDOW_DAYS_INSUFFICIENT",
            "readiness_transition": "NONE->NOT_READY",
            "window_days": 0.7,
            "hash_status": "OK",
            "HUMAN_AUTHORIZATION_REQUIRED": False,
            "run_dir": str(auto_dirs["runs"] / "x"),
        },
    )
    runner = CliRunner()
    result = runner.invoke(app, ["run-cycle", "--json"])
    assert result.exit_code == EXIT_OK
    payload = json.loads(result.stdout)
    assert payload["status"] == STATUS_NO_NEW_DATA
    assert payload["VALIDATE_AUTHORIZED"] is False
    assert payload["validation_command_executed"] is False

    assert exit_code_for_cycle_status(STATUS_COMPLETE) == EXIT_OK
    assert exit_code_for_cycle_status(STATUS_PARTIAL) == EXIT_OK
    assert exit_code_for_cycle_status(STATUS_NO_NEW_DATA) == EXIT_OK
    assert exit_code_for_cycle_status(STATUS_FAILED) == EXIT_FAILED
    assert exit_code_for_cycle_status(STATUS_BLOCKED) == EXIT_BLOCKED
    assert exit_code_for_cycle_status(STATUS_SKIPPED_LOCKED) == EXIT_SKIPPED_LOCKED


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
        "force-validate",
        "auto-validate",
    ):
        assert bad not in src
    assert "run-cycle" in src


def test_lock_owner_fields(auto_dirs):
    lock = AutomationLock(auto_dirs["lock"], run_id="owner-check", ttl_seconds=60)
    ok, _ = lock.acquire()
    assert ok
    meta = json.loads(auto_dirs["lock"].read_text(encoding="utf-8"))
    assert meta["run_id"] == "owner-check"
    assert meta["pid"] == os.getpid()
    assert "acquired_at" in meta
    assert "expires_at" in meta
    lock.release()
    assert not auto_dirs["lock"].exists()


def test_concurrent_cycles_second_skipped(auto_dirs):
    held = AutomationLock(auto_dirs["lock"], run_id="holder", ttl_seconds=600)
    assert held.acquire()[0]
    first = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **_k: (_ for _ in ()).throw(AssertionError("must not collect under lock")),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True},
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    second = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 1, tzinfo=UTC),
        collect_fn=lambda **_k: (_ for _ in ()).throw(AssertionError("must not collect under lock")),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True},
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert first["status"] == STATUS_SKIPPED_LOCKED
    assert second["status"] == STATUS_SKIPPED_LOCKED
    assert auto_dirs["lock"].exists()
    held.release()


def test_dead_pid_stale_lock(auto_dirs):
    dead = {
        "run_id": "dead-pid",
        "pid": 2_147_483_647,
        "acquired_at": "2026-07-18T00:00:00+00:00",
        "expires_at": "2099-01-01T00:00:00+00:00",
        "owner": "dead:2147483647",
    }
    auto_dirs["lock"].write_text(json.dumps(dead), encoding="utf-8")
    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    assert out["status"] in {STATUS_COMPLETE, STATUS_PARTIAL, STATUS_NO_NEW_DATA}
    assert not auto_dirs["lock"].exists()


def test_timeout_model_documented_in_report(auto_dirs):
    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    model = out["timeout_model"]
    assert model["HARD_CANCEL_MID_FLIGHT"] is False
    assert "checkpoint" in model["TIMEOUT_LIMITATION"]
    assert model["PROVIDER_TIMEOUT"] == "delegated_to_provider_retry_layer"


def test_state_alias_failure_preserves_immutable_history(auto_dirs, monkeypatch):
    real_write = automation_mod._write_json

    def flaky_write(path, doc):
        if path.name == "automation_state.json":
            raise OSError("simulated alias failure")
        return real_write(path, doc)

    monkeypatch.setattr(automation_mod, "_write_json", flaky_write)
    out = run_cycle(
        as_of=datetime(2026, 7, 18, 6, 0, tzinfo=UTC),
        collect_fn=lambda **kwargs: _base_collect_result(dry_run=bool(kwargs.get("dry_run"))),
        readiness_fn=lambda **_k: _ready_report(),
        ops_fn=lambda **_k: {"hash_integrity_ok": True, "n_observations_total": 12},
        skip_idempotency_check=True,
        lock_path=auto_dirs["lock"],
        state_path=auto_dirs["state"],
        runs_dir=auto_dirs["runs"],
        events_path=auto_dirs["events"],
    )
    report = Path(out["run_dir"]) / "cycle_report.json"
    assert report.is_file()
    body = json.loads(report.read_text(encoding="utf-8"))
    assert body["automation_state_update_ok"] is False
    assert "simulated alias failure" in body["automation_state_update_error"]
