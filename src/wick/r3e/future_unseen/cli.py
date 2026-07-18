"""CLI: python -m wick.r3e.future_unseen ..."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import typer

from wick.r3e.future_unseen.collector import run_collect
from wick.r3e.future_unseen.ingest import ingest_batch
from wick.r3e.future_unseen.initialization import initialize_collection
from wick.r3e.future_unseen.ops_report import build_ops_report
from wick.r3e.future_unseen.paths import REPORTS_DIR, SPEC_PATH
from wick.r3e.future_unseen.protections import parse_market_ts
from wick.r3e.future_unseen.readiness import (
    default_report_path,
    evaluate_readiness,
    exit_code_for_status,
)

app = typer.Typer(
    name="future_unseen",
    help="R3E future-unseen final validation infrastructure",
    no_args_is_help=True,
)


@app.command("init")
def init_cmd() -> None:
    """Formally initialize collection (idempotent; no ingest; no validate)."""
    result = initialize_collection()
    typer.echo(
        json.dumps(
            {
                "freeze": result["freeze_sha256"],
                "formal_collection_state": result["collection_state"]["R3E_FUTURE_DATA_COLLECTION"],
                "commit": result["commit"],
                "validate_executed": False,
                "n_observations": result["ops"]["n_observations_total"],
            }
        )
    )


@app.command("ops-report")
def ops_report_cmd(
    out: Path = typer.Option(REPORTS_DIR / "ops_collection_report.json", "--out"),
) -> None:
    """Operational collection report (no effect metrics)."""
    report = build_ops_report(out_path=out)
    # Preserve formal lifecycle overlay if present
    state_path = Path("data/future_unseen/manifests/collection_state.json")
    formal = None
    if state_path.exists():
        formal = json.loads(state_path.read_text(encoding="utf-8")).get(
            "R3E_FUTURE_DATA_COLLECTION"
        )
    payload = {
        **report,
        "formal_collection_state": formal,
        "validation_status": "NOT_RUN",
        "effect_evaluation_status": "NOT_EVALUATED",
    }
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    typer.echo(
        json.dumps(
            {
                "status_data_driven": report["collection_status"],
                "formal_collection_state": formal,
                "n": report["n_observations_total"],
                "hash_ok": report["hash_integrity_ok"],
                "series_missing": len(report["series_missing"]),
                "effect_metrics_disclosed": report["effect_metrics_disclosed"],
                "validation_status": "NOT_RUN",
            }
        )
    )


@app.command("ingest-json")
def ingest_json_cmd(
    path: Path | None = typer.Argument(None, exists=True, readable=True),
    input_path: Path | None = typer.Option(
        None, "--input", exists=True, readable=True, help="JSON list of observations"
    ),
    origin: str = typer.Option("cli", "--origin"),
) -> None:
    """Ingest a JSON list of observation dicts (append-only, post-cutoff only)."""
    src = input_path or path
    if src is None:
        raise typer.BadParameter("provide PATH or --input <arquivo.json>")
    records = json.loads(src.read_text(encoding="utf-8"))
    if not isinstance(records, list):
        raise typer.BadParameter("input must be a JSON list of records")
    result = ingest_batch(records, origin=origin)
    typer.echo(
        json.dumps(
            {
                "batch_id": result.batch_id,
                "accepted": result.accepted,
                "rejected": result.rejected,
                "file_sha256": result.file_sha256,
            }
        )
    )


@app.command("collect")
def collect_cmd(
    dry_run: bool = typer.Option(False, "--dry-run", help="Do not write to official store"),
    series: str | None = typer.Option(
        None, "--series", help="Filter by official symbol (does not alter frozen universe)"
    ),
    provider: str | None = typer.Option(
        None, "--provider", help="Filter by source (binance|yahoo)"
    ),
    as_of: str | None = typer.Option(
        None,
        "--as-of",
        help="Timezone-aware UTC timestamp for deterministic closed-candle decisions",
    ),
    output_report: Path | None = typer.Option(
        None, "--output-report", help="Directory for this run's operational reports"
    ),
    max_retries: int = typer.Option(3, "--max-retries", min=0, max=10),
) -> None:
    """Incrementally collect closed post-cutoff OHLCV into the official store."""
    as_of_dt: datetime | None = None
    if as_of is not None:
        as_of_dt = parse_market_ts(as_of)
    result = run_collect(
        dry_run=dry_run,
        series_filter=series,
        provider_filter=provider,
        as_of=as_of_dt,
        max_retries=max_retries,
        output_report_dir=output_report,
    )
    typer.echo(
        json.dumps(
            {
                "collection_run_id": result["collection_run_id"],
                "run_status": result["run_status"],
                "dry_run": result["dry_run"],
                "n_before": result["n_observations_before"],
                "n_after": result["n_observations_after"],
                "n_candidates": result["n_candidates"],
                "persist": result["persist"],
                "ops": result["ops"],
                "validate_executed": False,
            },
            indent=2,
        )
    )


@app.command("readiness")
def readiness_cmd(
    as_of: str | None = typer.Option(
        None,
        "--as-of",
        help="Timezone-aware UTC timestamp for deterministic window/open-candle checks",
    ),
    output_report: Path | None = typer.Option(
        None,
        "--output-report",
        help="Write full readiness JSON report to this path (default under reports/)",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Escalate open/future candle findings from NOT_READY to BLOCKED",
    ),
    as_json: bool = typer.Option(
        True,
        "--json/--human",
        help="Emit JSON summary (default) or a short human line",
    ),
) -> None:
    """Operational readiness gate (READY|NOT_READY|BLOCKED). Read-only; never runs validate."""
    as_of_dt = parse_market_ts(as_of) if as_of is not None else None
    report = evaluate_readiness(as_of=as_of_dt, strict=strict)
    out_path = output_report or default_report_path()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary = {
        "readiness_status": report["readiness_status"],
        "readiness_reason": report["readiness_reason"],
        "window_days": report["window_days"],
        "series_with_min_bars": report["series_with_min_bars"],
        "required_series": report["required_series"],
        "hash_status": report["hash_status"],
        "manifest_status": report["manifest_status"],
        "collector_status": report["collector_status"],
        "validate_executed": report["scientific_safety"]["validation_command_executed"],
        "effect_peeking_performed": report["scientific_safety"]["effect_peeking_performed"],
        "VALIDATE_AUTHORIZED": False,
        "report_path": str(out_path),
    }
    if as_json:
        typer.echo(json.dumps(summary, indent=2))
    else:
        typer.echo(
            f"{report['readiness_status']} reason={report['readiness_reason']} "
            f"window_days={report['window_days']:.4f} "
            f"complete_series={report['series_with_min_bars']}/{report['required_series']} "
            f"hash={report['hash_status']} report={out_path}"
        )
    raise typer.Exit(code=exit_code_for_status(report["readiness_status"]))


@app.command("validate")
def validate_cmd(
    manifest: Path | None = typer.Option(None, "--manifest"),
    spec: Path = typer.Option(SPEC_PATH, "--spec"),
    out_dir: Path = typer.Option(REPORTS_DIR, "--out-dir"),
) -> None:
    """Run final validation when collection completeness is met."""
    # Lazy import: keep collect path free of validate/gate imports at module load for tests
    # that inspect collector dependencies; validate remains available as an explicit command.
    from wick.r3e.future_unseen.validate import run_validation

    out = run_validation(manifest_path=manifest, spec_path=spec, out_dir=out_dir)
    gate = out["gate"]
    typer.echo(
        json.dumps(
            {
                "decision": gate.get("decision"),
                "R3E_GATE": gate.get("R3E_GATE"),
                "ECONOMIC_INTERPRETATION_ALLOWED": gate.get("ECONOMIC_INTERPRETATION_ALLOWED"),
                "R4_STATUS": gate.get("R4_STATUS"),
            }
        )
    )


def main() -> None:
    app()
