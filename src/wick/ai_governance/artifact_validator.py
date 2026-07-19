"""Structural validator for AI governance review/implementation artifacts.

Offline only: no network, no scientific pipeline execution.

Includes the G1 pre-implementation impact-assessment gate.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b", re.IGNORECASE)

ALLOWED_REVIEW_STATUS = {"PENDING", "APPROVED", "CHANGES_REQUIRED", "BLOCKED"}
ALLOWED_MERGE_STATUS = {"BLOCKED", "AWAITING_HUMAN_AUTHORIZATION", "MERGED"}
ALLOWED_CHANGE_RISK = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
ALLOWED_IMPACT_STATUS = {
    "NOT_REQUIRED",
    "DRAFT",
    "PENDING_REVIEW",
    "APPROVED",
    "CHANGES_REQUIRED",
    "BLOCKED",
}

# Merge commit of this gate PR becomes the effective date; until then use sentinel.
ENFORCEMENT_EFFECTIVE_FROM_SENTINEL = "AFTER_MERGE_OF_IMPACT_ASSESSMENT_GATE"

REQUIRED_ANY = {
    "TASK_ID": ("TASK_ID",),
    "REVIEW_OR_IMPL_STATUS": ("REVIEW_STATUS", "IMPLEMENTATION_STATUS", "CURRENT_REVIEW_STATUS"),
    "MERGE": ("MERGE_STATUS", "CURRENT_MERGE_STATUS"),
    "ANTI_VALIDATE": ("VALIDATION_COMMAND_EXECUTED",),
    "ANTI_PEEK": ("EFFECT_PEEKING_PERFORMED",),
}

REQUIRED_IMPACT_FIELDS = (
    "TASK_ID",
    "CHANGE_RISK",
    "IMPACT_ASSESSMENT_STATUS",
    "IMPLEMENTATION_AUTHORIZED",
    "REPOSITORY",
    "BASE_BRANCH",
    "BASE_SHA",
    "ANALYZED_AT",
    "ANALYZED_BY",
)

REQUIRED_IMPACT_SECTION_MARKERS = (
    "objetivo",
    "contexto técnico",
    "componentes afetados",
    "arquivos previstos",
    "contratos e interfaces",
    "persistência e dados",
    "concorrência, locks e idempotência",
    "segurança",
    "observabilidade",
    "operação",
    "rollback",
    "compatibilidade",
    "testes necessários",
    "alternativas consideradas",
    "riscos",
    "questões abertas",
    "decisão arquitetural recomendada",
    "critérios para autorizar implementação",
)

FORBIDDEN_PLACEHOLDERS = (
    "TODO",
    "TBD",
    "TO_BE_FILLED",
    "FILL_ME",
    "FIXME",
    "<PENDING>",
)

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


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.lower() in {"true", "1", "yes"}


def _documentation_merge_recommended(block: str) -> bool:
    """Docs-only merge recommendation without executable implementation auth.

    When true, APPROVED MEDIUM/HIGH/CRITICAL impact may keep
    IMPLEMENTATION_AUTHORIZED=false (no ViewModel/fixture/screen/code work).
    """
    if _truthy(_field(block, "DOCUMENTATION_MERGE_RECOMMENDED")):
        return True
    if _truthy(_field(block, "I6A_DOCUMENTATION_MERGE_RECOMMENDED")):
        return True
    decision = _field(block, "DATA_CONTRACT_DECISION")
    return decision in {
        "AUTHORIZED_WITH_CONDITIONS",
        "AUTHORIZED_FOR_I6A_MERGE",
    }


def _is_legacy(block: str) -> bool:
    return _truthy(_field(block, "LEGACY_PRE_IMPACT_GATE"))


def _is_impact_assessment_path(path: str) -> bool:
    name = Path(path).name.upper()
    return "IMPACT_ASSESSMENT" in name


def _requires_independent_impact(risk: str | None) -> bool:
    return risk in {"MEDIUM", "HIGH", "CRITICAL"}


def _heading_blob(text: str) -> str:
    headings = re.findall(r"^#{1,6}\s+(.+)$", text, flags=re.MULTILINE)
    return "\n".join(h.strip().lower() for h in headings)


def _has_section(text: str, marker: str) -> bool:
    blob = _heading_blob(text)
    if marker in blob:
        return True
    # Also accept numbered forms in body headings like "1. Objetivo"
    return (
        re.search(rf"^#{{1,6}}\s*\d+\.\s*{re.escape(marker)}\b", text, flags=re.I | re.M)
        is not None
    )


def validate_impact_assessment_text(text: str, *, path: str = "<memory>") -> list[ValidationIssue]:
    """Validate a dedicated impact-assessment artifact."""
    issues: list[ValidationIssue] = []
    block = _meta_block(text)

    for name in REQUIRED_IMPACT_FIELDS:
        if _field(block, name) is None:
            issues.append(ValidationIssue(path, "error", f"missing impact field {name}"))

    risk = _field(block, "CHANGE_RISK")
    if risk is not None and risk not in ALLOWED_CHANGE_RISK:
        issues.append(ValidationIssue(path, "error", f"invalid CHANGE_RISK={risk}"))

    status = _field(block, "IMPACT_ASSESSMENT_STATUS")
    if status is not None and status not in ALLOWED_IMPACT_STATUS:
        issues.append(ValidationIssue(path, "error", f"invalid IMPACT_ASSESSMENT_STATUS={status}"))

    authorized = _field(block, "IMPLEMENTATION_AUTHORIZED")
    if authorized is not None and authorized.lower() not in {
        "true",
        "false",
        "0",
        "1",
        "yes",
        "no",
    }:
        issues.append(
            ValidationIssue(path, "error", f"invalid IMPLEMENTATION_AUTHORIZED={authorized}")
        )

    if status == "BLOCKED" and _truthy(authorized):
        issues.append(
            ValidationIssue(
                path,
                "error",
                "IMPLEMENTATION_AUTHORIZED cannot be true when IMPACT_ASSESSMENT_STATUS=BLOCKED",
            )
        )

    if status in {"DRAFT", "PENDING_REVIEW", "CHANGES_REQUIRED"} and _truthy(authorized):
        issues.append(
            ValidationIssue(
                path,
                "error",
                "IMPLEMENTATION_AUTHORIZED cannot be true before IMPACT_ASSESSMENT_STATUS=APPROVED",
            )
        )

    if (
        status == "APPROVED"
        and risk in {"MEDIUM", "HIGH", "CRITICAL"}
        and not _truthy(authorized)
        and not _documentation_merge_recommended(block)
    ):
        issues.append(
            ValidationIssue(
                path,
                "error",
                "APPROVED MEDIUM/HIGH/CRITICAL impact requires IMPLEMENTATION_AUTHORIZED=true",
            )
        )

    for marker in REQUIRED_IMPACT_SECTION_MARKERS:
        if not _has_section(text, marker):
            issues.append(
                ValidationIssue(path, "error", f"missing required impact section: {marker}")
            )

    if status == "APPROVED":
        for ph in FORBIDDEN_PLACEHOLDERS:
            if re.search(rf"\b{re.escape(ph)}\b", block):
                issues.append(
                    ValidationIssue(
                        path, "error", f"forbidden placeholder in approved impact: {ph}"
                    )
                )

    base_sha = _field(block, "BASE_SHA")
    if (
        base_sha
        and not SHA_RE.fullmatch(base_sha.split()[0])
        and base_sha not in {ENFORCEMENT_EFFECTIVE_FROM_SENTINEL, "TO_BE_RECORDED_EXTERNALLY"}
    ):
        issues.append(ValidationIssue(path, "error", "BASE_SHA is not a valid SHA-like value"))

    return issues


def _validate_impact_gate_on_artifact(text: str, block: str, *, path: str) -> list[ValidationIssue]:
    """Apply impact gate rules to specs/reviews/implementation reports."""
    issues: list[ValidationIssue] = []
    if _is_legacy(block):
        return issues

    risk = _field(block, "CHANGE_RISK")
    impact_status = _field(block, "IMPACT_ASSESSMENT_STATUS")
    authorized = _field(block, "IMPLEMENTATION_AUTHORIZED")

    # Historical artifacts without the new fields remain compatible.
    if risk is None and impact_status is None and authorized is None:
        return issues

    if risk is not None and risk not in ALLOWED_CHANGE_RISK:
        issues.append(ValidationIssue(path, "error", f"invalid CHANGE_RISK={risk}"))

    if impact_status is not None and impact_status not in ALLOWED_IMPACT_STATUS:
        issues.append(
            ValidationIssue(path, "error", f"invalid IMPACT_ASSESSMENT_STATUS={impact_status}")
        )

    if _requires_independent_impact(risk):
        if impact_status is None:
            issues.append(
                ValidationIssue(
                    path,
                    "error",
                    f"CHANGE_RISK={risk} requires IMPACT_ASSESSMENT_STATUS and independent impact file",
                )
            )
        elif impact_status != "APPROVED":
            issues.append(
                ValidationIssue(
                    path,
                    "error",
                    f"CHANGE_RISK={risk} requires IMPACT_ASSESSMENT_STATUS=APPROVED before implementation",
                )
            )
        if not _truthy(authorized) and not _documentation_merge_recommended(block):
            issues.append(
                ValidationIssue(
                    path,
                    "error",
                    f"CHANGE_RISK={risk} requires IMPLEMENTATION_AUTHORIZED=true before implementation",
                )
            )
        # Prefer an explicit path reference when claiming authorization
        if "docs/ai-impact/" not in text and "IMPACT_ASSESSMENT.md" not in text.upper():
            issues.append(
                ValidationIssue(
                    path,
                    "error",
                    "MEDIUM/HIGH/CRITICAL change must reference docs/ai-impact/<TASK_ID>_IMPACT_ASSESSMENT.md",
                )
            )

    if risk == "LOW":
        if impact_status is None:
            issues.append(
                ValidationIssue(
                    path,
                    "warning",
                    "LOW risk should set IMPACT_ASSESSMENT_STATUS=NOT_REQUIRED (simplified in-spec analysis)",
                )
            )
        elif impact_status not in {"NOT_REQUIRED", "APPROVED"}:
            issues.append(
                ValidationIssue(
                    path,
                    "error",
                    "LOW risk IMPACT_ASSESSMENT_STATUS must be NOT_REQUIRED or APPROVED",
                )
            )

    if impact_status == "BLOCKED" and _truthy(authorized):
        issues.append(
            ValidationIssue(
                path,
                "error",
                "IMPLEMENTATION_AUTHORIZED cannot be true when IMPACT_ASSESSMENT_STATUS=BLOCKED",
            )
        )

    impl_status = _field(block, "IMPLEMENTATION_STATUS")
    if (
        impl_status in {"IN_PROGRESS", "COMPLETE"}
        and _requires_independent_impact(risk)
        and (impact_status != "APPROVED" or not _truthy(authorized))
    ):
        issues.append(
            ValidationIssue(
                path,
                "error",
                "implementation before approved impact assessment is forbidden",
            )
        )

    return issues


def validate_artifact_text(text: str, *, path: str = "<memory>") -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    block = _meta_block(text)

    if _is_impact_assessment_path(path):
        return validate_impact_assessment_text(text, path=path)

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
    for name in (
        "HEAD_SHA_AT_REVIEW",
        "CURRENT_PR_HEAD",
        "BASE_SHA_AT_REVIEW",
        "HEAD_COMMIT",
        "BASE_SHA",
        "IMPLEMENTATION_HEAD",
    ):
        value = _field(block, name)
        if (
            value
            and not SHA_RE.fullmatch(value.split()[0])
            and value not in {"TO_BE_RECORDED_EXTERNALLY", ENFORCEMENT_EFFECTIVE_FROM_SENTINEL}
        ):
            issues.append(ValidationIssue(path, "error", f"{name} is not a valid SHA-like value"))

    issues.extend(_validate_impact_gate_on_artifact(text, block, path=path))
    return issues


def validate_paths(paths: Iterable[Path]) -> list[ValidationIssue]:
    out: list[ValidationIssue] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        out.extend(validate_artifact_text(text, path=str(path)))
    return out


def validate_task_bundle(
    *,
    impact_text: str | None = None,
    impact_path: str = "docs/ai-impact/TASK_IMPACT_ASSESSMENT.md",
    implementation_text: str | None = None,
    implementation_path: str = "reports/ai-implementation/TASK_IMPLEMENTATION_REPORT.md",
) -> list[ValidationIssue]:
    """Cross-check impact vs implementation for the same task."""
    issues: list[ValidationIssue] = []
    if impact_text is not None:
        issues.extend(validate_impact_assessment_text(impact_text, path=impact_path))
    if implementation_text is not None:
        issues.extend(validate_artifact_text(implementation_text, path=implementation_path))

    if impact_text is None or implementation_text is None:
        return issues

    impact_block = _meta_block(impact_text)
    impl_block = _meta_block(implementation_text)
    if _is_legacy(impl_block):
        return issues

    risk = _field(impl_block, "CHANGE_RISK") or _field(impact_block, "CHANGE_RISK")
    impact_status = _field(impact_block, "IMPACT_ASSESSMENT_STATUS")
    authorized = _field(impact_block, "IMPLEMENTATION_AUTHORIZED")
    impl_status = _field(impl_block, "IMPLEMENTATION_STATUS")

    if (
        _requires_independent_impact(risk)
        and (impact_status != "APPROVED" or not _truthy(authorized))
        and impl_status in {"IN_PROGRESS", "COMPLETE"}
    ):
        issues.append(
            ValidationIssue(
                implementation_path,
                "error",
                "implementation before approved impact assessment is forbidden",
            )
        )
    return issues
