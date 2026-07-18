"""Isolated paths for operational historical backfill (never future_unseen)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]

DEFAULT_OUTPUT_ROOT = REPO_ROOT / "data" / "operational_backfill" / "r3e_90d"
REPORTS_DIR = REPO_ROOT / "reports" / "r3e_operational_backfill"

# Official future-unseen roots — read-only for isolation proofs; never write here.
OFFICIAL_FU_ROOT = REPO_ROOT / "data" / "future_unseen"
OFFICIAL_FU_RAW = OFFICIAL_FU_ROOT / "raw"
OFFICIAL_FU_VALIDATED = OFFICIAL_FU_ROOT / "validated"
OFFICIAL_FU_MANIFESTS = OFFICIAL_FU_ROOT / "manifests"
OFFICIAL_FU_REPORTS = REPO_ROOT / "reports" / "r3e_future_unseen"
OFFICIAL_COLLECTION_STATE = OFFICIAL_FU_MANIFESTS / "collection_state.json"
OFFICIAL_CUTOFF_MANIFEST = OFFICIAL_FU_MANIFESTS / "cutoff_manifest.json"
OFFICIAL_MODEL_FREEZE = OFFICIAL_FU_MANIFESTS / "model_freeze.json"
OFFICIAL_OPS_REPORT = OFFICIAL_FU_REPORTS / "ops_collection_report.json"


def resolve_roots(output: Path | str | None = None) -> dict[str, Path]:
    root = Path(output) if output else DEFAULT_OUTPUT_ROOT
    return {
        "root": root,
        "raw": root / "raw",
        "validated": root / "validated",
        "manifests": root / "manifests",
    }


def ensure_dirs(output: Path | str | None = None) -> dict[str, Path]:
    roots = resolve_roots(output)
    for key in ("root", "raw", "validated", "manifests"):
        roots[key].mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    return roots


def assert_not_official_path(path: Path | str) -> None:
    text = str(path).replace("\\", "/")
    forbidden = (
        "data/future_unseen/raw",
        "data/future_unseen/validated",
        "data/future_unseen/manifests",
    )
    for root in forbidden:
        if root in text:
            raise RuntimeError(f"operational backfill must not write under {root}: {text}")
