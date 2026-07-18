"""Tests for R3E future-unseen validation infrastructure."""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from wick.r3e.future_unseen import config as fu_config
from wick.r3e.future_unseen.freeze import assert_freeze_matches_repo, build_model_freeze
from wick.r3e.future_unseen.gate import decide_gate
from wick.r3e.future_unseen.hashing import sha256_file, sha256_json
from wick.r3e.future_unseen.ingest import ingest_batch, write_cutoff_manifest
from wick.r3e.future_unseen.ops_report import FORBIDDEN_OPS_KEYS, build_ops_report
from wick.r3e.future_unseen.protections import (
    FutureUnseenProtectionError,
    assert_economic_interpretation_locked,
    assert_no_forbidden_path,
    assert_r4_not_opened,
    assert_strictly_after_cutoff,
)


@pytest.fixture()
def fu_dirs(tmp_path, monkeypatch):
    raw = tmp_path / "raw"
    val = tmp_path / "validated"
    man = tmp_path / "manifests"
    reports = tmp_path / "reports"
    for d in (raw, val, man, reports):
        d.mkdir()
    monkeypatch.setattr("wick.r3e.future_unseen.paths.RAW_DIR", raw)
    monkeypatch.setattr("wick.r3e.future_unseen.paths.VALIDATED_DIR", val)
    monkeypatch.setattr("wick.r3e.future_unseen.paths.MANIFESTS_DIR", man)
    monkeypatch.setattr("wick.r3e.future_unseen.paths.REPORTS_DIR", reports)
    monkeypatch.setattr("wick.r3e.future_unseen.paths.FREEZE_PATH", man / "model_freeze.json")
    monkeypatch.setattr(
        "wick.r3e.future_unseen.paths.CUTOFF_MANIFEST_PATH", man / "cutoff_manifest.json"
    )
    # Also patch modules that imported paths at function-level via package attrs
    import wick.r3e.future_unseen.freeze as freeze_mod
    import wick.r3e.future_unseen.ingest as ingest_mod
    import wick.r3e.future_unseen.ops_report as ops_mod

    monkeypatch.setattr(ingest_mod, "RAW_DIR", raw)
    monkeypatch.setattr(ingest_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(ingest_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(ops_mod, "VALIDATED_DIR", val)
    monkeypatch.setattr(ops_mod, "MANIFESTS_DIR", man)
    monkeypatch.setattr(ops_mod, "REPORTS_DIR", reports)
    monkeypatch.setattr(freeze_mod, "FREEZE_PATH", man / "model_freeze.json")
    return tmp_path


def _bar(ts: datetime, price: float = 100.0) -> dict:
    return {
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "source": "binance",
        "market_ts": ts.isoformat(),
        "open": price,
        "high": price * 1.01,
        "low": price * 0.99,
        "close": price * 1.001,
        "volume": 1000.0,
        "revision": 1,
    }


def test_reject_before_or_equal_cutoff():
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    with pytest.raises(FutureUnseenProtectionError):
        assert_strictly_after_cutoff(cut)
    with pytest.raises(FutureUnseenProtectionError):
        assert_strictly_after_cutoff(cut - timedelta(seconds=1))


def test_accept_after_cutoff():
    dt = assert_strictly_after_cutoff(fu_config.FUTURE_UNSEEN_CUTOFF + timedelta(hours=1))
    assert dt > fu_config.FUTURE_UNSEEN_CUTOFF


def test_ingest_rejects_pre_cutoff_and_accepts_post(fu_dirs):
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    recs = [
        _bar(cut - timedelta(hours=1)),
        _bar(cut),
        _bar(cut + timedelta(hours=1), 101.0),
        _bar(cut + timedelta(hours=2), 102.0),
    ]
    result = ingest_batch(recs, origin="unit-test")
    assert result.accepted == 2
    assert result.rejected == 2
    assert result.file_sha256
    assert Path(result.validated_path).is_file()


def test_duplicate_rejection(fu_dirs):
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    r = _bar(cut + timedelta(hours=3), 103.0)
    a = ingest_batch([r], origin="unit-test")
    assert a.accepted == 1
    b = ingest_batch([r], origin="unit-test")
    assert b.accepted == 0
    assert any("duplicate" in x.reason for x in b.rejections)


def test_silent_update_forbidden_requires_revision(fu_dirs):
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    r = _bar(cut + timedelta(hours=4), 104.0)
    ingest_batch([r], origin="unit-test")
    r2 = dict(r)
    r2["close"] = 105.0
    r2["revision"] = 1  # not incremented
    out = ingest_batch([r2], origin="unit-test")
    assert out.accepted == 0
    r2["revision"] = 2
    out2 = ingest_batch([r2], origin="unit-test")
    assert out2.accepted == 1


def test_forbidden_path_and_dataset_mix():
    with pytest.raises(FutureUnseenProtectionError):
        assert_no_forbidden_path("reports/r3e_real/executive_report.json")
    with pytest.raises(FutureUnseenProtectionError):
        assert_no_forbidden_path("/tmp/foo/reports/r3d/x.json")


def test_ops_report_has_no_effect_keys(fu_dirs):
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    ingest_batch([_bar(cut + timedelta(hours=5))], origin="unit-test")
    report = build_ops_report()
    assert report["effect_metrics_disclosed"] is False
    assert report["gate_preview_disclosed"] is False
    blob_keys = json.dumps(report)
    for k in FORBIDDEN_OPS_KEYS:
        assert f'"{k}"' not in blob_keys


def test_hash_tamper_detected(fu_dirs):
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    result = ingest_batch([_bar(cut + timedelta(hours=6))], origin="unit-test")
    path = Path(result.validated_path)
    path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    report = build_ops_report()
    assert report["hash_integrity_ok"] is False


def test_cutoff_manifest_immutable(fu_dirs):
    p1 = write_cutoff_manifest(commit="abc")
    p2 = write_cutoff_manifest(commit="def")
    assert p1 == p2
    data = json.loads(p1.read_text(encoding="utf-8"))
    assert data["FUTURE_UNSEEN_CUTOFF"] == fu_config.FUTURE_UNSEEN_CUTOFF_ISO


def test_gate_approved_rejected_inconclusive():
    base = dict(
        n_oos_primary=150,
        collection_complete=True,
        integrity_ok=True,
        protocol_ok=True,
        audit_findings_critical=False,
        commit="c0",
        freeze_sha256="f0",
        data_hash="d0",
    )
    approved = decide_gate(
        primary_delta={
            "delta": 0.01,
            "ci_low": 0.002,
            "ci_high": 0.02,
            "p_adj": 0.01,
            "effect_size": 0.5,
            "mean_left": 0.005,
        },
        **base,
    )
    assert approved["decision"] == "APPROVED"
    assert approved["ECONOMIC_INTERPRETATION_ALLOWED"] is True

    rejected = decide_gate(
        primary_delta={
            "delta": -0.01,
            "ci_low": -0.02,
            "ci_high": -0.002,
            "p_adj": 0.01,
            "effect_size": -0.5,
            "mean_left": -0.005,
        },
        **base,
    )
    assert rejected["decision"] == "REJECTED"
    assert rejected["R4_STATUS"] == "BLOCKED"
    assert rejected["ECONOMIC_INTERPRETATION_ALLOWED"] is False

    incon = decide_gate(
        primary_delta={
            "delta": 0.001,
            "ci_low": -0.01,
            "ci_high": 0.01,
            "p_adj": 0.4,
            "effect_size": 0.05,
            "mean_left": 0.001,
        },
        **base,
    )
    assert incon["decision"] == "INCONCLUSIVE"
    assert incon["R4_STATUS"] == "BLOCKED"


def test_gate_insufficient_sample_inconclusive():
    out = decide_gate(
        primary_delta={
            "delta": 0.01,
            "ci_low": 0.01,
            "ci_high": 0.02,
            "p_adj": 0.01,
            "mean_left": 0.01,
            "effect_size": 1.0,
        },
        n_oos_primary=10,
        collection_complete=True,
        integrity_ok=True,
        protocol_ok=True,
        audit_findings_critical=False,
        commit="c0",
        freeze_sha256="f0",
        data_hash="d0",
    )
    assert out["decision"] == "INCONCLUSIVE"


def test_r4_blocked_without_full_approval():
    with pytest.raises(FutureUnseenProtectionError):
        assert_r4_not_opened(gate="REJECTED", economic_ok=False, audit="APPROVED")
    with pytest.raises(FutureUnseenProtectionError):
        assert_r4_not_opened(gate="APPROVED", economic_ok=False, audit="APPROVED")
    # full approval path does not raise
    assert_r4_not_opened(gate="APPROVED", economic_ok=True, audit="APPROVED")


def test_economic_locked_before_final():
    with pytest.raises(FutureUnseenProtectionError):
        assert_economic_interpretation_locked(True, final_decision_made=False)


def test_protocol_freeze_and_tamper(fu_dirs, monkeypatch):
    write_cutoff_manifest()
    freeze = build_model_freeze(force=True)
    assert freeze["frozen"] is True
    assert_freeze_matches_repo()
    # tamper freeze protocol
    path = fu_dirs / "manifests" / "model_freeze.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["protocol"]["random_seed"] = 999
    path.write_text(json.dumps(data) + "\n", encoding="utf-8")
    with pytest.raises(FutureUnseenProtectionError):
        assert_freeze_matches_repo()


def test_reproducibility_seed_constant():
    assert fu_config.RANDOM_SEED == 42
    assert fu_config.N_BOOTSTRAP == 1000
    a = sha256_json({"seed": 42, "x": [1, 2, 3]})
    b = sha256_json({"seed": 42, "x": [1, 2, 3]})
    assert a == b


def test_manifest_hash_stable(fu_dirs):
    cut = fu_config.FUTURE_UNSEEN_CUTOFF
    r = ingest_batch([_bar(cut + timedelta(hours=7))], origin="unit-test")
    h1 = sha256_file(Path(r.validated_path))
    h2 = sha256_file(Path(r.validated_path))
    assert h1 == h2 == r.file_sha256


def test_collection_not_started_state(fu_dirs):
    report = build_ops_report()
    assert report["collection_status"] == "NOT_STARTED"


def test_initialize_collection_idempotent_sets_in_progress(fu_dirs, monkeypatch):
    import wick.r3e.future_unseen.initialization as init_mod

    monkeypatch.setattr(init_mod, "MANIFESTS_DIR", fu_dirs / "manifests")
    monkeypatch.setattr(init_mod, "REPORTS_DIR", fu_dirs / "reports")
    (fu_dirs / "reports").mkdir(exist_ok=True)
    a = init_mod.initialize_collection()
    b = init_mod.initialize_collection()
    assert a["collection_state"]["R3E_FUTURE_DATA_COLLECTION"] == "IN_PROGRESS"
    assert b["collection_state"]["R3E_FUTURE_DATA_COLLECTION"] == "IN_PROGRESS"
    assert a["collection_state"]["ECONOMIC_INTERPRETATION_ALLOWED"] is False
    assert a["collection_state"]["R4_STATUS"] == "BLOCKED"
    assert a["collection_state"]["validation_command_executed"] is False
    assert (fu_dirs / "manifests" / "initialization_manifest.json").exists()
    # cutoff not rewritten to a different value
    cut = json.loads((fu_dirs / "manifests" / "cutoff_manifest.json").read_text())
    assert cut["FUTURE_UNSEEN_CUTOFF"] == fu_config.FUTURE_UNSEEN_CUTOFF_ISO


def test_validate_not_ready_without_collection(fu_dirs, monkeypatch, tmp_path):
    """validate must not approve with empty/incomplete future data."""
    import wick.r3e.future_unseen.initialization as init_mod
    import wick.r3e.future_unseen.validate as val_mod

    monkeypatch.setattr(init_mod, "MANIFESTS_DIR", fu_dirs / "manifests")
    monkeypatch.setattr(init_mod, "REPORTS_DIR", fu_dirs / "reports")
    monkeypatch.setattr(val_mod, "REPORTS_DIR", fu_dirs / "reports")
    (fu_dirs / "reports").mkdir(exist_ok=True)
    init_mod.initialize_collection()
    out = val_mod.run_validation(out_dir=fu_dirs / "reports", force_evaluate=False)
    assert out["gate"]["R3E_GATE"] == "PENDING_FUTURE_UNSEEN_DATA"
    assert out["gate"]["ECONOMIC_INTERPRETATION_ALLOWED"] is False
    assert out["gate"]["R4_STATUS"] == "BLOCKED"
    assert (
        out["gate"]["decision"] in {"NOT_READY", "INCONCLUSIVE", "PENDING_FUTURE_UNSEEN_DATA"}
        or out["gate"].get("final_decision") is False
    )
