# Fluxo Oficial de Mudanças com IA

## 1. Objetivo

Definir o processo obrigatório para qualquer mudança criada ou apoiada por IA.

## 2. Estrutura de artefatos

```text
docs/
├── ai-specs/
│   └── <TASK_ID>_SPEC.md
├── ai-impact/
│   └── <TASK_ID>_IMPACT_ASSESSMENT.md
├── ai-reviews/
│   └── <TASK_ID>_REVIEW.md
└── ai-governance/

prompts/
├── cursor/
│   └── <TASK_ID>_CURSOR_PROMPT.md
└── codex/
    └── <TASK_ID>_CODEX_PROMPT.md

reports/
└── ai-implementation/
    └── <TASK_ID>_IMPLEMENTATION_REPORT.md
```

## 3. Estados oficiais da tarefa

```text
SPEC_STATUS = DRAFT | APPROVED
CHANGE_RISK = LOW | MEDIUM | HIGH | CRITICAL
IMPACT_ASSESSMENT_STATUS =
  NOT_REQUIRED | DRAFT | PENDING_REVIEW | APPROVED | CHANGES_REQUIRED | BLOCKED
IMPLEMENTATION_AUTHORIZED = false | true
IMPLEMENTATION_STATUS = NOT_STARTED | IN_PROGRESS | COMPLETE | BLOCKED
REVIEW_STATUS = PENDING | APPROVED | CHANGES_REQUIRED | BLOCKED
MERGE_STATUS = BLOCKED | AWAITING_HUMAN_AUTHORIZATION | MERGED
```

## 4. Sequência obrigatória

```text
1. Especificação
2. Análise de Impacto Arquitetural
3. Aprovação da Análise de Impacto
4. Prompt de Implementação
5. Implementação
6. Revisão Independente
7. Autorização Humana
8. Pós-merge
```

## 5. Etapa 1 — Especificação

A especificação deve definir:

- objetivo;
- motivação;
- escopo;
- não escopo;
- critérios de aceite;
- arquivos esperados;
- testes obrigatórios;
- riscos;
- restrições científicas;
- ações proibidas;
- estado esperado após a implementação;
- `CHANGE_RISK` preliminar.

Nenhuma implementação começa com `SPEC_STATUS = DRAFT`.

## 6. Etapa 2 — Análise de Impacto Arquitetural

Antes do código, a análise responde:

```text
WHAT_WILL_CHANGE
WHAT_CAN_BREAK
WHICH_CONTRACTS_ARE_AFFECTED
WHICH_ARCHITECTURE_WILL_BE_USED
WHICH_RISKS_REMAIN
HOW_TO_TEST
HOW_TO_ROLL_BACK
```

### Classificação de risco

| CHANGE_RISK | Exigência |
|---|---|
| LOW | Análise simplificada na spec (`IMPACT_ASSESSMENT_STATUS=NOT_REQUIRED`) |
| MEDIUM | Arquivo independente em `docs/ai-impact/` |
| HIGH | Arquivo independente + revisão + autorização explícita |
| CRITICAL | Análise reforçada + autorização humana específica |

Durante a análise:

```text
PHASE = IMPACT_ANALYSIS_ONLY
IMPLEMENTATION_AUTHORIZED = false
```

Proibido nesta fase: alterar código, migrations, dados, abrir PR de implementação.

Se houver ambiguidade material:

```text
IMPACT_ASSESSMENT_STATUS = BLOCKED
```

e solicitar decisão humana.

### Gate de autorização

Para `CHANGE_RISK = MEDIUM | HIGH | CRITICAL`:

```text
IMPACT_ASSESSMENT_STATUS = APPROVED
IMPLEMENTATION_AUTHORIZED = true
```

são obrigatórios **antes** de qualquer alteração de código.

## 7. Etapa 3 — Prompt de execução

O prompt para Cursor ou Codex deve:

