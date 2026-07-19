# UX-R1 — Operational MVP State Matrix

```text
DOCUMENT = UX-R1-OPERATIONAL-MVP_STATE-MATRIX
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B3
TASK_ID = OPERATIONAL-MVP-SCREEN-CONTRACTS-001
UI_IMPLEMENTATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
EFFECTIVE_AT = 2026-07-19T13:45:00Z
```

Visual semantics (align UX-B2 draft): `NEUTRAL` | `INFO` | `ATTENTION` | `SUCCESS_OPS` | `ERROR` | `BLOCKED` | `DEFERRED`.

`SUCCESS_OPS` never means profit. `ATTENTION` covers `NOT_READY`.

---

## 1. Per-state contract (all screens)

| STATE | Plain-language message | Technical detail | Visual semantic | Allowed actions | Prohibited implications |
|-------|------------------------|------------------|-----------------|-----------------|-------------------------|
| LOADING | Carregando estado operacional… | Fetching index/artifacts | NEUTRAL | wait, cancel navigation | “sistema saudável” |
| EMPTY | Ainda não há dados para mostrar aqui. | No matching artifacts | INFO | refresh, open runbooks | failure |
| PARTIAL | Alguns dados estão disponíveis; outros não. | Subset of sources missing | ATTENTION | refresh, open available evidence | completeness |
| STALE | Estes dados podem estar desatualizados. | generated_at older than threshold | ATTENTION | manual refresh | live accuracy |
| UNAVAILABLE | Dado indisponível neste ambiente. | Source NOT_AVAILABLE | DEFERRED / INFO | refresh later, use fixture mode explicitly | failure of collection |
| ERROR | Falha real detectada. | hard_error / integrity fail / unreadable required artifact | ERROR | open failed execution, copy IDs, download evidence | profit/loss meaning |
| BLOCKED | Uma condição impede avançar. | blockers[] or activation blocked | BLOCKED | read checklist, no activate | NOT_READY confusion |
| NOT_READY | Ainda não há dados suficientes ou critérios atendidos. | readiness_status=NOT_READY | ATTENTION | continue monitoring collection | system failure; validate ready |
| READY | Critérios formais de prontidão atendidos. | readiness_status=READY | SUCCESS_OPS | still no validate CTA | validate authorized; profitable model |

---

## 2. Dimension axes

```text
collection = healthy | warning | unhealthy
readiness = ready | not_ready | blocked | error | unavailable
scheduler = inactive | deferred_blocked | active_forbidden_without_evidence
host = known | unknown | deferred
data = fresh | stale | unavailable
incident = open | closed_or_none
```

Current production-contract defaults:

```text
scheduler = deferred_blocked
host = deferred
operational_debt = OPEN
```

`scheduler=active` is **out of allowed live representation** until authorization evidence exists. Fixtures may include a labeled demo-only “would-be active” only if explicitly marked non-operational and still `scientific_interpretation_allowed=false` — **not** in the required eight scenarios; required scenarios keep scheduler not activated.

---

## 3. Combination matrix (overview-oriented)

| ID | collection | readiness | scheduler | host | data | incident | Overview banner | Next safe action (typical) | Notes |
|----|------------|-----------|-----------|------|------|----------|-----------------|----------------------------|-------|
| C01 | healthy | not_ready | deferred_blocked | deferred | fresh | none | ATTENTION + DEFERRED debt | Discovery no host / continuar coleta | Matches current repo snapshot family |
| C02 | healthy | not_ready | deferred_blocked | deferred | stale | none | ATTENTION + STALE | Atualizar artefatos / refresh | |
| C03 | healthy | not_ready | deferred_blocked | deferred | unavailable | none | PARTIAL/UNAVAILABLE | Usar host real ou fixtures | Cursor ephemeral |
| C04 | warning | not_ready | deferred_blocked | deferred | fresh | none | ATTENTION (warnings) | Investigar avisos na execução | provider_failures soft |
| C05 | unhealthy | not_ready | deferred_blocked | deferred | fresh | open | ERROR | Abrir última falha | collection_failure |
| C06 | unhealthy | error | deferred_blocked | deferred | fresh | open | ERROR | Integridade/store | hash/manifest fail |
| C07 | healthy | blocked | deferred_blocked | deferred | fresh | none | BLOCKED | Remover blocker (ops) | blockers[] present |
| C08 | healthy | ready | deferred_blocked | deferred | fresh | none | SUCCESS_OPS + BLOCKED validate | Não executar validate | fixture readiness_ready_but_validation_not_authorized |
| C09 | healthy | not_ready | deferred_blocked | known | fresh | none | ATTENTION | Continuar coleta; scheduler ainda blocked | discovery done, activation still blocked |
| C10 | healthy | not_ready | deferred_blocked | unknown | fresh | none | ATTENTION + host unknown | Rodar discovery | |
| C11 | healthy | unavailable | deferred_blocked | deferred | unavailable | none | PARTIAL | Gerar readiness report no host | |
| C12 | healthy | not_ready | deferred_blocked | deferred | fresh | open | ATTENTION + incident | Ver incidente (future B7) / execução | do not invent incident detail |
| C13 | — | — | deferred_blocked | deferred | — | none | EMPTY executions | Sem histórico ainda | no_execution_history |
| C14 | healthy | not_ready | deferred_blocked | deferred | partial | none | PARTIAL | Aceitar partial metadata | partial_metadata fixture |

