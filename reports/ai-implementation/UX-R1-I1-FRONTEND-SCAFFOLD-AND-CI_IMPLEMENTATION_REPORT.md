# UX-R1-I1 — Frontend Scaffold and CI — Implementation Report

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
PARENT_TASK = DESIGN-SYSTEM-FOUNDATION-001
TASK_ID = FRONTEND-SCAFFOLD-AND-CI-001
INCREMENT = I1
PHASE = IMPLEMENTATION
TITLE = Frontend Scaffold and CI
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
IMPLEMENTATION_REPORT_STATUS = FINAL
REVIEW_STATUS_AT_IMPLEMENTATION_REPORT_CREATION = PENDING
CURRENT_REVIEW_STATUS = APPROVED
CURRENT_MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
REPOSITORY = multivacia/wick
PULL_REQUEST = 51
BASE_BRANCH = main
BASE_SHA = 2fbf91c248acc381e940d433934633279338ef3b
HEAD_BRANCH = feature/ux-r1-i1-frontend-scaffold-and-ci
IMPLEMENTATION_HEAD = 29e05752a1e3f11f0ba560df825c4cc47ca9d8a4
CONTENT_REVIEWED_THROUGH_HEAD = 29e05752a1e3f11f0ba560df825c4cc47ca9d8a4
FINAL_CANDIDATE_HEAD = 29e05752a1e3f11f0ba560df825c4cc47ca9d8a4
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
I1_IMPLEMENTATION_AUTHORIZED = true
I2_IMPLEMENTATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
CREATED_AT = 2026-07-19T16:12:00Z
UPDATED_AT = 2026-07-19T16:23:38Z
```

Impact path: `docs/ai-impact/UX-R1-DESIGN-SYSTEM-IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md`

## Natureza

Implementação do scaffold frontend e CI (I1 only). Não implementa telas operacionais,
tokens, componentes, integração de dados, nem altera estado científico R3E.

## Divergências

1. Autorização mergeada documentava `FRONTEND_ROOT = frontend/`; a tarefa I1 de execução
   fixa `FRONTEND_LOCATION = web/`. Este report e o código seguem `web/`.
2. Autorização I1 mencionava pacote vazio `wick-ds`; a estrutura mínima autorizada na
   tarefa I1 não inclui esse pacote — omitido de propósito.

## Arquivos criados / alterados

### Criados

```text
web/package.json
web/pnpm-lock.yaml
web/.nvmrc
web/.npmrc
web/tsconfig.json
web/tsconfig.app.json
web/tsconfig.node.json
web/tsconfig.vitest.json
web/vite.config.ts
web/vitest.config.ts
web/eslint.config.js
web/index.html
web/README.md
web/public/.gitkeep
web/src/main.tsx
web/src/App.tsx
web/src/scaffoldCopy.ts
web/src/styles.css
web/src/vite-env.d.ts
web/tests/setup.ts
web/tests/App.test.tsx
web/tests/a11y/scaffold.a11y.test.tsx
.github/workflows/dependency-review.yml
docs/ai-specs/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_IMPLEMENTATION_SPEC.md
reports/ai-implementation/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_IMPLEMENTATION_REPORT.md
docs/ai-reviews/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_TECHNICAL-AND-SAFETY_REVIEW.md
reports/ai-implementation/UX-R1-I1-FRONTEND-SCAFFOLD-AND-CI_HANDOFF.md
```

### Alterados

```text
.github/workflows/ci.yml
.gitignore
docs/PROJECT.md
```

## Dependências adicionadas (exatas)

Runtime:

```text
react@19.2.7
react-dom@19.2.7
```

Dev/tooling (principais):

```text
typescript@5.9.3
vite@8.1.5
@vitejs/plugin-react@6.0.3
vitest@4.1.10
@testing-library/react@16.3.2
@testing-library/jest-dom@6.9.1
@testing-library/dom@10.4.1
jest-axe@10.0.0
axe-core@4.11.0
jsdom@27.4.0
eslint@9.39.5
typescript-eslint@8.64.0
eslint-plugin-jsx-a11y@6.10.2
eslint-plugin-react-hooks@7.0.1
eslint-plugin-react-refresh@0.4.26
```

## Toolchain

```text
NODE_VERSION = 22 (LTS; .nvmrc)
PNPM_VERSION = 10.33.3
FRONTEND_FRAMEWORK = React
LANGUAGE = TypeScript
BUILD_TOOL = Vite
FRONTEND_LOCATION = web/
```

## Comandos e resultados

```text
pnpm --dir web install --frozen-lockfile = PASS
pnpm --dir web typecheck = PASS
pnpm --dir web lint = PASS
pnpm --dir web test = PASS (2 tests)
pnpm --dir web test:a11y = PASS (1 test)
pnpm --dir web build = PASS
pnpm --dir web audit = PASS (no known vulnerabilities)
pnpm --dir web licenses = PASS (react/react-dom/scheduler = MIT)
uv run ruff check . = PASS
uv run ruff format --check . = PASS
uv run pytest = PASS (249 passed)
uv run python scripts/validate_ai_governance_artifacts.py <I1 artifacts> = PASS (errors=0 warnings=0)
```

## Segurança / segurança científica / operacional

- Placeholder neutro apenas; sem métricas sintéticas.
- Sem secrets, analytics, fonts remotas, endpoints de produção.
- `VITE_` documentado; sourcemaps de produção desabilitados.
- HOST_DISCOVERY / OPERATIONAL_DEBT / SCHEDULER / R3E inalterados.

## Rollback

Reverter o PR I1 ou remover `web/` + jobs frontend adicionados.


## Documented CI exception

```text
DEPENDENCY_REVIEW_JOB = ADVISORY_CONTINUE_ON_ERROR
REASON = GitHub Dependency graph not enabled on repository (action error: Dependency review is not supported)
ENFORCEABLE_SUBSTITUTES = pnpm audit (CI frontend-validate) + pnpm licenses list + committed lockfile + exact pins
```
