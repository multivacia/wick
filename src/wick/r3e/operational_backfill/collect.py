"""Collect 90-day historical OHLCV for operational validation (no M4/M5/validate)."""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.ingestion.gaps import detect_gaps
from wick.ingestion.providers import get_provider
from wick.ingestion.providers.base import MarketDataProvider
from wick.ingestion.validators import RawCandle, filter_closed_candles, validate_ohlcv
from wick.r3d.universe import UNIVERSE, SeriesSpec
from wick.r3e.future_unseen.config import FUTURE_UNSEEN_CUTOFF_ISO
from wick.r3e.future_unseen.hashing import sha256_file, sha256_json
from wick.r3e.operational_backfill.config import (
    BACKFILL_END,
    BACKFILL_START,
    CLASSIFICATION,
    EXPERIMENT_ID,
    MIN_BARS_CRYPTO_1D,
    MIN_BARS_CRYPTO_1H,
    MIN_BARS_STOCK_1D,
    MIN_BARS_STOCK_1H,
)
from wick.r3e.operational_backfill.mapping import build_provider_mapping
from wick.r3e.operational_backfill.paths import REPORTS_DIR, assert_not_official_path, ensure_dirs
from wick.r3e.operational_backfill.policy import HistoricalOperationalBackfillPolicy
from wick.r3e.operational_backfill.store import store_batch

ProviderFactory = Callable[[str], MarketDataProvider]


def _min_bars(spec: SeriesSpec) -> int:
    if spec.asset_class == "crypto":
        return MIN_BARS_CRYPTO_1H if spec.timeframe == "1h" else MIN_BARS_CRYPTO_1D
    return MIN_BARS_STOCK_1H if spec.timeframe == "1h" else MIN_BARS_STOCK_1D


def _candle_to_record(
    candle: RawCandle,
    *,
    symbol: str,
    timeframe: str,
    source: str,
) -> dict[str, Any]:
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "source": source,
        "market_ts": candle.timestamp.astimezone(UTC).isoformat(),
        "open": float(candle.open),
        "high": float(candle.high),
        "low": float(candle.low),
        "close": float(candle.close),
        "volume": float(candle.volume),
        "revision": 1,
    }


