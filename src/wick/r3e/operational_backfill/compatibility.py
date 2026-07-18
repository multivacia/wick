"""Schema compatibility vs future-unseen ingest contract (no official writes)."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.config import FUTURE_UNSEEN_CUTOFF_ISO
from wick.r3e.future_unseen.hashing import sha256_json
from wick.r3e.operational_backfill.config import CLASSIFICATION, EXPERIMENT_ID
from wick.r3e.operational_backfill.paths import REPORTS_DIR
from wick.r3e.operational_backfill.schema import (
    REQUIRED_FIELDS,
    is_structurally_compatible_with_future_unseen,
)
from wick.r3e.operational_backfill.store import load_all_validated


def build_schema_compatibility_report(
    *,
    output: Path | str | None = None,
    sample_size: int = 5,
) -> dict[str, Any]:
    records = load_all_validated(output)
    sample = records[:sample_size]
    structural_ok = (
        all(is_structurally_compatible_with_future_unseen(r) for r in sample) if sample else False
    )

    # Temporal eligibility for future-unseen is always false for this sandbox window.
    temporally_eligible = False
    if sample:
        from wick.r3e.future_unseen.protections import assert_strictly_after_cutoff

        for r in sample:
            try:
                assert_strictly_after_cutoff(r["market_ts"])
                temporally_eligible = True
                break
            except Exception:
                continue

    report = {
        "experiment_id": EXPERIMENT_ID,
        "classification": CLASSIFICATION,
        "required_fields": list(REQUIRED_FIELDS) + ["revision"],
        "sample_size": len(sample),
        "STRUCTURAL_SCHEMA_COMPATIBLE": bool(structural_ok and sample),
        "FUTURE_UNSEEN_TEMPORALLY_ELIGIBLE": temporally_eligible,
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "note": (
            "Structural compatibility means a record could be submitted to ingest-json "
            "schema validation; historical timestamps remain ineligible for the official gate."
        ),
        "sample_market_ts": [r.get("market_ts") for r in sample],
        "official_dirs_written": False,
    }
    report["sha256"] = sha256_json(report)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORTS_DIR / "schema_compatibility.json"
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def run_official_reject_probe(
    *,
    output: Path | str | None = None,
    sample_size: int = 3,
) -> dict[str, Any]:
    """Attempt official ingest-json against a temp future_unseen tree; expect full reject."""
    from wick.r3e.future_unseen import ingest as ingest_mod
    from wick.r3e.future_unseen import ops_report as ops_mod
    from wick.r3e.future_unseen import paths as paths_mod

    records = load_all_validated(output)[:sample_size]
    if not records:
        return {
            "OFFICIAL_FUTURE_INGEST_REJECTED_HISTORICAL_DATA": True,
            "OFFICIAL_COLLECTION_STATE_UNCHANGED": True,
            "note": "no validated backfill records available for probe",
            "accepted": 0,
            "rejected": 0,
            "sample_size": 0,
        }

    with tempfile.TemporaryDirectory(prefix="fu_probe_") as tmp:
        tmp_path = Path(tmp)
        raw = tmp_path / "raw"
        val = tmp_path / "validated"
        man = tmp_path / "manifests"
        reports = tmp_path / "reports"
        for d in (raw, val, man, reports):
            d.mkdir()

        # Patch official module paths to temp (never touch persistent official dirs).
        originals = {
            "paths.RAW": paths_mod.RAW_DIR,
            "paths.VAL": paths_mod.VALIDATED_DIR,
            "paths.MAN": paths_mod.MANIFESTS_DIR,
            "paths.REP": paths_mod.REPORTS_DIR,
            "ingest.RAW": ingest_mod.RAW_DIR,
            "ingest.VAL": ingest_mod.VALIDATED_DIR,
            "ingest.MAN": ingest_mod.MANIFESTS_DIR,
            "ops.VAL": ops_mod.VALIDATED_DIR,
            "ops.MAN": ops_mod.MANIFESTS_DIR,
            "ops.REP": ops_mod.REPORTS_DIR,
        }
        paths_mod.RAW_DIR = raw
        paths_mod.VALIDATED_DIR = val
        paths_mod.MANIFESTS_DIR = man
        paths_mod.REPORTS_DIR = reports
        ingest_mod.RAW_DIR = raw
        ingest_mod.VALIDATED_DIR = val
        ingest_mod.MANIFESTS_DIR = man
        ops_mod.VALIDATED_DIR = val
        ops_mod.MANIFESTS_DIR = man
        ops_mod.REPORTS_DIR = reports
        try:
            result = ingest_mod.ingest_batch(
                records,
                origin="operational-backfill-negative-probe",
            )
            rejected_all = result.accepted == 0 and result.rejected == len(records)
            reasons = [r.reason for r in result.rejections]
            cutoff_reasons = all(
                "not strictly after cutoff" in r or "cutoff" in r.lower() for r in reasons
            )
        finally:
            paths_mod.RAW_DIR = originals["paths.RAW"]
            paths_mod.VALIDATED_DIR = originals["paths.VAL"]
            paths_mod.MANIFESTS_DIR = originals["paths.MAN"]
            paths_mod.REPORTS_DIR = originals["paths.REP"]
            ingest_mod.RAW_DIR = originals["ingest.RAW"]
            ingest_mod.VALIDATED_DIR = originals["ingest.VAL"]
            ingest_mod.MANIFESTS_DIR = originals["ingest.MAN"]
            ops_mod.VALIDATED_DIR = originals["ops.VAL"]
            ops_mod.MANIFESTS_DIR = originals["ops.MAN"]
            ops_mod.REPORTS_DIR = originals["ops.REP"]

    report = {
        "OFFICIAL_FUTURE_INGEST_REJECTED_HISTORICAL_DATA": bool(rejected_all and cutoff_reasons),
        "sample_size": len(records),
        "accepted": result.accepted,
        "rejected": result.rejected,
        "rejection_reasons": reasons,
        "temp_dirs_only": True,
        "persistent_official_dirs_used": False,
        "classification": CLASSIFICATION,
    }
    report["sha256"] = sha256_json(report)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "official_reject_probe.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return report
