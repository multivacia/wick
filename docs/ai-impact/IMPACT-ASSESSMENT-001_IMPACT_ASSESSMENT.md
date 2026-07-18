# IMPACT-ASSESSMENT-001 — Análise de Impacto Arquitetural

## Metadados

```text
TASK_ID = IMPACT-ASSESSMENT-001
CHANGE_RISK = HIGH
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
REPOSITORY = multivacia/wick
BASE_BRANCH = main
BASE_SHA = fd4cf1df3961a2411c3e367fd675b89ef05858a6
ANALYZED_AT = 2026-07-18T20:06:48Z
ANALYZED_BY = cursor-agent
PHASE = IMPLEMENTATION_AUTHORIZED
RELATED_SPEC = AI-GOVERNANCE / G1 / IMPACT-ASSESSMENT-001
ENFORCEMENT_EFFECTIVE_FROM = AFTER_MERGE_OF_IMPACT_ASSESSMENT_GATE
```

## 1. Objetivo

Formalizar um gate obrigatório de análise de impacto arquitetural entre especificação aprovada e autorização de implementação, com classificação de risco, template, workflow e validador offline.

## 2. Contexto técnico

O Wick já possui specs, reviews, guardrails e um validador estrutural offline. Falta uma etapa explícita que force desenho, riscos, rollback e contratos **antes** do código — especialmente para automação, locks, filesystem e dados científicos.

## 3. Componentes afetados

- `docs/ai-governance/*` (workflow, checklist, roles, guardrails)
- `docs/ai-impact/*` (novo)
- `templates/*` (novo template + atualização de templates existentes)
- `src/wick/ai_governance/artifact_validator.py`
- `scripts/validate_ai_governance_artifacts.py`
- `tests/test_ai_governance_artifact_validator.py`

## 4. Arquivos previstos

- criar `templates/AI_IMPACT_ASSESSMENT_TEMPLATE.md`
- criar `docs/ai-impact/README.md`
- criar este arquivo de impacto
- atualizar docs de governança e templates
- evoluir validador e testes
- criar handoff `reports/ai-implementation/AI-GOV-G1-IMPACT-001_HANDOFF.md`

## 5. Contratos e interfaces

- novo contrato documental: campos `CHANGE_RISK`, `IMPACT_ASSESSMENT_STATUS`, `IMPLEMENTATION_AUTHORIZED`
- validador passa a rejeitar MEDIUM/HIGH/CRITICAL sem impacto aprovado
- artefatos legados sem os novos campos permanecem válidos (`LEGACY_PRE_IMPACT_GATE` ou ausência dos campos)

## 6. Persistência e dados

Sem alteração de store científico, manifests ou dados operacionais. Apenas arquivos markdown/código de governança.

## 7. Concorrência, locks e idempotência

Não introduz locks de runtime. O gate é documental/validador. Idempotente: revalidar artefatos não muda estado científico.

## 8. Segurança

- sem segredos
- sem mudança de permissões
- sem authorize validate
- reforça fail-closed: implementação bloqueada até impacto aprovado

## 9. Observabilidade

- issues estruturais do validador (`error`/`warning`)
- handoff e PR draft registram enforcement e status B4

## 10. Operação

Após merge, novas tarefas MEDIUM+ devem criar impacto antes do código. B4 aberto deve retornar a `IMPACT_ANALYSIS_ONLY` até produzir impacto aprovado.

## 11. Rollback

Reverter o merge do PR de governança remove o enforcement novo. Artefatos históricos não precisam ser reescritos.

## 12. Compatibilidade

```text
LEGACY_PRE_IMPACT_GATE = true
```

permitido para entregas anteriores. Novas tarefas após `ENFORCEMENT_EFFECTIVE_FROM` seguem o gate.

## 13. Testes necessários

- LOW sem arquivo independente
- MEDIUM sem impacto → erro
- HIGH draft → erro
- HIGH aprovado → válido
- implementação antes da aprovação → erro
- campos/seções ausentes → erro
- BLOCKED ⇒ não autoriza implementação
- compatibilidade histórica

## 14. Alternativas consideradas

1. Apenas checklist textual sem validador — rejeitada (não enforce).
2. Exigir impacto para LOW também — rejeitada (ruído).
3. Gate documental + validador offline — escolhida.

## 15. Riscos

- falso negativo se artefato omitir `CHANGE_RISK` deliberadamente — mitigado por checklist/review humana
- atrito em mudanças rápidas — mitigado por LOW simplificado
- B4 já implementado em PR aberta — mitigado por bloqueio explícito pós-merge deste gate

## 16. Questões abertas

Nenhuma material. `ENFORCEMENT_EFFECTIVE_FROM` concreto = merge commit deste PR.

## 17. Decisão arquitetural recomendada

Implementar o gate documental + validador agora; não tocar no código do B4 nesta tarefa.

## 18. Critérios para autorizar implementação

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
CHANGE_RISK = HIGH
```

Autoriza apenas a mudança de governança G1; não autoriza implementação/continuação do B4.