def collect_series(
    spec: SeriesSpec,
    *,
    start: datetime,
    end: datetime,
    provider: MarketDataProvider,
    policy: HistoricalOperationalBackfillPolicy,
    now_utc: datetime | None = None,
) -> dict[str, Any]:
    """Fetch one series; failures are captured without raising (caller continues)."""
    series_key = f"{spec.source}|{spec.symbol}|{spec.timeframe}"
    meta: dict[str, Any] = {
        "series_key": series_key,
        "requested_start": start.isoformat(),
        "requested_end": end.isoformat(),
        "effective_start": None,
        "effective_end": None,
        "inclusion_rule": "market_ts in [start, end] AND market_ts <= FUTURE_UNSEEN_CUTOFF",
        "alignment_reason": None,
        "provider_error": None,
        "known_limitation": None,
        "n_fetched": 0,
        "n_open_rejected": 0,
        "n_ohlcv_rejected": 0,
        "n_post_cutoff_rejected": 0,
        "n_policy_rejected": 0,
        "n_accepted_candidate": 0,
        "status": "MISSING",
    }
    records: list[dict[str, Any]] = []
    rejections: list[dict[str, Any]] = []

    try:
        result = provider.fetch_ohlcv(spec.symbol, spec.timeframe, start, end)
    except Exception as exc:  # noqa: BLE001 — isolate series failures
        meta["provider_error"] = f"{type(exc).__name__}: {exc}"
        meta["status"] = "PROVIDER_FAILURE"
        return {"meta": meta, "records": records, "rejections": rejections, "gaps": []}

    meta["known_limitation"] = result.known_limitation
    meta["n_fetched"] = len(result.candles)
    if result.actual_start is not None:
        meta["effective_start"] = result.actual_start.astimezone(UTC).isoformat()
        meta["alignment_reason"] = "provider actual_start/actual_end when available"
    if result.actual_end is not None:
        meta["effective_end"] = result.actual_end.astimezone(UTC).isoformat()

    closed, opened = filter_closed_candles(
        result.candles, spec.timeframe, now_utc=now_utc or datetime.now(UTC)
    )
    meta["n_open_rejected"] = len(opened)
    for c in opened:
        rejections.append(
            {
                "reason": "candle_not_closed",
                "market_ts": c.timestamp.astimezone(UTC).isoformat(),
                "series": series_key,
            }
        )

    timestamps: list[datetime] = []
    for candle in closed:
        v = validate_ohlcv(candle)
        if not v.ok:
            meta["n_ohlcv_rejected"] += 1
            rejections.append(
                {
                    "reason": f"ohlcv_invalid: {v.reason}",
                    "market_ts": candle.timestamp.astimezone(UTC).isoformat(),
                    "series": series_key,
                }
            )
            continue
        try:
            ts = policy.assert_eligible(candle.timestamp)
        except Exception as exc:  # HistoricalBackfillPolicyError / tz
            reason = str(exc)
            if "after FUTURE_UNSEEN_CUTOFF" in reason or "after backfill end" in reason:
                meta["n_post_cutoff_rejected"] += 1
            else:
                meta["n_policy_rejected"] += 1
            rejections.append(
                {
                    "reason": reason,
                    "market_ts": candle.timestamp.astimezone(UTC).isoformat(),
                    "series": series_key,
                }
            )
            continue
        rec = _candle_to_record(
            candle, symbol=spec.symbol, timeframe=spec.timeframe, source=spec.source
        )
        records.append(rec)
        timestamps.append(ts)

    meta["n_accepted_candidate"] = len(records)
    if records:
        meta["effective_start"] = meta["effective_start"] or min(r["market_ts"] for r in records)
        meta["effective_end"] = meta["effective_end"] or max(r["market_ts"] for r in records)

    gaps = detect_gaps(
        timestamps,
        asset_symbol=spec.symbol,
        timeframe=spec.timeframe,
        asset_type=spec.asset_class,
    )
    gap_dicts = [
        {
            **asdict(g),
            "gap_start": g.gap_start.isoformat(),
            "gap_end": g.gap_end.isoformat(),
        }
        for g in gaps
    ]

    n = len(records)
    minimum = _min_bars(spec)
    if n == 0 and meta["status"] != "PROVIDER_FAILURE":
        meta["status"] = "MISSING"
    elif n >= minimum:
        meta["status"] = "COMPLETE"
    else:
        meta["status"] = "PARTIAL"
    meta["min_bars_operational"] = minimum

    return {"meta": meta, "records": records, "rejections": rejections, "gaps": gap_dicts}


