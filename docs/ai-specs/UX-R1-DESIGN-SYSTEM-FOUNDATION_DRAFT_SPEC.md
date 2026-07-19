# UX-R1 — Design System Foundation — Draft Spec

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B2
TASK_ID = DESIGN-SYSTEM-FOUNDATION-001
PHASE = IMPACT_ASSESSMENT_ONLY
SPEC_STATUS = DRAFT
IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B2_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-DESIGN-SYSTEM-FOUNDATION-001_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = PENDING_REVIEW
REVIEW_STATUS = PENDING
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
SPEC_VERSION = 0.1.0-draft
CREATED_AT = 2026-07-19T12:31:41Z
```

Este documento é **rascunho**. Não autoriza implementação.

## 1. Arquitetura proposta

```text
RECOMMENDED = OPTION_B_HEADLESS_PLUS_WICK_TOKENS
TOKEN_LAYER = CSS custom properties (--wick-*)
VISUAL_LAYER = WICK semantic styles
PRIMITIVES = accessible headless (library TBD by human)
PREFERRED_STACK = React + TypeScript (align R5; human confirmation required)
```

## 2. Tokens

Categorias:

```text
color.background.* / color.text.* / color.border.* / color.status.*
space.* / size.* / radius.* / shadow.*
font.family.* / font.size.* / font.weight.* / line.height.*
breakpoint.* / motion.duration.* / motion.easing.* / z_index.*
```

Convenção: semântico na API pública; raw só no tema. Light primary; dark supported. Proibido cor hardcoded em componentes de produto. Versionar `DESIGN_TOKEN_CONTRACT_VERSION`.

## 3. Componentes (inventário alvo)

```text
Button, Input, Textarea, Select
Card (somente quando interação exigir container)
Badge / StatusBadge
Alert
Table (+ mobile card transform)
Progress / Checklist progress
Tooltip
Modal / Dialog
Drawer
Navigation (sidebar, bottom nav)
FocusRing / SkipLink
DemoDataLabel
EvidencePanel primitives (run_id, hash display)
```

## 4. Semantic statuses

```text
NORMAL | SUCCESS | ATTENTION | BLOCKED | ERROR | UNAVAILABLE | INFORMATIONAL
```

- `NOT_READY` → ATTENTION (não ERROR)
- `BLOCKED` científico → BLOCKED (não ERROR automático)
- SUCCESS ≠ profit
- ERROR só falha real
- Sempre texto + ícone + SR label

## 5. Accessibility acceptance criteria

```text
WCAG_TARGET = 2.2 AA
```

Keyboard, focus visible, SR semantics, contrast, non-color cues, 200% zoom, reduced motion, 44px touch, table a11y, modal focus management, plain-language + technical expansion.

## 6. Responsive behavior

Desktop sidebar; tablet collapsible; mobile bottom nav per UX-B1 IA. Tables → cards; wrap long IDs; stacked filters/checklists.

## 7. Fixture rules

```text
DEMONSTRATION DATA label mandatory
No implied profit / model accuracy / readiness / scheduler / validate
```

## 8. Test matrix

Mandatory before DS implementation merge:

- unit tokens
- component tests
- a11y (axe + keyboard)
- semantic-status
- fixture-label
- scientific-state safety
- theme light/dark
- responsive smoke

Visual regression: recommended phase-2.

## 9. Implementation increments (future)

1. Token contract + themes + StatusBadge + DemoDataLabel  
2. Form controls + Alert + Table + Progress  
3. Overlay (Tooltip/Modal/Drawer) + Navigation primitives  
4. Catalog/docs + a11y report gate  

## 10. Prohibited patterns

```text
Full external trading UI kits as default look
Neon / ticker / decorative gauges
Green/red P&L semantics
Color-only status
Hidden technical state
Fake economic results
Secrets in client bundles
Implementing app routes/pages under guise of design system without authorization
```
