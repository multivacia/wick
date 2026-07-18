"""Structural validator for AI governance review/implementation artifacts.

Offline only: no network, no scientific pipeline execution.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b", re.IGNORECASE)

ALLOWED_REVIEW_STATUS = {"PENDING", "APPROVED", "CHANGES_REQUIRED", "BLOCKED"}
ALLOWED_MERGE_STATUS = {"BLOCKED", "AWAITING_HUMAN_AUTHORIZATION", "MERGED"}

FORBIDDEN_SCIENCE_KEYS = {
    "delta_candle",
    "m5_minus_m4",
    "p_value",
    "p_adj",
    "fdr",
    "mean_net",
    "sharpe",
    "pnl",
    "gate_decision",
}

REQUIRED_ANY = {
    "TASK_ID": ("TASK_ID",),
    "REVIEW_OR_IMPL_STATUS": ("REVIEW_STATUS", "IMPLEMENTATION_STATUS", "CURRENT_REVIEW_STATUS"),
    "MERGE": ("MERGE_STATUS", "CURRENT_MERGE_STATUS"),
    "ANTI_VALIDATE": ("VALIDATION_COMMAND_EXECUTED",),
    "ANTI_PEEK": ("EFFECT_PEEKING_PERFORMED",),
}


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    severity: str  # error|warning
    message: str


def _meta_block(text: str) -> str:
    m = re.search(r"```text\n(.*?)```", text, flags=re.DOTALL)
    return m.group(1) if m else text


def _field(block: str, name: str) -> str | None:
    m = re.search(rf"^{re.escape(name)}\s*=\s*(.+)$", block, flags=re.MULTILINE)
    if not m:
        return None
    return m.group(1).strip()


def validate_artifact_text(text: str, *, path: str = "<memory>") -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    block = _meta_block(text)

    for label, names in REQUIRED_ANY.items():
        if not any(_field(block, n) is not None for n in names):
            issues.append(
                ValidationIssue(path, "error", f"missing required field group {label}: {names}")
            )

    review = _field(block, "REVIEW_STATUS") or _field(block, "CURRENT_REVIEW_STATUS")
    if review and review not in ALLOWED_REVIEW_STATUS:
        issues.append(ValidationIssue(path, "error", f"invalid REVIEW_STATUS={review}"))

    merge = _field(block, "MERGE_STATUS") or _field(block, "CURRENT_MERGE_STATUS")
    if merge and merge not in ALLOWED_MERGE_STATUS:
        issues.append(ValidationIssue(path, "error", f"invalid MERGE_STATUS={merge}"))

    # Auto-merge authorization forbidden (ignore markdown emphasis between words)
    normalized = re.sub(r"[*_`]", "", text.lower())
    if "autoriza merge automático" in normalized and "não autoriza" not in normalized:
        issues.append(
            ValidationIssue(path, "error", "document appears to authorize automatic merge")
        )

    head = _field(block, "HEAD_SHA_AT_REVIEW") or _field(block, "HEAD_COMMIT")
    current = _field(block, "CURRENT_PR_HEAD")
    if (
        head
        and current
        and head != current
        and "PREVIOUSLY_REVIEWED_HEAD" not in block
        and "COMMITS_RECONCILED" not in block
    ):
        issues.append(
            ValidationIssue(
                path,
                "error",
                "CURRENT_PR_HEAD != HEAD_SHA_AT_REVIEW without reconciliation fields",
            )
        )

    # Distinguish declared vs executed tests when both mentioned loosely
    if "148 PASSED" in text and "TESTS_EXECUTED_THIS_REVIEW" in block:
        executed = _field(block, "TESTS_EXECUTED_THIS_REVIEW") or ""
        if "148" in executed and "DECLARED" not in text:
            issues.append(
                ValidationIssue(
                    path,
                    "warning",
                    "possible confusion between declared previous tests and executed tests",
                )
            )

    # Forbidden science keys as metadata assignments
    for key in FORBIDDEN_SCIENCE_KEYS:
        if re.search(rf"^{key}\s*=", block, flags=re.MULTILINE | re.IGNORECASE):
            issues.append(
                ValidationIssue(path, "error", f"forbidden scientific key assigned: {key}")
            )

    val = _field(block, "VALIDATION_COMMAND_EXECUTED")
    if val is not None and val.lower() not in {"false", "0", "no"}:
        issues.append(
            ValidationIssue(
                path, "error", "VALIDATION_COMMAND_EXECUTED must be false in ops reviews"
            )
        )

    peek = _field(block, "EFFECT_PEEKING_PERFORMED")
    if peek is not None and peek.lower() not in {"false", "0", "no"}:
        issues.append(
            ValidationIssue(path, "error", "EFFECT_PEEKING_PERFORMED must be false in ops reviews")
        )

    # SHA format when present
    for name in ("HEAD_SHA_AT_REVIEW", "CURRENT_PR_HEAD", "BASE_SHA_AT_REVIEW", "HEAD_COMMIT"):
        value = _field(block, name)
        if value and not SHA_RE.fullmatch(value.split()[0]):
            issues.append(ValidationIssue(path, "error", f"{name} is not a valid SHA-like value"))

    return issues


def validate_paths(paths: Iterable[Path]) -> list[ValidationIssue]:
    out: list[ValidationIssue] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        out.extend(validate_artifact_text(text, path=str(path)))
    return out
