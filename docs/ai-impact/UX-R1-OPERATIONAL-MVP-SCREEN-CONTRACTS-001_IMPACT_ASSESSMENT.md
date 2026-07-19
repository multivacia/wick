# UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS-001 — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B3
TASK_ID = OPERATIONAL-MVP-SCREEN-CONTRACTS-001
TITLE = Operational MVP Screen Contracts
CHANGE_RISK = MEDIUM
PHASE = SPECIFICATION_AND_IMPACT_ASSESSMENT
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B3_IMPLEMENTATION_AUTHORIZED = false
DESIGN_SYSTEM_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
OLD_BASE_SHA = 5e438b8ad84d13f0c22c4017d3d3e26ac3c26647
NEW_BASE_SHA = 0c19cf978d24fad6f2e4e10403140f25b946b621
BASE_SHA = 0c19cf978d24fad6f2e4e10403140f25b946b621
REBASED_AT = 2026-07-19T15:55:00Z
REBASING_STATUS = COMPLETE
ANALYZED_AT = 2026-07-19T13:30:00Z
APPROVED_AT = 2026-07-19T13:45:00Z
RECONCILED_AT = 2026-07-19T15:55:00Z
ANALYZED_BY = cursor-agent
APPROVED_BY = cursor-agent-independent-review
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
UX_B2_AUTHORIZATION_STATUS = MERGED
UX_B4_STATUS = MERGED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
RECOMMENDED_DECISION = APPROVED
RECOMMENDED_DATA_ACCESS = GENERATED_OPERATIONAL_INDEX_PLUS_CLI_READ_ONLY
RECOMMENDED_DATA_ACCESS_SCOPE = ARCHITECTURAL_RECOMMENDATION_ONLY
DECISION = APPROVED
```

## SUMMARY

Esta tarefa define contratos de tela do MVP operacional (Visão Geral, Execuções, Readiness, Host e Scheduler) **sem** implementar UI, rotas, tokens, clientes de API ou alteração de backend.

`IMPLEMENTATION_AUTHORIZED=true` (gate G1) autoriza apenas a conclusão e candidatura a merge destes artefatos de especificação. **Não** autoriza código de frontend. `UX_B3_IMPLEMENTATION_AUTHORIZED=false` e `UI_IMPLEMENTATION_AUTHORIZED=false` permanecem obrigatórios.

```text
SCREENS = Visão Geral | Execuções | Readiness | Host e Scheduler
UI_CODE = NONE
R3E_SCIENTIFIC_STATE = UNCHANGED
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
```

## CURRENT_DATA_SOURCES

Inventário verificado no checkout `main` (`5e438b8`):

| Fonte | Path | Classificação | Telas |
|-------|------|---------------|-------|
| Estado oficial | `docs/PROJECT.md` | CURRENTLY_AVAILABLE | Todas |
| Collection state | `data/future_unseen/manifests/collection_state.json` | CURRENTLY_AVAILABLE | Visão Geral, Readiness, Host |
| Cutoff / init / freeze | `data/future_unseen/manifests/*.json` | CURRENTLY_AVAILABLE | Visão Geral, Readiness |
| Observation index | `data/future_unseen/manifests/observation_index.json` | CURRENTLY_AVAILABLE | Readiness, Execuções |
| Raw/validated JSONL | `data/future_unseen/{raw,validated}/` | NOT_AVAILABLE neste checkout (gitignored) | Execuções (detalhe) |
| Readiness report | `reports/r3e_future_unseen/readiness_report.json` | CURRENTLY_AVAILABLE | Readiness, Visão Geral |
| Ops reports | `reports/r3e_future_unseen/ops_report.json`, `ops_collection_report.json` | CURRENTLY_AVAILABLE | Visão Geral, Readiness |
| Automation state | `reports/r3e_future_unseen/automation_state.json` | CURRENTLY_AVAILABLE | Todas |
| Cycle reports | `reports/r3e_future_unseen/automation_runs/*/cycle_report.json` | CURRENTLY_AVAILABLE | Execuções, Visão Geral, Host |
| Collection runs | `reports/r3e_future_unseen/collection_runs/*/collection_run.json` (+ satélites) | CURRENTLY_AVAILABLE | Execuções |
| Automation events | `reports/r3e_future_unseen/automation_events.jsonl` | NOT_AVAILABLE (ausente) | Execuções, Visão Geral |
| Lock file | `reports/r3e_future_unseen/automation.lock` | NOT_AVAILABLE quando ausente (gitignored) | Host, Execuções |
| Lock CLI | `python -m wick.r3e.future_unseen lock-status` | DERIVABLE_WITHOUT_NEW_BACKEND | Host |
| History CLI | `python -m wick.r3e.future_unseen history` | DERIVABLE_WITHOUT_NEW_BACKEND | Visão Geral, Execuções, Host |
| Host discovery result | `R3E_LOCAL_HOST_DISCOVERY_RESULT.md` | NOT_AVAILABLE (operador no host real) | Host |
| Ops discovery docs | `docs/operations/R3E_LOCAL_PERSISTENT_HOST_DISCOVERY.md`, HostGator decisions | CURRENTLY_AVAILABLE | Host |
| Scheduler checklist | `docs/checklists/R3E_FUTURE_UNSEEN_SCHEDULER_ACTIVATION_CHECKLIST.md` | CURRENTLY_AVAILABLE | Host |
| Systemd templates | `ops/local/systemd/*` | CURRENTLY_AVAILABLE (prepared ≠ activated) | Host |
| Healthcheck scripts | `scripts/r3e_future_unseen_local_healthcheck.sh` | REQUIRES_NEW_READ_ONLY_ADAPTER | Host |
| Backup archives | `backups/fu_backup_*.tar.gz` | NOT_AVAILABLE neste checkout | Host (leve) |
| Failure taxonomy | `docs/operations/R3E_FUTURE_UNSEEN_FAILURE_TAXONOMY.md` | CURRENTLY_AVAILABLE | Execuções, Host, Visão Geral |
| UX foundation | `docs/ux/*`, `docs/ai-specs/UX-R1-EXPERIENCE-FOUNDATION_SPEC.md` | CURRENTLY_AVAILABLE | Todas (IA/linguagem) |
| Top-level `runs/`, `artifacts/` | — | NOT_AVAILABLE (não existem) | — |
| Métricas econômicas / validate success | — | PROHIBITED_TO_INFER | — |

Snapshot operacional observado (artefatos 2026-07-18):

```text
readiness_status = NOT_READY
readiness_reason = WINDOW_DAYS_INSUFFICIENT
window_days ≈ 0.79 / 90
n_observations_total = 85
series_complete = 0 / 16
last_run_status = COMPLETE (dry_run_only cycles present)
SCHEDULER_ACTIVATED = false
HOST_DISCOVERY_RESULT = missing
backups = missing
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
```

## SCREEN_SCOPE

| Screen (contrato) | Nome UX (IA) | Objetivo único |
|-------------------|--------------|----------------|
| Visão Geral | Visão Geral | Status operacional + próxima ação segura |
| Execuções | Execuções da Coleta | Listar/detalhar ciclos e evidências |
| Readiness | Prontidão | Critérios de prontidão sem alarmismo |
| Host e Scheduler | Host e Automação | Host deferred + scheduler blocked |

Fora de escopo desta tarefa: Experimento R3E (UX-B9), Backups/Incidentes completos (UX-B7), código UI, Design System implementation.

## DATA_GAPS

| Gap | Impacto | Mitigação de contrato |
|-----|---------|----------------------|
| Discovery result ausente | Host incompleto | Exibir `HOST_DISCOVERY=DEFERRED` + EMPTY/UNAVAILABLE explícito |
| Lock/events/backups ausentes | Campos host/execuções | `NULL_BEHAVIOR=UNAVAILABLE` (não FAIL) |
| Raw/validated JSONL gitignored | Detalhe de barras | Linkar paths; conteúdo via adapter no host |
| Sem índice único de execuções | Listagem | Adapter gera índice a partir de `automation_runs` + `collection_runs` |
| Sem campo `OPERATIONAL_DEBT` | Dívida operacional | Composição DERIVED_READ_ONLY a partir de discovery/scheduler/checklist |
| Sem `NEXT_ACTION` canônico no store | Visão Geral | DERIVED_READ_ONLY por regras documentadas |
| Healthcheck exige layout `$HOME/wick-r3e` | Host live | Adapter CLI; neste workspace = UNAVAILABLE |

## READ_ONLY_ADAPTER_OPTIONS

| Opção | Descrição | Complexity | Freshness | Security | Testability | Cross-platform | Failure modes | Coupling | Migration cost |
|-------|-----------|------------|-----------|----------|-------------|----------------|---------------|----------|----------------|
| A. Static artifact parsing | UI lê JSON/MD do disco | Low | Stale se UI remota | Paths/secrets risk | High (fixtures) | Weak (path layout) | Missing files | High path coupling | Low→medium |
| B. CLI-backed read-only adapter | Wrappers `history`/`lock-status`/`readiness` | Medium | On-demand | Bound CLI surface | High | Medium | CLI exit/timeout | Medium | Medium |
| C. Lightweight local API | HTTP local read-only | High | Good | Auth/surface growth | Medium | Good for remote UI | Port/auth | Low UI coupling | High |
| D. Generated operational index | Job/CLI gera `ops_index.json` normalizado | Medium | Near-real (on refresh) | Single artifact | High | Good | Stale index | Low | Medium |

## RECOMMENDED_DATA_ACCESS

```text
RECOMMENDED = D + B
RECOMMENDED_DATA_ACCESS = GENERATED_OPERATIONAL_INDEX_PLUS_CLI_READ_ONLY
SCOPE = ARCHITECTURAL_RECOMMENDATION_ONLY
INDEX_GENERATED_IN_THIS_TASK = false
ADAPTER_IMPLEMENTED_IN_THIS_TASK = false
API_IMPLEMENTED_IN_THIS_TASK = false
PRIMARY = generated operational index (normalized screen DTOs from existing artifacts)
SECONDARY = CLI read-only commands for lock-status / history / backup-verify when index stale or missing
DEFERRED = lightweight local API (C) until UI authorization + multi-client need
REJECTED_FOR_MVP = pure A without normalization (fragile cross-path, inconsistent shapes)
FUTURE_REQUIREMENT = any future index/adapter/API implementation requires its own impact assessment and explicit authorization
```

Justificativa: artefatos atuais são ricos mas heterogêneos; um índice normalizado preserva proveniência, melhora testabilidade com fixtures, e evita expor filesystem cru à UI. CLI cobre diagnóstico vivo sem mudar comportamento científico. Esta recomendação **não** cria o índice nem implementa adapter/API nesta tarefa.

## SECURITY_IMPACT

- Classificação de campos: PUBLIC_OPERATIONAL / INTERNAL_OPERATIONAL / SENSITIVE / SECRET.
- Secrets nunca renderizados; paths mascarados por padrão; hostnames/usernames mascarados.
- Downloads de evidência apenas INTERNAL_OPERATIONAL; stack traces colapsados.
- Nenhuma credencial de provider no contrato MVP.

## ACCESSIBILITY_IMPACT

- Target WCAG 2.2 AA (contrato; implementação futura em UX-B10).
- Status nunca só por cor; landmarks e hierarquia de headings definidos por tela.
- Tabelas com alternativa mobile; touch targets e reduced motion documentados.

## RESPONSIVE_IMPACT

- Desktop / tablet / mobile layouts por tela (contrato).
- Mobile alinha à IA: Início / Coleta / Prontidão / Operação / Mais.
- Sem cards no hero; conteúdo operacional usa listas/tabelas semânticas.

## SCIENTIFIC_SAFETY

```text
NOT_READY ≠ failure
READY ≠ validate authorized ≠ profitable
BLOCKED ≠ ERROR
green ≠ profit
R3E_GATE remains PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
VALIDATE_AUTHORIZED = false
validation_command_executed must remain false in this track
No fabricated metrics (return, accuracy, ratio de risco-retorno)
```

## OPERATIONAL_DEBT_REPRESENTATION

Dívida operacional **não** é um score. Representação obrigatória:

```text
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
```

Fontes: docs de discovery, checklist de ativação, `SCHEDULER_ACTIVATION_AUTHORIZED=false`, ausência de result file, HostGator `DEFERRED_FUTURE_MIGRATION`. Nunca exibir debt como concluído.

## DEPENDENCIES

| Dependência | Status |
|-------------|--------|
| UX-B1 Experience Foundation | MERGED |
| UX-B2 Design System impact | MERGED |
| UX-B2 I1 implementation authorization | MERGED as parallel track (`AUTHORIZED_FOR_INCREMENT_I1_ONLY`; execution still blocked) |
| UX-B4 operational language / microcopy | INDEPENDENT_TRACK (PR #42 draft; parallel) |
| R3E readiness / automation artifacts | CURRENTLY_AVAILABLE (read-only) |
| UI implementation authorization | false |
| Host discovery on real host | DEFERRED (não bloqueia contratos) |

### Integration boundaries (parallel tracks)

```text
UX-B2 = future frontend / design-system architecture (tokens, primitives, I1 scaffold when separately authorized)
UX-B3 = screen and data contracts (this task)
UX-B4 = terminology and microcopy (operational language catalogs)
```

UX-B3 remains valid without merge of UX-B4 and without I1 execution. Future UI implementation must consume all approved contracts from B2+B3+B4 when available.

## IMPLEMENTATION_BOUNDARY

Autorizado nesta PR:

- docs de impacto, spec, catálogos, state matrix, fixtures catalog, review, handoff;
- atualização de status em `docs/PROJECT.md` e backlog UX.

Proibido:

- frontend code, routes, components, CSS, tokens;
- install de deps JS;
- API clients / backend behavior changes;
- execute collect / run-cycle / validate;
- activate scheduler;
- inferir métricas ausentes;
- desbloquear R4/R5.

## TEST_STRATEGY

| Camada | Agora | Futuro (UI) |
|--------|-------|-------------|
| Governance validator | Obrigatório nesta PR | Contínuo |
| pytest / ruff | Suite completa (sem regressão) | Contínuo |
| Contract snapshot tests | N/A (docs) | Contra fixtures seguros |
| Adapter unit tests | N/A | Quando adapter autorizado |
| A11y / responsive | Contrato documentado | UX-B10 |

## ROLLBACK_STRATEGY

- Docs-only: revert do commit/PR remove contratos sem efeito em runtime científico.
- Nenhum migration, schema ou store alterado.
- Status PROJECT/backlog reverte junto com o PR se necessário.

## BLOCKERS

Nenhum blocker para **especificação**.

Blockers para **implementação UI futura** (não desta tarefa):

```text
UX_B3_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
HOST_DISCOVERY = DEFERRED (dados live incompletos; fixtures cobrem protótipo)
```

## DECISION

```text
DECISION = APPROVED
RECOMMENDED_DECISION = APPROVED
```

Contratos aprovados como fonte de verdade para protótipo operacional futuro. Implementação de UI permanece bloqueada até autorização explícita.

---

## 1. Objetivo

Produzir análise de impacto e contratos de tela do MVP operacional UX-R1 (quatro telas), com proveniência de dados, estados, fixtures seguros, acessibilidade/responsivo e avaliação de adapter read-only — sem código de UI e sem mudança científica R3E.

## 2. Contexto técnico

- Frontend ausente; Design System impact mergeado, implementação DS bloqueada.
- Coleta future-unseen com artefatos em `reports/r3e_future_unseen/` e manifests em `data/future_unseen/manifests/`.
- Readiness atual `NOT_READY` / `WINDOW_DAYS_INSUFFICIENT`.
- Scheduler: templates preparados; ativação não autorizada.
- Host discovery: aguarda operador no host real; Cursor env ≠ ops host.
- Trilha UX paralela: `R3E_SCIENTIFIC_STATE=UNCHANGED`.

## 3. Componentes afetados

**Afetados (docs):** `docs/ai-impact/`, `docs/ai-specs/`, `docs/ai-reviews/`, `docs/ux/`, `docs/PROJECT.md`, `reports/ai-implementation/`.

**Não afetados:** `src/wick/r3e/**` runtime, migrations, store, validate, scheduler activation, providers.

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS-001_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md
docs/ux/UX-R1-OPERATIONAL-MVP_DATA-CONTRACT-CATALOG.md
docs/ux/UX-R1-OPERATIONAL-MVP_STATE-MATRIX.md
docs/ux/UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG.md
docs/ai-reviews/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_REVIEW.md
reports/ai-implementation/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_HANDOFF.md
docs/PROJECT.md
docs/ux/UX-R1_BACKLOG.md
```

## 5. Contratos e interfaces

- Contratos de tela e campo (USER_LABEL + TECHNICAL_LABEL).
- Proveniência por campo (SOURCE_TYPE/PATH/FIELD).
- Matriz de estados e fixtures rotulados `DADOS_DEMONSTRATIVOS`.
- Interface futura do índice operacional (DTO read-only) — especificação apenas.
- Nenhuma interface mutável; ações destrutivas proibidas no MVP.

## 6. Persistência e dados

- Somente leitura de artefatos existentes.
- Nenhum schema novo no banco.
- Índice operacional proposto seria artefato gerado (futuro), não store científico.
- Fixtures: catálogo documental; **sem** arquivos executáveis nesta tarefa.

## 7. Concorrência, locks e idempotência

- UI/contratos não adquirem `automation.lock`.
- Exibição de lock via `lock-status` (ABSENT/ACTIVE/STALE/INVALID).
- Refresh manual; auto-refresh conservador; dados stale explicitados.
- Idempotência de coleta permanece propriedade do backend; UI apenas exibe `idempotency_status`.

## 8. Segurança

Ver SECURITY_IMPACT. Mascaramento obrigatório de secrets, tokens, env values, stack traces. Paths e hostnames mascarados por padrão (INTERNAL_OPERATIONAL com reveal controlado futuro).

## 9. Observabilidade

- Campos de falha mapeados à taxonomy operacional.
- Links para artefatos brutos (open raw / download evidence) como read-only.
- Timestamps sempre com timezone (UTC+offset).

## 10. Operação

- Dívida operacional e scheduler blocked sempre visíveis.
- Próxima ação segura derivada; nunca sugere `validate` ou ativação sem autorização.
- Fixtures para prototipagem offline quando host/dados live indisponíveis.

## 11. Rollback

Ver ROLLBACK_STRATEGY. Revert docs-only sem impacto científico.

## 12. Compatibilidade

- Compatível com UX-B1 IA/linguagem e UX-B2 semantic status model (NOT_READY→ATTENTION).
- Compatível com artefatos R3E-B2/B4/B5 existentes.
- Não depende de ativação de scheduler nem de discovery concluída.

## 13. Testes necessários

Ver TEST_STRATEGY. Nesta PR: pytest, ruff, governance validator.

## 14. Alternativas consideradas

| Alternativa | Resultado |
|-------------|-----------|
| Contratos só com fixtures, ignorando artefatos reais | Rejeitada — perde rastreabilidade |
| API local imediata (C) | Adiada — custo alto sem UI authorized |
| Parsing estático puro (A) | Rejeitada como primário — frágil |
| Índice gerado + CLI (D+B) | **Recomendada** |
| Incluir Experimento R3E nesta tarefa | Fora de escopo (UX-B9) |

## 15. Riscos

| Risco | Mitigação |
|-------|-----------|
| Operador interpreta READY como validate | Copy + scientific_safety blocks |
| Green = lucro | Semantic model + proibição econômica |
| Debt exibido como done | Campos fixos DEFERRED/OPEN/BLOCKED |
| Paths/secrets vazam em UI | Security classification + masking |
| Spec diverge de artefatos reais | Catalog com SOURCE_PATH verificados |
| B2 DS ainda sem implementação | Contratos independentes; tokens depois |

## 16. Questões abertas

| Questão | Disposição |
|---------|------------|
| Formato exato do `ops_index.json` | Definido na spec como contrato DTO; geração futura |
| Paginação/retenção de execuções | Contrato: page size 25; retenção segue scripts ops (não inventar history) |
| Auto-refresh interval | Default off; se enabled futuro ≥ 60s + stale warning |
| Reveal de paths mascarados | Admin-only futuro; MVP mascara sempre |

Nenhuma questão aberta bloqueia a aprovação dos contratos.

## 17. Decisão arquitetural recomendada

```text
APPROVE screen contracts as documentation source of truth
RECOMMENDED_DATA_ACCESS = GENERATED_OPERATIONAL_INDEX_PLUS_CLI_READ_ONLY
KEEP UI_IMPLEMENTATION_AUTHORIZED = false
KEEP UX_B3_IMPLEMENTATION_AUTHORIZED = false
KEEP HOST_DISCOVERY = DEFERRED
KEEP OPERATIONAL_DEBT = OPEN
KEEP SCHEDULER_ACTIVATION = BLOCKED
KEEP R3E_SCIENTIFIC_STATE = UNCHANGED
```

## 18. Critérios para autorizar implementação

Implementação de UI **somente** quando **todos** forem verdadeiros:

1. `UX_B3_IMPLEMENTATION_AUTHORIZED=true` explícito (humano)
2. `UI_IMPLEMENTATION_AUTHORIZED=true` explícito (humano)
3. UX-B2 implementation authorized **ou** decisão explícita de protótipo fixtures-only sem DS package
4. Contratos desta PR mergeados (ou HEAD autorizado)
5. Fixtures seguros implementados conforme catálogo
6. Adapter/índice read-only especificado em tarefa própria (sem mutação científica)
7. Sem alteração de `VALIDATE_AUTHORIZED`, scheduler activation, ou R4/R5
