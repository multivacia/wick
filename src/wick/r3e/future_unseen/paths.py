"""Isolated filesystem roots for future-unseen data."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

RAW_DIR = REPO_ROOT / "data" / "future_unseen" / "raw"
VALIDATED_DIR = REPO_ROOT / "data" / "future_unseen" / "validated"
MANIFESTS_DIR = REPO_ROOT / "data" / "future_unseen" / "manifests"
REPORTS_DIR = REPO_ROOT / "reports" / "r3e_future_unseen"
SPEC_PATH = REPO_ROOT / "docs" / "specs" / "R3E_FUTURE_UNSEEN_VALIDATION_SPEC.md"
FREEZE_PATH = MANIFESTS_DIR / "model_freeze.json"
CUTOFF_MANIFEST_PATH = MANIFESTS_DIR / "cutoff_manifest.json"
COLLECTION_STATE_PATH = MANIFESTS_DIR / "collection_state.json"


def ensure_dirs() -> None:
    for d in (RAW_DIR, VALIDATED_DIR, MANIFESTS_DIR, REPORTS_DIR):
        d.mkdir(parents=True, exist_ok=True)
