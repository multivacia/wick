"""Freeze M4/M5 protocol artifacts before future-unseen evaluation."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from typing import Any

from wick.r3e import config as r3e_config
from wick.r3e.future_unseen.config import (
    EXPERIMENT_ID,
    FUTURE_UNSEEN_CUTOFF_ISO,
    PROTOCOL_REF,
)
from wick.r3e.future_unseen.hashing import sha256_file, sha256_json
from wick.r3e.future_unseen.paths import FREEZE_PATH, REPO_ROOT, ensure_dirs
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


def _module_hash(rel: str) -> dict[str, str]:
    path = REPO_ROOT / rel
    return {"path": rel, "sha256": sha256_file(path)}


def build_model_freeze(*, force: bool = False) -> dict[str, Any]:
    """Record exact M4/M5 protocol artifacts. Immutable once written (unless force)."""
    ensure_dirs()
    if FREEZE_PATH.exists() and not force:
        existing = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
        if existing.get("frozen"):
            return existing

    artifacts = [
        _module_hash("src/wick/r3e/config.py"),
        _module_hash("src/wick/r3e/models.py"),
        _module_hash("src/wick/r3e/preprocess.py"),
        _module_hash("src/wick/r3e/scoring.py"),
        _module_hash("src/wick/r3e/compare.py"),
        _module_hash("src/wick/r3e/pipeline.py"),
        _module_hash("src/wick/r3e/future_unseen/config.py"),
        _module_hash("docs/specs/R3E_FUTURE_UNSEEN_VALIDATION_SPEC.md"),
    ]
    payload = {
        "experiment_id": EXPERIMENT_ID,
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "commit": _git_commit(),
        "frozen_at": datetime.now(UTC).isoformat(),
        "frozen": True,
        "models": {
            "M4": {
                "features": list(r3e_config.FEATURE_SETS["M4"]),
                "role": "context_only",
            },
            "M5": {
                "features": list(r3e_config.FEATURE_SETS["M5"]),
                "role": "context_plus_candle",
            },
        },
        "protocol": PROTOCOL_REF,
        "preprocessing": {
            "fit_on_train_only": True,
            "unknown_category_explicit": True,
            "impute_train_statistics_only": True,
        },
        "walk_forward": {
            "nested_expanding": True,
            "hyperparams_inner_only": True,
            "defined_before_unblinding": True,
            "uses_only_information_available_at_time_t": True,
        },
        "artifacts": artifacts,
        "tuning_after_cutoff_forbidden": True,
    }
    payload["freeze_sha256"] = sha256_json(payload)
    FREEZE_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def load_model_freeze() -> dict[str, Any]:
    if not FREEZE_PATH.exists():
        raise FutureUnseenProtectionError("model freeze missing; run freeze before validate")
    return json.loads(FREEZE_PATH.read_text(encoding="utf-8"))


def assert_freeze_matches_repo() -> dict[str, Any]:
    freeze = load_model_freeze()
    for art in freeze.get("artifacts", []):
        path = REPO_ROOT / art["path"]
        if not path.is_file():
            raise FutureUnseenProtectionError(f"frozen artifact missing: {art['path']}")
        actual = sha256_file(path)
        if actual != art["sha256"]:
            raise FutureUnseenProtectionError(
                f"protocol altered after freeze: {art['path']} hash mismatch"
            )
    # Protocol dict must still match live PROTOCOL_REF
    if freeze.get("protocol") != PROTOCOL_REF:
        raise FutureUnseenProtectionError("PROTOCOL_REF drifted versus freeze record")
    return freeze
