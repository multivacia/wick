# UX-R1-I6A — Overview Screen Data and Fixture Preparation — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
WORKSTREAM = I6A
TASK_ID = OVERVIEW-SCREEN-DATA-AND-FIXTURE-PREPARATION-001
TITLE = Overview Screen Data and Fixture Preparation
PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = DOCUMENTATION_AND_DATA_CONTRACT_ONLY
RUNTIME_IMPLEMENTATION_AUTHORIZED = false
I6A_DOCUMENTATION_MERGE_RECOMMENDED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
NO_TYPESCRIPT_FIXTURE_FILES = true
NO_VIEWMODEL_IMPLEMENTATION = true
NO_SCREEN_IMPLEMENTATION = true
NO_OPERATIONAL_INDEX = true
NO_ADAPTER = true
NO_REAL_DATA_INTEGRATION = true
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 6ff45b9bd50349cc12061346c24a86fec0cf7645
OLD_BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
I2_STATUS = ASSESSMENT_MERGED
I2_IMPLEMENTATION_AUTHORIZED = false
I5A_STATUS = ARCHITECTURE_MERGED
I5_ARCHITECTURE_DECISION = AUTHORIZED_WITH_CONDITIONS
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
PARALLEL_KICKOFF_STATUS = COMPLETE
ANALYZED_AT = 2026-07-19T19:00:00Z
ANALYZED_BY = cursor-agent
APPROVED_AT = 2026-07-19T19:00:00Z
APPROVED_BY = cursor-agent-docs-package
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
SCIENTIFIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
I6A_STATUS = DATA_PREPARATION_IN_PROGRESS
REVIEW_STATUS = APPROVED
DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
AUTHORIZATION_CONDITIONS = C1-C8
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
RECOMMENDED_DECISION = AUTHORIZED_WITH_CONDITIONS
DECISION = AUTHORIZED_WITH_CONDITIONS
SAFE_FIXTURE_CATALOG_CHANGE_STATUS = REVIEWED_AND_IN_SCOPE
SAFE_FIXTURE_CATALOG_CHANGE_PURPOSE = Compatibility/alignment extension mapping eight B3 scenarios to Overview ViewModel values; docs-only; no executable fixtures
WCAG = 2.2 AA
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_IMPACT_ASSESSMENT.md
```

## SUMMARY

Pacote **somente documentação** que detalha o contrato de ViewModel read-only da tela Visão Geral e os cenários de fixture demonstrativos necessários para um protótipo futuro — **sem** implementar ViewModel TypeScript, fixtures `.ts`/`.json` executáveis, tela, índice operacional, adapter ou integração com dados reais.

```text
IMPLEMENTATION_AUTHORIZED = true
= authorization to execute this documentation/data-contract preparation task only

IMPLEMENTATION_SCOPE = DOCUMENTATION_AND_DATA_CONTRACT_ONLY

RUNTIME_IMPLEMENTATION_AUTHORIZED = false
= no executable frontend, ViewModel, fixture, adapter, integration, router or screen work is authorized

DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
I6A_DOCUMENTATION_MERGE_RECOMMENDED = true
AUTOMATIC_MERGE_AUTHORIZED = false

