# COLLECTION-AUTOMATION-001 — Análise de Impacto Arquitetural

## Metadados

```text
RELEASE = R3E
BACKLOG_ITEM = B4
TASK_ID = COLLECTION-AUTOMATION-001
TITLE = Future-Unseen Collection Automation and Readiness Monitoring
CHANGE_RISK = HIGH
PHASE = IMPLEMENTATION_AUTHORIZED_WITH_CHANGES
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
PR_UNDER_ANALYSIS = 19
PR19_ACTION = CHANGES_REQUIRED_BEFORE_REVIEW
PR19_HEAD_ANALYZED = 5ab4456fafc39984b3b282a6cd5876ba12f2c517
PROPOSED_IMPLEMENTATION_CLASSIFICATION = PROPOSED_IMPLEMENTATION_FOR_ARCHITECTURAL_REVIEW
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 8c6cb4966fdb13abd34a4c066597ceea4c4cfaf9
ANALYZED_AT = 2026-07-18T20:15:18Z
APPROVED_AT = 2026-07-18T20:23:54Z
ANALYZED_BY = cursor-agent
APPROVED_BY = human
G1_ENFORCEMENT_EFFECTIVE_FROM = 3e839a25c3fa1e855cefbaefa07af69e1f906faa
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
MERGE_STATUS = BLOCKED
```

## 1. Objetivo

Avaliar, antes de qualquer merge da PR #19, a arquitetura e o impacto da automação operacional de coleta incremental future-unseen + readiness monitoring, sem autorizar implementação adicional nem validação científica.

## 2. Contexto técnico

Arquitetura atual (main pós-G1 / B3):

- CLI: `init`, `collect`, `ops-report`, `readiness`, `ingest-json`, `validate` (validate proibido operacionalmente)
- Collector: `run_collect` — dry-run/live, closed candles, cutoff, retries, reports em `collection_runs/`
- Readiness: `evaluate_readiness` — READY/NOT_READY/BLOCKED, read-only
- Store: `data/future_unseen/{raw,validated,manifests}` append-only
- Estado: `collection_state.json` com locks científicos (`validation_command_executed=false`, R4 BLOCKED)
- Execução atual: manual (dry-run → collect → idempotency → ops → readiness)
- Provedores: binance/yahoo via factory R1; falha parcial isolada por série

A PR #19 propõe orquestrar esse fluxo em `run-cycle` com lock, histórico e scheduler documentado.

## 3. Componentes afetados

Propostos na PR #19 (não mergeados):

- novo: `src/wick/r3e/future_unseen/automation.py`
- alterado: `src/wick/r3e/future_unseen/cli.py` (`run-cycle`)
- novo: `tests/test_r3e_future_unseen_automation.py`
- novo: `scripts/r3e_future_unseen_run_cycle.sh`
- novo: runbook/spec/review/reports B4
- artefatos: `automation_runs/`, `automation_state.json`, `automation.lock` (gitignored)
- `.gitignore` para lock file
- refresh de ops/readiness reports (dry-run-only evidence)

Não afeta: cutoff, freeze, universo, thresholds, validate/gate, R4/R5.

## 4. Arquivos previstos

Já presentes na PR #19 (proposta):

```text
src/wick/r3e/future_unseen/automation.py
src/wick/r3e/future_unseen/cli.py
tests/test_r3e_future_unseen_automation.py
scripts/r3e_future_unseen_run_cycle.sh
docs/runbooks/R3E_FUTURE_UNSEEN_AUTOMATION_RUNBOOK.md
docs/ai-specs/R3E-B4-COLLECTION-AUTOMATION-001_SPEC.md
docs/ai-reviews/R3E-B4-COLLECTION-AUTOMATION-001_REVIEW.md
reports/ai-implementation/R3E-B4-COLLECTION-AUTOMATION-001_*.md
reports/r3e_future_unseen/automation_*
```

Ajustes documentais pós-aprovação deste impacto (não nesta fase): campos G1 (`CHANGE_RISK`, `IMPACT_ASSESSMENT_STATUS`, `IMPLEMENTATION_AUTHORIZED`) nos artefatos B4.

## 5. Contratos e interfaces

