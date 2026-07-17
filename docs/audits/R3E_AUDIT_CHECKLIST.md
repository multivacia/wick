# R3E — Checklist de Auditoria

## Temporalidade e leakage
- [ ] Holdout R3D não reutilizado
- [ ] Splits estritamente temporais
- [ ] Nested walk-forward correto
- [ ] Scaler ajustado apenas no treino
- [ ] Encoder ajustado apenas no treino
- [ ] Imputação ajustada apenas no treino
- [ ] Threshold escolhido apenas no treino
- [ ] Hiperparâmetros escolhidos apenas no treino interno

## Comparação
- [ ] M4 e M5 usam as mesmas observações
- [ ] Custos idênticos
- [ ] Horizonte idêntico
- [ ] Política de sobreposição idêntica
- [ ] Delta M5-M4 calculado diretamente
- [ ] Nenhum ativo removido após resultados

## Features
- [ ] Apenas features aprovadas
- [ ] Nenhuma feature futura
- [ ] UNKNOWN preservado
- [ ] Categorias desconhecidas auditadas
- [ ] Nenhum identificador memoriza o período

## Estatística
- [ ] Block bootstrap temporal
- [ ] FDR por família
- [ ] p-value bruto e ajustado
- [ ] Tamanho do efeito
- [ ] IC 95%
- [ ] Seed reproduzível
- [ ] Concentração temporal
- [ ] Concentração por ativo

## Economia
- [ ] Retorno líquido
- [ ] Três cenários de custo
- [ ] Long-only
- [ ] Bearish não virou short
- [ ] Drawdown e exposição
- [ ] Número de operações

## Integridade
- [ ] Manifesto congelado
- [ ] Grid não ampliado
- [ ] Períodos não escolhidos depois
- [ ] Resultados negativos visíveis
- [ ] R4 não iniciado
- [ ] Dados futuros ainda exigidos
