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

## 10. Regra de parada

Se qualquer etapa detectar mudança fora do escopo, quebra científica, teste insuficiente ou evidência contraditória:

```text
IMPLEMENTATION_STATUS = BLOCKED
MERGE_STATUS = BLOCKED
```