READY != VALIDATION_AUTHORIZED
DATA_CONTRACT_APPROVED != SCREEN_IMPLEMENTATION_AUTHORIZED
FIXTURE_SPEC_APPROVED != EXECUTABLE_FIXTURE_AUTHORIZED
VIEWMODEL_CONTRACT_APPROVED != VIEWMODEL_IMPLEMENTATION_AUTHORIZED
```

```text
SCREEN = Visão Geral (Screen 1)
DELIVERABLE = ViewModel contract + fixture scenario specs (markdown)
CODE = NONE
TYPESCRIPT_FIXTURES = NONE
R3E_SCIENTIFIC_STATE = UNCHANGED
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
```

## SCOPE

Incluído:

- Contrato de campos do Overview ViewModel (docs).
- Especificação detalhada dos oito cenários B3 já catalogados, com valores de ViewModel para Visão Geral.
- Extensão documental do catálogo B3 de fixtures seguros (`docs/ux/UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG.md`) — compatibility/alignment required by I6A; `SAFE_FIXTURE_CATALOG_CHANGE_STATUS=REVIEWED_AND_IN_SCOPE`.
- Impact assessment, spec, review e handoff de governança.
- Status `I6A_STATUS=DATA_PREPARATION_IN_PROGRESS` em `docs/PROJECT.md`.

Excluído (proibido nesta fase):

- Arquivos TypeScript/JSON de fixture.
- Implementação de ViewModel, hooks, adapters ou screens.
- Índice operacional gerado.
- Integração com artefatos live / CLI / API.
- Qualquer mudança científica R3E, validate, scheduler ou R4/R5.

## UPSTREAM DEPENDENCIES

| Dependência | Status |
|-------------|--------|
| UX-B3 Operational MVP Screen Contracts | MERGED |
| UX-B4 Operational Language / Microcopy | MERGED |
| UX-B1 Experience Foundation | MERGED |
| UX-B2 I1 Frontend Scaffold | MERGED (I2+ não autorizado) |
| UX-R1 I2 Design Tokens Assessment | ASSESSMENT_MERGED; implementation unauthorized |
| UX-R1 I5A Application Shell Architecture | ARCHITECTURE_MERGED; router/shell unauthorized |
| Screen contracts Spec §4 Visão Geral | AUTHORITATIVE |
| Data Contract Catalog Screen 1 | AUTHORITATIVE |
| Safe Fixture Catalog (8 scenarios) | AUTHORITATIVE base; extended here |
| I5A shell route/title/breadcrumb/boundary contracts | AUTHORITATIVE for shell; not duplicated in ViewModel |

## SCIENTIFIC_SAFETY

```text
NOT_READY != ERROR
BLOCKED != FAILED
READY != VALIDATION_AUTHORIZED
COLLECTION_COMPLETE != SCIENTIFIC_VALIDATION
SCIENTIFIC_VALIDATION != ECONOMIC_RETURN
SUCCESS != PROFIT
NO_HISTORY != SYSTEM_FAILURE
PARTIAL_METADATA != FABRICATED_DATA
UNKNOWN != HEALTHY
UNKNOWN != FAILED
HOST_DISCOVERY deferred != host failure
SCHEDULER_ACTIVATION blocked != collection failure
R3E_GATE remains PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
SCIENTIFIC_INTERPRETATION_ALLOWED = false on all fixtures
VALIDATE_AUTHORIZED = false in all required scenarios
validation_command_executed must remain false
No fabricated economic or scientific success
Never infer values from missing evidence (use UNKNOWN|NOT_AVAILABLE|DEFERRED|NOT_AUTHORIZED)
```

## OPERATIONAL_CONSTRAINTS

```text
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
```

## IMPLEMENTATION_BOUNDARY

Autorizado:

- Artefatos markdown listados em “Arquivos previstos”.
- Atualização mínima de `docs/PROJECT.md` (`I6A_STATUS` apenas).
- Refinamento documental do catálogo B3 de fixtures (Overview ViewModel values).

Proibido:

- `web/**` código de tela / ViewModel / fixtures TS.
- Adapter, índice operacional, API.
- Mutação de store, coleta, validate, scheduler.
- Definir `I2_IMPLEMENTATION_AUTHORIZED` ou `I5A_*`.

## TEST_STRATEGY

| Camada | Nesta tarefa |
|--------|--------------|
| Governance validator | Obrigatório nos quatro artefatos de governança |
| pytest / ruff | Suite completa (sem regressão) |
| web typecheck/lint/test/a11y/build | Smoke de não-regressão; zero mudanças em `web/` |
| Fixture executável / snapshot UI | Fora de escopo (docs only) |

## ROLLBACK_STRATEGY

Revert do commit/PR documental remove contratos I6A sem efeito em runtime científico ou frontend. Nenhum migration, schema ou store alterado.

## DECISION

```text
DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
DECISION = AUTHORIZED_WITH_CONDITIONS
RECOMMENDED_DECISION = AUTHORIZED_WITH_CONDITIONS
PHASE = DATA_CONTRACT_AND_FIXTURE_PREPARATION
NEXT = human review/merge of docs; ViewModel/TS fixtures/screen remain unauthorized
```

## AUTHORIZATION_CONDITIONS

```text
CONDITION_ID = C1_DOCS_MERGE
DESCRIPTION = Human merges this I6A data-contract docs package into main
OWNER = Gustavo Almeida
VERIFICATION_METHOD = PR #57 merge commit on main
STATUS = OPEN

CONDITION_ID = C2_I6_SCREEN_FLAG_FLIP
DESCRIPTION = Explicit human sets I6_SCREEN_IMPLEMENTATION_AUTHORIZED=true before Overview UI
OWNER = Gustavo Almeida
VERIFICATION_METHOD = docs/PROJECT.md flag flip in separate implementation task
STATUS = OPEN

CONDITION_ID = C3_NO_TS_FIXTURES_UNTIL_AUTHORIZED
DESCRIPTION = No TypeScript/JSON fixture files until TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED=true
OWNER = Gustavo Almeida / implementing agent
VERIFICATION_METHOD = PR file list excludes web fixture materialization; PROJECT.md flag
STATUS = SATISFIED (docs); OPEN (code)

CONDITION_ID = C4_VIEWMODEL_SCHEMA_FREEZE
DESCRIPTION = Future ViewModel code implements the 17 required field groups with attribute matrix
OWNER = implementing agent (future I6)
VERIFICATION_METHOD = type review vs UX-R1-I6A-OVERVIEW-VIEWMODEL-CONTRACT.md
STATUS = SATISFIED (specified); OPEN (code)

CONDITION_ID = C5_SEMANTIC_SAFETY
DESCRIPTION = Preserve NOT_READY!=ERROR, READY!=VALIDATION_AUTHORIZED, SUCCESS!=PROFIT, UNKNOWN!=HEALTHY/FAILED, etc.
OWNER = implementing agent (future I6)
VERIFICATION_METHOD = fixture + UI copy review vs B4 guardrails and this impact
STATUS = SATISFIED (specified); OPEN (code)

CONDITION_ID = C6_A11Y_WCAG_22_AA
DESCRIPTION = Overview UI meets WCAG 2.2 AA (headings, status not by color, live regions, named links)
OWNER = implementing agent (future I6 / UX-B10)
VERIFICATION_METHOD = a11y tests + keyboard checklist
STATUS = SATISFIED (specified); OPEN (code)

CONDITION_ID = C7_SCIENTIFIC_OPERATIONAL_INVARIANTS
DESCRIPTION = R3E unchanged; HOST_DISCOVERY=DEFERRED; OPERATIONAL_DEBT=OPEN; SCHEDULER_ACTIVATION=BLOCKED
OWNER = all agents
VERIFICATION_METHOD = PROJECT.md + artifact metadata
STATUS = SATISFIED

CONDITION_ID = C8_NO_SCREEN_NO_LIVE_DATA_NOW
DESCRIPTION = UI_SCREEN / VIEWMODEL / TS fixture / operational data integration flags remain false until separate auth
OWNER = Gustavo Almeida
VERIFICATION_METHOD = PROJECT.md + PR file list (no web/src ViewModel/fixtures/adapters)
STATUS = SATISFIED
```

---

## 1. Objetivo

Preparar, em documentação apenas, o contrato de ViewModel read-only da Visão Geral e os cenários de fixture demonstrativos (fonte sintética) necessários para um protótipo futuro da tela Overview, sem implementar código, fixtures TypeScript, adapter, índice operacional ou integração com dados reais.

## 2. Contexto técnico

- Contratos de tela UX-B3 e linguagem UX-B4 já estão MERGED e são a fonte de verdade funcional.
- Screen contracts Spec §4 define blocos de informação, composição de estado e regras de próxima ação segura.
- Catálogo B3 de data contracts (Screen 1) lista campos, proveniência e comportamentos NULL/EMPTY/ERROR.
- Catálogo B3 de fixtures seguros nomeia oito cenários; I6A detalha valores de ViewModel Overview por cenário.
- Scaffold `web/` (I1) existe; I6 screen implementation permanece não autorizada.
- Host discovery continua DEFERRED; scheduler BLOCKED; debt OPEN; R3E gate PENDING_FUTURE_UNSEEN_DATA.

## 3. Componentes afetados

**Afetados (docs):** `docs/ai-impact/`, `docs/ai-specs/`, `docs/ai-reviews/`, `docs/ux/`, `docs/PROJECT.md`, `reports/ai-implementation/`.

**Não afetados:** `src/wick/**` runtime, migrations, store future-unseen, validate, scheduler activation, providers, `web/src/**` (nenhuma alteração de código).

## 4. Arquivos previstos

```text
docs/ai-impact/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_SPEC.md
docs/ai-reviews/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_REVIEW.md
docs/ux/UX-R1-I6A-OVERVIEW-VIEWMODEL-CONTRACT.md
docs/ux/UX-R1-I6A-OVERVIEW-FIXTURE-SCENARIOS.md
docs/ux/UX-R1-OPERATIONAL-MVP_SAFE-FIXTURE-CATALOG.md
reports/ai-implementation/UX-R1-I6A-OVERVIEW-DATA-AND-FIXTURES_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

- Overview ViewModel: campos read-only com USER_LABEL + TECHNICAL_LABEL, tipo, nullable, freshness, security class e notas de segurança científica.
- Regras de composição `overall_operational_state` e `next_safe_action` herdadas de Spec §4 (sem reinterpretação científica).
- Fixtures: contrato documental por cenário; `SOURCE=SYNTHETIC`; badge `DADOS_DEMONSTRATIVOS`.
- Nenhuma interface mutável; nenhuma ação destrutiva; nenhum CTA de validate.
- Interface futura de adapter/índice permanece fora de escopo (recomendação B3 intacta, não implementada).

## 6. Persistência e dados

- Sem schema novo, migration ou escrita em store.
- Fixtures são especificações markdown; não materializam JSON/TS nesta fase.
- Dados demonstrativos não devem ser confundidos com evidência de repositório.
- Quando UI for autorizada no futuro, materialização de fixtures exigirá tarefa própria.

## 7. Concorrência, locks e idempotência

- Documentação não adquire `automation.lock`.
- ViewModel futuro apenas exibe estado de lock se/quando evidência existir; I6A não inventa locks.
- Fixtures não simulam unlock ou mutação.
- Idempotência de coleta permanece propriedade do backend; Overview só referencia IDs evidentes ou sintéticos rotulados.

## 8. Segurança

- Classificação por campo: PUBLIC_OPERATIONAL / INTERNAL_OPERATIONAL / SENSITIVE.
- Paths e hostnames mascarados em contratos; secrets nunca renderizados.
- Fixtures sintéticos não embutem credenciais, tokens ou paths reais de operador.
- Evidence links em fixtures apontam para paths sintéticos rotulados, nunca para inventar artefatos no repo.

## 9. Observabilidade

- Freshness e `stale_flag` documentados (threshold Overview: 6h, herdado de B3).
- Evidence links e provenance footer obrigatórios no contrato.
- Timestamps sempre com timezone (UTC+offset).
- Falhas mapeadas à taxonomia operacional existente; sem inventar incidentes reais.

## 10. Operação

- Dívida operacional OPEN e scheduler BLOCKED visíveis em todos os cenários obrigatórios.
- Host DEFERRED como default operacional.
- `next_safe_action` nunca sugere validate nem ativação de scheduler.
- Badge `DADOS_DEMONSTRATIVOS` obrigatório em todo fixture.

## 11. Rollback

Revert docs-only. Sem impacto científico, sem rollback de dados, sem migration.

## 12. Compatibilidade

- Compatível com UX-B3 Screen 1 catalog, Spec §4, state matrix e safe fixture catalog.
- Consome microcopy UX-B4 (status/empty/failure/guardrails) sem duplicar catálogos.
- Não altera flags I2/I5A; não autoriza I6 screen implementation.
- Não depende de discovery concluída nem de scheduler ativo.

## 13. Testes necessários

Nesta PR: `uv run ruff check .`, `uv run pytest -q`, governance validator nos artefatos de impacto/spec/review/handoff, e smoke `pnpm --dir web` (typecheck, lint, test, test:a11y, build) sem mudanças de código web.

## 14. Alternativas consideradas

| Alternativa | Resultado |
|-------------|-----------|
| Materializar fixtures TypeScript/JSON agora | Rejeitada — fase docs-only; `NO_TYPESCRIPT_FIXTURE_FILES` |
| Implementar ViewModel + tela Overview | Rejeitada — `I6_SCREEN_IMPLEMENTATION_AUTHORIZED=false` |
| Gerar índice operacional nesta tarefa | Rejeitada — `NO_OPERATIONAL_INDEX` |
| Ligar fixtures a artefatos live do checkout | Rejeitada — `NO_REAL_DATA_INTEGRATION`; evita efeito peeking |
| Criar novos cenários além dos oito B3 | Rejeitada — I6A detalha apenas os oito já catalogados |
| Contratos docs + extensão B3 Overview values | **Adotada** |

## 15. Riscos

| Risco | Mitigação |
|-------|-----------|
| Fixture READY lido como validate liberado | Copy obrigatória + `VALIDATE_AUTHORIZED=false` em todos os cenários |
| Fixture saudável lido como edge/lucro | Guardrails B4 + flags científicas/econômicas false |
| Inventar IDs como evidência de repo | `SOURCE=SYNTHETIC` + proibição explícita |
| Escopo vazar para código web | Boundary flags + review checklist |
| Divergência vs Spec §4 | ViewModel contract referencia campos B3 sem inventar semântica |

## 16. Questões abertas

| Questão | Disposição |
|---------|------------|
| Path final de fixtures JSON quando UI autorizada | Decidido em tarefa futura de materialização; fora de I6A |
| Adapter/índice que alimentará o ViewModel live | Permanece recomendação B3; requer impact assessment próprio |
| Intervalo de auto-refresh Overview | Herda B3 (default off; se futuro ≥ 60s + stale) |
| Reveal de paths mascarados | Admin-only futuro; MVP mascara sempre |

Nenhuma questão aberta bloqueia a aprovação deste pacote documental.

## 17. Decisão arquitetural recomendada

```text
DATA_CONTRACT_DECISION = AUTHORIZED_WITH_CONDITIONS
APPROVE I6A docs package (ViewModel contract + fixture scenario specs) with C1–C8
KEEP UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
KEEP I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
KEEP RUNTIME_IMPLEMENTATION_AUTHORIZED = false
KEEP VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
KEEP TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
KEEP OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
KEEP NO_TYPESCRIPT_FIXTURE_FILES = true
KEEP HOST_DISCOVERY = DEFERRED
KEEP OPERATIONAL_DEBT = OPEN
KEEP SCHEDULER_ACTIVATION = BLOCKED
KEEP R3E_SCIENTIFIC_STATE = UNCHANGED
SET I6A_STATUS = DATA_PREPARATION_IN_PROGRESS
AUTOMATIC_MERGE_AUTHORIZED = false
```

## 18. Critérios para autorizar implementação

Implementação de tela Overview / ViewModel / fixtures executáveis **somente** quando **todos** forem verdadeiros:

1. Este pacote I6A mergeado (C1) e HEAD explicitamente autorizado.
2. `I6_SCREEN_IMPLEMENTATION_AUTHORIZED=true` explícito (humano) — C2.
3. `UI_SCREEN_IMPLEMENTATION_AUTHORIZED=true` explícito (humano).
4. `VIEWMODEL_IMPLEMENTATION_AUTHORIZED=true` e/ou `TYPESCRIPT_FIXTURE_IMPLEMENTATION_AUTHORIZED=true` conforme escopo — C3/C4.
5. Impact assessment próprio para materialização de fixtures e/ou adapter/índice.
6. Sem alteração de `VALIDATE_AUTHORIZED`, scheduler activation, R4/R5 ou estado científico R3E — C7.
7. Fixtures materializados preservam `DADOS_DEMONSTRATIVOS` e flags científicas/econômicas false — C5.
8. Nenhuma integração live sem `OPERATIONAL_DATA_INTEGRATION_AUTHORIZED=true` — C8.
9. A11y WCAG 2.2 AA verified for UI — C6.
