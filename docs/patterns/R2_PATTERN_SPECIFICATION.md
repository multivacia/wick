# Wick — R2 Pattern Specification

> **Arquivo sugerido:** `docs/patterns/R2_PATTERN_SPECIFICATION.md`  
> **Status:** proposta para aprovação humana antes da implementação  
> **Objetivo:** transformar a R2 em uma especificação executável, auditável e suficientemente precisa para que o Cursor implemente sem inventar regras metodológicas.

---

# 1. Objetivo da R2

A R2 deve:

- detectar formas geométricas de candlestick;
- calcular e registrar o contexto em que cada forma ocorreu;
- processar confirmação somente quando o candle confirmador já estiver fechado;
- persistir resultados de forma idempotente;
- manter versões explícitas das regras e dos parâmetros;
- permitir reprocessamento auditável;
- produzir dados confiáveis para a R3.

A R2 não deve:

- calcular retorno;
- executar backtest;
- classificar uma estratégia como lucrativa;
- recomendar compra ou venda;
- conectar corretora;
- executar ordens;
- usar machine learning;
- otimizar parâmetros;
- alterar os dados da R1 sem necessidade técnica comprovada.

---

# 2. Princípios inegociáveis

## 2.1. Forma não é contexto

A forma geométrica deve ser detectada independentemente da tendência.

Exemplo:

- um `HAMMER` pode ser detectado em tendência de alta, baixa, lateral ou contexto desconhecido;
- o contexto clássico de martelo pode ser tendência de baixa;
- isso não deve impedir o registro da forma fora desse contexto.

A R3 será responsável por medir se determinado padrão funciona melhor em algum contexto específico.

## 2.2. Detecção não é recomendação

A existência de um padrão não equivale a:

- sinal de compra;
- sinal de venda;
- oportunidade de investimento;
- estratégia aprovada.

A R2 apenas afirma:

> “A geometria desta formação atende à regra versionada X.”

## 2.3. Nenhuma informação futura

Para detectar um padrão ancorado no candle `t`, o motor pode ler apenas candles até `t`.

É proibido:

- usar `t+1` durante a detecção;
- usar médias centradas;
- preencher dados ausentes com valores posteriores;
- normalizar usando o dataset inteiro;
- recalcular features de `t` com dados posteriores;
- usar o candle confirmador antes de seu fechamento.

## 2.4. Somente candles fechados

Nenhuma forma, feature, tendência ou confirmação pode usar candle ainda em formação.

A R1 continua sendo a fonte de verdade para `is_closed`.

## 2.5. Sobreposição é permitida

Um candle pode:

- atender a mais de um padrão;
- participar de padrões diferentes;
- ser âncora de um padrão e participante de outro.

A R2 não deve impor exclusividade artificial.

## 2.6. Dados insuficientes não podem ser inventados

Quando não houver histórico suficiente:

- feature indisponível = `NULL`;
- tendência = `UNKNOWN`;
- volatilidade = `UNKNOWN`;
- força = `UNKNOWN`;
- a forma ainda pode ser detectada se não depender daquela feature;
- nunca reduzir silenciosamente a janela;
- nunca preencher artificialmente.

---

# 3. Fonte de verdade e precedência

A ordem de precedência para a R2 é:

1. `CLAUDE.md`
2. `docs/PROJECT.md`
3. `docs/architecture/DATA_MODEL.md`
4. `docs/architecture/DATA_QUALITY.md`
5. este documento
6. `docs/releases/R2_SPEC.md`
7. código aprovado da R1
8. prompt de implementação

Regra:

- documentos vencem para metodologia, invariantes e comportamento;
- código aprovado vence para nomes reais e contratos técnicos existentes;
- divergências que alterem comportamento devem ser reportadas e não resolvidas silenciosamente.

---

# 4. Decisões fechadas, delegadas e pendentes

## 4.1. Decisões fechadas

O Cursor não pode alterar:

- somente candles fechados;
- zero look-ahead;
- forma separada de contexto;
- confirmação posterior;
- sobreposição permitida;
- parâmetros versionados;
- golden datasets imutáveis sem autorização;
- sem retorno e sem backtest;
- sem machine learning;
- sem short;
- sem recomendação financeira.