- referenciar a especificação **e** o impacto aprovado;
- declarar `IMPLEMENTATION_AUTHORIZED = true` somente se o impacto estiver aprovado;
- proibir expansão de escopo;
- exigir branch dedicada;
- exigir relatório de implementação;
- listar comandos permitidos e proibidos;
- exigir testes;
- impedir merge automático.

## 8. Etapa 4 — Implementação

O executor deve:

1. confirmar branch e commit-base;
2. confirmar impacto aprovado / autorização;
3. implementar apenas o escopo;
4. executar testes;
5. registrar falhas;
6. gerar o relatório de implementação;
7. abrir PR draft quando aplicável;
8. parar sem fazer merge.

## 9. Etapa 5 — Revisão independente

A revisão pós-implementação responde:

```text
WAS_THE_APPROVED_DESIGN_FOLLOWED
IS_THE_IMPLEMENTATION_CORRECT
ARE_THE_EVIDENCES_SUFFICIENT
```

E compara:

- especificação;
- análise de impacto aprovada;
- diff;
- testes;
- relatório de implementação;
- CI;
- restrições científicas.

Decisão:

```text
REVIEW_STATUS = APPROVED | CHANGES_REQUIRED | BLOCKED
```

## 10. Etapa 6 — Autorização humana

Mesmo com revisão aprovada:

```text
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

Somente uma pessoa autorizada pode decidir o merge.

## 11. Etapa 7 — Pós-merge

Após o merge, registrar:

- PR;
- merge commit;
- horário;
- CI;
- estado oficial alterado;
- itens que permaneceram bloqueados;
- próximos passos.

## 12. Compatibilidade histórica

```text
ENFORCEMENT_EFFECTIVE_FROM = AFTER_MERGE_OF_IMPACT_ASSESSMENT_GATE
```

Artefatos anteriores ao merge do gate G1 podem declarar:

```text
LEGACY_PRE_IMPACT_GATE = true
```

Não reescrever a história. Novas tarefas após a vigência devem seguir o gate.

## 13. Identidade Git obrigatória em artefatos

Campos derivados de Git/GitHub/CI/testes **não** podem ser preenchidos apenas com texto de prompt. Devem ser consultados na fonte.

Campos mínimos em specs, relatórios e revisões:

```text
REPOSITORY
PULL_REQUEST
BASE_BRANCH
HEAD_BRANCH
BASE_SHA_AT_REVIEW
HEAD_SHA_AT_REVIEW
CURRENT_PR_HEAD
CHANGE_RISK
IMPACT_ASSESSMENT_STATUS
IMPLEMENTATION_AUTHORIZED
ORIGINAL_IMPLEMENTATION_COMMITS
REVIEW_COMMITS
CI_STATUS
CI_CHECKED_AT
TESTS_DECLARED_PREVIOUSLY / DECLARED_PREVIOUS_TESTS
TESTS_EXECUTED_THIS_REVIEW
VALIDATION_COMMAND_EXECUTED
EFFECT_PEEKING_PERFORMED
SCIENTIFIC_STATE (R3E_GATE, ECONOMIC_INTERPRETATION_ALLOWED, R4_STATUS, R5_STATUS)
MERGE_STATUS
```

### Validade da revisão pelo HEAD

Uma revisão só é válida para `HEAD_SHA_AT_REVIEW`.

Se `CURRENT_PR_HEAD != HEAD_SHA_AT_REVIEW`, a revisão deve:

```text
A. reconciliar formalmente os commits adicionais como não materiais; ou
B. realizar revisão complementar; ou
C. voltar para REVIEW_STATUS = CHANGES_REQUIRED
```

## 14. Regra de parada

Se qualquer etapa detectar mudança fora do escopo, quebra científica, teste insuficiente, impacto ausente/não aprovado ou evidência contraditória:

```text
IMPLEMENTATION_STATUS = BLOCKED
MERGE_STATUS = BLOCKED
IMPLEMENTATION_AUTHORIZED = false
```
