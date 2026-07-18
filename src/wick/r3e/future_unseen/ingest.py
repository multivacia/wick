"""Append-only ingestion of future-unseen OHLCV observations.

Only market timestamps strictly after FUTURE_UNSEEN_CUTOFF are accepted.
Silent updates/overwrites are forbidden; provider corrections create new revisions.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.config import (
    EXPERIMENT_ID,
    FUTURE_UNSEEN_CUTOFF_ISO,
    SERIES_UNIVERSE,
)
from wick.r3e.future_unseen.hashing import sha256_file, sha256_json
from wick.r3e.future_unseen.paths import MANIFESTS_DIR, RAW_DIR, VALIDATED_DIR, ensure_dirs
from wick.r3e.future_unseen.protections import (
    FutureUnseenProtectionError,
    assert_no_forbidden_path,
    assert_strictly_after_cutoff,
)


@dataclass
class ObservationRecord:
    symbol: str
    timeframe: str
    source: str
    market_ts: str  # ISO UTC of the closed bar
    open: float
    high: float
    low: float
    close: float
    volume: float
    revision: int = 1
    ingested_at: str = ""
    record_id: str = ""

    def key(self) -> tuple[str, str, str, str]:
        return (self.symbol, self.timeframe, self.source, self.market_ts)


@dataclass
class Rejection:
    reason: str
    record: dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchIngestResult:
    batch_id: str
    accepted: int
    rejected: int
    rejections: list[Rejection]
    raw_path: str
    validated_path: str
    manifest_path: str
    batch_sha256: str
    file_sha256: str
    series_counts: dict[str, int]
    first_market_ts: str | None
    last_market_ts: str | None


def _series_key(symbol: str, timeframe: str, source: str) -> str:
    return f"{source}|{symbol}|{timeframe}"


def _load_index() -> dict[str, dict[str, Any]]:
    path = MANIFESTS_DIR / "observation_index.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_index(index: dict[str, dict[str, Any]]) -> None:
    path = MANIFESTS_DIR / "observation_index.json"
    path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _official_series_set() -> set[tuple[str, str, str]]:
    return set(SERIES_UNIVERSE)


def ingest_batch(
    records: list[dict[str, Any]],
    *,
    origin: str,
    batch_id: str | None = None,
) -> BatchIngestResult:
    """Validate and append a batch of future-unseen observations.

    ``origin`` must not point at forbidden historical/exploratory roots.
    """
    ensure_dirs()
    assert_no_forbidden_path(origin)
    batch_id = (
        batch_id or f"fu_{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    )
    now = datetime.now(UTC).isoformat()
    index = _load_index()
    official = _official_series_set()

    accepted: list[ObservationRecord] = []
    rejections: list[Rejection] = []

    for raw in records:
        try:
            symbol = str(raw["symbol"])
            timeframe = str(raw["timeframe"])
            source = str(raw["source"])
            if (symbol, timeframe, source) not in official:
                raise FutureUnseenProtectionError(
                    f"series not in official universe: {source}|{symbol}|{timeframe}"
                )
            market_ts = assert_strictly_after_cutoff(raw["market_ts"])
            ohlcv = {k: float(raw[k]) for k in ("open", "high", "low", "close", "volume")}
            if not (ohlcv["low"] <= ohlcv["open"] <= ohlcv["high"]):
                raise FutureUnseenProtectionError("OHLC inconsistency (open)")
            if not (ohlcv["low"] <= ohlcv["close"] <= ohlcv["high"]):
                raise FutureUnseenProtectionError("OHLC inconsistency (close)")

            key = _series_key(symbol, timeframe, source) + "|" + market_ts.isoformat()
            revision = int(raw.get("revision", 1))
            if key in index:
                prev = index[key]
                # Silent overwrite forbidden: identical OHLCV → duplicate reject;
                # changed OHLCV requires higher revision and audit trail.
                same = all(abs(float(prev[k]) - ohlcv[k]) < 1e-12 for k in ohlcv)
                if same:
                    raise FutureUnseenProtectionError("duplicate observation (identical OHLCV)")
                if revision <= int(prev.get("revision", 1)):
                    raise FutureUnseenProtectionError(
                        "provider correction requires incremented revision; silent update forbidden"
                    )
            rec = ObservationRecord(
                symbol=symbol,
                timeframe=timeframe,
                source=source,
                market_ts=market_ts.isoformat(),
                revision=revision,
                ingested_at=now,
                record_id=str(uuid.uuid4()),
                **ohlcv,
            )
            accepted.append(rec)
            index[key] = {
                **ohlcv,
                "revision": revision,
                "record_id": rec.record_id,
                "batch_id": batch_id,
                "ingested_at": now,
                "market_ts": rec.market_ts,
                "previous_record_id": None if key not in index else index[key].get("record_id"),
            }
        except (KeyError, TypeError, ValueError, FutureUnseenProtectionError) as exc:
            rejections.append(Rejection(reason=str(exc), record=dict(raw)))

    # Detect gaps within this batch per series (missing expected step)
    gaps = _detect_batch_gaps(accepted)

    raw_path = RAW_DIR / f"{batch_id}.jsonl"
    val_path = VALIDATED_DIR / f"{batch_id}.jsonl"
    lines = [json.dumps(asdict(r), sort_keys=True) for r in accepted]
    payload = "\n".join(lines) + ("\n" if lines else "")
    raw_path.write_text(payload, encoding="utf-8")
    val_path.write_text(payload, encoding="utf-8")
    file_hash = sha256_file(val_path)

    series_counts: dict[str, int] = {}
    for r in accepted:
        sk = _series_key(r.symbol, r.timeframe, r.source)
        series_counts[sk] = series_counts.get(sk, 0) + 1

    first_ts = min((r.market_ts for r in accepted), default=None)
    last_ts = max((r.market_ts for r in accepted), default=None)

    manifest = {
        "batch_id": batch_id,
        "experiment_id": EXPERIMENT_ID,
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "origin": origin,
        "created_at": now,
        "accepted": len(accepted),
        "rejected": len(rejections),
        "rejections": [asdict(x) for x in rejections],
        "gaps_detected": gaps,
        "series_counts": series_counts,
        "first_market_ts": first_ts,
        "last_market_ts": last_ts,
        "raw_path": str(raw_path),
        "validated_path": str(val_path),
        "file_sha256": file_hash,
        "append_only": True,
        "silent_overwrite_forbidden": True,
    }
    manifest["batch_sha256"] = sha256_json(manifest)
    man_path = MANIFESTS_DIR / f"batch_{batch_id}.json"
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    _save_index(index)
    _update_collection_state()

    return BatchIngestResult(
        batch_id=batch_id,
        accepted=len(accepted),
        rejected=len(rejections),
        rejections=rejections,
        raw_path=str(raw_path),
        validated_path=str(val_path),
        manifest_path=str(man_path),
        batch_sha256=manifest["batch_sha256"],
        file_sha256=file_hash,
        series_counts=series_counts,
        first_market_ts=first_ts,
        last_market_ts=last_ts,
    )


def _detect_batch_gaps(records: list[ObservationRecord]) -> list[dict[str, Any]]:
    """Flag non-monotonic or large gaps within a batch (no fill)."""
    by_series: dict[str, list[ObservationRecord]] = {}
    for r in records:
        by_series.setdefault(_series_key(r.symbol, r.timeframe, r.source), []).append(r)
    gaps: list[dict[str, Any]] = []
    for sk, rows in by_series.items():
        rows = sorted(rows, key=lambda x: x.market_ts)
        for a, b in zip(rows, rows[1:], strict=False):
            if b.market_ts <= a.market_ts:
                gaps.append(
                    {"series": sk, "kind": "non_monotonic", "a": a.market_ts, "b": b.market_ts}
                )
    return gaps


def _update_collection_state() -> None:
    from wick.r3e.future_unseen.ops_report import build_ops_report

    report = build_ops_report()
    prev_path = MANIFESTS_DIR / "collection_state.json"
    prev = json.loads(prev_path.read_text(encoding="utf-8")) if prev_path.exists() else {}
    # Once formally started (IN_PROGRESS/COMPLETE), do not regress to NOT_STARTED
    # merely because a batch is empty of new accepts.
    data_status = report["collection_status"]
    formal = prev.get("R3E_FUTURE_DATA_COLLECTION")
    if formal in {"IN_PROGRESS", "COMPLETE"} and data_status == "NOT_STARTED":
        collection = formal
    else:
        collection = data_status if data_status != "NOT_STARTED" else (formal or data_status)
    state = {
        **{
            k: v
            for k, v in prev.items()
            if k.startswith("R3E_") or k in {"cutoff", "engine_version"}
        },
        "R3E_FUTURE_DATA_COLLECTION": collection,
        "R3E_GATE": "PENDING_FUTURE_UNSEEN_DATA",
        "ECONOMIC_INTERPRETATION_ALLOWED": False,
        "R4_STATUS": "BLOCKED",
        "R5_STATUS": "NOT_STARTED",
        "updated_at": datetime.now(UTC).isoformat(),
        "cutoff": FUTURE_UNSEEN_CUTOFF_ISO,
        "validation_command_executed": False,
        "effect_peeking_performed": False,
    }
    prev_path.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def write_cutoff_manifest(*, commit: str | None = None) -> Path:
    ensure_dirs()
    payload = {
        "FUTURE_UNSEEN_CUTOFF": FUTURE_UNSEEN_CUTOFF_ISO,
        "experiment_id": EXPERIMENT_ID,
        "immutable": True,
        "rule": "market_ts must be strictly greater than cutoff; ingest time is not a substitute",
        "commit": commit,
        "created_at": datetime.now(UTC).isoformat(),
    }
    payload["sha256"] = sha256_json(payload)
    path = MANIFESTS_DIR / "cutoff_manifest.json"
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing.get("FUTURE_UNSEEN_CUTOFF") != FUTURE_UNSEEN_CUTOFF_ISO:
            raise FutureUnseenProtectionError("cutoff manifest already frozen with different value")
        return path
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def load_all_validated_records() -> list[dict[str, Any]]:
    ensure_dirs()
    out: list[dict[str, Any]] = []
    for path in sorted(VALIDATED_DIR.glob("*.jsonl")):
        assert_no_forbidden_path(path)
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            assert_strictly_after_cutoff(rec["market_ts"])
            out.append(rec)
    return out
