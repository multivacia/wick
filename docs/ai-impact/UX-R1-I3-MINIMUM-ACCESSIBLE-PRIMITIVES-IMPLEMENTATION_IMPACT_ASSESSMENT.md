# UX-R1-I3-MINIMUM-ACCESSIBLE-PRIMITIVES-IMPLEMENTATION — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = I2-I5-I6-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
TASK_ID = MINIMUM-ACCESSIBLE-PRIMITIVES-IMPLEMENTATION-001
TITLE = Minimum Accessible Primitives Implementation
INCREMENT = I3
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = true
I3_IMPLEMENTATION_AUTHORIZED = true
I3_MERGE_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = cba89b190c501b6f10cdc4280d641657fad29e5b
ANALYZED_AT = 2026-07-19T21:17:00Z
ANALYZED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTHORIZATION_DECISION = HUMAN_AUTHORIZED_FOR_THIS_TASK
RADIX_DECISION = PARTIAL_INSTALLATION_FOR_DIALOG_ONLY
NEW_RUNTIME_DEPENDENCIES = 1
FRONTEND_LOCATION = web/
I2_TOKEN_CONTRACT_VERSION = 1.0.0
```

G1 note: `IMPLEMENTATION_AUTHORIZED=true` and `I3_IMPLEMENTATION_AUTHORIZED=true` cover **I3 minimum primitives only**. They do **not** authorize router, shell, screens, ViewModel, fixtures, or operational data.

## MANDATORY_CONSTRAINTS

```text
NO_ROUTER_INSTALLATION
NO_SHELL_IMPLEMENTATION
NO_SCREEN_IMPLEMENTATION
NO_VIEWMODEL_IMPLEMENTATION
NO_FIXTURE_IMPLEMENTATION
NO_OPERATIONAL_DATA_INTEGRATION
NO_FULL_RADIX_SUITE
TOKEN_ONLY_STYLING = true
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
I6D_DECISION = BLOCKED
I3_PREREQUISITE_DECISION = I3_REQUIRED_BEFORE_I5_AND_I6C
HOST_DISCOVERY = DEFERRED
SCHEDULER_ACTIVATION = BLOCKED
R3E_SCIENTIFIC_STATE_CHANGE = false
```

## SUMMARY

Implement the minimum accessible primitive layer under `web/src/components/primitives/` consuming merged I2 `--wick-*` tokens. Install only `@radix-ui/react-dialog` for Dialog/Drawer focus management. No shell, navigation, screens, or router.

## 1. Objetivo

Entregar primitivos reutilizáveis e acessíveis (Button, Link, StatusBadge, Card, Stack, Inline, PageHeader, Section, Alert, Skeleton, VisuallyHidden, Dialog, Drawer) com WCAG 2.2 AA, token-only styling e testes — pré-requisito para I5/I6C, sem implementar shell ou telas.

## 2. Contexto técnico

- I2 tokens/themes MERGED (PR #69).
- Cross-increment auth MERGED; I3 `AUTHORIZED_WITH_CONDITIONS`; human task flips `I3_IMPLEMENTATION_AUTHORIZED=true`.
- Scaffold `web/` React 19 + Vitest + axe; no components yet.
- Preferred Radix path: partial Dialog-only install.

## 3. Componentes afetados

| Componente | Impacto |
|------------|---------|
| `web/src/components/primitives/**` | Novo |
| `web/package.json` / lockfile | +`@radix-ui/react-dialog` |
| `web/tests/primitives/**` | Novos testes |
| `web/tests/a11y/**` | Smoke a11y de primitivos |
| Backend / R3E / scheduler | Não afetados |

## 4. Arquivos previstos

```text
web/src/components/primitives/{Button,Link,StatusBadge,Card,Stack,Inline,PageHeader,Section,Alert,Skeleton,VisuallyHidden,Dialog,Drawer}/**
web/src/components/primitives/index.ts
web/src/components/primitives/primitives.css
web/tests/primitives/*.test.tsx
web/tests/a11y/primitives.a11y.test.tsx
docs/ai-impact/UX-R1-I3-MINIMUM-ACCESSIBLE-PRIMITIVES-IMPLEMENTATION_IMPACT_ASSESSMENT.md
docs/ai-specs/UX-R1-I3-MINIMUM-ACCESSIBLE-PRIMITIVES-IMPLEMENTATION_SPEC.md
docs/ai-reviews/UX-R1-I3-MINIMUM-ACCESSIBLE-PRIMITIVES-IMPLEMENTATION_REVIEW.md
reports/ai-implementation/UX-R1-I3-MINIMUM-ACCESSIBLE-PRIMITIVES-IMPLEMENTATION_HANDOFF.md
docs/PROJECT.md
```

## 5. Contratos e interfaces

```text
RADIX_DECISION = PARTIAL_INSTALLATION_FOR_DIALOG_ONLY
ALLOWED_DEP = @radix-ui/react-dialog
STYLING = --wick-* tokens only
STATUS_VOCAB = healthy|completed|attention|not_ready|blocked|deferred|unknown|fault|informational
COLOR_IS_NOT_SOLE_MEANING = true
SCREEN_AGNOSTIC = true
ROUTER_AGNOSTIC = true
DATA_SOURCE_AGNOSTIC = true
```

Drawer reuses Dialog primitives with side presentation CSS (not a navigation drawer).

## 6. Persistência e dados

Nenhuma. Sem adapters, fixtures operacionais ou integração de coleta/validate.

## 7. Concorrência, locks e idempotência

N/A backend. Dialog open state é local React state; focus trap via Radix.

## 8. Segurança

```text
NO_SECRETS = true
EXTERNAL_LINK_REL = noreferrer noopener when target=_blank
LICENSE_REVIEW = MIT Radix Dialog (acceptable)
pnpm audit --audit-level high required
```

## 9. Observabilidade

Sem telemetria. Testes automatizados + axe smoke.

## 10. Operação

Não altera scheduler, host discovery, coleta ou validate.

## 11. Rollback

```text
ROLLBACK = revert PR; remove primitives + @radix-ui/react-dialog; restore package lock
NEVER via R3E / validate / scheduler
```

## 12. Compatibilidade

- Consome I2 tokens; não redefine raw/semantic.
- I5/I6C devem importar estes primitivos; I3 não antecipa rotas.

## 13. Testes necessários

```text
Button semantics/disabled/loading
Link external safety
StatusBadge all statuses + text meaning
Alert roles
Skeleton reduced-motion
VisuallyHidden
Dialog open/close/escape/focus trap/restoration
Drawer semantics
primitive axe smoke
```

## 14. Alternativas consideradas

| Alternativa | Decisão |
|-------------|--------|
| Full Radix suite | REJECTED |
| Native Dialog only (no Radix) | REJECTED — higher a11y risk; prefer Dialog package |
| Defer Drawer | REJECTED — implement as Dialog presentation variant |
| Tailwind / CSS-in-JS | REJECTED |
| Storybook | REJECTED (`STORYBOOK_ADDED=false`) |

## 15. Riscos

| Risco | Severidade | Mitigação |
|-------|------------|-----------|
| A11y regressions in Dialog | MEDIUM | Radix + axe + interaction tests |
| Status color-only misuse | MEDIUM | Required text label in StatusBadge |
| Scope creep to shell/screens | HIGH | Hard file constraints + review |

## 16. Questões abertas

```text
NONE_BLOCKING
FULL_RADIX_SUITE = deferred to later increments if ever needed
```

## 17. Decisão arquitetural recomendada

Plain React primitives + token CSS for non-overlay; `@radix-ui/react-dialog` only for Dialog/Drawer focus management; Drawer as side-presented Dialog; WCAG 2.2 AA tests; no router/shell/screens.

## 18. Critérios para autorizar implementação

```text
1. This impact IMPACT_ASSESSMENT_STATUS = APPROVED
2. IMPLEMENTATION_AUTHORIZED = true
3. I3_IMPLEMENTATION_AUTHORIZED = true (human task)
4. Scope limited to primitives listed
5. I3_MERGE_AUTHORIZED remains false until human merge
```

All criteria satisfied for proceeding with I3 code in this task/PR.
