# UX-R1-I5 — Application Shell and Navigation — Implementation Specification

```text
RELEASE = UX-R1
INCREMENT = I5
TASK_ID = APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION-001
PHASE = IMPLEMENTATION
CHANGE_RISK = MEDIUM
SPEC_STATUS = IMPLEMENTED
IMPACT_ASSESSMENT_PATH = docs/ai-impact/UX-R1-I5-APPLICATION-SHELL-AND-NAVIGATION-IMPLEMENTATION_IMPACT_ASSESSMENT.md
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
IMPLEMENTATION_STATUS = COMPLETE
I5_IMPLEMENTATION_AUTHORIZED = true
ROUTER_INSTALLATION_AUTHORIZED = true
I5_MERGE_AUTHORIZED = false
I6_VIEWMODEL_IMPLEMENTATION_AUTHORIZED = false
I6_FIXTURE_IMPLEMENTATION_AUTHORIZED = false
I6_SCREEN_IMPLEMENTATION_AUTHORIZED = false
OPERATIONAL_DATA_INTEGRATION_AUTHORIZED = false
UI_SCREEN_IMPLEMENTATION_AUTHORIZED = false
PARALLEL_TASKS_ALLOWED = false
ROUTER_PACKAGE = react-router-dom@7.18.1
NEW_RUNTIME_DEPENDENCIES = 1
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
REVIEW_STATUS = APPROVED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
CREATED_AT = 2026-07-20T12:06:00Z
```

## Scope delivered

```text
ApplicationShell, PrimarySidebar, MobileNavigationDrawer, TopBar,
MainContentRegion, SkipLink, NavigationItem, NavigationGroup,
ThemeControl, RoutePlaceholder, AppRoutes / AppRouter
```

Location: `web/src/shell/`, `web/src/app/`. Styling: `shell.css` using only `--wick-*` tokens.

## Routes

```text
/ → /overview
/overview
/future-collection/runs
/future-collection/readiness
/operations/host-scheduler
* → not-found placeholder
```

Divergence from I5A path names (`/collection/*`, `/ops/host`) is intentional per authorized human prompt; documented in impact assessment.

## Responsive

```text
SIDEBAR_COLLAPSE_BEHAVIOR = persistent sidebar at min-width 1024px;
  below that, sidebar CSS-hidden and MobileNavigationDrawer via I3 Drawer
```

## Accessibility notes

```text
AUTOMATED = axe smoke + keyboard + drawer Escape/close-after-nav
MANUAL_REMAINING = full SR matrix; zoom 200% layout across host devices
```