- novo comando: `python -m wick.r3e.future_unseen run-cycle`
- flags: `--as-of`, `--dry-run-only`, `--skip-idempotency-check`, `--output-dir`, `--json/--human`, `--strict`, `--max-retries`, `--timeout-seconds`
- exit codes: `0=COMPLETE|PARTIAL|NO_NEW_DATA`, `1=FAILED`, `3=BLOCKED`, `4=SKIPPED_LOCKED`
- reutiliza contratos existentes de `run_collect` / `evaluate_readiness` / `build_ops_report`
- JSON de ciclo imutável + `automation_state.json` derivável
- eventos de transição READY/BLOCKED sem autorizar validate

## 6. Persistência e dados

- store oficial permanece append-only via `ingest_batch`
- dry-run-only não grava store
- histórico imutável sob `reports/r3e_future_unseen/automation_runs/<run_id>/`
- estado resumido sobrescreve apenas o alias operacional `automation_state.json`
- lock file não versionado
- risco de misturar backfill: preflight/readiness já bloqueiam mistura; ciclo não altera regras

## 7. Concorrência, locks e idempotência

- lock atômico `O_CREAT|O_EXCL` em `reports/r3e_future_unseen/automation.lock`
- TTL default 3300s; stale se expirado ou pid morto
- impede sobreposição de ciclos
- idempotência: reexecução pós-collect com mesmo `--as-of` deve aceitar 0 novas observações
- recuperação: falha após collect libera lock; reexecução segura (collector idempotente)

## 8. Segurança

- sem import de validate/gate no módulo de automação
- sem flags de bypass científico
- READY ⇒ `HUMAN_AUTHORIZATION_REQUIRED=true`, `VALIDATE_AUTHORIZED=false`
- sem credenciais em relatórios de ciclo (provedores via env existentes; não logar secrets)
- GitHub Actions **não** persiste store oficial (correto)

## 9. Observabilidade

- `cycle_report.json` por run
- `automation_state.json` resumido
- `automation_events.jsonl` para READY/BLOCKED
- espelha readiness/ops reports
- exit codes operacionais distintos de readiness CLI (0/2/3)

## 10. Operação

- cadência recomendada: horário no minuto 15
- runner: script local + cron/systemd
- store ownership: host durável com volume do repositório/dados
- dry-run evidence na PR #19: store 85 inalterado; readiness NOT_READY (window)

## 11. Rollback

- reverter merge da PR #19 remove código/orquestração
- store append-only não é “desfeito”; observações aceitas permanecem (esperado)
- lock stale é removível manualmente se necessário
- estado resumido pode ser regenerado a partir dos runs imutáveis

## 12. Compatibilidade

- não quebra comandos manuais existentes
- G1 agora exige impacto aprovado antes de avançar merge/implementação adicional
- artefatos B4 pré-G1 precisam alinhar metadados após aprovação deste impacto
- PR #19 permanece draft/bloqueada até decisão humana sobre este impacto

## 13. Testes necessários

Já cobertos na proposta PR #19 (evidência declarada; revalidar no tip se houver mudanças):

- ciclo completo / no-new-data / partial provider
- retry/timeout/lock/stale/interrupt/rerun/idempotency
- histórico imutável / estado derivável
- transições NOT_READY→READY/BLOCKED
- anti-validate / anti-ciência / sem credenciais
- JSON/exit codes

Pós-ajuste: reexecutar suite + validador G1 nos artefatos atualizados.

## 14. Alternativas consideradas

1. **Runner local agnóstico + cron/systemd** — prós: store durável, controle de credenciais, simples; contras: exige host operacional. **Recomendada.**
2. **GitHub Actions schedule** — prós: gerenciado; contras: ephemeral, sem volume oficial, risco de secrets/provedores. **Rejeitada para persistência do store.**
3. **Scheduler em container/host** — prós: isolação; contras: overhead; aceitável se volume montado. **Alternativa compatível com (1).**
4. **Serviço persistente dedicado** — prós: HA; contras: complexidade prematura. **Adiar.**

## 15. Riscos

```text
RISK = concurrent_cycles_corrupt_or_duplicate_work
IMPACT = HIGH
LIKELIHOOD = LOW
MITIGATION = atomic lock + TTL + stale recovery + idempotent collect
RESIDUAL_RISK = LOW

RISK = github_actions_used_as_store_owner
IMPACT = CRITICAL
LIKELIHOOD = LOW
MITIGATION = runbook forbids Actions persistence; local runner documented
RESIDUAL_RISK = LOW

RISK = accidental_validate_from_automation
IMPACT = CRITICAL
LIKELIHOOD = LOW
MITIGATION = no validate import/call; READY emits human-auth signal only
RESIDUAL_RISK = LOW

RISK = timeout_only_checked_between_steps
IMPACT = MEDIUM
LIKELIHOOD = MEDIUM
MITIGATION = document limitation; optional later hard cancel around provider calls
RESIDUAL_RISK = MEDIUM

RISK = governance_artifacts_predate_G1_fields
IMPACT = MEDIUM
LIKELIHOOD = HIGH (current)
MITIGATION = retrofit CHANGE_RISK/IMPACT fields after this assessment is approved
RESIDUAL_RISK = LOW after retrofit

RISK = partial_provider_failure_misclassified
IMPACT = MEDIUM
LIKELIHOOD = MEDIUM
MITIGATION = PARTIAL status preserves accepted data; failures counted
RESIDUAL_RISK = LOW
```

