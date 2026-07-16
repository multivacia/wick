# Metodologia Quantitativa

## Objetivo

Avaliar se um padrão e seu contexto apresentam vantagem preditiva e, separadamente, se geram uma estratégia executável long-only após custos.

## Disponibilidade temporal

### Sem confirmação

- padrão concluído em `t`;
- sinal disponível após `close[t]`;
- entrada: `open[t+1]`.

### Com confirmação

- padrão concluído em `t`;
- confirmação conhecida após `close[t+1]`;
- entrada: `open[t+2]`.

É proibido usar confirmação de `t+1` e entrada em `open[t+1]`.

## Horizonte

`exit_index = entry_index + N - 1`

`exit_price = close[exit_index]`

Horizontes:
`N ∈ {1, 3, 5, 10}`

## Retornos

Long executável:

`gross_return = exit_price / entry_price - 1`

Direcional bearish, apenas como poder preditivo:

`directional_return = entry_price / exit_price - 1`

Não rotular retorno direcional bearish como lucro executável sem short explicitamente habilitado.

## Custos

Custos por lado:
- taxa de entrada;
- taxa de saída;
- slippage de entrada;
- slippage de saída.

Primeira versão:
`net_return = gross_return - total_cost`

Cenários:
- OPTIMISTIC
- BASE
- STRESSED

## Particionamento

- 70% inicial: treino/pesquisa.
- 30% final: holdout intocado.
- Walk-forward dentro dos 70%.
- Após congelar parâmetros, tocar o holdout uma única vez.

## Baselines

- entradas aleatórias pareadas;
- estratégia somente com tendência;
- retorno do ativo nas mesmas janelas;
- buy-and-hold como contexto;
- comparação ajustada por exposição quando aplicável.

## Significância

- block bootstrap temporal;
- intervalo de 95%;
- mínimo de 1.000 reamostragens;
- seed fixa;
- FDR Benjamini–Hochberg;
- exibir p-value bruto e ajustado.

## Amostras

- < 30: insuficiente;
- 30–99: exploratória;
- 100–299: evidência moderada;
- >= 300: mais confiável, ainda sujeita a dependência.

## Sobreposição

Produzir:
1. relatório de todos os sinais;
2. relatório executável sem posições simultâneas no mesmo ativo.

## Classificação de resultado

- PROMISING
- INCONCLUSIVE
- NO_EDGE
- NEGATIVE

## Relatório executivo obrigatório

Para cada estratégia:
- descrição simples;
- sinais;
- retorno líquido médio;
- intervalo de confiança;
- custo base e estressado;
- estabilidade;
- baseline;
- principais riscos;
- decisão recomendada.

## Auditoria

O motor próprio é a fonte auditável. vectorbt é usado como validação complementar. Resultados centrais devem coincidir dentro de tolerância definida.
