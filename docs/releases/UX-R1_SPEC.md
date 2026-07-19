# UX-R1 — WICK OPERATIONAL EXPERIENCE

## Identidade da release

```text
RELEASE_ID = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
RELEASE_THEME = Accessible operational and scientific experience
RELEASE_STATUS = PLANNING
RELEASE_OWNER = Gustavo Almeida
BACKLOG_ITEM = UX-B1
TASK_ID = UX-RELEASE-FOUNDATION-001
PHASE = RELEASE_DEFINITION_AND_DESIGN_FOUNDATION
CHANGE_RISK = MEDIUM
IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
CREATED_AT = 2026-07-19T03:13:15Z
```

## Objetivo

Transformar o WICK em uma interface operacional compreensível, segura e auditável para não-economistas, preservando a terminologia financeira, estatística e científica formal como camada explicativa secundária.

## Independência científica

Esta release é **paralela** ao estado científico de R3E. Não deve:

- modificar modelos R3E;
- executar coleta;
- executar `validate`;
- alterar readiness;
- ativar scheduler;
- expor resultados econômicos;
- alterar thresholds científicos congelados;
- desbloquear R4 ou R5.

## Fonte de verdade UX

| Artefato | Caminho |
|----------|---------|
| Princípios | `docs/ux/WICK_UX_PRINCIPLES.md` |
| Personas | `docs/ux/WICK_UX_PERSONAS.md` |
| Linguagem | `docs/ux/WICK_UX_LANGUAGE_AND_TERMINOLOGY_GUIDE.md` |
| Direção visual | `docs/ux/WICK_VISUAL_DIRECTION.md` |
| Arquitetura de informação | `docs/ux/WICK_INFORMATION_ARCHITECTURE.md` |
| Backlog | `docs/ux/UX-R1_BACKLOG.md` |
| Spec de fundação | `docs/ai-specs/UX-R1-EXPERIENCE-FOUNDATION_SPEC.md` |
| Impacto | `docs/ai-impact/UX-RELEASE-FOUNDATION-001_IMPACT_ASSESSMENT.md` |
| Review | `docs/ai-reviews/UX-R1-EXPERIENCE-FOUNDATION_REVIEW.md` |

## MVP funcional (protótipo)

1. Visão Geral
2. Execuções da Coleta
3. Prontidão
4. Host e Automação
5. Experimento R3E — vista explicativa

Implementação de telas **não autorizada** nesta tarefa (`UI_IMPLEMENTATION_AUTHORIZED = false`).

## Relação com R3E

```text
UX_TRACK = PARALLEL
R3E_SCIENTIFIC_STATE = UNCHANGED
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA (inalterado)
R4_STATUS = BLOCKED (inalterado)
R5_STATUS = NOT_STARTED (inalterado)
```
