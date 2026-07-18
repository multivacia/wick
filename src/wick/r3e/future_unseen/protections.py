"""Hard-fail protections for future-unseen final validation."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from wick.r3e.future_unseen.config import (
    FORBIDDEN_DATA_ROOTS,
    FUTURE_UNSEEN_CUTOFF,
    GATE_APPROVED,
    PROTOCOL_REF,
)
from wick.r3e.future_unseen.hashing import verify_file_hash


class FutureUnseenProtectionError(RuntimeError):
    """Mandatory failure for protocol / integrity violations."""


def parse_market_ts(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        dt = value
    else:
        text = value.strip()
        if text.endswith("Z"):
            text = text[:-1] + "+00:00"
        dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        raise FutureUnseenProtectionError("market timestamp must be timezone-aware UTC")
    return dt.astimezone(FUTURE_UNSEEN_CUTOFF.tzinfo)


def assert_strictly_after_cutoff(
    market_ts: str | datetime, *, cutoff: datetime | None = None
) -> datetime:
    cut = cutoff or FUTURE_UNSEEN_CUTOFF
    dt = parse_market_ts(market_ts)
    if dt <= cut:
        raise FutureUnseenProtectionError(
            f"market timestamp {dt.isoformat()} is not strictly after cutoff {cut.isoformat()}"
        )
    return dt


def assert_no_forbidden_path(path: Path | str) -> None:
    text = str(path).replace("\\", "/")
    for root in FORBIDDEN_DATA_ROOTS:
        if root in text:
            raise FutureUnseenProtectionError(
                f"forbidden dataset root referenced: {root} in {text}"
            )


def assert_protocol_unchanged(executed: dict[str, Any]) -> None:
    for key, expected in PROTOCOL_REF.items():
        if key not in executed:
            raise FutureUnseenProtectionError(f"missing protocol field: {key}")
        if executed[key] != expected:
            raise FutureUnseenProtectionError(
                f"protocol drift on {key}: executed={executed[key]!r} frozen={expected!r}"
            )


def assert_manifest_hashes(files: list[dict[str, Any]]) -> None:
    for entry in files:
        path = Path(entry["path"])
        if not path.is_file():
            raise FutureUnseenProtectionError(f"manifest file missing: {path}")
        verify_file_hash(path, entry["sha256"])


def assert_sufficient_sample(*, n_oos: int, minimum: int) -> None:
    if n_oos < minimum:
        raise FutureUnseenProtectionError(f"insufficient OOS sample: n={n_oos} < minimum={minimum}")


def assert_r4_not_opened(*, gate: str, economic_ok: bool, audit: str) -> None:
    if gate == GATE_APPROVED and economic_ok and audit == "APPROVED":
        return
    # Any attempt to claim R4 unlocked otherwise is a hard fail when checked
    raise FutureUnseenProtectionError(
        "R4 remains BLOCKED unless R3E_GATE=APPROVED, "
        "ECONOMIC_INTERPRETATION_ALLOWED=true, and R3E_FUTURE_UNSEEN_AUDIT=APPROVED"
    )


def assert_economic_interpretation_locked(allowed: bool, *, final_decision_made: bool) -> None:
    if allowed and not final_decision_made:
        raise FutureUnseenProtectionError(
            "cannot mark ECONOMIC_INTERPRETATION_ALLOWED=true before final gate decision"
        )
