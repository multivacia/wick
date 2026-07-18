"""Formal initialization of future-unseen collection (no effect evaluation)."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick import __version__ as ENGINE_VERSION
from wick.r3e.future_unseen.config import (
    EXPERIMENT_ID,
    FUTURE_UNSEEN_CUTOFF_ISO,
    STATUS_COLLECTION_IN_PROGRESS,
)
from wick.r3e.future_unseen.freeze import assert_freeze_matches_repo, build_model_freeze
from wick.r3e.future_unseen.hashing import sha256_file, sha256_json
from wick.r3e.future_unseen.ingest import write_cutoff_manifest
from wick.r3e.future_unseen.ops_report import build_ops_report
from wick.r3e.future_unseen.paths import (
    MANIFESTS_DIR,
    REPO_ROOT,
    REPORTS_DIR,
    SPEC_PATH,
    ensure_dirs,
)
from wick.r3e.future_unseen.protections import FutureUnseenProtectionError


def _git_commit() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "UNKNOWN"


def initialize_collection(*, force_restart_marker: bool = False) -> dict[str, Any]:
    """Idempotent formal start of future-unseen collection.

    - Creates directories if needed
    - Preserves existing cutoff / freeze manifests (no overwrite of cutoff)
    - Does not ingest data
    - Does not run validate
    - Sets R3E_FUTURE_DATA_COLLECTION = IN_PROGRESS
    """
    ensure_dirs()
    commit = _git_commit()
    cutoff_path = write_cutoff_manifest(commit=commit)
    freeze = build_model_freeze(force=False)
    freeze = assert_freeze_matches_repo()

    # Confirm cutoff consistency
    cutoff_doc = json.loads(Path(cutoff_path).read_text(encoding="utf-8"))
    if cutoff_doc.get("FUTURE_UNSEEN_CUTOFF") != FUTURE_UNSEEN_CUTOFF_ISO:
        raise FutureUnseenProtectionError("cutoff mismatch during initialization")
    if freeze.get("cutoff") != FUTURE_UNSEEN_CUTOFF_ISO:
        raise FutureUnseenProtectionError("freeze cutoff mismatch during initialization")

    now = datetime.now(UTC).isoformat()
    state = {
        "R3E_FUTURE_VALIDATION_ENGINE": "COMPLETE",
        "R3E_FUTURE_VALIDATION_AUDIT": "COMPLETE",
        "R3E_FUTURE_DATA_COLLECTION": STATUS_COLLECTION_IN_PROGRESS,
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "ECONOMIC_INTERPRETATION_ALLOWED": False,
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "engine_version": ENGINE_VERSION,
        "commit": commit,
        "updated_at": now,
        "validation_command_executed": False,
        "effect_peeking_performed": False,
        "initialization": "FORMAL_START",
    }
    state_path = MANIFESTS_DIR / "collection_state.json"
    state_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    init_manifest = {
        "kind": "FUTURE_UNSEEN_INITIALIZATION",
        "experiment_id": EXPERIMENT_ID,
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "commit": commit,
        "engine_version": ENGINE_VERSION,
        "created_at": now,
        "idempotent": True,
        "force_restart_marker": force_restart_marker,
        "actions": {
            "directories_ensured": True,
            "cutoff_preserved": True,
            "freeze_preserved_or_created": True,
            "data_ingested": False,
            "validate_executed": False,
            "effect_metrics_computed": False,
        },
        "artifacts": {
            "cutoff_manifest": str(cutoff_path),
            "cutoff_sha256": cutoff_doc.get("sha256"),
            "model_freeze": str(MANIFESTS_DIR / "model_freeze.json"),
            "freeze_sha256": freeze.get("freeze_sha256"),
            "config_sha256": sha256_file(REPO_ROOT / "src/wick/r3e/future_unseen/config.py"),
            "spec_sha256": sha256_file(SPEC_PATH),
            "collection_state": str(state_path),
        },
        "official_state": {
            "R3E_FUTURE_VALIDATION_ENGINE": "COMPLETE",
            "R3E_FUTURE_VALIDATION_AUDIT": "COMPLETE",
            "R3E_FUTURE_DATA_COLLECTION": STATUS_COLLECTION_IN_PROGRESS,
            "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
            "ECONOMIC_INTERPRETATION_ALLOWED": False,
            "R4_STATUS": "BLOCKED",
            "R5_STATUS": "NOT_STARTED",
        },
    }
    init_manifest["sha256"] = sha256_json(init_manifest)
    init_path = MANIFESTS_DIR / "initialization_manifest.json"
    # Idempotent: rewrite initialization manifest with updated timestamps/commit is allowed
    # (does not mutate cutoff or protocol freeze content).
    init_path.write_text(json.dumps(init_manifest, indent=2) + "\n", encoding="utf-8")

    ops = build_ops_report(out_path=REPORTS_DIR / "ops_collection_report.json")
    # Ops report computes collection_status from data volume; overlay formal IN_PROGRESS
    # in a companion field without inventing effect metrics.
    ops_overlay = {
        **ops,
        "formal_collection_state": STATUS_COLLECTION_IN_PROGRESS,
        "note": (
            "Operational completeness may remain NOT_STARTED/IN_PROGRESS based on "
            "observations; formal collection lifecycle is IN_PROGRESS after init."
        ),
        "validation_status": "NOT_RUN",
        "effect_evaluation_status": "NOT_EVALUATED",
    }
    (REPORTS_DIR / "ops_collection_report.json").write_text(
        json.dumps(ops_overlay, indent=2) + "\n", encoding="utf-8"
    )

    return {
        "initialization_manifest": init_manifest,
        "collection_state": state,
        "ops": {
            "n_observations_total": ops["n_observations_total"],
            "collection_status_data_driven": ops["collection_status"],
            "formal_collection_state": STATUS_COLLECTION_IN_PROGRESS,
            "hash_integrity_ok": ops["hash_integrity_ok"],
            "series_missing_n": len(ops["series_missing"]),
            "effect_metrics_disclosed": ops["effect_metrics_disclosed"],
            "validation_status": "NOT_RUN",
        },
        "freeze_sha256": freeze["freeze_sha256"],
        "commit": commit,
    }
