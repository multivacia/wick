# R1 — Setup e Ingestão

## Objetivo

Criar infraestrutura, schema e ingestão OHLCV confiável, idempotente e auditável.

## Escopo

- projeto Python com uv;
- config via pydantic-settings;
- Docker Compose;
- PostgreSQL;
- TimescaleDB opcional;
- Alembic;
- asset, candle e ingestion_run;
- Binance/ccxt;
- Yahoo/yfinance;
- brapi plugável;
- CLI;
- testes sem rede;
- relatório de qualidade.

## Decisões

- Binance pública não requer chave para market data.
- yfinance não requer cadastro.
- brapi usa token para cobertura ampla; implementação deve funcionar sem ela.
- histórico parcial gera `PARTIAL`.
- ações 1h usam cobertura real disponível.
- candle aberto é descartado por cálculo de tempo, não apenas posição da API.
- upsert pode atualizar candle corrigido e incrementar revisão.
- `uv.lock` deve ser commitado.

## Critérios de aceite

- ambiente sobe do zero;
- migrations funcionam;
- reexecução não duplica;
- atualização busca somente faltantes;
- candle aberto rejeitado;
- dados inválidos rejeitados;
- cobertura parcial visível;
- testes verdes;
- README reproduzível.

## Interação humana obrigatória

- fonte não consegue atender requisito marcado como obrigatório;
- mudança de schema destrutiva;
- necessidade de credencial paga;
- inconsistência grave entre fontes.
