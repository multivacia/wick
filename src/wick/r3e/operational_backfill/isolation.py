"""Snapshot and compare official future-unseen protected state."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.hashing import sha256_file, sha256_json
from wick.r3e.operational_backfill.paths import (
    OFFICIAL_COLLECTION_STATE,
    OFFICIAL_CUTOFF_MANIFEST,
    OFFICIAL_FU_RAW,
    OFFICIAL_FU_VALIDATED,
    OFFICIAL_MODEL_FREEZE,
    OFFICIAL_OPS_REPORT,
)


def _safe_hash(path: Path) -> str | None:
    if not path.is_file():
        return None
    return sha256_file(path)


def _safe_json(path: Path) -> Any:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _list_data_files(root: Path) -> list[str]:
    if not root.is_dir():
        return []
    return sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file())


def snapshot_official_state() -> dict[str, Any]:
    state = _safe_json(OFFICIAL_COLLECTION_STATE) or {}
    ops = _safe_json(OFFICIAL_OPS_REPORT) or {}
    snap = {
        "cutoff_manifest_sha256": _safe_hash(OFFICIAL_CUTOFF_MANIFEST),
        "model_freeze_sha256": _safe_hash(OFFICIAL_MODEL_FREEZE),
        "collection_state_sha256": _safe_hash(OFFICIAL_COLLECTION_STATE),
        "collection_state": state,
        "n_observations": ops.get("n_observations_total"),
        "series_present": ops.get("series_received"),
        "series_missing": ops.get("series_missing"),
        "formal_collection_state": ops.get("formal_collection_state")
        or state.get("R3E_FUTURE_DATA_COLLECTION"),
        "R3E_GATE": state.get("R3E_GATE"),
        "R4_STATUS": state.get("R4_STATUS"),
        "ECONOMIC_INTERPRETATION_ALLOWED": state.get("ECONOMIC_INTERPRETATION_ALLOWED"),
        "validation_command_executed": state.get("validation_command_executed"),
        "effect_peeking_performed": state.get("effect_peeking_performed"),
        "ops_report_sha256": _safe_hash(OFFICIAL_OPS_REPORT),
        "official_raw_files": _list_data_files(OFFICIAL_FU_RAW),
        "official_validated_files": _list_data_files(OFFICIAL_FU_VALIDATED),
    }
    snap["snapshot_sha256"] = sha256_json(
        {k: v for k, v in snap.items() if k != "collection_state"}
    )
    return snap


def compare_snapshots(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    protected_keys = (
        "cutoff_manifest_sha256",
        "model_freeze_sha256",
        "collection_state_sha256",
        "n_observations",
        "series_present",
        "series_missing",
        "formal_collection_state",
        "R3E_GATE",
        "R4_STATUS",
        "ECONOMIC_INTERPRETATION_ALLOWED",
        "validation_command_executed",
        "effect_peeking_performed",
        "official_raw_files",
        "official_validated_files",
    )
    diffs: dict[str, Any] = {}
    for key in protected_keys:
        if before.get(key) != after.get(key):
            diffs[key] = {"before": before.get(key), "after": after.get(key)}
    return {
        "OFFICIAL_COLLECTION_STATE_UNCHANGED": len(diffs) == 0,
        "differences": diffs,
        "before_snapshot_sha256": before.get("snapshot_sha256"),
        "after_snapshot_sha256": after.get("snapshot_sha256"),
    }
