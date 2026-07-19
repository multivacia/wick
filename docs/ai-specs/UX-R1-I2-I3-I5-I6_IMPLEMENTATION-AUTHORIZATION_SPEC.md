# UX-R1 — I2 / I3 / I5 / I6 Implementation Authorization Spec

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
TASK_ID = I2-I5-I6-IMPLEMENTATION-AUTHORIZATION-ASSESSMENT-001
PHASE = IMPLEMENTATION_AUTHORIZATION_ASSESSMENT
SPEC_STATUS = ACTIVE
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I2-I3-I5-I6_IMPLEMENTATION-AUTHORIZATION_IMPACT_ASSESSMENT.md
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_SCOPE = AUTHORIZATION_ASSESSMENT_DOCUMENTATION_ONLY
ASSESSMENT_ONLY = true
IMPLEMENTATION_EXECUTION_AUTHORIZED = false
REVIEW_STATUS = APPROVED
I2_IMPLEMENTATION_AUTHORIZED = false
I3_IMPLEMENTATION_AUTHORIZED = false
I5_IMPLEMENTATION_AUTHORIZED = false
ROUTER_INSTALLATION_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
SPEC_VERSION = 1.0.0
CREATED_AT = 2026-07-19T19:18:37Z
I2_DECISION = AUTHORIZED_WITH_CONDITIONS
I3_DECISION = AUTHORIZED_WITH_CONDITIONS
I3_PREREQUISITE_DECISION = I3_REQUIRED_BEFORE_I5_AND_I6C
I5_DECISION = AUTHORIZED_WITH_CONDITIONS
I6B_DECISION = AUTHORIZED_WITH_CONDITIONS
I6C_DECISION = AUTHORIZED_WITH_CONDITIONS
I6D_DECISION = BLOCKED
NEXT_RECOMMENDED_TASK = I2_DESIGN_TOKENS_AND_THEMES_IMPLEMENTATION
```

This specification defines **authorization boundaries** across I2/I3/I5/I6. It does not authorize executable product work inside the assessment PR.

## 1. Non-monolithic decomposition

```text
STEP_1 = I2 tokens/themes
STEP_2 = I3 minimum accessible primitives
STEP_3 = I5 router + shell/navigation
STEP_4 = I6B typed ViewModel + demonstration fixtures
STEP_5 = I6C Visão Geral with demonstration fixtures
STEP_6 = I6D read-only operational-data adapter/integration
```

No step becomes executable merely because its documentation is merged.

## 2. Dependency rules

```text
I2 -> I3
I2 -> I5
I3 -> I5
I2 -> I6C
I3 -> I6C
I5 -> I6C
I6B -> I6C
I6C -> I6D
B3_DATA_ACCESS -> I6D
B4_SEMANTIC_LANGUAGE -> I6B/I6C/I6D
```

```text
I3_PREREQUISITE_DECISION = I3_REQUIRED_BEFORE_I5_AND_I6C
ROUTER_INSTALLATION_OWNER = I5_IMPLEMENTATION
ROUTER_RECOMMENDATION = react-router
```

## 3. Normative authorization matrix

```text
INCREMENT = I2
SCOPE = design tokens, semantic tokens, light/dark themes, status/focus/motion tokens, CSS --wick-* output, token tests
PREREQUISITES = I1 MERGED; I2 assessment MERGED
DECISION = AUTHORIZED_WITH_CONDITIONS
OPEN_CONDITIONS = human I2_IMPLEMENTATION_AUTHORIZED flip; I2 C3-C8; no components/router/screens
SEPARATE_TASK_REQUIRED = true
HUMAN_AUTHORIZATION_REQUIRED = true
IMPLEMENTATION_FLAG_REMAINS_FALSE = true

INCREMENT = I3
SCOPE = Button, Link, StatusBadge, Card, Stack, Inline, PageHeader, Section, Alert, Skeleton, Dialog_or_Drawer_Primitive, FocusTrap_Primitive, VisuallyHidden
PREREQUISITES = I2 implementation MERGED
DECISION = AUTHORIZED_WITH_CONDITIONS
OPEN_CONDITIONS = minimum set freeze; Radix only where required; a11y tests
SEPARATE_TASK_REQUIRED = true
HUMAN_AUTHORIZATION_REQUIRED = true
IMPLEMENTATION_FLAG_REMAINS_FALSE = true

INCREMENT = I5
SCOPE = react-router install, route registry, application shell, desktop/mobile nav, skip link, landmarks, focus restoration, document title, 404, error/loading boundaries
PREREQUISITES = I2+I3 MERGED; I5A architecture MERGED
DECISION = AUTHORIZED_WITH_CONDITIONS
OPEN_CONDITIONS = I5A C2-C8; router pin+license audit; no screen content in shell
SEPARATE_TASK_REQUIRED = true
HUMAN_AUTHORIZATION_REQUIRED = true
IMPLEMENTATION_FLAG_REMAINS_FALSE = true

