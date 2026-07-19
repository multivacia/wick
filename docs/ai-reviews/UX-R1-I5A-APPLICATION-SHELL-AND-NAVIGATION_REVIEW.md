# UX-R1-I5A — Application Shell and Navigation — Revisão Independente

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
WORKSTREAM = I5A
TASK_ID = APPLICATION-SHELL-AND-NAVIGATION-ARCHITECTURE-001
REVIEW_TYPE = ARCHITECTURE_AND_GOVERNANCE
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
AUTOMATIC_MERGE_AUTHORIZED = false
CHANGE_RISK = MEDIUM
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
SPEC_PATH = docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md
IMPLEMENTATION_AUTHORIZED = true
UI_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
NO_ROUTER_INSTALLATION = true
NO_SHELL_IMPLEMENTATION = true
NO_NAVIGATION_COMPONENTS = true
NO_SCREEN_IMPLEMENTATION = true
NO_REAL_DATA = true
R3E_SCIENTIFIC_STATE_CHANGE = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = 221aacc7141697403e9bbbc9f8690953b683e3a9
BASE_SHA_AT_REVIEW = 221aacc7141697403e9bbbc9f8690953b683e3a9
HEAD_BRANCH = cursor/ux-r1-i5a-application-shell-architecture-1b6b
CONTENT_REVIEWED_THROUGH_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
FINAL_CANDIDATE_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
IMPLEMENTATION_HEAD = 98a52e229cbd872466c6815635d707a398bb0324
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
REVIEWED_AT = 2026-07-19T17:05:00Z
REVIEWED_BY = cursor-agent-independent-review
FULL_TEST_SUITE = PASS
LINT_STATUS = PASS
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
WEB_REGRESSION = PASS
```

## Materiais revisados

- `docs/ai-impact/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_IMPACT_ASSESSMENT.md`
- `docs/ai-specs/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_SPEC.md`
- `reports/ai-implementation/UX-R1-I5A-APPLICATION-SHELL-AND-NAVIGATION_HANDOFF.md`
- `docs/ux/WICK_INFORMATION_ARCHITECTURE.md`
- `docs/ai-specs/UX-R1-OPERATIONAL-MVP-SCREEN-CONTRACTS_SPEC.md` (routes / navigation)
- `docs/ai-specs/UX-R1-EXPERIENCE-FOUNDATION_SPEC.md` (shell inventory, a11y, responsive)
- `docs/ai-specs/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_IMPLEMENTATION_SPEC.md` (no router in I1)
- `web/package.json` / `web/src/App.tsx` (scaffold-only; no router dependency)
- `docs/PROJECT.md` (I5A_STATUS line only; UI_SCREEN_IMPLEMENTATION_AUTHORIZED remains false)

## Checklist de revisão

| Critério | Resultado | Notas |
|----------|-----------|-------|
| Docs-only boundary | PASS | Sem mudanças em `web/` ou deps |
| G1 docs auth ≠ UI auth | PASS | `IMPLEMENTATION_AUTHORIZED=true` scoped; `I5_*=false` |
| IA hierarchy alignment | PASS | Visão Geral, Coleta Futura, Operação, Experimentos, Governança |
| MVP routes prepared | PASS | overview, runs, readiness, host |
| B3 route key compatibility | PASS | `/overview`, `/collection/runs`, `/collection/readiness`, `/ops/host` |
| URL conventions | PASS | kebab, query filters, no secrets |
| Frame / header / sidebar / mobile | PASS | Specified |
| Breadcrumbs + page title | PASS | Specified |
| Loading / error / not-found | PASS | Specified |
| Deep links | PASS | Bookmarkable; missing run → Not Found |
| Keyboard + responsive | PASS | Skip link, breakpoints, reduced motion |
| Landmarks + focus restoration | PASS | IA-matching landmark tree |
| Access + auth boundaries | PASS | Future-safe; MVP local trusted |
| Router recommendation without install | PASS | React Router future; `NO_ROUTER_INSTALLATION` |
| R3E scientific unchanged | PASS | Gates preserved |
| Operational flags preserved | PASS | HOST_DISCOVERY/DEBT/SCHEDULER |
| No I2/I6A status pollution | PASS | Only `I5A_STATUS` added |
| Forbidden placeholders absent | PASS | No incomplete marker tokens |
| Automatic merge blocked | PASS | `AUTOMATIC_MERGE_AUTHORIZED=false` |

## Achados

### Críticos / Altos

Nenhum.

### Médios (aceitos / não bloqueantes)

1. Experimento R3E permanece rota reservada; chrome MVP omite até UX-B9 — consistente com IA “fora do MVP inicial” vs inventário de páginas (tela 5). Spec escolhe omitir do chrome até autorização de tela: aceito.
2. Auth provider undecided — correto para arquitetura; não bloqueia docs.

### Baixos

1. Breakpoint pixel guidelines (1100/768) são recomendações de shell; Design System I2 pode refinar tokens de layout sem invalidar hierarquia.

## Decisão

```text
REVIEW_STATUS = APPROVED
DECISION = APPROVED
IMPLEMENTATION_AUTHORIZED = true
AUTHORIZATION_SCOPE = DOCS_PACKAGE_ONLY
UI_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
AUTOMATIC_MERGE_AUTHORIZED = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

Arquitetura aprovada para merge humano documental. **Nenhum** código de shell, router ou tela autorizado.

## Condições de merge

1. Validação local: ruff, pytest, governance validator (4 artefatos), web typecheck/lint/test/a11y/build verdes
2. Diff limitado a docs + `I5A_STATUS` em PROJECT.md
3. Sem instalação de React Router ou componentes de navegação
4. Autorização humana de merge (sem auto-merge)
5. Pós-merge: implementação I5 permanece bloqueada até task/autorização separada