## 4.2. Decisões técnicas delegadas

O Cursor pode decidir:

- organização interna de módulos;
- nomes de helpers;
- divisão de arquivos;
- estratégia de cache;
- uso de dataclasses, Pydantic ou estruturas equivalentes;
- otimizações locais;
- implementação do hash de parâmetros;
- forma de serialização dos golden datasets.

## 4.3. Decisões que exigem interação humana

O Cursor deve parar quando:

- uma fórmula estiver ausente;
- um limiar estiver indefinido;
- dois padrões entrarem em conflito lógico;
- um golden dataset contradizer a regra;
- uma alteração mudar o significado financeiro;
- uma migration for destrutiva;
- um cálculo precisar usar dado futuro;
- uma biblioteca externa tiver regra diferente da especificação;
- a implementação exigir mudar os parâmetros aprovados.

---

# 5. Notação e variáveis fundamentais

Para cada candle `c`:

```python
open_ = c.open
high = c.high
low = c.low
close = c.close
volume = c.volume
```

## 5.1. Grandezas base

```python
body = abs(close - open_)
candle_range = high - low
upper_wick = high - max(open_, close)
lower_wick = min(open_, close) - low
mid_body = (open_ + close) / 2
```

## 5.2. Direção

```python
is_bull = close > open_
is_bear = close < open_
```

Quando o corpo relativo for menor ou igual ao limiar de doji, o candle deve ser tratado como neutro para classificação geométrica.

## 5.3. Proporções

Somente quando `candle_range > epsilon`:

```python
body_ratio = body / candle_range
upper_wick_ratio = upper_wick / candle_range
lower_wick_ratio = lower_wick / candle_range
close_position = (close - low) / candle_range
open_position = (open_ - low) / candle_range
```

Para proporções em relação ao corpo:

```python
safe_body = max(body, epsilon)
upper_wick_to_body = upper_wick / safe_body
lower_wick_to_body = lower_wick / safe_body
```

## 5.4. Candle degenerado

Quando:

```python
candle_range <= epsilon
```

o candle deve:

- ser marcado como degenerado;
- não participar de padrões dependentes de proporção;
- não provocar divisão por zero;
- ser contabilizado em relatório de qualidade;
- não ser classificado como doji automaticamente.

---

# 6. Parâmetros globais propostos

> Estes valores são a proposta inicial oficial da R2. Qualquer mudança futura exige nova versão e novo hash de parâmetros.

```yaml
epsilon: 1.0e-12

doji_body_ratio_max: 0.10

small_body_vs_median_max: 0.75
large_body_vs_median_min: 1.50

median_body_window: 14
atr_window: 14
sma_window: 20
volume_window: 20
range_position_window: 20

hammer_body_ratio_max: 0.35
hammer_lower_wick_to_body_min: 2.0
hammer_upper_wick_to_body_max: 0.5
hammer_close_position_min: 0.60

inverted_hammer_body_ratio_max: 0.35
inverted_hammer_upper_wick_to_body_min: 2.0
inverted_hammer_lower_wick_to_body_max: 0.5
inverted_hammer_close_position_min: 0.40

shooting_star_body_ratio_max: 0.35
shooting_star_upper_wick_to_body_min: 2.0
shooting_star_lower_wick_to_body_max: 0.5
shooting_star_close_position_max: 0.40

engulfing_body_min_factor: 1.0
engulfing_allow_equal_boundaries: true

morning_star_middle_body_ratio_max: 0.30
morning_star_recovery_min: 0.50

evening_star_middle_body_ratio_max: 0.30
evening_star_decline_min: 0.50
```

---

# 7. Features oficiais da R2

A R2 deve calcular e persistir apenas as features abaixo.

## 7.1. Geometria

- `body`
- `candle_range`
- `upper_wick`
- `lower_wick`
- `body_ratio`
- `upper_wick_ratio`
- `lower_wick_ratio`
- `upper_wick_to_body`
- `lower_wick_to_body`
- `close_position`
- `open_position`
- `is_bull`
- `is_bear`
- `is_doji`
- `is_degenerate`

## 7.2. Tamanho relativo

- `median_body_14`
- `body_vs_median_14`
- `is_small_body`
- `is_large_body`

