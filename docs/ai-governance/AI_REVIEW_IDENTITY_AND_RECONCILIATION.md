# Identidade de Revisão e Reconciliação de HEAD

## Objetivo

Impedir que revisões aprovadas para um commit antigo sejam tratadas como válidas para um tip diferente sem reconciliação explícita.

## Campos obrigatórios

```text
REPOSITORY
PULL_REQUEST
BASE_BRANCH
HEAD_BRANCH
BASE_SHA_AT_REVIEW
HEAD_SHA_AT_REVIEW
CURRENT_PR_HEAD
ORIGINAL_IMPLEMENTATION_COMMITS
REVIEW_COMMITS
CI_STATUS
CI_CHECKED_AT
DECLARED_PREVIOUS_TESTS
TESTS_EXECUTED_THIS_REVIEW
VALIDATION_COMMAND_EXECUTED
EFFECT_PEEKING_PERFORMED
R3E_GATE
ECONOMIC_INTERPRETATION_ALLOWED
R4_STATUS
R5_STATUS
MERGE_STATUS
```

## Fonte da verdade

Nenhum campo derivado de Git, GitHub, CI ou testes pode ser preenchido apenas com base em texto fornecido no prompt. Consultar a fonte correspondente.

## Regra soberana

Uma revisão só é válida para `HEAD_SHA_AT_REVIEW`.

Se `CURRENT_PR_HEAD != HEAD_SHA_AT_REVIEW`:

```text
A. reconciliar formalmente commits adicionais como não materiais; ou
B. realizar revisão complementar; ou
C. REVIEW_STATUS = CHANGES_REQUIRED
```

## Reconciliação documental

Quando aplicável, registrar:

```text
PREVIOUSLY_REVIEWED_HEAD =
CURRENT_REVIEWED_HEAD =
COMMITS_RECONCILED =
CHANGE_CLASSIFICATION = DOCUMENTATION_AND_GOVERNANCE_ONLY | CODE_OR_BEHAVIOR_CHANGED
TECHNICAL_REVIEW_REMAINS_VALID =
SCIENTIFIC_SAFETY_REVIEW_REMAINS_VALID =
```

Se `CHANGE_CLASSIFICATION = CODE_OR_BEHAVIOR_CHANGED`, a opção A não basta: executar B ou C.

## Status histórico vs atual

Em relatórios de implementação, preferir:

```text
IMPLEMENTATION_STATUS
REVIEW_STATUS_AT_IMPLEMENTATION_REPORT_CREATION
CURRENT_REVIEW_STATUS
CURRENT_MERGE_STATUS
```

## Política do commit de identidade

O commit que apenas grava/atualiza campos de identidade (`HEAD_SHA_AT_REVIEW`, `CURRENT_PR_HEAD`, `CI_*`, reconciliação) avança o tip em um SHA.

Esse commit de identidade é classificado como `DOCUMENTATION_AND_GOVERNANCE_ONLY`.

Não encadear infinitamente novos commits só para auto-referenciar o próprio SHA. Registrar:

```text
HEAD_SHA_AT_REVIEW = <tip de conteúdo revisado>
CURRENT_PR_HEAD = <tip real consultado no Git após o push>
```

Se diferirem apenas pelo commit de identidade/pin, reconciliar formalmente e manter `TECHNICAL_REVIEW_REMAINS_VALID = true`.

## Enforcement

Usar `scripts/validate_ai_governance_artifacts.py` para checagens estruturais offline.
