# R2 — Detecção, Contexto e Confirmação

## Objetivo

Detectar formas de candle deterministicamente, armazenar contexto e processar confirmação posterior sem olhar o futuro.

## Escopo

- features base;
- detectores unitários;
- padrões de 1, 2 e 3 candles;
- contexto de tendência;
- volume relativo;
- ATR/regime de volatilidade;
- retornos passados;
- posição no range;
- confirmação posterior;
- persistência versionada;
- CLI incremental;
- testes.

## Features mínimas

- trend_direction
- trend_strength
- volume_ratio_20
- atr_14
- volatility_regime
- return_5
- return_20
- range_position_20
- distance_from_sma_20

## Decisões

- forma e contexto separados;
- mediana para tamanho relativo;
- padrão pode se sobrepor;
- âncora é último candle;
- confirmação nasce PENDING;
- confirmação só é resolvida após candle seguinte fechar;
- detector_version e parameters_hash obrigatórios;
- sem ML.

## Critérios de aceite

- fórmulas explícitas;
- positivo, negativo e limítrofe por padrão;
- idempotência;
- contexto salvo;
- confirmação posterior;
- nenhuma leitura futura;
- auditoria aprovada.
