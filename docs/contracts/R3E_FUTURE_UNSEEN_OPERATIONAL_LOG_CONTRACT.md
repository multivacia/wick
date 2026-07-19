# R3E Future-Unseen Operational Log Contract

```text
RELEASE = R3E
BACKLOG_ITEM = B5
SUBTASK = B5-P1
TASK_ID = PARALLEL-OPERATIONAL-HARDENING-001
DOCUMENT = OPERATIONAL_LOG_CONTRACT
FORMAT = JSON_LINES
PHASE = PREPARATION_ONLY
VALIDATE_AUTHORIZED = false
```

## Purpose

Stable, host-independent structured logging for collection automation and ops tooling.
Preferred sink: append-only JSON Lines (`.jsonl`).

## Required fields

| Field | Type | Notes |
|---|---|---|
| `timestamp_utc` | string (ISO-8601 UTC) | Always timezone-aware UTC |
| `run_id` | string \| null | Automation/collection run id when applicable |
| `event` | string | Stable event name (e.g. `cycle_start`, `lock_status`, `backup_verify`) |
| `severity` | string | `DEBUG` \| `INFO` \| `WARNING` \| `ERROR` \| `CRITICAL` |
| `status` | string | Operational status for the event |
| `host_id` | string \| null | Opaque host identifier; never invent when unknown |
| `process_id` | integer \| null | OS pid |
| `store_path` | string \| null | Logical/relative path preferred |
| `report_path` | string \| null | Path to related report artifact |
| `lock_status` | string \| null | `ABSENT` \| `ACTIVE` \| `STALE` \| `INVALID` \| null |
| `accepted_count` | integer \| null | Observations accepted this event/run |
| `rejected_count` | integer \| null | Observations rejected this event/run |
| `store_before` | integer \| null | Store observation count before |
| `store_after` | integer \| null | Store observation count after |
| `readiness_status` | string \| null | `READY` \| `NOT_READY` \| `BLOCKED` \| null |
| `readiness_reason` | string \| null | Operational reason code only |
| `duration_ms` | integer \| null | Event duration |
| `exit_code` | integer \| null | Process/command exit code |
| `failure_category` | string \| null | From failure taxonomy |
| `message` | string | Short human-readable summary; no secrets |

## Rules

1. JSON Lines preferred (`\n`-delimited objects).
2. No secrets, tokens, API keys, passwords, or credential material.
3. No full environment dump.
4. Stable field names; additive evolution only (never rename/remove without version bump).
5. UTC timestamps only.
6. Do not log scientific effect metrics, economic interpretation, or validate outputs.
7. `failure_category` values must come from `docs/operations/R3E_FUTURE_UNSEEN_FAILURE_TAXONOMY.md`.
8. Backward-compatible: unknown extra fields allowed for consumers that ignore them.

## Forbidden content examples

```text
api_key
Authorization
password
token
secret
AWS_SECRET
BINANCE_API_SECRET
full os.environ dump
effect_size
p_value
economic_interpretation
validate decision payloads beyond operational denial flags
```

## Minimal example

```json
{"timestamp_utc":"2026-07-19T00:00:00+00:00","run_id":"fu_auto_example","event":"cycle_complete","severity":"INFO","status":"COMPLETE","host_id":null,"process_id":1234,"store_path":"data/future_unseen","report_path":"reports/r3e_future_unseen/automation_runs/fu_auto_example/cycle_report.json","lock_status":"ABSENT","accepted_count":2,"rejected_count":0,"store_before":10,"store_after":12,"readiness_status":"NOT_READY","readiness_reason":"WINDOW_INCOMPLETE","duration_ms":1200,"exit_code":0,"failure_category":null,"message":"automation cycle complete"}
```

## Implementation note

Python helper: `wick.r3e.future_unseen.ops_hardening.build_operational_log_event`.
Existing `automation_events.jsonl` remains valid; new fields may be added additively.
