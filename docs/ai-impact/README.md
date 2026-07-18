# Análises de Impacto Arquitetural (AI Impact Gate)

Este diretório armazena análises de impacto **pré-implementação**.

## Quando é obrigatório

| CHANGE_RISK | Artefato |
|---|---|
| LOW | Análise simplificada dentro da spec (`IMPACT_ASSESSMENT_STATUS=NOT_REQUIRED`) |
| MEDIUM | `docs/ai-impact/<TASK_ID>_IMPACT_ASSESSMENT.md` independente |
| HIGH | Arquivo independente + revisão + autorização explícita |
| CRITICAL | Arquivo independente reforçado + autorização humana específica |

## Nome do arquivo

```text
docs/ai-impact/<TASK_ID>_IMPACT_ASSESSMENT.md
```

Template: `templates/AI_IMPACT_ASSESSMENT_TEMPLATE.md`

## Estados

```text
IMPACT_ASSESSMENT_STATUS =
  NOT_REQUIRED |
  DRAFT |
  PENDING_REVIEW |
  APPROVED |
  CHANGES_REQUIRED |
  BLOCKED

IMPLEMENTATION_AUTHORIZED = false | true
```

Durante a análise:

```text
PHASE = IMPACT_ANALYSIS_ONLY
IMPLEMENTATION_AUTHORIZED = false
```

É proibido alterar código, dados, migrations ou abrir PR de implementação nesta fase.

## Enforcement

```text
ENFORCEMENT_EFFECTIVE_FROM = AFTER_MERGE_OF_IMPACT_ASSESSMENT_GATE
```

Após o merge do gate G1, o valor efetivo é o merge commit correspondente.

Artefatos históricos podem declarar:

```text
LEGACY_PRE_IMPACT_GATE = true
```

## Relação com B4

Enquanto o B4 / `COLLECTION-AUTOMATION-001` não tiver impacto aprovado:

```text
B4_STATUS = IMPACT_ANALYSIS_REQUIRED
PHASE = IMPACT_ANALYSIS_ONLY
IMPLEMENTATION_AUTHORIZED = false
```

A PR de implementação do B4 não deve avançar sem `docs/ai-impact/COLLECTION-AUTOMATION-001_IMPACT_ASSESSMENT.md` aprovado.
