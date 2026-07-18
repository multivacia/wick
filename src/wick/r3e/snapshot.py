"""Auditable data snapshot for R3E real-data development runs."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from wick.db.models import Asset, Candle, CandleRevisionEvent, IngestionRun
from wick.r3d.coverage import assess_universe
from wick.r3d.universe import UNIVERSE
from wick.r3e.config import R3D_HOLDOUT_FRAC
from wick.r3e.nested_wf import development_cutoff


def _pkg_version(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def _series_hash(session: Session, asset_id: Any, timeframe: str) -> str:
    rows = session.scalars(
        select(Candle)
        .where(
            Candle.asset_id == asset_id, Candle.timeframe == timeframe, Candle.is_closed.is_(True)
        )
        .order_by(Candle.timestamp)
    ).all()
    h = hashlib.sha256()
    for r in rows:
        h.update(
            (
                f"{r.timestamp.isoformat()}|{r.open}|{r.high}|{r.low}|{r.close}|"
                f"{r.volume}|{r.source}|{r.data_revision}\n"
            ).encode()
        )
    return h.hexdigest()


def identify_r3d_holdout_intervals(session: Session) -> list[dict[str, Any]]:
    """Identify exact candle intervals consumed as R3D holdout (last 30% per series).

    R3D used ``development_cutoff(n, 0.30)`` on ordered closed candles. The holdout
    is ``[cut, n)`` and MUST NOT be used as confirmatory final validation in R3E.
    """
    out: list[dict[str, Any]] = []
    for spec in UNIVERSE:
        asset = session.scalar(
            select(Asset).where(Asset.symbol == spec.symbol, Asset.source == spec.source)
        )
        if asset is None:
            out.append(
                {
                    "symbol": spec.symbol,
                    "source": spec.source,
                    "timeframe": spec.timeframe,
                    "status": "MISSING_INSTRUMENT",
                    "r3e_confirmatory_claim_allowed_on_holdout": False,
                }
            )
            continue
        rows = session.scalars(
            select(Candle)
            .where(
                Candle.asset_id == asset.id,
                Candle.timeframe == spec.timeframe,
                Candle.is_closed.is_(True),
            )
            .order_by(Candle.timestamp)
        ).all()
        n = len(rows)
        if n == 0:
            out.append(
                {
                    "symbol": spec.symbol,
                    "source": spec.source,
                    "timeframe": spec.timeframe,
                    "status": "EMPTY",
                    "n_candles": 0,
                    "r3e_confirmatory_claim_allowed_on_holdout": False,
                }
            )
            continue
        cut = development_cutoff(n, R3D_HOLDOUT_FRAC)
        holdout = rows[cut:]
        out.append(
            {
                "symbol": spec.symbol,
                "source": spec.source,
                "timeframe": spec.timeframe,
                "asset_class": spec.asset_class,
                "n_candles": n,
                "development_n": cut,
                "holdout_n": n - cut,
                "holdout_frac": R3D_HOLDOUT_FRAC,
                "development_first_ts": rows[0].timestamp.isoformat(),
                "development_last_ts": rows[cut - 1].timestamp.isoformat() if cut > 0 else None,
                "holdout_first_ts": holdout[0].timestamp.isoformat() if holdout else None,
                "holdout_last_ts": holdout[-1].timestamp.isoformat() if holdout else None,
                "r3d_holdout_consumed": True,
                "r3e_confirmatory_claim_allowed_on_holdout": False,
                "status": "IDENTIFIED",
            }
        )
    return out


def build_data_snapshot(session: Session, *, out_dir) -> dict[str, Any]:
    """Build auditable snapshot: ids, hashes, coverage, revisions, failures."""
    from pathlib import Path

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    coverage = assess_universe(session, UNIVERSE)
    series: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    partial: list[dict[str, Any]] = []

    for cov in coverage:
        entry = cov.to_dict()
        if cov.asset_id and cov.candle_count:
            entry["series_hash_sha256"] = _series_hash(session, cov.asset_id, cov.timeframe)
            revs = [
                r[0]
                for r in session.execute(
                    select(Candle.data_revision)
                    .where(
                        Candle.asset_id == cov.asset_id,
                        Candle.timeframe == cov.timeframe,
                    )
                    .distinct()
                ).all()
            ]
            entry["revisions_observed"] = revs
            n_rev_events = session.scalar(
                select(func.count())
                .select_from(CandleRevisionEvent)
                .join(Candle, CandleRevisionEvent.candle_id == Candle.id)
                .where(Candle.asset_id == cov.asset_id, Candle.timeframe == cov.timeframe)
            )
            entry["revision_events"] = int(n_rev_events or 0)
        else:
            entry["series_hash_sha256"] = None
            entry["revisions_observed"] = []
            entry["revision_events"] = 0

        if cov.coverage_status == "MISSING":
            failures.append({**entry, "reason": "missing_or_empty"})
        elif cov.coverage_status == "PARTIAL":
            # Same human acceptance as R3D for stock 1d ~4.988y
            if (
                cov.asset_class == "stock"
                and cov.timeframe == "1d"
                and cov.span_years is not None
                and cov.span_years >= 4.98
            ):
                entry["status"] = "PARTIAL_ACCEPTED"
                partial.append(entry)
            else:
                entry["status"] = "PARTIAL"
                partial.append(entry)
        else:
            entry["status"] = "OK"
        series.append(entry)

    jobs = []
    for j in session.scalars(
        select(IngestionRun).order_by(IngestionRun.started_at.desc()).limit(50)
    ).all():
        jobs.append(
            {
                "run_id": j.run_id,
                "source": j.source,
                "status": j.status,
                "started_at": j.started_at.isoformat() if j.started_at else None,
                "finished_at": j.finished_at.isoformat() if j.finished_at else None,
                "error_summary": j.error_summary,
                "quality_report": j.quality_report,
            }
        )

    payload = {
        "data_snapshot_id": f"r3e-real-{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}",
        "created_at_utc": datetime.now(UTC).isoformat(),
        "ingest_date_utc": datetime.now(UTC).date().isoformat(),
        "provider_versions": {
            "binance": "data-api.binance.vision",
            "yahoo": f"yfinance={_pkg_version('yfinance')}",
            "ccxt": _pkg_version("ccxt"),
        },
        "series": series,
        "partial_series": partial,
        "failures": failures,
        "recent_ingest_jobs": jobs,
        "aggregate_hash_sha256": hashlib.sha256(
            json.dumps(
                [
                    {
                        "symbol": s.get("symbol"),
                        "timeframe": s.get("timeframe"),
                        "n": s.get("candle_count"),
                        "hash": s.get("series_hash_sha256"),
                        "first": s.get("first_ts"),
                        "last": s.get("last_ts"),
                    }
                    for s in series
                ],
                sort_keys=True,
                default=str,
            ).encode()
        ).hexdigest(),
        "r3d_holdout_policy": {
            "frac": R3D_HOLDOUT_FRAC,
            "confirmatory_reuse_forbidden": True,
            "note": "Holdout intervals recorded separately in r3d_holdout_intervals.json",
        },
    }
    (out_dir / "data_snapshot.json").write_text(
        json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8"
    )
    return payload