def run_collect(
    *,
    start: datetime | None = None,
    end: datetime | None = None,
    output: Path | str | None = None,
    provider_factory: ProviderFactory | None = None,
    now_utc: datetime | None = None,
) -> dict[str, Any]:
    """Run full-universe historical collect into isolated sandbox."""
    start = start or BACKFILL_START
    end = end or BACKFILL_END
    if end > BACKFILL_END:
        raise ValueError("end must not exceed FUTURE_UNSEEN_CUTOFF / BACKFILL_END")
    roots = ensure_dirs(output)
    assert_not_official_path(roots["root"])
    factory = provider_factory or get_provider
    policy = HistoricalOperationalBackfillPolicy(start=start, end=end)
    mapping = build_provider_mapping()

    series_results: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    all_rejections: list[dict[str, Any]] = []
    all_gaps: list[dict[str, Any]] = []
    provider_failures: list[dict[str, Any]] = []

    # Cache providers by source
    providers: dict[str, MarketDataProvider] = {}

    for spec in UNIVERSE:
        if spec.source not in providers:
            try:
                providers[spec.source] = factory(spec.source)
            except Exception as exc:  # noqa: BLE001
                provider_failures.append(
                    {"source": spec.source, "error": f"{type(exc).__name__}: {exc}"}
                )
                series_results.append(
                    {
                        "meta": {
                            "series_key": f"{spec.source}|{spec.symbol}|{spec.timeframe}",
                            "status": "PROVIDER_FAILURE",
                            "provider_error": str(exc),
                            "n_accepted_candidate": 0,
                        },
                        "records": [],
                        "rejections": [],
                        "gaps": [],
                    }
                )
                continue
        provider = providers[spec.source]
        out = collect_series(
            spec,
            start=start,
            end=end,
            provider=provider,
            policy=policy,
            now_utc=now_utc,
        )
        series_results.append(out)
        all_records.extend(out["records"])
        all_rejections.extend(out["rejections"])
        all_gaps.extend(out["gaps"])
        if out["meta"].get("provider_error"):
            provider_failures.append(
                {
                    "series": out["meta"]["series_key"],
                    "error": out["meta"]["provider_error"],
                }
            )

        # Persist per-series batch for append-only audit trail
        if out["records"] or out["rejections"]:
            store_batch(
                out["records"],
                output=roots["root"],
                batch_id=(
                    "ob_"
                    + out["meta"]["series_key"].replace("|", "_").replace("/", "")
                    + "_"
                    + datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
                ),
                origin="operational-backfill-collect",
                series_meta=out["meta"],
            )

    # Write run-level rejection audit (provider/open/ohlcv/policy)
    rej_path = roots["manifests"] / "collection_rejections.json"
    rej_doc = {
        "experiment_id": EXPERIMENT_ID,
        "classification": CLASSIFICATION,
        "n_rejections": len(all_rejections),
        "rejections": all_rejections[:5000],  # cap size
        "truncated": len(all_rejections) > 5000,
    }
    rej_path.write_text(json.dumps(rej_doc, indent=2) + "\n", encoding="utf-8")

    statuses = [r["meta"]["status"] for r in series_results]
    n_complete = statuses.count("COMPLETE")
    n_partial = statuses.count("PARTIAL")
    n_missing = statuses.count("MISSING") + statuses.count("PROVIDER_FAILURE")

    if n_complete == len(UNIVERSE):
        run_status = "COMPLETE"
    elif n_complete + n_partial > 0:
        run_status = "PARTIAL"
    else:
        run_status = "FAILED"

    run_manifest = {
        "kind": "OPERATIONAL_BACKFILL_RUN",
        "experiment_id": EXPERIMENT_ID,
        "classification": CLASSIFICATION,
        "requested_start": start.isoformat(),
        "requested_end": end.isoformat(),
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "created_at": datetime.now(UTC).isoformat(),
        "R3E_OPERATIONAL_BACKFILL_RUN": run_status,
        "R3E_OPERATIONAL_BACKFILL_SCIENTIFIC_ELIGIBILITY": False,
        "n_series_expected": len(UNIVERSE),
        "n_series_complete": n_complete,
        "n_series_partial": n_partial,
        "n_series_missing": n_missing,
        "n_bars_accepted_candidates": len(all_records),
        "n_rejections": len(all_rejections),
        "n_gaps": len(all_gaps),
        "provider_failures": provider_failures,
        "series": [r["meta"] for r in series_results],
        "output_root": str(roots["root"]),
        "models_executed": [],
        "validate_executed": False,
        "effect_peeking_performed": False,
        "gate_impact_allowed": False,
    }
    run_manifest["sha256"] = sha256_json(run_manifest)
    man_path = roots["manifests"] / "run_manifest.json"
    man_path.write_text(json.dumps(run_manifest, indent=2) + "\n", encoding="utf-8")

    # Aggregate store stats from batch manifests
    accepted_total = 0
    rejected_store = 0
    duplicates = 0
    file_hashes_ok = True
    hash_errors: list[str] = []
    for batch_path in sorted(roots["manifests"].glob("batch_*.json")):
        doc = json.loads(batch_path.read_text(encoding="utf-8"))
        accepted_total += int(doc.get("accepted", 0))
        rejected_store += int(doc.get("rejected", 0))
        duplicates += int(doc.get("duplicates_rejected", 0))
        val = Path(doc["validated_path"])
        if val.is_file():
            actual = sha256_file(val)
            if actual != doc.get("file_sha256"):
                file_hashes_ok = False
                hash_errors.append(str(val))

    return {
        "run_manifest": run_manifest,
        "mapping": mapping,
        "series_results": series_results,
        "gaps": all_gaps,
        "rejections": all_rejections,
        "accepted_total": accepted_total,
        "rejected_store": rejected_store,
        "duplicates": duplicates,
        "hash_integrity_ok": file_hashes_ok,
        "hash_errors": hash_errors,
        "output_root": str(roots["root"]),
        "reports_dir": str(REPORTS_DIR),
        "run_status": run_status,
        "n_complete": n_complete,
        "n_partial": n_partial,
        "n_missing": n_missing,
    }
