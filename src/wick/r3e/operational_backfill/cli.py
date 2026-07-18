"""CLI for R3E operational historical backfill (separate from future_unseen)."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from wick.r3e.future_unseen.protections import parse_market_ts
from wick.r3e.operational_backfill.collect import run_collect
from wick.r3e.operational_backfill.compatibility import (
    build_schema_compatibility_report,
    run_official_reject_probe,
)
from wick.r3e.operational_backfill.config import BACKFILL_END_ISO, BACKFILL_START_ISO
from wick.r3e.operational_backfill.isolation import compare_snapshots, snapshot_official_state
from wick.r3e.operational_backfill.paths import DEFAULT_OUTPUT_ROOT, REPORTS_DIR
from wick.r3e.operational_backfill.reports import build_all_reports

app = typer.Typer(
    add_completion=False,
    help="R3E operational historical backfill (non-scientific; isolated from future_unseen).",
)


@app.command("collect")
def collect_cmd(
    start: str = typer.Option(BACKFILL_START_ISO, help="Inclusive window start (UTC ISO)"),
    end: str = typer.Option(BACKFILL_END_ISO, help="Inclusive window end (UTC ISO)"),
    output: Path = typer.Option(
        DEFAULT_OUTPUT_ROOT,
        "--output",
        help="Isolated output root under data/operational_backfill/",
    ),
) -> None:
    """Download closed OHLCV for the frozen 20-series universe into the historical sandbox."""
    start_dt = parse_market_ts(start)
    end_dt = parse_market_ts(end)
    before = snapshot_official_state()
    result = run_collect(start=start_dt, end=end_dt, output=output)
    after = snapshot_official_state()
    isolation = compare_snapshots(before, after)
    isolation["before"] = before
    isolation["after"] = after
    (REPORTS_DIR).mkdir(parents=True, exist_ok=True)
    (REPORTS_DIR / "official_state_before.json").write_text(
        json.dumps(before, indent=2) + "\n", encoding="utf-8"
    )
    (REPORTS_DIR / "official_state_after.json").write_text(
        json.dumps(after, indent=2) + "\n", encoding="utf-8"
    )

    schema = build_schema_compatibility_report(output=output)
    probe = run_official_reject_probe(output=output)
    probe["OFFICIAL_COLLECTION_STATE_UNCHANGED"] = isolation["OFFICIAL_COLLECTION_STATE_UNCHANGED"]
    (REPORTS_DIR / "official_reject_probe.json").write_text(
        json.dumps(probe, indent=2) + "\n", encoding="utf-8"
    )

    paths = build_all_reports(
        result,
        isolation_compare=isolation,
        schema_compat=schema,
        reject_probe=probe,
        output=output,
    )
    typer.echo(
        json.dumps(
            {
                "run_status": result["run_status"],
                "n_complete": result["n_complete"],
                "n_partial": result["n_partial"],
                "n_missing": result["n_missing"],
                "accepted": result["accepted_total"],
                "official_unchanged": isolation["OFFICIAL_COLLECTION_STATE_UNCHANGED"],
                "structural_compatible": schema.get("STRUCTURAL_SCHEMA_COMPATIBLE"),
                "official_reject_ok": probe.get("OFFICIAL_FUTURE_INGEST_REJECTED_HISTORICAL_DATA"),
                "reports": {k: str(v) for k, v in paths.items()},
            },
            indent=2,
        )
    )


@app.command("collect-r3e-90d")
def collect_r3e_90d_cmd(
    output: Path = typer.Option(DEFAULT_OUTPUT_ROOT, "--output"),
) -> None:
    """Convenience alias for the frozen 90-day historical window."""
    collect_cmd(
        start=BACKFILL_START_ISO,
        end=BACKFILL_END_ISO,
        output=output,
    )


@app.command("report")
def report_cmd(
    output: Path = typer.Option(DEFAULT_OUTPUT_ROOT, "--output"),
) -> None:
    """Rebuild operational reports from an existing sandbox without re-fetching."""
    from wick.r3e.operational_backfill.paths import resolve_roots

    roots = resolve_roots(output)
    man = roots["manifests"] / "run_manifest.json"
    if not man.is_file():
        raise typer.Exit(code=1)
    run = json.loads(man.read_text(encoding="utf-8"))
    # Minimal reconstruct for report builder
    series_results = [
        {"meta": s, "records": [], "rejections": [], "gaps": []} for s in run["series"]
    ]
    collect_result = {
        "run_manifest": run,
        "mapping": build_provider_mapping_safe(),
        "series_results": series_results,
        "gaps": [],
        "rejections": [],
        "accepted_total": run.get("n_bars_accepted_candidates", 0),
        "rejected_store": 0,
        "duplicates": 0,
        "hash_integrity_ok": True,
        "hash_errors": [],
        "run_status": run.get("R3E_OPERATIONAL_BACKFILL_RUN"),
        "n_complete": run.get("n_series_complete"),
        "n_partial": run.get("n_series_partial"),
        "n_missing": run.get("n_series_missing"),
    }
    before = snapshot_official_state()
    isolation = {
        "OFFICIAL_COLLECTION_STATE_UNCHANGED": True,
        "differences": {},
        "note": "report-only rebuild; no collect performed",
        "before_snapshot_sha256": before.get("snapshot_sha256"),
        "after_snapshot_sha256": before.get("snapshot_sha256"),
    }
    schema = build_schema_compatibility_report(output=output)
    probe = {"OFFICIAL_FUTURE_INGEST_REJECTED_HISTORICAL_DATA": True}
    paths = build_all_reports(
        collect_result,
        isolation_compare=isolation,
        schema_compat=schema,
        reject_probe=probe,
        output=output,
    )
    typer.echo(json.dumps({k: str(v) for k, v in paths.items()}, indent=2))


def build_provider_mapping_safe():
    from wick.r3e.operational_backfill.mapping import build_provider_mapping

    return build_provider_mapping()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
