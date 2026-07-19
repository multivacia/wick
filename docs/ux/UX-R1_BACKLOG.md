# UX-R1 — Backlog

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
RELEASE_STATUS = PLANNING
DOCUMENT_VERSION = 1.0.0
EFFECTIVE_AT = 2026-07-19T03:13:15Z
```

## Fronteira MVP

```text
UX-B1 = REQUIRED
UX-B2 = REQUIRED
UX-B3 = REQUIRED
UX-B4 = REQUIRED
UX-B5 = REQUIRED
UX-B6 = REQUIRED
UX-B7 = OPTIONAL_AFTER_CORE
UX-B8 = OPTIONAL_AFTER_CORE
UX-B9 = REQUIRED
UX-B10 = REQUIRED
UX-B11 = REQUIRED_BEFORE_RELEASE_CLOSE
```

Protótipo funcional inicial (somente estas telas):

```text
1. Visão Geral
2. Execuções da Coleta
3. Prontidão
4. Host e Automação
5. Experimento R3E — explanatory view
```

## Itens

### UX-B1 — Experience Foundation

```text
TASK_ID = UX-RELEASE-FOUNDATION-001
STATUS = MERGED
PRIORITY = P0
MVP = REQUIRED
PR = 31
MERGE_COMMIT = 5101c6534388a2494bc15e0a718f27563d898569
```

Entregáveis:

- princípios UX versionados;
- personas;
- guia de linguagem;
- direção visual;
- arquitetura de informação;
- backlog do protótipo;
- análise de impacto.

**Nota:** esta tarefa **não** implementa telas (`UI_IMPLEMENTATION_AUTHORIZED = false`).

---

### UX-B2 — Design System Foundation

```text
TASK_ID = DESIGN-SYSTEM-FOUNDATION-001
STATUS = AUTHORIZATION_MERGED_I1_BLOCKED
PHASE = IMPLEMENTATION_AUTHORIZATION_ASSESSMENT
PRIORITY = P0
MVP = REQUIRED
DEPENDS_ON = UX-B1
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
IMPACT_ASSESSMENT_STATUS = APPROVED
UX_B2_IMPACT_STATUS = MERGED
UX_B2_AUTHORIZATION_STATUS = MERGED
UX_B2_AUTHORIZATION_DECISION = AUTHORIZED_FOR_INCREMENT_I1_ONLY
UX_B2_AUTHORIZED_INCREMENT = I1
I1_IMPLEMENTATION_STATUS = BLOCKED_PENDING_SEPARATE_TASK_AND_HUMAN_AUTHORIZATION
RECOMMENDED_ARCHITECTURE = HEADLESS_PRIMITIVES_PLUS_WICK_TOKENS
```

Entregáveis:

- color tokens;
- typography;
- spacing;
- cards;
- badges;
- buttons;
- tables;
- alerts;
- status components;
- responsive rules;
- accessibility baseline.

---

### UX-B3 — Functional Prototype: Overview

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P0
MVP = REQUIRED
DEPENDS_ON = UX-B2
```

Entregáveis:

- application shell;
- sidebar;
- header;
- global status;
- main readiness banner;
- summary cards;
- next-action card;
- recent timeline.

---

### UX-B4 — Operational Language and Microcopy

```text
TASK_ID = OPERATIONAL-LANGUAGE-MICROCOPY-001
STATUS = CONTENT_DESIGN_READY_FOR_HUMAN_REVIEW
PRIORITY = P0
MVP = REQUIRED
PHASE = CONTENT_DESIGN_AND_GOVERNANCE
DEPENDS_ON = UX-B1
INDEPENDENT_OF = UX-B2, UX-B3
UX_B4_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
IMPACT_ASSESSMENT_STATUS = APPROVED
```

Entregáveis (docs-only):

- guia operacional de linguagem;
- catálogo de status;
- catálogo de empty states;
- microcopy de falhas/avisos (taxonomia R3E);
- guardrails científicos e econômicos;
- impact assessment + review + handoff.

**Trilhas paralelas:** UX-B2 define design system / arquitetura frontend futura; UX-B3 define contratos de tela/dados/estado; UX-B4 define terminologia e microcopy oficiais. Implementação futura consome as três.

**Nota:** o rótulo legado “Functional Prototype: Collection Runs” permanece como trabalho de protótipo de UI futuro (lista/detalhe de execuções), **após** autorização de UI — não faz parte desta entrega de conteúdo.

