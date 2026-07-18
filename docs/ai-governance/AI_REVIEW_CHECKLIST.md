# Checklist de Revisão de Mudanças Geradas por IA

## Identificação

- [ ] Task ID informado
- [ ] Branch dedicada
- [ ] Commit-base identificado
- [ ] PR em draft
- [ ] Escopo compatível com a especificação

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
- [ ] Resultado real dos testes foi registrado
- [ ] Testes cobrem casos negativos
- [ ] Testes cobrem limites
- [ ] CI está verde
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
