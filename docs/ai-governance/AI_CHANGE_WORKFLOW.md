# Fluxo Oficial de Mudanças com IA

## 1. Objetivo

Definir o processo obrigatório para qualquer mudança criada ou apoiada por IA.

## 2. Estrutura de artefatos

```text
docs/
├── ai-specs/
│   └── <TASK_ID>_SPEC.md
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
IMPLEMENTATION_STATUS = NOT_STARTED | IN_PROGRESS | COMPLETE | BLOCKED
REVIEW_STATUS = PENDING | APPROVED | CHANGES_REQUIRED | BLOCKED
MERGE_STATUS = BLOCKED | AWAITING_HUMAN_AUTHORIZATION | MERGED
```

## 4. Etapa 1 — Especificação

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
- estado esperado após a implementação.

Nenhuma implementação começa com `SPEC_STATUS = DRAFT`.

## 5. Etapa 2 — Prompt de execução

O prompt para Cursor ou Codex deve:

- referenciar a especificação;
- proibir expansão de escopo;
- exigir branch dedicada;
- exigir relatório de implementação;
- listar comandos permitidos e proibidos;
- exigir testes;
- impedir merge automático.

## 6. Etapa 3 — Implementação

O executor deve:

1. confirmar branch e commit-base;
2. implementar apenas o escopo;
3. executar testes;
4. registrar falhas;
5. gerar o relatório de implementação;
6. abrir PR draft quando aplicável;
7. parar sem fazer merge.

## 7. Etapa 4 — Revisão independente

A revisão deve comparar:

- especificação;
- diff;
- testes;
- relatório de implementação;
- CI;
- restrições científicas.

O revisor deve emitir uma decisão:

```text
REVIEW_STATUS = APPROVED
```

ou:

```text
REVIEW_STATUS = CHANGES_REQUIRED
```

ou:

```text
REVIEW_STATUS = BLOCKED
```

## 8. Etapa 5 — Autorização humana

Mesmo com revisão aprovada:

```text
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```

Somente uma pessoa autorizada pode decidir o merge.

## 9. Etapa 6 — Pós-merge

Após o merge, registrar:

- PR;
- merge commit;
- horário;
- CI;
- estado oficial alterado;
- itens que permaneceram bloqueados;
- próximos passos.

## 10. Identidade Git obrigatória em artefatos

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

Erros a impedir:

1. revisão aprovada para commit antigo sem reconciliação do tip;
2. relatório histórico com status atual ambíguo;
3. evidência declarada apresentada como teste reexecutado;
4. CI antigo confundido com CI do tip atual;
5. revisão documental autorizando merge implicitamente;
6. alteração posterior de código sem nova revisão;
7. hashes inventados ou desatualizados;
8. atualização de status sem timestamp/evidência;
9. execução acidental de validação científica em revisão operacional.

Ordem operacional:

1. consultar estado real do Git e da PR;
2. implementar;
3. executar testes permitidos;
4. gerar relatório com hashes reais;
5. atualizar branch com a base, quando necessário;
6. obter tip definitivo;
7. revisar o tip definitivo;
8. confirmar CI do mesmo tip;
9. gerar revisão formal;
10. bloquear merge até decisão humana.

## 11. Regra de parada

Se qualquer etapa detectar mudança fora do escopo, quebra científica, teste insuficiente ou evidência contraditória:

```text
IMPLEMENTATION_STATUS = BLOCKED
MERGE_STATUS = BLOCKED
```
