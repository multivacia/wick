"""Tests for offline AI governance artifact validator."""

from __future__ import annotations

from wick.ai_governance.artifact_validator import (
    validate_artifact_text,
    validate_impact_assessment_text,
    validate_task_bundle,
)

_IMPACT_SECTIONS = "\n".join(
    f"## {i}. {title}\n\nconteudo\n"
    for i, title in enumerate(
        [
            "Objetivo",
            "Contexto técnico",
            "Componentes afetados",
            "Arquivos previstos",
            "Contratos e interfaces",
            "Persistência e dados",
            "Concorrência, locks e idempotência",
            "Segurança",
            "Observabilidade",
            "Operação",
            "Rollback",
            "Compatibilidade",
            "Testes necessários",
            "Alternativas consideradas",
            "Riscos",
            "Questões abertas",
            "Decisão arquitetural recomendada",
            "Critérios para autorizar implementação",
        ],
        start=1,
    )
)


def _approved_impact(**overrides: str) -> str:
    fields = {
        "TASK_ID": "DEMO-HIGH-001",
        "CHANGE_RISK": "HIGH",
        "IMPACT_ASSESSMENT_STATUS": "APPROVED",
        "IMPLEMENTATION_AUTHORIZED": "true",
        "REPOSITORY": "multivacia/wick",
        "BASE_BRANCH": "main",
        "BASE_SHA": "fd4cf1df3961a2411c3e367fd675b89ef05858a6",
        "ANALYZED_AT": "2026-07-18T20:06:48Z",
        "ANALYZED_BY": "tester",
    }
    fields.update(overrides)
    meta = "\n".join(f"{k} = {v}" for k, v in fields.items())
    return f"```text\n{meta}\n```\n\n{_IMPACT_SECTIONS}\n"


def test_accepts_consistent_review_metadata():
    text = """
```text
TASK_ID = DEMO-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
HEAD_SHA_AT_REVIEW = 69636de475c1985d50281245a8279605c6b37d5a
CURRENT_PR_HEAD = 69636de475c1985d50281245a8279605c6b37d5a
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
TESTS_EXECUTED_THIS_REVIEW = 33 PASSED
```
A aprovação técnica/documental **não** autoriza merge automático.
"""
    issues = validate_artifact_text(text)
    assert not [i for i in issues if i.severity == "error"]


def test_rejects_head_mismatch_without_reconciliation():
    text = """
```text
TASK_ID = DEMO-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
HEAD_SHA_AT_REVIEW = 25135e15d2a9339370542d00013dfae00df34a1c
CURRENT_PR_HEAD = 69636de475c1985d50281245a8279605c6b37d5a
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
"""
    issues = validate_artifact_text(text)
    assert any("without reconciliation" in i.message for i in issues)


def test_accepts_head_mismatch_with_reconciliation():
    text = """
```text
TASK_ID = DEMO-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
HEAD_SHA_AT_REVIEW = 69636de475c1985d50281245a8279605c6b37d5a
CURRENT_PR_HEAD = 69636de475c1985d50281245a8279605c6b37d5a
PREVIOUSLY_REVIEWED_HEAD = 25135e15d2a9339370542d00013dfae00df34a1c
COMMITS_RECONCILED = abc1234
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
"""
    issues = validate_artifact_text(text)
    assert not [i for i in issues if i.severity == "error"]


def test_rejects_validate_executed_true():
    text = """
```text
TASK_ID = DEMO-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = BLOCKED
VALIDATION_COMMAND_EXECUTED = true
EFFECT_PEEKING_PERFORMED = false
```
"""
    issues = validate_artifact_text(text)
    assert any("VALIDATION_COMMAND_EXECUTED" in i.message for i in issues)


def test_accepts_negated_auto_merge_with_markdown_emphasis():
    text = """
```text
TASK_ID = DEMO-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
A aprovação técnica/documental **não** autoriza merge automático.
"""
    issues = validate_artifact_text(text)
    assert not [i for i in issues if i.severity == "error"]


def test_low_risk_without_independent_impact_ok():
    text = """
```text
TASK_ID = DEMO-LOW-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CHANGE_RISK = LOW
IMPACT_ASSESSMENT_STATUS = NOT_REQUIRED
IMPLEMENTATION_AUTHORIZED = true
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
"""
    issues = validate_artifact_text(text)
    assert not [i for i in issues if i.severity == "error"]