Definições:

```python
body_vs_median_14 = body / median_body_14
is_small_body = body_vs_median_14 <= small_body_vs_median_max
is_large_body = body_vs_median_14 >= large_body_vs_median_min
```

Se a mediana for zero ou inexistente:

- `body_vs_median_14 = NULL`;
- flags relativas = `NULL`.

## 7.3. ATR

Usar True Range:

```python
tr = max(
    high - low,
    abs(high - previous_close),
    abs(low - previous_close),
)
```

ATR 14 oficial:

```python
atr_14 = média aritmética simples dos últimos 14 true ranges
```

Na primeira R2, não usar suavização de Wilder.

## 7.4. Tendência

Calcular:

- `sma_20`
- `sma_20_previous`
- `sma_20_slope`
- `distance_from_sma_20`
- `return_5`
- `return_20`
- `trend_direction`
- `trend_strength`

Definições:

```python
sma_20 = mean(close[t-19:t+1])
sma_20_previous = mean(close[t-20:t])
sma_20_slope = (sma_20 - sma_20_previous) / sma_20_previous
distance_from_sma_20 = close[t] / sma_20 - 1
return_5 = close[t] / close[t-5] - 1
return_20 = close[t] / close[t-20] - 1
```

Classificação proposta:

```yaml
trend_up:
  sma_20_slope_min: 0.001
  return_20_min: 0.02

trend_down:
  sma_20_slope_max: -0.001
  return_20_max: -0.02
```

Regras:

```python
if slope >= 0.001 and return_20 >= 0.02:
    trend_direction = "UP"
elif slope <= -0.001 and return_20 <= -0.02:
    trend_direction = "DOWN"
else:
    trend_direction = "SIDEWAYS"
```

Se dados insuficientes:

```text
trend_direction = UNKNOWN
```

## 7.5. Força da tendência

```python
trend_strength_score = abs(return_20) / max(atr_14 / close, epsilon)
```

Classificação proposta:

```yaml
WEAK: score < 2
MODERATE: 2 <= score < 4
STRONG: score >= 4
UNKNOWN: dados insuficientes
```

## 7.6. Volume relativo

```python
volume_ratio_20 = volume[t] / mean(volume[t-19:t+1])
```

Quando volume for nulo, zero ou não confiável:

- `volume_ratio_20 = NULL`;
- `volume_regime = UNKNOWN`.

Classificação proposta:

```yaml
LOW: ratio < 0.75
NORMAL: 0.75 <= ratio < 1.50
HIGH: 1.50 <= ratio < 2.50
EXTREME: ratio >= 2.50
UNKNOWN: sem dados
```

## 7.7. Regime de volatilidade

```python
normalized_atr = atr_14 / close
```

Calcular a mediana dos últimos 100 valores válidos de `normalized_atr`.

```python
volatility_ratio = normalized_atr / median_normalized_atr_100
```

Classificação:

```yaml
LOW: ratio < 0.75
NORMAL: 0.75 <= ratio < 1.50
HIGH: ratio >= 1.50
UNKNOWN: dados insuficientes
```

## 7.8. Posição no range

```python
range_high_20 = max(high[t-19:t+1])
range_low_20 = min(low[t-19:t+1])
range_position_20 = (close[t] - range_low_20) / (range_high_20 - range_low_20)
```

Quando denominador for zero:

```text
range_position_20 = NULL
```

Classificação opcional persistida:

```yaml
BOTTOM: position <= 0.25
MIDDLE: 0.25 < position < 0.75
TOP: position >= 0.75
UNKNOWN: sem dados
```

---

# 8. Catálogo oficial de padrões — R2 v1

A primeira versão deve implementar apenas:

1. `DOJI`
2. `HAMMER`
3. `INVERTED_HAMMER`
4. `SHOOTING_STAR`
5. `BULLISH_ENGULFING`
6. `BEARISH_ENGULFING`
7. `MORNING_STAR`
8. `EVENING_STAR`

Outros padrões ficam fora desta release.

---

# 9. DOJI

```yaml
pattern_type: DOJI
version: 1.0.0
length: 1
anchor: current
signal: neutral
classical_context: any
context_required_for_detection: false
```

## Condições

