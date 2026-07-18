# <TASK_ID> — Análise de Impacto Arquitetural

## Metadados

```text
TASK_ID =
CHANGE_RISK = LOW | MEDIUM | HIGH | CRITICAL
IMPACT_ASSESSMENT_STATUS = DRAFT | PENDING_REVIEW | APPROVED | CHANGES_REQUIRED | BLOCKED
IMPLEMENTATION_AUTHORIZED = false
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA =
ANALYZED_AT =
ANALYZED_BY =
PHASE = IMPACT_ANALYSIS_ONLY
RELATED_SPEC =
```

Regra: para `CHANGE_RISK = MEDIUM | HIGH | CRITICAL`, a implementação só pode começar quando:

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
```

## 1. Objetivo

## 2. Contexto técnico

## 3. Componentes afetados

## 4. Arquivos previstos

## 5. Contratos e interfaces

## 6. Persistência e dados

## 7. Concorrência, locks e idempotência

## 8. Segurança

## 9. Observabilidade

## 10. Operação

## 11. Rollback

## 12. Compatibilidade

## 13. Testes necessários

## 14. Alternativas consideradas

## 15. Riscos

## 16. Questões abertas

## 17. Decisão arquitetural recomendada

## 18. Critérios para autorizar implementação

```text
IMPACT_ASSESSMENT_STATUS =
IMPLEMENTATION_AUTHORIZED =
CHANGE_RISK =
```
