"""CLI: python -m wick.r3e.future_unseen ..."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from wick.r3e.future_unseen.ingest import ingest_batch
from wick.r3e.future_unseen.initialization import initialize_collection
from wick.r3e.future_unseen.ops_report import build_ops_report
from wick.r3e.future_unseen.paths import REPORTS_DIR, SPEC_PATH
from wick.r3e.future_unseen.validate import run_validation

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
