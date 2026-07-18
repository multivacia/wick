"""CLI: python -m wick.r3e.future_unseen ..."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from wick.r3e.future_unseen.freeze import build_model_freeze
from wick.r3e.future_unseen.ingest import ingest_batch, write_cutoff_manifest
from wick.r3e.future_unseen.ops_report import build_ops_report
from wick.r3e.future_unseen.paths import REPORTS_DIR, SPEC_PATH, ensure_dirs
from wick.r3e.future_unseen.validate import run_validation

app = typer.Typer(
    name="future_unseen",
    help="R3E future-unseen final validation infrastructure",
    no_args_is_help=True,
)


@app.command("init")
def init_cmd() -> None:
    """Create directories, cutoff manifesto, and model freeze."""
    ensure_dirs()
    write_cutoff_manifest()
    freeze = build_model_freeze()
    ops = build_ops_report()
    typer.echo(json.dumps({"freeze": freeze["freeze_sha256"], "ops": ops["collection_status"]}))


@app.command("ops-report")
def ops_report_cmd(
    out: Path = typer.Option(REPORTS_DIR / "ops_collection_report.json", "--out"),
) -> None:
    """Operational collection report (no effect metrics)."""
    report = build_ops_report(out_path=out)
    typer.echo(
        json.dumps({"status": report["collection_status"], "n": report["n_observations_total"]})
    )


@app.command("ingest-json")
def ingest_json_cmd(
    path: Path = typer.Argument(..., exists=True, readable=True),
    origin: str = typer.Option("cli", "--origin"),
) -> None:
    """Ingest a JSON list of observation dicts (append-only, post-cutoff only)."""
    records = json.loads(path.read_text(encoding="utf-8"))
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


@app.command("validate")
def validate_cmd(
    manifest: Path | None = typer.Option(None, "--manifest"),
    spec: Path = typer.Option(SPEC_PATH, "--spec"),
    out_dir: Path = typer.Option(REPORTS_DIR, "--out-dir"),
) -> None:
    """Run final validation when collection completeness is met."""
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
