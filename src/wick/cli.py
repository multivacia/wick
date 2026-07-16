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


if __name__ == "__main__":
    app()
