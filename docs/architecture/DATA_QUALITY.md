# Qualidade e Auditoria dos Dados

## Estados de execução

- `SUCCESS`: intervalo solicitado atendido segundo as capacidades conhecidas da fonte.
- `PARTIAL`: dados úteis foram salvos, mas cobertura ou ativos ficaram incompletos.
- `FAILED`: não houve entrega confiável.

## Validações OHLCV

- `high >= max(open, close)`
- `low <= min(open, close)`
- `high >= low`
- preços não negativos
- volume não negativo
- timestamp válido e UTC
- chave única sem duplicação
- candle fechado conforme timeframe e margem de segurança

## Candle fechado

Um candle é elegível quando:

`open_time + timeframe_duration <= now_utc - safety_delay`

Default:
`CANDLE_CLOSE_SAFETY_DELAY_SECONDS=30`

## Histórico parcial

Nunca preencher artificialmente.

Registrar:
- período pedido;
- período retornado;
- primeiro e último candle;
- limitação conhecida;
- status `PARTIAL`.

## Lacunas

### Cripto

Esperar continuidade 24/7. Ausência de intervalo gera alerta.

### Ações

Não considerar noites, fins de semana ou feriados como lacunas. A validação ideal usa calendário de pregão. Caso o calendário não esteja implementado, indicar explicitamente que a checagem foi parcial.

## Revisões da fonte

Ao receber OHLCV diferente para a mesma chave:
- comparar;
- atualizar de forma controlada;
- incrementar `data_revision`;
- preservar datas de primeira e última ingestão;
- registrar evento de revisão;
- marcar resultados derivados como potencialmente afetados.

## Retries

- exponential backoff;
- jitter;
- máximo de cinco tentativas;
- respeitar `Retry-After`;
- não repetir automaticamente erro de autenticação/configuração;
- falha de um ativo não deve impedir todos os demais;
- resultado global vira `PARTIAL`.

## Dados ajustados

Quando disponíveis, preservar OHLC original e dados ajustados separadamente. O relatório deve indicar qual série foi usada.

## Relatório de execução

Cada ingestão deve produzir resumo legível e JSON estruturado contendo:
- run_id;
- fonte;
- ativos;
- timeframes;
- cobertura;
- inserções;
- atualizações;
- rejeições;
- lacunas;
- retries;
- status.