```python
not is_degenerate
body_ratio <= doji_body_ratio_max
```

## Observações

- não exigir tendência;
- não exigir cor;
- um doji pode coexistir com outro padrão somente se todas as regras forem satisfeitas;
- corpo exatamente no limite deve detectar.

---

# 10. HAMMER

```yaml
pattern_type: HAMMER
version: 1.0.0
length: 1
anchor: current
signal: bullish
classical_context: DOWN
context_required_for_detection: false
```

## Condições

```python
not is_degenerate
body_ratio <= hammer_body_ratio_max
lower_wick_to_body >= hammer_lower_wick_to_body_min
upper_wick_to_body <= hammer_upper_wick_to_body_max
close_position >= hammer_close_position_min
not is_doji
```

## Observações

- cor do corpo não é obrigatória;
- a forma em tendência de alta continua sendo registrada como `HAMMER`;
- contexto clássico fica armazenado separadamente.

---

# 11. INVERTED_HAMMER

```yaml
pattern_type: INVERTED_HAMMER
version: 1.0.0
length: 1
anchor: current
signal: bullish
classical_context: DOWN
context_required_for_detection: false
```

## Condições

```python
not is_degenerate
body_ratio <= inverted_hammer_body_ratio_max
upper_wick_to_body >= inverted_hammer_upper_wick_to_body_min
lower_wick_to_body <= inverted_hammer_lower_wick_to_body_max
close_position >= inverted_hammer_close_position_min
not is_doji
```

---

# 12. SHOOTING_STAR

```yaml
pattern_type: SHOOTING_STAR
version: 1.0.0
length: 1
anchor: current
signal: bearish
classical_context: UP
context_required_for_detection: false
```

## Condições

```python
not is_degenerate
body_ratio <= shooting_star_body_ratio_max
upper_wick_to_body >= shooting_star_upper_wick_to_body_min
lower_wick_to_body <= shooting_star_lower_wick_to_body_max
close_position <= shooting_star_close_position_max
not is_doji
```

---

# 13. BULLISH_ENGULFING

```yaml
pattern_type: BULLISH_ENGULFING
version: 1.0.0
length: 2
anchor: second_candle
signal: bullish
classical_context: DOWN
context_required_for_detection: false
```

Defina:

```python
prev = candle[t-1]
curr = candle[t]
```

## Condições

```python
prev.is_bear
curr.is_bull
curr.open <= prev.close
curr.close >= prev.open
curr.body >= prev.body * engulfing_body_min_factor
not prev.is_doji
not curr.is_doji
```

Se `engulfing_allow_equal_boundaries = true`, igualdade é aceita.

A regra considera o corpo, não exige engolfar pavios.

---

# 14. BEARISH_ENGULFING

```yaml
pattern_type: BEARISH_ENGULFING
version: 1.0.0
length: 2
anchor: second_candle
signal: bearish
classical_context: UP
context_required_for_detection: false
```

## Condições

```python
prev.is_bull
curr.is_bear
curr.open >= prev.close
curr.close <= prev.open
curr.body >= prev.body * engulfing_body_min_factor
not prev.is_doji
not curr.is_doji
```

A regra considera o corpo, não exige engolfar pavios.

---

# 15. MORNING_STAR

```yaml
pattern_type: MORNING_STAR
version: 1.0.0
length: 3
anchor: third_candle
signal: bullish
classical_context: DOWN
context_required_for_detection: false
```

Defina:

```python
c1 = candle[t-2]
c2 = candle[t-1]
c3 = candle[t]
```

## Condições

```python
c1.is_bear
c1.is_large_body is True

c2.body_ratio <= morning_star_middle_body_ratio_max

c3.is_bull
c3.close >= c1.close + (c1.open - c1.close) * morning_star_recovery_min

not c1.is_doji
not c3.is_doji
```

## Gap

Na R2 v1, gap não é obrigatório.

Motivo:

- cripto negocia 24/7;
- ações podem apresentar gap;
- exigir gap impediria comparabilidade entre mercados.

O contexto de gap pode ser adicionado como feature futura.

---

# 16. EVENING_STAR

```yaml
pattern_type: EVENING_STAR
version: 1.0.0
length: 3
anchor: third_candle
signal: bearish
classical_context: UP
context_required_for_detection: false
```

