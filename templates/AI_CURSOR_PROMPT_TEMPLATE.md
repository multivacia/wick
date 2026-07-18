# Prompt de execução — <TASK_ID>

Você é o agente executor desta tarefa.

Leia integralmente:

```text
docs/ai-governance/
docs/ai-specs/<TASK_ID>_SPEC.md
```

## Regras obrigatórias

1. Trabalhe em branch dedicada.
2. Não altere a `main`.
3. Não expanda o escopo.
4. Não reescreva a especificação.
5. Não faça merge.
6. Não use force-push.
7. Execute os testes definidos na especificação.
8. Gere:
   `reports/ai-implementation/<TASK_ID>_IMPLEMENTATION_REPORT.md`
9. Pare após concluir a implementação e o relatório.

## Proibições científicas

- não executar `validate`;
- não consultar métricas de efeito;
- não alterar cutoff;
- não alterar freeze;
- não alterar thresholds congelados;
- não liberar interpretação econômica;
- não iniciar R4 ou R5.

## Resultado esperado

```text
IMPLEMENTATION_STATUS = COMPLETE
REVIEW_STATUS = PENDING
MERGE_STATUS = BLOCKED
```
