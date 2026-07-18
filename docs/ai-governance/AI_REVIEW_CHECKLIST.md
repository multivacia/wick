# Checklist de Revisão de Mudanças Geradas por IA

## Identificação

- [ ] Task ID informado
- [ ] Branch dedicada
- [ ] Commit-base identificado (`BASE_SHA_AT_REVIEW`)
- [ ] `HEAD_SHA_AT_REVIEW` = tip efetivamente revisado
- [ ] `CURRENT_PR_HEAD` consultado no GitHub/Git
- [ ] Se `CURRENT_PR_HEAD != HEAD_SHA_AT_REVIEW`, há reconciliação/revisão complementar/`CHANGES_REQUIRED`
- [ ] PR em draft
- [ ] Escopo compatível com a especificação
- [ ] `CHANGE_RISK` classificado
- [ ] Impacto pré-implementação presente/aprovado quando exigido (`MEDIUM|HIGH|CRITICAL`)
- [ ] `IMPLEMENTATION_AUTHORIZED = true` somente após impacto aprovado
- [ ] Revisão confirma que o desenho aprovado no impacto foi seguido
- [ ] Campos Git/CI/testes preenchidos a partir de fonte real (não só prompt)

## Diff

- [ ] Todos os arquivos alterados foram listados
- [ ] Não há alterações fora do escopo
- [ ] Não há refatoração oportunista
- [ ] Não há mudanças cosméticas desnecessárias
- [ ] Não há segredos ou credenciais
- [ ] Não há código morto novo
- [ ] Não há flags inseguras

## Comportamento

- [ ] Critérios de aceite atendidos
- [ ] Casos de erro tratados
- [ ] Idempotência verificada quando aplicável
- [ ] Timezones tratados quando aplicável
- [ ] Entradas inválidas rejeitadas
- [ ] Falhas parciais não corrompem estado

## Testes

- [ ] Testes novos foram adicionados
- [ ] Testes existentes continuam passando
- [ ] `TESTS_EXECUTED_THIS_REVIEW` registra apenas o que foi reexecutado agora
- [ ] `DECLARED_PREVIOUS_TESTS` não é apresentado como reexecução
- [ ] Testes cobrem casos negativos
- [ ] Testes cobrem limites
- [ ] `CI_STATUS` / `CI_CHECKED_AT` referem-se ao tip atual (`CURRENT_PR_HEAD`)
- [ ] Nenhum teste foi removido para “fazer passar”

## Documentação

- [ ] Runbook atualizado
- [ ] Auditoria atualizada
- [ ] Relatório de implementação presente
- [ ] Estados oficiais atualizados corretamente
- [ ] Limitações registradas

## Segurança científica

- [ ] `validate` não foi executado sem autorização
- [ ] Nenhuma métrica de efeito foi consultada
- [ ] Cutoff inalterado
- [ ] Freeze inalterado
- [ ] Thresholds inalterados
- [ ] Custos e grids inalterados
- [ ] Nenhum peeking foi realizado
- [ ] Interpretação econômica permanece bloqueada quando aplicável
- [ ] R4 e R5 permanecem bloqueadas quando aplicável

## Decisão

```text
REVIEW_STATUS =
MERGE_STATUS =
REVIEWER =
REVIEWED_AT =
```

### Resultado permitido

- `APPROVED`
- `CHANGES_REQUIRED`
- `BLOCKED`

Mesmo quando aprovado:

```text
MERGE_STATUS = AWAITING_HUMAN_AUTHORIZATION
```
