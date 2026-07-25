# Wick — Encerramento

**Repo:** `multivacia/wick`
**Status:** **ENCERRADO** — 25 de julho de 2026
**Motivo:** objetivo cumprido. A pergunta foi respondida.

> Leia este arquivo antes de qualquer outro. Ele existe porque o resultado do projeto está distribuído em 442 arquivos de documentação e não seria encontrado de outro modo.

---

## 1. A pergunta

> Padrões de candlestick apresentam vantagem preditiva líquida, após custos, fora da amostra?

## 2. A resposta

**Nenhuma vantagem mensurável foi encontrada.**

### Experimento `r3d-real-validation-v1` (16/07/2026)

| | |
|---|---|
| Gate final | `REJECTED_NO_MEASURABLE_EDGE_V1` |
| Combinações avaliadas | 3.840 |
| Aprovadas | **0** |
| Reprovadas | 568 |
| Inconclusivas | 3.272 |
| Holdout | consumido |

*Fonte: `reports/r3d/technical_summary.json`*

### Experimento `r3e-contextual-edge-v1` (18/07/2026)

Testou se o padrão de candle acrescenta informação **além** do contexto de mercado (M5 = contexto + candle, contra M4 = contexto puro).

| | |
|---|---|
| Classificação | `CANDLE_ADDS_NO_VALUE` |
| Séries | 20 (10 ativos × 1h, 1d) |
| `CONTEXT_HAS_NO_EDGE` | 115 |
| `INCONCLUSIVE` | 69 |
| `CANDLE_ADDS_NO_VALUE` | 16 |
| Positivos | **0** |
| Gate | `PENDING_FUTURE_UNSEEN_DATA` — R4 bloqueado, R5 não iniciado |

*Fonte: `reports/r3e_real/executive_report.json`*

**Universo:** BTC/USDT, ETH/USDT, SOL/USDT, BNB/USDT, XRP/USDT, PETR4.SA, VALE3.SA, ITUB4.SA, AAPL, MSFT.
**Padrões:** Doji, Hammer, Inverted Hammer, Shooting Star, Bullish/Bearish Engulfing, Morning/Evening Star.
**Horizontes:** 1, 3, 5, 10 candles. **Custos:** 4 cenários, BASE = 0,24% round-trip.

## 3. O que NÃO se pode concluir

Rigor exige delimitar o achado:

- **Não está provado que padrões de candlestick não funcionam.** A maioria das células (3.272 de 3.840) ficou *inconclusiva*, tipicamente por amostra insuficiente — não *rejeitada*.
- O resultado vale para **estes** padrões, **este** universo, **estes** horizontes, **esta** regra de entrada e saída (horizonte fixo, sem stop/alvo), **este** período.
- Regras discricionárias, timeframes menores, outros mercados ou combinações com filtros de contexto não foram testados de forma conclusiva.
- `ECONOMIC_INTERPRETATION_ALLOWED: false` nos relatórios — os números não autorizam interpretação econômica direta.

O que está estabelecido é mais modesto e mais útil: **nenhuma vantagem explorável foi encontrada onde se procurou, e a procura foi metodologicamente honesta.**

## 4. Como ler este repositório

Cinco arquivos importam:

| Arquivo | Por quê |
|---|---|
| `reports/r3d/technical_summary.json` | O veredito |
| `reports/r3e_real/executive_report.json` | O veredito contextual |
| `src/wick/patterns/detectors.py` | Detecção, 8 padrões, causal |
| `src/wick/backtest/engine.py` | Motor de trade auditável |
| `src/wick/quant/stats.py` | FDR, bootstrap em bloco, split temporal |

O resto — `web/` (17.800 linhas), `ops/`, `docs/ai-impact/`, `docs/ai-reviews/`, `docs/ai-specs/` — é infraestrutura e processo que não contribui para o achado.

## 5. Restrição para quem retomar

**O holdout foi consumido** (`holdout_consumed: true`).

Qualquer novo ciclo de ajuste sobre a mesma base histórica é contaminado: cada tentativa adicional sobre dados já vistos é garimpo de p-valor, e um "resultado positivo" obtido assim não significa nada. O próprio código reconhece isso — o gate está travado em `PENDING_FUTURE_UNSEEN_DATA`.

Retomada legítima exige uma destas condições:

1. Dados genuinamente posteriores ao cutoff (`2026-07-18T01:30:00Z`), com modelos congelados. O módulo `src/wick/r3e/future_unseen/` foi construído para isso.
2. Uma hipótese diferente, em dados diferentes — o que é um projeto novo, não uma continuação deste.

## 6. Retrospectiva — o que o PoC de IA ensinou

Este foi o objetivo real: exercitar desenvolvimento assistido por IA em um domínio de rigor metodológico alto.

### Funcionou

- **O núcleo científico ficou correto.** Detecção causal ancorada, entrada em `open[t+1]`, saída em `close[entrada+N-1]`, custos versionados, FDR, bootstrap em bloco para autocorrelação serial, tiers de amostra. Um agente bem instruído produziu código quantitativo que resiste a auditoria.
- **Invariantes escritas antes do código pegaram erros.** "Somente candles fechados", "nenhuma informação futura", "toda fórmula com exemplo manual e teste" — presentes no `CLAUDE.md`, refletidas na implementação.
- **A honestidade metodológica sobreviveu à pressão do resultado.** O sistema entregou `REJECTED` e travou o próprio gate em vez de se ajustar até parecer positivo. Isso é o mais difícil de conseguir e foi conseguido.
- **32 arquivos de teste / 6.184 linhas** para 13.400 linhas de fonte — proporção saudável, gerada sem que fosse preciso brigar por ela.

### Não funcionou

- **Documentação superou código em 2,7×.** 442 arquivos, 55.900 linhas. 145 deles são artefatos de processo (`ai-impact`, `ai-reviews`, `ai-specs`, `ai-governance`). Um único *impact assessment* de tela de UI chegou a 22 mil caracteres.
- **A governança virou o produto.** O processo criado para dar rastreabilidade ao trabalho de IA passou a consumir mais esforço do que o trabalho que rastreava. Agente que produz documento barato produz documento em excesso.
- **O projeto não parou quando devia.** O veredito negativo saiu em 16/07. Depois disso ainda foram construídos um frontend Next.js completo, um coletor com timers systemd, healthchecks, backup e preparação de host. Nada disso alterava a resposta.
- **Ausência de fronteira de escopo escrita.** Cada peça nova parecia pré-requisito da anterior. Sem um "isto o projeto deliberadamente não faz", não houve onde parar.

### A lição transferível

O gargalo do desenvolvimento assistido por IA não é a qualidade do código. É **saber quando parar** — e essa continua sendo uma decisão humana.

Um agente responde bem à pergunta "o que falta construir?" e sempre encontra resposta. Ele não faz a pergunta que importa: *"isso ainda serve ao objetivo?"*. No Wick, o objetivo foi atingido em 16 de julho e o trabalho continuou por mais nove dias.

Em projetos futuros, escrever **antes da primeira linha de código**:
1. A pergunta única que o projeto responde.
2. O critério de encerramento — inclusive por resultado negativo.
3. A lista explícita do que o projeto não faz.

---

## 7. Estado final

| | |
|---|---|
| Capital arriscado | **R$ 0,00** |
| Ordens executadas | nenhuma |
| Pergunta respondida | sim |
| Resultado | negativo |
| Projeto | **encerrado** |

*Um projeto de validação que impede uma aposta ruim entregou exatamente o que prometeu.*

