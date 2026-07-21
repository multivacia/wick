# UX-R1-I6K — Host/Scheduler Screen Implementation Spec

```text
RELEASE = UX-R1
INCREMENT = I6K
TASK_ID = HOST-SCHEDULER-SCREEN-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
IMPACT = docs/ai-impact/UX-R1-I6K-HOST-SCHEDULER-SCREEN-IMPLEMENTATION_IMPACT_ASSESSMENT.md
ROUTE = /operations/host-scheduler
SCREEN = Host e Automação
FIXTURE_ID = current_project_state_illustrative
READ_ONLY = true
FIXTURE_BACKED = true
NO_VISIBLE_FIXTURE_SELECTOR = true
```

## Objective

Deliver the fixture-backed, read-only **Host e Automação** product screen at `/operations/host-scheduler`, consuming merged `HostSchedulerViewModel` fields only. Explain known operational state without implying host discovery, scheduler installation or activation.

## Behavior

Answer in plain language first:

1. What is the host discovery state?
2. Is operational debt open?
3. What is the scheduler state?
4. Which known environment fields are available (none fabricated)?
5. Is cadence known?
6. What is the last known cycle?
7. Is next expected run known?
8. What blocks activation?
9. What is the next safe human action?

## Sections

```text
PageHeader
SyntheticDataNotice
HostDiscoveryStatus
OperationalDebtNotice
SchedulerStatus
KnownEnvironmentDetails
CadenceState
LastKnownRun
NextExpectedRun
BlockingReason
NextSafeHumanAction
EvidenceReference
PartialUnknownState
```

Visible synthetic labels: `Dados ilustrativos`, `Synthetic fixture`, `Não representa evidência operacional real`, plus activation disclaimer.

Official debt wording when open:

```text
Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.
```

## Semantics

```text
DEFERRED != COMPLETE
DEFERRED != FAILED
BLOCKED != FAULT
UNKNOWN != OFFLINE
NOT_CONFIGURED != FAILED
SCHEDULER_INACTIVE != SCHEDULER_FAILED
MISSING != FALSE
MISSING != ZERO
ILLUSTRATIVE != OPERATIONAL
```

Red reserved for confirmed fault only. Hostname, IP, paths, cadence and next-run remain unavailable when absent from the ViewModel.

## Architecture

```text
web/src/screens/host-scheduler/**
AppRoutes: replace host-scheduler placeholder only
Nav label: Host e Automação
Product fixture remains current_project_state_illustrative
No ACTIVE/COMPLETE product fixture
```

## Out of scope

Real host discovery, credentials, IPs, sensitive paths, scheduler activation/install/configure, start/stop/retry/run-now/collection/validation controls, real data, new dependencies, scientific state change.