## Condições

```python
c1.is_bull
c1.is_large_body is True

c2.body_ratio <= evening_star_middle_body_ratio_max

c3.is_bear
c3.close <= c1.close - (c1.close - c1.open) * evening_star_decline_min

not c1.is_doji
not c3.is_doji
```

Gap não é obrigatório na v1.

---

# 17. Regras de confirmação

A confirmação é independente da detecção.

## 17.1. Estados

```text
PENDING
CONFIRMED
NOT_CONFIRMED
NOT_APPLICABLE
```

## 17.2. Disponibilidade

Para padrão ancorado em `t`:

- detecção ocorre após fechamento de `t`;
- confirmação só pode ser processada após fechamento de `t+1`.

## 17.3. Regras oficiais

### Regra A — close reference

Bullish:

```python
close[t+1] > close[t]
```

Bearish:

```python
close[t+1] < close[t]
```

Código:

```text
CONFIRM_CLOSE_V1
```

### Regra B — extreme reference

Bullish:

```python
close[t+1] > high[t]
```

Bearish:

```python
close[t+1] < low[t]
```

Código:

```text
CONFIRM_EXTREME_V1
```

## 17.4. Doji

Para `DOJI`:

```text
confirmation_status = NOT_APPLICABLE
```

na R2 v1.

## 17.5. Persistência

Guardar:

- `confirmation_rule_version`;
- `confirmation_candle_id`;
- `confirmed_at`;
- resultado por regra.

A implementação pode usar entidade filha para suportar múltiplas regras de confirmação.

---

# 18. Persistência

## 18.1. pattern_detected

Campos mínimos:

```text
id
anchor_candle_id
start_candle_id
pattern_length
pattern_type
signal
detector_version
parameters_hash
detected_at
run_id
context_features
created_at
updated_at
```

Chave lógica:

```text
(anchor_candle_id, pattern_type, detector_version, parameters_hash)
```

## 18.2. pattern_confirmation

Campos mínimos:

```text
id
pattern_detected_id
confirmation_rule_version
confirmation_status
confirmation_candle_id
evaluated_at
created_at
updated_at
```

Chave lógica:

```text
(pattern_detected_id, confirmation_rule_version)
```

## 18.3. Context features

Persistir como JSONB versionado ou tabela dedicada.

Campos obrigatórios:

```text
context_version
trend_direction
trend_strength
sma_20
sma_20_slope
distance_from_sma_20
return_5
return_20
atr_14
normalized_atr
volatility_regime
volume_ratio_20
volume_regime
range_position_20
range_position_bucket
```

---

# 19. Idempotência

Rerodar o detector:

- não duplica padrão;
- não duplica confirmação;
- atualiza somente se versão ou parâmetros forem diferentes;
- novo detector gera nova linha;
- alteração de parâmetro gera novo `parameters_hash`;
- histórico anterior permanece preservado.

---

# 20. CLI

Comando sugerido:

```bash
uv run python scripts/detect.py
```

Flags:

```text
--assets
--timeframes
--start
--end
--incremental
--reprocess
--detector-version
--confirmation-rule
--dry-run
```

## 20.1. Incremental

Default.

Processa a partir do último candle elegível ainda não analisado para a versão atual.

## 20.2. Reprocess

Recalcula o intervalo solicitado usando a mesma versão.

Não apaga resultados de outras versões.

## 20.3. Dry run

Calcula e apresenta resumo sem persistir.

---

# 21. Golden datasets

Criar:

```text
tests/golden/r2/
├── doji.json
├── hammer.json
├── inverted_hammer.json
├── shooting_star.json
├── bullish_engulfing.json
├── bearish_engulfing.json
├── morning_star.json
├── evening_star.json
├── confirmation.json
└── context_features.json
```

Cada caso deve conter:

```json
{
  "case_id": "HAMMER_POSITIVE_001",
  "rule_version": "1.0.0",
  "candles": [],
  "expected": {
    "detected": true,
    "pattern_type": "HAMMER"
  },
  "reason": "Pavio inferior >= 2x corpo, pavio superior pequeno e corpo fora de doji."
}
```

---

