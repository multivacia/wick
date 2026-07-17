"""R3E experiment manifesto — freeze before outer-test evaluation completes."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.patterns.params import DEFAULT_PARAMS, DETECTOR_VERSION
from wick.r3e.config import (
    COST_MODEL_VERSION,
    EXPERIMENT_ID,
    FEATURE_SET_VERSION,
    HOLDOUT_POLICY,
    LOGISTIC_GRID,
    MODEL_VERSION,
    N_BOOTSTRAP,
    PARENT_EXPERIMENT_ID,
    RANDOM_SEED,
    RIDGE_GRID,
    SCORE_POLICIES,
)


def build_manifest(
    *,
    data_snapshot_hash: str,
    train_windows: list[dict[str, Any]],
    test_windows: list[dict[str, Any]],
    selected_hyperparameters: dict[str, Any],
    score_policy: dict[str, str],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "experiment_id": EXPERIMENT_ID,
        "parent_experiment_id": PARENT_EXPERIMENT_ID,
        "model_version": MODEL_VERSION,
        "feature_set_version": FEATURE_SET_VERSION,
        "cost_model_version": COST_MODEL_VERSION,
        "detector_version": DETECTOR_VERSION,
        "parameters_hash": DEFAULT_PARAMS.parameters_hash(),
        "data_snapshot_hash": data_snapshot_hash,
        "train_windows": train_windows,
        "test_windows": test_windows,
        "random_seed": RANDOM_SEED,
        "n_bootstrap": N_BOOTSTRAP,
        "hyperparameter_grid": {"logistic": LOGISTIC_GRID, "ridge": RIDGE_GRID},
        "selected_hyperparameters": selected_hyperparameters,
        "score_policy": score_policy,
        "score_policies_allowed": list(SCORE_POLICIES),
        "holdout_policy": HOLDOUT_POLICY,
        "created_at": datetime.now(UTC).isoformat(),
        "frozen_at": None,
        "r3d_holdout_reuse": False,
        "notes": [
            "R3D holdout excluded from R3E development and must not be reused as final validation.",
            "Grid and score policies frozen; do not widen after results.",
            "R3E_GATE maximum = PENDING_FUTURE_UNSEEN_DATA.",
        ],
    }
    if extra:
        payload.update(extra)
    return payload


def freeze_manifest(path: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    path = Path(path)
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing.get("frozen_at"):
            raise RuntimeError("Manifest already frozen — refusing to mutate")
    manifest = dict(manifest)
    if manifest.get("frozen_at"):
        raise RuntimeError("Manifest already frozen — refusing to mutate")
    manifest["frozen_at"] = datetime.now(UTC).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, default=str) + "\n", encoding="utf-8")
    return manifest