def test_medium_without_impact_errors():
    text = """
```text
TASK_ID = DEMO-MED-001
IMPLEMENTATION_STATUS = COMPLETE
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CHANGE_RISK = MEDIUM
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
"""
    issues = validate_artifact_text(text)
    assert any("IMPACT_ASSESSMENT_STATUS" in i.message for i in issues if i.severity == "error")
    assert any("IMPLEMENTATION_AUTHORIZED" in i.message for i in issues if i.severity == "error")


def test_high_draft_impact_errors():
    text = """
```text
TASK_ID = DEMO-HIGH-001
IMPLEMENTATION_STATUS = IN_PROGRESS
MERGE_STATUS = BLOCKED
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = DRAFT
IMPLEMENTATION_AUTHORIZED = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
Refs docs/ai-impact/DEMO-HIGH-001_IMPACT_ASSESSMENT.md
"""
    issues = validate_artifact_text(text)
    assert any("APPROVED" in i.message for i in issues if i.severity == "error")
    assert any("before approved impact" in i.message for i in issues if i.severity == "error")


def test_high_approved_impact_valid():
    text = """
```text
TASK_ID = DEMO-HIGH-001
IMPLEMENTATION_STATUS = COMPLETE
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
Impact path: docs/ai-impact/DEMO-HIGH-001_IMPACT_ASSESSMENT.md
"""
    issues = validate_artifact_text(text)
    assert not [i for i in issues if i.severity == "error"]


def test_implementation_before_approval_bundle_error():
    impact = _approved_impact(
        IMPACT_ASSESSMENT_STATUS="DRAFT",
        IMPLEMENTATION_AUTHORIZED="false",
    )
    impl = """
```text
TASK_ID = DEMO-HIGH-001
IMPLEMENTATION_STATUS = COMPLETE
MERGE_STATUS = BLOCKED
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = DRAFT
IMPLEMENTATION_AUTHORIZED = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
docs/ai-impact/DEMO-HIGH-001_IMPACT_ASSESSMENT.md
"""
    issues = validate_task_bundle(impact_text=impact, implementation_text=impl)
    assert any("before approved impact" in i.message for i in issues if i.severity == "error")


def test_impact_missing_fields_error():
    text = """
```text
TASK_ID = DEMO-HIGH-001
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = DRAFT
```
"""
    issues = validate_impact_assessment_text(
        text, path="docs/ai-impact/DEMO-HIGH-001_IMPACT_ASSESSMENT.md"
    )
    assert any("missing impact field" in i.message for i in issues)


def test_impact_missing_sections_error():
    text = """
```text
TASK_ID = DEMO-HIGH-001
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = DRAFT
IMPLEMENTATION_AUTHORIZED = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = fd4cf1df3961a2411c3e367fd675b89ef05858a6
ANALYZED_AT = 2026-07-18T20:06:48Z
ANALYZED_BY = tester
```

## 1. Objetivo

somente uma seção
"""
    issues = validate_impact_assessment_text(
        text, path="docs/ai-impact/DEMO-HIGH-001_IMPACT_ASSESSMENT.md"
    )
    assert any("missing required impact section" in i.message for i in issues)


def test_blocked_status_forbids_authorization():
    text = _approved_impact(
        IMPACT_ASSESSMENT_STATUS="BLOCKED",
        IMPLEMENTATION_AUTHORIZED="true",
    )
    issues = validate_impact_assessment_text(
        text, path="docs/ai-impact/DEMO-HIGH-001_IMPACT_ASSESSMENT.md"
    )
    assert any("BLOCKED" in i.message for i in issues if i.severity == "error")


def test_legacy_pre_impact_gate_compatible():
    text = """
```text
TASK_ID = OLD-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = MERGED
LEGACY_PRE_IMPACT_GATE = true
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = DRAFT
IMPLEMENTATION_AUTHORIZED = false
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
"""
    issues = validate_artifact_text(text)
    assert not [i for i in issues if i.severity == "error"]


def test_historical_artifact_without_new_fields_still_valid():
    text = """
```text
TASK_ID = HIST-001
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```
"""
    issues = validate_artifact_text(text)
    assert not [i for i in issues if i.severity == "error"]


def test_approved_impact_file_valid():
    issues = validate_impact_assessment_text(
        _approved_impact(),
        path="docs/ai-impact/DEMO-HIGH-001_IMPACT_ASSESSMENT.md",
    )
    assert not [i for i in issues if i.severity == "error"]