# 22. Testes obrigatórios por padrão

Cada padrão deve ter:

1. positivo claro;
2. negativo claro;
3. limite inferior;
4. limite exato;
5. limite superior;
6. escala multiplicada por 10;
7. deslocamento aditivo;
8. candle futuro alterado;
9. candle aberto rejeitado;
10. rerun idempotente.

---

# 23. Testes metamórficos

## 23.1. Escala

Multiplicar todos os preços por fator positivo não altera o resultado.

## 23.2. Translação

Somar constante a todos os preços não altera proporções.

## 23.3. Futuro

Alterar `t+1` não altera a detecção em `t`.

## 23.4. Rerun

Executar duas vezes produz o mesmo conjunto lógico.

## 23.5. Ordem

Candles devem ser processados em ordem temporal.

Entrada desordenada deve:

- ser ordenada explicitamente; ou
- ser rejeitada.

A decisão deve ser única e documentada.

Recomendação: ordenar internamente e registrar alerta.

---

# 24. Auditoria adversarial

A auditoria da R2 deve tentar encontrar:

- look-ahead;
- candle aberto;
- fórmula divergente;
- hard-code fora do catálogo;
- divisão por zero;
- comparação absoluta indevida;
- contexto com dados futuros;
- confirmação antecipada;
- duplicação;
- migration inconsistente;
- parâmetros sem versão;
- golden dataset alterado;
- detector dependente de biblioteca externa;
- ausência de caso limítrofe;
- uso incorreto de tendência;
- tratamento incorreto de dados insuficientes.

---

# 25. Bibliotecas externas

TA-Lib ou equivalentes podem ser usadas somente como comparação.

Regras:

- especificação Wick é a fonte oficial;
- divergência deve ser reportada;
- código não deve ser alterado apenas para coincidir com biblioteca;
- biblioteca externa não substitui golden datasets.

---

# 26. Critérios de aceite

A R2 só pode ser concluída quando:

- oito padrões implementados;
- features oficiais calculadas;
- golden datasets presentes e imutáveis;
- testes positivos, negativos e limítrofes;
- testes metamórficos;
- confirmação posterior;
- nenhuma leitura futura;
- somente candles fechados;
- idempotência;
- versions e hashes persistidos;
- migrations do zero;
- CI verde;
- auditoria sem CRITICAL/HIGH;
- relatório final entregue;
- R3 não iniciada automaticamente.

---

# 27. Relatório final obrigatório

O Cursor deve entregar:

- branch;
- PR;
- commits;
- migrations;
- padrões implementados;
- versões;
- parâmetros;
- features;
- confirmação;
- golden datasets;
- quantidade de testes antes/depois;
- CI;
- evidência de zero look-ahead;
- divergências;
- limitações;
- achados da auditoria;
- recomendação de gate.

---

# 28. Gate

Estados possíveis:

```text
R2_GATE = PENDING_SPEC_APPROVAL
R2_GATE = PENDING_IMPLEMENTATION
R2_GATE = PENDING_AUDIT
R2_GATE = APPROVED
R2_GATE = REJECTED
```

A implementação só pode começar quando:

```text
R2_GATE = PENDING_IMPLEMENTATION
```

A R3 só pode começar quando:

```text
R2_GATE = APPROVED
```

---

# 29. Escopo futuro

Ficam fora da R2 v1:

- Harami;
- Piercing Line;
- Dark Cloud Cover;
- Three White Soldiers;
- Three Black Crows;
- Marubozu;
- Spinning Top;
- Fibonacci;
- RSI;
- MACD;
- Bollinger Bands;
- notícias;
- sentimento;
- machine learning;
- otimização de parâmetros;
- recomendação de investimento.

Esses itens podem entrar em releases posteriores, sempre com versão própria e nova validação.

---

# 30. Aviso metodológico

As regras deste documento são definições operacionais do Wick.

Elas não representam consenso universal sobre candlestick. Diferentes autores e bibliotecas podem usar limiares diferentes.

O objetivo da R2 não é provar que uma definição é “a verdadeira”, mas garantir que:

- a definição seja explícita;
- a implementação seja determinística;
- o resultado seja reproduzível;
- a R3 consiga medir seu valor preditivo honestamente.