INCREMENT = I6B
SCOPE = typed Overview ViewModel; eight synthetic fixtures; fixture validation; freshness/provenance; unknown/partial/stale; safe next-action codes
PREREQUISITES = I6A MERGED; prefer I2 for status token alignment
DECISION = AUTHORIZED_WITH_CONDITIONS
OPEN_CONDITIONS = I6A C3-C5; DADOS_DEMONSTRATIVOS; no real data
SEPARATE_TASK_REQUIRED = true
HUMAN_AUTHORIZATION_REQUIRED = true
IMPLEMENTATION_FLAG_REMAINS_FALSE = true

INCREMENT = I6C
SCOPE = Visão Geral screen using demonstration fixtures only
PREREQUISITES = I2+I3+I5+I6B MERGED
DECISION = AUTHORIZED_WITH_CONDITIONS
OPEN_CONDITIONS = I6A C2/C6; UX states; WCAG 2.2 AA; no real-data adapter
SEPARATE_TASK_REQUIRED = true
HUMAN_AUTHORIZATION_REQUIRED = true
IMPLEMENTATION_FLAG_REMAINS_FALSE = true

INCREMENT = I6D
SCOPE = generated operational index + CLI read-only adapter
PREREQUISITES = I6C + B3 index + host discovery path + security review
DECISION = BLOCKED
OPEN_CONDITIONS = HOST_DISCOVERY not deferred; index schema; filesystem safety; read-only guarantee
SEPARATE_TASK_REQUIRED = true
HUMAN_AUTHORIZATION_REQUIRED = true
IMPLEMENTATION_FLAG_REMAINS_FALSE = true
```

## 4. I2 implementation boundaries (future task only)

Allowed after separate human authorization:

```text
- raw + semantic + motion token sources
- light and dark themes
- status semantics binding
- focus tokens
- contrast requirements and tests
- reduced-motion strategy
- CSS custom property output (--wick-*)
- versioning/deprecation notes for DESIGN_TOKEN_CONTRACT_VERSION
- rollback by removing token/theme files
```

Mandatory safeguards:

```text
NOT_READY != ERROR
BLOCKED != FAILED
READY != VALIDATION_AUTHORIZED
GREEN = healthy/completed only
AMBER = attention/not-ready
PURPLE_OR_GRAY = blocked/deferred/unknown
RED = confirmed fault only
COLOR_IS_NOT_SOLE_MEANING = true
```

Prohibited in I2:

```text
components, Radix, router, shell, screens, adapters, real data, scheduler, validate, collection
```

## 5. I3 minimum primitives (future task only)

```text
REQUIRED_BEFORE_I5_AND_I6C = true
RADIX_POLICY = partial — install only primitives needed for Dialog/FocusTrap/VisuallyHidden after license review
DEFER_FULL_RADIX_SUITE = true
```

## 6. I5 shell boundaries (future task only)

```text
ROUTER = react-router
SHELL_OWNS = chrome, nav, landmarks, titles, boundaries
SHELL_DOES_NOT_OWN = Overview content ViewModel, scientific conclusions, operational write actions
```

## 7. I6B / I6C / I6D boundaries

I6B fixtures must preserve:

```text
DADOS_DEMONSTRATIVOS = true
SOURCE = SYNTHETIC
SCIENTIFIC_INTERPRETATION_ALLOWED = false
ECONOMIC_INTERPRETATION_ALLOWED = false
```

I6C screen must not:

```text
real-data adapter, collection execution, validation command, scheduler activation,
scientific conclusion, financial return claims, editable operational actions
```

I6D remains:

```text
BLOCKED
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
```

## 8. Next task

```text
NEXT_RECOMMENDED_TASK = I2_DESIGN_TOKENS_AND_THEMES_IMPLEMENTATION
NEXT_TASK_SCOPE = tokens/themes/CSS variables/tests only
NEXT_TASK_RISK = MEDIUM
NEXT_TASK_PREREQUISITES = merge this assessment; open separate I2 implementation task; flip I2_IMPLEMENTATION_AUTHORIZED
NEXT_TASK_PROHIBITED_ACTIONS = components; Radix; router; shell; screens; fixtures TS; real data; scheduler; validate; collection
PARALLEL_TASKS_ALLOWED = false
```

## 9. Explicit non-goals of this assessment PR

```text
NO_TOKEN_CSS
NO_RADIX_INSTALL
NO_COMPONENT_CODE
NO_ROUTER_INSTALL
NO_SHELL_CODE
NO_VIEWMODEL_TS
NO_FIXTURE_TS
NO_OVERVIEW_SCREEN
NO_OPERATIONAL_ADAPTER
NO_GOVERNANCE_VALIDATOR_CHANGE
NO_SCHEDULER_ACTIVATION
NO_COLLECTION_OR_VALIDATE
```
