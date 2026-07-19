# UX-R1-OPERATIONAL-LANGUAGE-MICROCOPY-001 — Análise de Impacto

## Metadados

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B4
TASK_ID = OPERATIONAL-LANGUAGE-MICROCOPY-001
TITLE = Operational Language and Microcopy System
CHANGE_RISK = MEDIUM
PHASE = CONTENT_DESIGN_AND_GOVERNANCE
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
UX_B4_IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
DESIGN_SYSTEM_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
OLD_BASE_SHA = 5e438b8ad84d13f0c22c4017d3d3e26ac3c26647
BASE_SHA = b0303cf8b7017a87da9eec546126daef64f458a4
NEW_BASE_SHA = b0303cf8b7017a87da9eec546126daef64f458a4
REBASING_STATUS = COMPLETE
CONFLICTS_RESOLVED = docs/PROJECT.md, docs/ux/UX-R1_BACKLOG.md
ANALYZED_AT = 2026-07-19T13:26:43Z
RECONCILED_AT = 2026-07-19T15:40:00Z
ANALYZED_BY = cursor-agent
APPROVED_BY = cursor-agent
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
RECOMMENDED_DECISION = APPROVED
DECISION = APPROVED
FULL_TEST_SUITE = PASS (226 passed, 23 skipped)
LINT_STATUS = PASS
GOVERNANCE_VALIDATOR = ERRORS_0_WARNINGS_0
```

Authorization note: `IMPLEMENTATION_AUTHORIZED=true` covers **this documentation package only** (content design + governance merge). It does **not** authorize UI code, design-system code, collection commands, scheduler activation, or `validate`. `UX_B4_IMPLEMENTATION_AUTHORIZED=false` and `UI_IMPLEMENTATION_AUTHORIZED=false` remain binding.

Rebase note: rebased onto `origin/main` (`b0303cf`) preserving UX-B2 authorization track (PR #43 MERGED, I1-only) and UX-B3 independent/parallel track. UX-B4 status set to `CONTENT_DESIGN_READY_FOR_HUMAN_REVIEW`.

## SUMMARY

Define the official operational language system for UX-R1: glossary, status semantics, empty states, failure/warning microcopy, and scientific/economic guardrails. Docs-only; R3E scientific state unchanged.

## CURRENT_LANGUAGE_STATE

| Asset | State |
|-------|-------|
| Foundation language guide | Exists (`WICK_UX_LANGUAGE_AND_TERMINOLOGY_GUIDE.md`) — partial glossary |
| Status catalog | Missing before this task |
| Empty-state catalog | Missing before this task |
| Failure microcopy mapped to taxonomy | Missing before this task |
| Economic/scientific copy guardrails (dedicated) | Partial in foundation; expanded here |
| UI strings in code | None (no frontend) |

## TERMINOLOGY_RISKS

- Operators confuse collection success with scientific approval.
- English jargon (`store`, `scheduler`, `readiness`) without Portuguese first.
- Code/reason mismatches (`SERIES_INCOMPLETE` UX vs `SERIES_INSUFFICIENT` runtime) if technical layer omitted.

Mitigation: two-layer rule; bilingual policy; explicit code-alignment notes.

## STATUS_COMMUNICATION_RISKS

- `NOT_READY` painted as ERROR.
- `READY` implying validate authorization.
- Deferred debt styled as complete.
- Green implying profit.

Mitigation: status catalog mandatory rules + visual direction cross-reference.

## SCIENTIFIC_SAFETY

No change to readiness/validate/gates. Copy forbids premature validation language and effect peeking narratives.

## ECONOMIC_INTERPRETATION_SAFETY

`ECONOMIC_INTERPRETATION_ALLOWED=false` preserved. Prohibited phrases and safe replacements locked in guardrails doc.

## ACCESSIBILITY

Sentence complexity, first-use expansion, screen-reader wording, non-color meaning defined in language guide §10.

## LOCALIZATION

`pt-BR` formats mandatory; technical IDs remain ASCII.

## DEPENDENCIES

| Dependency | Relationship |
|------------|--------------|
| UX-B1 foundation | Reused; not modified in behavior |
| UX-B2 design system | Independent parallel track; defines future DS/frontend architecture (impacto MERGED; I1 auth MERGED; execution still blocked) |
| UX-B3 screen contracts | Independent parallel track; defines operational screen/data/state contracts (not duplicated here) |
| Failure taxonomy | Source of truth for failure codes |
| R3E readiness runtime | Codes referenced; not changed |

## IMPLEMENTATION_BOUNDARY

```text
ALLOWED = docs/ux catalogs, impact, review, handoff, PROJECT.md status fields, ux README/backlog notes
FORBIDDEN = UI components, routes, themes, APIs, runtime, migrations, scheduler enablement, validate
```

## TEST_STRATEGY

| Layer | Action |
|-------|--------|
| pytest | Full suite must PASS (no code change expected) |
| ruff | PASS |
| governance validator | Validate impact assessment artifact → ERRORS_0_WARNINGS_0 |
| content review | Independent review checklist |

## ROLLBACK_STRATEGY

Revert documentation commits / close PR. No runtime rollback needed.

## BLOCKERS

None for documentation merge. UI microcopy implementation remains blocked until explicit UI authorization.

Human merge authorization still required.

## DECISION

```text
DECISION = APPROVED
```

Content design package approved for human merge review. UI implementation not authorized.

## 1. Objetivo

Produzir o sistema oficial de linguagem operacional e microcopy do UX-R1 sem implementar UI nem alterar estado científico R3E.

## 2. Contexto técnico

Frontend ausente. Fundação UX-B1 mergeada. Impacto UX-B2 mergeado; implementação DS bloqueada. Host discovery adiada; scheduler bloqueado; coleta future-unseen em progresso operacional separado.

## 3. Componentes afetados

Documentação UX e artefatos de governança AI. Nenhum componente runtime.

## 4. Arquivos previstos

```text
docs/ux/UX-R1-OPERATIONAL-LANGUAGE-GUIDE.md
docs/ux/UX-R1-STATUS-MESSAGE-CATALOG.md
docs/ux/UX-R1-EMPTY-STATE-CATALOG.md
docs/ux/UX-R1-FAILURE-AND-WARNING-MICROCOPY.md
docs/ux/UX-R1-SCIENTIFIC-AND-ECONOMIC-LANGUAGE-GUARDRAILS.md
docs/ai-impact/UX-R1-OPERATIONAL-LANGUAGE-MICROCOPY-001_IMPACT_ASSESSMENT.md
docs/ai-reviews/UX-R1-OPERATIONAL-LANGUAGE-MICROCOPY_REVIEW.md
reports/ai-implementation/UX-R1-OPERATIONAL-LANGUAGE-MICROCOPY_HANDOFF.md
docs/PROJECT.md
docs/ux/README.md
docs/ux/UX-R1_BACKLOG.md
```

## 5. Contratos e interfaces

Nenhum contrato de API alterado. Contratos de copy (status/empty/failure) tornam-se referência para UX-B3+ quando UI for autorizada.

## 6. Persistência e dados

Nenhuma migration; nenhum schema; nenhum store touch.

## 7. Concorrência, locks e idempotência

Sem mudança. Linguagem de lock alinhada à taxonomia (`LOCK_ACTIVE` ≠ falha).

## 8. Segurança

Sem segredos. Copy instrui redação de credenciais e proíbe inventar host values.

## 9. Observabilidade

Microcopy referencia `run_id`, failure codes e evidências; não altera logging runtime.

## 10. Operação

Linguagem de débito operacional (`HOST_DISCOVERY=DEFERRED`, `OPERATIONAL_DEBT=OPEN`, `SCHEDULER_ACTIVATION=BLOCKED`) padronizada.

## 11. Rollback

Git revert dos docs. Sem estado operacional a desfazer.

## 12. Compatibilidade

Compatível com fundação B1; estende glossário. Não conflita com DS B2 (independente).

## 13. Testes necessários

pytest + ruff + `python scripts/validate_ai_governance_artifacts.py` no impact assessment.

## 14. Alternativas consideradas

| Option | Outcome |
|--------|---------|
| A — Only expand foundation guide | Rejected: missing status/empty/failure catalogs required by UX-B4 prompt |
| B — Full catalogs + guardrails (chosen) | Approved: complete content system |
| C — Implement UI strings in code now | Rejected: UI unauthorized |

## 15. Riscos

| Risk | Severity | Mitigation |
|------|----------|------------|
| Backlog ID collision (older B4 = Collection Runs prototype) | MEDIUM | Document TASK_ID `OPERATIONAL-LANGUAGE-MICROCOPY-001`; backlog note |
| Runtime code alias drift | LOW | Technical layer shows exact runtime code |
| Reviewers treat docs as UI auth | MEDIUM | Explicit false flags in PROJECT/handoff |

## 16. Questões abertas

Nenhuma bloqueante. Futuro: amarrar strings a componentes quando UI for autorizada (fora deste pacote).

## 17. Decisão arquitetural recomendada

Manter linguagem como **fonte documental versionada** consumida por contratos de tela futuros; sem i18n runtime neste estágio.

## 18. Critérios para autorizar implementação

UI microcopy implementation requires **all**:

```text
UX_B4_IMPLEMENTATION_AUTHORIZED = true   (explicit human)
UI_IMPLEMENTATION_AUTHORIZED = true      (explicit human)
UX-B3 contracts consuming catalogs (or equivalent)
No R3E scientific state change implied by copy
```

This PR does not set those flags to true.
