# Contrato para Regras de Candlestick

Este documento define o formato obrigatório de cada padrão. As fórmulas específicas devem ser preenchidas/revisadas antes da implementação completa da R2.

## Variáveis base

```python
body = abs(close - open)
candle_range = high - low
upper_wick = high - max(open, close)
lower_wick = min(open, close) - low
mid_body = (open + close) / 2
is_bull = close > open
is_bear = close < open
body_ratio = body / candle_range  # somente quando range > 0
```

## Candle degenerado

Quando `candle_range <= epsilon`:
- marcar como degenerado;
- evitar divisões;
- não detectar padrões que dependam de proporções;
- registrar para auditoria.

## Tamanho relativo

Default:
- mediana dos corpos dos 14 candles anteriores;
- ATR 14;
- proporção do corpo no range.

Não usar valores absolutos de preço.

## Forma e contexto

A forma deve ser detectada independentemente da tendência. O contexto é armazenado separadamente.

## Sobreposição

Um candle pode participar de vários padrões. Não impor exclusividade.

## Âncora

Em padrões de 2 ou 3 candles, a âncora é o último candle que completa a formação.

## Template obrigatório por padrão

```text
pattern_type:
version:
length:
signal:
description:
required_candles:
shape_formula:
relative_size_formula:
trend_required_for_classical_interpretation:
trend_is_detection_requirement: false
positive_examples:
negative_examples:
boundary_examples:
known_conflicts:
parameters:
```

## Confirmação

A confirmação não altera o momento de detecção.

Status:
- PENDING
- CONFIRMED
- NOT_CONFIRMED
- NOT_APPLICABLE

Devem existir versões independentes:
- fechamento além do fechamento do candle âncora;
- fechamento além da máxima/mínima da formação.

Cada versão deve ter identificador próprio.
