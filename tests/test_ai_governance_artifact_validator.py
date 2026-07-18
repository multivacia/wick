"""Tests for offline AI governance artifact validator."""

from __future__ import annotations

from wick.ai_governance.artifact_validator import validate_artifact_text


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
