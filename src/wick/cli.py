"""Wick CLI."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import typer
from rich.console import Console

from wick import __version__
from wick.config import get_settings
from wick.db.session import session_scope
from wick.ingestion.providers import get_provider
from wick.ingestion.service import IngestionService, IngestRequest

app = typer.Typer(
    name="wick", help="Wick — candlestick research ingestion CLI", no_args_is_help=True
)
console = Console()


def _parse_dt(value: str) -> datetime:
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


@app.callback()
def main() -> None:
    """Wick CLI."""


@app.command("version")
def version_cmd() -> None:
    """Print package version."""
    console.print(__version__)


@app.command("ingest")
def ingest_cmd(
    source: str = typer.Option(..., "--source", "-s", help="binance | yahoo | brapi"),
    symbols: str = typer.Option(
        ...,
        "--symbols",
        help="Comma-separated symbols, e.g. BTC/USDT,ETH/USDT or AAPL,MSFT",
    ),
    timeframes: str = typer.Option(
        "1d",
        "--timeframes",
        "-t",
        help="Comma-separated timeframes: 1m,5m,15m,1h,4h,1d,1w",
    ),
    start: str = typer.Option(..., "--start", help="ISO8601 start (UTC)"),
    end: str = typer.Option(..., "--end", help="ISO8601 end (UTC)"),
    incremental: bool = typer.Option(
        True,
        "--incremental/--full",
        help="Fetch only missing range after latest stored candle",
    ),
    report_path: Path | None = typer.Option(
        None,
        "--report",
        help="Write JSON quality report to this path",
    ),
) -> None:
    """Ingest OHLCV candles from a market data source."""
    settings = get_settings()
    provider = get_provider(source, settings)
    symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]
    tf_list = [t.strip() for t in timeframes.split(",") if t.strip()]
    if not symbol_list:
        raise typer.BadParameter("At least one symbol is required")
    if not tf_list:
        raise typer.BadParameter("At least one timeframe is required")

    request = IngestRequest(
        source=provider.name,
        symbols=symbol_list,
        timeframes=tf_list,
        start=_parse_dt(start),
        end=_parse_dt(end),
        incremental=incremental,
    )

    with session_scope(settings) as session:
        service = IngestionService(session, provider, settings)
        outcome = service.run(request)
        report = outcome.report

    console.print(report.render_text())
    out = report_path or Path(f"reports/ingestion_{report.run_id}.json")
    report.write(out)
    console.print(f"Quality report written to {out}")
    if report.status == "FAILED":
        raise typer.Exit(code=1)


@app.command("db-check")
def db_check() -> None:
    """Verify database connectivity."""
    from sqlalchemy import text

    settings = get_settings()
    with session_scope(settings) as session:
        session.execute(text("SELECT 1"))
    console.print("Database OK")


@app.command("detect")
def detect_cmd(
    symbols: str = typer.Option(..., "--assets", help="Comma-separated asset symbols"),
    timeframes: str = typer.Option("1d", "--timeframes"),
    source: str = typer.Option("binance", "--source", help="Asset source to resolve"),
    start: str | None = typer.Option(None, "--start"),
    end: str | None = typer.Option(None, "--end"),
    incremental: bool = typer.Option(True, "--incremental/--full-scan"),
    reprocess: bool = typer.Option(False, "--reprocess"),
    dry_run: bool = typer.Option(False, "--dry-run"),
    detector_version: str | None = typer.Option(None, "--detector-version"),
) -> None:
    """Detect R2 candlestick patterns on stored closed candles (no returns)."""
    from sqlalchemy import select

    from wick.db.models import Asset
    from wick.detection.service import DetectionService
    from wick.patterns.params import DETECTOR_VERSION

    settings = get_settings()
    symbol_list = [s.strip() for s in symbols.split(",") if s.strip()]
    tf_list = [t.strip() for t in timeframes.split(",") if t.strip()]
    start_dt = _parse_dt(start) if start else None
    end_dt = _parse_dt(end) if end else None
    version = detector_version or DETECTOR_VERSION

    with session_scope(settings) as session:
        svc = DetectionService(
            session,
            detector_version=version,
            dry_run=dry_run,
            safety_delay_seconds=settings.candle_close_safety_delay_seconds,
        )
        for sym in symbol_list:
            assets = list(
                session.execute(
                    select(Asset).where(Asset.symbol == sym, Asset.source == source)
                ).scalars()
            )
            if not assets:
                console.print(f"Asset not found: {sym} source={source}")
                continue
            for asset in assets:
                for tf in tf_list:
                    summary = svc.detect_asset_timeframe(
                        asset_id=asset.id,
                        timeframe=tf,
                        start=start_dt,
                        end=end_dt,
                        incremental=incremental and not reprocess,
                        reprocess=reprocess,
                    )
                    console.print(
                        f"{asset.symbol} {tf}: scanned={summary.candles_scanned} "
                        f"inserted={summary.patterns_inserted} "
                        f"unchanged={summary.patterns_unchanged} "
                        f"confirmations={summary.confirmations_upserted} "
                        f"dry_run={summary.dry_run} run={summary.run_id}"
                    )
                    for note in summary.notes:
                        console.print(f"  note: {note}")


if __name__ == "__main__":
    app()