## 16. Questões abertas

1. Deve o timeout interromper `run_collect` mid-flight (thread/process), ou basta fail-closed no próximo checkpoint? Recomendação atual: checkpoint é aceitável para v0.1; ADJUST opcional depois.
2. Lock path em `reports/` vs `manifests/` — ambos aceitáveis; manter `reports/` (já gitignored para lock).
3. Quem opera o host cron em produção? Fora do escopo de código; requisito operacional humano.

## 17. Decisão arquitetural recomendada

```text
RUNNER_STRATEGY = local_agnostic_script
SCHEDULER_STRATEGY = cron_or_systemd_hourly_minute_15
STORE_OWNERSHIP = durable_host_volume_not_github_actions
LOCK_PATH = reports/r3e_future_unseen/automation.lock
LOCK_MECHANISM = atomic_file_O_CREAT_EXCL
LOCK_TTL = 3300_seconds
PROVIDER_TIMEOUT = delegated_to_provider_retry_layer
CYCLE_TIMEOUT = 3000_seconds_checkpointed
RETRY_POLICY = max_retries_passthrough_to_run_collect_default_3
EXIT_CODES = 0_complete_partial_nonewdata__1_failed__3_blocked__4_skipped_locked
RUN_HISTORY_STRATEGY = immutable_per_run_directory
STATE_SUMMARY_STRATEGY = automation_state.json_derived_from_last_run
RECOVERY_STRATEGY = release_lock_on_exit_plus_idempotent_rerun
OBSERVABILITY_STRATEGY = cycle_report_plus_events_jsonl_plus_ops_readiness_aliases
ROLLBACK_STRATEGY = revert_pr_code_keep_append_only_store
RECOMMENDED_DECISION = APPROVE_WITH_CHANGES
PR19_ACTION = CHANGES_REQUIRED_BEFORE_REVIEW
```

### Avaliação da implementação existente (PR #19)

| Decisão implementada | Classificação | Justificativa |
|---|---|---|
| `run-cycle` orchestration order | ACCEPT | Alinha dry-run→collect→idempotency→ops→readiness |
| Atomic file lock + TTL/stale | ACCEPT | Fail-closed e recuperável |
| Local cron/systemd; no Actions store | ACCEPT | Store ownership correto |
| Immutable automation_runs + state summary | ACCEPT | Auditável e derivável |
| READY without validate | ACCEPT | Segurança científica preservada |
| Exit codes 0/1/3/4 | ACCEPT | Operacionalmente claros |
| Checkpoint-only cycle timeout | ADJUST | Documentar; considerar hard-timeout futuro |
| B4 governance docs pre-G1 fields | ADJUST | Retrofit obrigatório pós-aprovação deste impacto |
| Review claiming merge-ready pre-impact | ADJUST | PR #19 deve ficar `MERGE_STATUS=BLOCKED` até impacto aprovado |
| GH Actions scheduled collect | REJECT (not present) | Corretamente ausente |

## 18. Critérios para autorizar implementação

Para promover:

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
```

exigir:

1. revisão humana desta análise com decisão explícita;
2. confirmação de que PR #19 permanece sem merge até autorização;
3. lista de ajustes ADJUST aplicada (ou waiver humano documentado);
4. artefatos B4 atualizados com campos G1 e referência a este impacto;
5. revalidação: `validate_ai_governance_artifacts` + testes relevantes no tip;
6. `VALIDATION_COMMAND_EXECUTED = false` preservado;
7. nenhuma mudança de cutoff/freeze/thresholds/validate.

Estado após aprovação humana:

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
PR19_ACTION = CHANGES_REQUIRED_BEFORE_REVIEW
MERGE_STATUS = BLOCKED
```

Autoriza ajustes na PR #19. Não autoriza merge imediato nem `validate`.