---

## 4. Screen-specific state applications

### Visão Geral

| STATE | When | Message | Actions |
|-------|------|---------|---------|
| LOADING | initial fetch | Carregando resumo operacional… | none mutating |
| EMPTY | no automation_state and no readiness | Ainda não há resumo operacional. | refresh |
| PARTIAL | some blocks missing | Resumo parcial: host/scheduler/incidentes podem estar indisponíveis. | open available screens |
| STALE | overview sources &gt; 6h | Resumo pode estar desatualizado. | refresh |
| UNAVAILABLE | cannot read core JSON | Não foi possível ler o estado operacional neste ambiente. | switch to demo fixtures explicitly |
| ERROR | last fail or integrity | Há falha operacional real. | open Execuções |
| BLOCKED | blockers or activation attempt context | Há bloqueio operacional/científico. | read-only details |
| NOT_READY | readiness NOT_READY | Dados ainda não prontos para o gate formal. | continue collection narrative |
| READY | readiness READY | Critérios formais atendidos — validate não autorizado. | no validate |

### Execuções

| STATE | When | Message | Actions |
|-------|------|---------|---------|
| LOADING | listing | Carregando execuções… | — |
| EMPTY | zero run dirs | Nenhuma execução encontrada nas evidências. | refresh |
| PARTIAL | list ok, detail missing files | Execução parcial: alguns artefatos ausentes. | open available files |
| STALE | N/A list; detail if nested reports old | Evidências antigas. | refresh |
| UNAVAILABLE | reports root missing | Diretório de execuções indisponível. | — |
| ERROR | status FAILED / unreadable detail | Execução falhou ou evidência corrompida. | download evidence |
| BLOCKED | status BLOCKED | Ciclo bloqueado por regra operacional. | inspect blockers |
| NOT_READY | readiness fields on detail | Ciclo terminou com prontidão ainda incompleta. | link Readiness |
| READY | rare detail badge | Ciclo viu READY formal — validate não liberado. | no validate |

### Readiness

| STATE | When | Message | Actions |
|-------|------|---------|---------|
| LOADING | — | Carregando prontidão… | — |
| EMPTY | no report | Nenhuma avaliação de prontidão disponível. | — |
| PARTIAL | report missing series tables | Avaliação parcial. | — |
| STALE | generated_at old | Avaliação desatualizada. | refresh / re-run readiness on host (not via UI) |
| UNAVAILABLE | path missing | Relatório indisponível neste checkout. | — |
| ERROR | hash/manifest invalid or parse error | Falha de integridade ou leitura. | open technical expand |
| BLOCKED | blockers[] non-empty | Bloqueios impedem READY. | explain blockers |
| NOT_READY | status NOT_READY | Critérios ainda não atendidos. | show progress |
| READY | status READY | Critérios atendidos; validate bloqueado. | show scientific_safety |

### Host e Scheduler

| STATE | When | Message | Actions |
|-------|------|---------|---------|
| LOADING | — | Carregando host e automação… | — |
| EMPTY | no docs and no discovery | Sem metadados de host. | — |
| PARTIAL | docs present, discovery missing | Discovery pendente; templates podem existir. | open runbook |
| STALE | healthcheck old | Estado do host pode estar velho. | refresh |
| UNAVAILABLE | healthcheck cannot run here | Healthcheck indisponível neste ambiente. | DEFERRED |
| ERROR | invalid lock / healthcheck FAILED | Problema real de host/lock. | lock-status detail |
| BLOCKED | SCHEDULER_ACTIVATION BLOCKED | Ativação do scheduler bloqueada. | checklist read-only |
| NOT_READY | N/A primary (use DEFERRED) | — | use DEFERRED for discovery |
| READY | N/A for scheduler | Do not show scheduler READY | — |
| DEFERRED | discovery deferred | Discovery adiada; dívida operacional aberta. | runbook |

---

## 5. Conflict resolution rules

1. ERROR outranks ATTENTION/NOT_READY for banner color, but NOT_READY chip remains visible if still true.
2. BLOCKED (scientific/activation) remains visible even when collection healthy.
3. STALE stacks with any other state (banner + badge).
4. DEFERRED host/scheduler never auto-upgrades to healthy-active.
5. Missing backups → UNAVAILABLE, not ERROR.
6. Absent lock → idle OK, not ERROR.
7. Fixtures must not override live mode silently; `data_mode=DEMONSTRATION_FIXTURE` required.

---

## 6. Incident axis (MVP-light)

Until UX-B7:

- `incident=none` → EMPTY block “Nenhum incidente registrado neste MVP”.
- `incident=open` only if future incident artifact exists; otherwise PROHIBITED_TO_INFER.

---

## 7. Mapping to current repository evidence

| Observed | Matrix row |
|----------|------------|
| readiness NOT_READY, window insufficient, scheduler not activated, discovery missing, automation COMPLETE dry runs | C01 (+ possibly C14 for partial raw store) |
| automation.lock absent | lock ABSENT idle |
| backups missing | UNAVAILABLE |
| automation_events.jsonl missing | PARTIAL timeline |
