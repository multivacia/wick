# Cadastros e Credenciais das Fontes

## Binance

Para candles e demais dados públicos de mercado usados na R1:
- cadastro não é necessário;
- API key não é necessária;
- usar endpoints públicos/market-data-only;
- implementação padrão chama `https://data-api.binance.vision` (klines públicos);
- respeitar rate limits.

Uma conta Binance só será relevante no futuro para endpoints privados ou operação real. Isso está fora do escopo atual.

## Yahoo Finance / yfinance

- não exige cadastro;
- não exige API key;
- é uma biblioteca não oficial que acessa dados do Yahoo Finance;
- pode sofrer limitações e mudanças;
- intraday possui cobertura histórica limitada;
- o sistema deve tratar cobertura parcial.

## brapi

- alguns ativos podem ser testados sem token;
- para cobertura ampla, limites estáveis e uso regular, criar cadastro;
- token deve ficar em `.env`;
- a R1 não deve depender da brapi para funcionar;
- cadastrar apenas quando for validar a fonte alternativa brasileira.

## PostgreSQL/TimescaleDB

- nenhum cadastro externo é necessário para uso local via Docker.
- **PostgreSQL 16** é a versão oficial/homologada (Compose + CI).
- **PostgreSQL 15** é o mínimo tecnicamente suportado (`NULLS NOT DISTINCT`).
- TimescaleDB é opcional (`docker compose --profile timescale`); imagem versionada `timescale/timescaledb:2.28.3-pg16`.
- serviços gerenciados na nuvem só serão avaliados depois.

## GitHub

- repositório privado já é suficiente;
- nenhum marketplace financeiro deve ser conectado;
- secrets nunca devem ser commitados.

## Ação recomendada agora

Nenhum cadastro é obrigatório para o Cursor iniciar a R1.

Cadastro opcional recomendado:
- brapi, quando chegar o momento de testar cobertura ampliada de ações brasileiras.

Não criar conta de corretora nem chave de negociação nesta fase.
