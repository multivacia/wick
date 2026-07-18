"""Append-only storage for operational historical backfill artifacts."""

from __future__ import annotations

import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.hashing import sha256_file, sha256_json
from wick.r3e.operational_backfill.config import CLASSIFICATION, EXPERIMENT_ID
from wick.r3e.operational_backfill.paths import assert_not_official_path, ensure_dirs
from wick.r3e.operational_backfill.schema import (
    StructuralValidationError,
    validate_structural_record,
)


@dataclass
class Rejection:
    reason: str
    record: dict[str, Any] = field(default_factory=dict)


@dataclass
class StoreBatchResult:
    batch_id: str
    accepted: int
    rejected: int
    rejections: list[Rejection]
    raw_path: str
    validated_path: str
    manifest_path: str
    file_sha256: str
    batch_sha256: str
    series_counts: dict[str, int]
    first_market_ts: str | None
    last_market_ts: str | None
    duplicates: int
    revisions: int


def _series_key(symbol: str, timeframe: str, source: str) -> str:
    return f"{source}|{symbol}|{timeframe}"


def _index_path(manifests: Path) -> Path:
    return manifests / "observation_index.json"


def _load_index(manifests: Path) -> dict[str, dict[str, Any]]:
    path = _index_path(manifests)
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _save_index(manifests: Path, index: dict[str, dict[str, Any]]) -> None:
    path = _index_path(manifests)
    assert_not_official_path(path)
    path.write_text(json.dumps(index, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def store_batch(
    records: list[dict[str, Any]],
    *,
    output: Path | str | None = None,
    batch_id: str | None = None,
    origin: str = "operational-backfill-collect",
    series_meta: dict[str, Any] | None = None,
) -> StoreBatchResult:
    roots = ensure_dirs(output)
    assert_not_official_path(roots["raw"])
    assert_not_official_path(roots["validated"])
    assert_not_official_path(roots["manifests"])

    batch_id = (
        batch_id or f"ob_{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}_{uuid.uuid4().hex[:8]}"
    )
    now = datetime.now(UTC).isoformat()
    index = _load_index(roots["manifests"])

    accepted: list[dict[str, Any]] = []
    rejections: list[Rejection] = []
    duplicates = 0
    revisions = 0

    for raw in records:
        try:
            rec = validate_structural_record(raw)
            key = (
                _series_key(rec["symbol"], rec["timeframe"], rec["source"]) + "|" + rec["market_ts"]
            )
            if key in index:
                prev = index[key]
                same = all(
                    abs(float(prev[k]) - float(rec[k])) < 1e-12
                    for k in ("open", "high", "low", "close", "volume")
                )
                if same:
                    duplicates += 1
                    raise StructuralValidationError("duplicate observation (identical OHLCV)")
                if int(rec["revision"]) <= int(prev.get("revision", 1)):
                    raise StructuralValidationError(
                        "provider correction requires incremented revision; silent update forbidden"
                    )
                revisions += 1
            rec["ingested_at"] = now
            rec["record_id"] = str(uuid.uuid4())
            accepted.append(rec)
            index[key] = {
                "open": rec["open"],
                "high": rec["high"],
                "low": rec["low"],
                "close": rec["close"],
                "volume": rec["volume"],
                "revision": rec["revision"],
                "record_id": rec["record_id"],
                "batch_id": batch_id,
                "ingested_at": now,
                "market_ts": rec["market_ts"],
            }
        except (StructuralValidationError, KeyError, TypeError, ValueError) as exc:
            rejections.append(Rejection(reason=str(exc), record=dict(raw)))

    raw_path = roots["raw"] / f"{batch_id}.jsonl"
    val_path = roots["validated"] / f"{batch_id}.jsonl"
    lines = [json.dumps(r, sort_keys=True) for r in accepted]
    payload = "\n".join(lines) + ("\n" if lines else "")
    raw_path.write_text(payload, encoding="utf-8")
    val_path.write_text(payload, encoding="utf-8")
    file_hash = sha256_file(val_path)

    series_counts: dict[str, int] = {}
    for r in accepted:
        sk = _series_key(r["symbol"], r["timeframe"], r["source"])
        series_counts[sk] = series_counts.get(sk, 0) + 1

    first_ts = min((r["market_ts"] for r in accepted), default=None)
    last_ts = max((r["market_ts"] for r in accepted), default=None)

    manifest = {
        "batch_id": batch_id,
        "experiment_id": EXPERIMENT_ID,
        "origin": origin,
        "created_at": now,
        "accepted": len(accepted),
        "rejected": len(rejections),
        "rejections": [asdict(x) for x in rejections],
        "duplicates_rejected": duplicates,
        "revisions_accepted": revisions,
        "series_counts": series_counts,
        "first_market_ts": first_ts,
        "last_market_ts": last_ts,
        "raw_path": str(raw_path),
        "validated_path": str(val_path),
        "file_sha256": file_hash,
        "append_only": True,
        "silent_overwrite_forbidden": True,
        "classification": CLASSIFICATION,
        "series_meta": series_meta or {},
    }
    manifest["batch_sha256"] = sha256_json(manifest)
    man_path = roots["manifests"] / f"batch_{batch_id}.json"
    man_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    _save_index(roots["manifests"], index)

    return StoreBatchResult(
        batch_id=batch_id,
        accepted=len(accepted),
        rejected=len(rejections),
        rejections=rejections,
        raw_path=str(raw_path),
        validated_path=str(val_path),
        manifest_path=str(man_path),
        file_sha256=file_hash,
        batch_sha256=manifest["batch_sha256"],
        series_counts=series_counts,
        first_market_ts=first_ts,
        last_market_ts=last_ts,
        duplicates=duplicates,
        revisions=revisions,
    )


def load_all_validated(output: Path | str | None = None) -> list[dict[str, Any]]:
    roots = ensure_dirs(output)
    out: list[dict[str, Any]] = []
    for path in sorted(roots["validated"].glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out
