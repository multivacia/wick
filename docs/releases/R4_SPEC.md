# R4 — Paper Trading

## Objetivo

Aplicar ao vivo e sem dinheiro as estratégias congeladas na R3.

## Estados

- DETECTED
- AWAITING_CONFIRMATION
- CONFIRMED
- NOT_CONFIRMED
- OPEN
- AWAITING_EXIT
- CLOSED
- CANCELLED
- ERROR

## Execução

- polling idempotente;
- 1h: consultar periodicamente após fechamento;
- 1d: consultar após fechamento da sessão;
- validar timestamp da fonte;
- recuperar falhas na próxima execução;
- estado sempre persistido no banco.

## Alertas

Sem confirmação:
- após fechamento do padrão;
- informar entrada potencial no próximo candle.

Com confirmação:
- após fechamento do confirmador;
- informar entrada potencial no candle posterior.

## Comparação

Usar parâmetros congelados da R3:
- expectativa;
- frequência;
- custos;
- distribuição;
- regime;
- desvio entre esperado e realizado.

## Conclusões distintas

- R4_IMPLEMENTATION_COMPLETE
- R4_VALIDATION_COMPLETE

## Gate temporal

- pelo menos 3 meses;
- pelo menos 100 sinais executáveis por estratégia, quando possível;
- idealmente mais de um regime.