---

### UX-B4-RUNS — Functional Prototype: Collection Runs (UI futuro)

```text
TASK_ID = COLLECTION-RUNS-PROTOTYPE
STATUS = PLANNED
PRIORITY = P0
MVP = REQUIRED
DEPENDS_ON = UX-B2, UX-B4
UI_IMPLEMENTATION_AUTHORIZED = false
```

Entregáveis (quando UI autorizada):

- run list;
- filters;
- run details;
- structured logs;
- evidence links;
- plain-language failure descriptions (consumindo catálogos UX-B4).

---

### UX-B5 — Functional Prototype: Readiness

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P0
MVP = REQUIRED
DEPENDS_ON = UX-B2
```

Entregáveis:

- readiness summary;
- 90-day progress;
- gate checklist;
- blocked action explanation;
- technical details expansion.

---

### UX-B6 — Functional Prototype: Host and Scheduler

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P0
MVP = REQUIRED
DEPENDS_ON = UX-B2
```

Entregáveis:

- host status;
- persistent path;
- scheduler state;
- activation stepper;
- operational checklist;
- safe action confirmations.

---

### UX-B7 — Backups and Incidents

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P1
MVP = OPTIONAL_AFTER_CORE
DEPENDS_ON = UX-B3
```

Entregáveis:

- backup list;
- verification state;
- incident list;
- incident detail;
- operator recommendation.

---

### UX-B8 — Governance and Backlog

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P1
MVP = OPTIONAL_AFTER_CORE
DEPENDS_ON = UX-B3
```

Entregáveis:

- Kanban;
- PR and commit evidence;
- approvals;
- handoffs;
- dependencies;
- blocked items.

---

### UX-B9 — Experiment R3E Explanation

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P0
MVP = REQUIRED
DEPENDS_ON = UX-B2
```

Entregáveis:

- experiment objective in plain language;
- current scientific state;
- frozen protocol;
- technical glossary;
- no premature economic result.

---

### UX-B10 — Responsive and Accessibility Review

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P0
MVP = REQUIRED
DEPENDS_ON = UX-B3, UX-B4, UX-B5, UX-B6, UX-B9
```

Entregáveis:

- tablet;
- mobile;
- keyboard navigation;
- contrast;
- screen-reader semantics;
- zoom;
- reduced motion;
- accessibility report.

---

### UX-B11 — Usability Validation

```text
TASK_ID = TBD
STATUS = PLANNED
PRIORITY = P0
MVP = REQUIRED_BEFORE_RELEASE_CLOSE
DEPENDS_ON = UX-B10
```

Entregáveis:

- test script;
- non-economist user test;
- technical reviewer test;
- findings;
- prioritized corrections.

## Política de dados do protótipo

Permitido:

```text
REAL_OPERATIONAL_METADATA
SAFE_FIXTURES
CLEARLY_LABELED_DEMO_DATA
```

Proibido:

- fabricar resultados científicos;
- exibir lucro falso;
- apresentar performance inventada como real;
- implicar readiness indevida;
- implicar ativação de scheduler;
- implicar execução de `validate`.

Todo fixture deve exibir:

```text
DEMONSTRATION DATA
```

## Ordem sugerida pós-UX-B1

```text
UX-B1 → UX-B2 → (UX-B3 ∥ UX-B4 ∥ UX-B5 ∥ UX-B6 ∥ UX-B9) → UX-B10 → UX-B11
UX-B7 / UX-B8 após o core, se capacidade permitir
```

## Autorizações

```text
IMPLEMENTATION_AUTHORIZED = false
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UX_FOUNDATION_MERGE_AUTHORIZED = true
UX_B2_IMPLEMENTATION_AUTHORIZED = false
UX_B4_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
UX_B1_STATUS = MERGED
UX_B2_IMPACT_STATUS = MERGED
UX_B2_AUTHORIZATION_STATUS = MERGED
UX_B2_AUTHORIZATION_DECISION = AUTHORIZED_FOR_INCREMENT_I1_ONLY
UX_B2_AUTHORIZED_INCREMENT = I1
I1_IMPLEMENTATION_STATUS = BLOCKED_PENDING_SEPARATE_TASK_AND_HUMAN_AUTHORIZATION
UX_B3_STATUS = INDEPENDENT_TRACK
UX_B4_STATUS = CONTENT_DESIGN_READY_FOR_HUMAN_REVIEW
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
```
