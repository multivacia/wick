# CLAUDE.md — Wick

## Missão

Construir um sistema de pesquisa quantitativa para avaliar se padrões de candlestick apresentam vantagem preditiva líquida após custos, antes de qualquer uso de dinheiro real.

## Fonte de verdade

Leia, nesta ordem:
1. `docs/PROJECT.md`
2. especificação da release em `docs/releases/`
3. documentos de arquitetura relacionados
4. código e migrations existentes

Quando documentação e código divergirem:
- não esconda a divergência;
- siga o código apenas para detalhes de implementação já consolidados;
- pare para decisão humana se a divergência alterar regra de negócio, cálculo, dados ou metodologia.

## Stack

- Python 3.11+
- uv
- SQLAlchemy 2.x
- psycopg 3
- Alembic
- PostgreSQL obrigatório
- TimescaleDB opcional
- Polars para transformação/consulta analítica
- NumPy para cálculos
- pandas somente na fronteira de bibliotecas que o exijam
- vectorbt como validação complementar, não como única implementação
- scipy
- pydantic-settings
- pytest
- ruff
- Docker Compose para infraestrutura local

## Invariantes

- UTC com timezone em todos os timestamps.
- Somente candles fechados.
- Ingestão e processamento idempotentes.
- Nenhum segredo no repositório.
- Toda fórmula importante deve ter exemplo manual e teste automatizado.
- Toda execução relevante deve possuir `run_id`.
- Toda regra quantitativa deve possuir versão.
- Toda alteração de parâmetro deve gerar nova versão ou novo experimento.
- Nenhuma informação futura pode ser utilizada antes de estar disponível.
- Nenhuma operação short é simulada por padrão.
- Nenhuma ordem real é permitida antes da R6.

## Comandos mínimos de validação

```bash
uv sync
uv run alembic upgrade head
uv run ruff check .
uv run ruff format --check .
uv run pytest
```

## Política de interação humana

Não interrompa por:
- nomes internos;
- helpers;
- layout de pastas equivalente;
- correções de lint;
- decisões triviais de implementação.

Interrompa por:
- fórmulas ambíguas;
- mudança de entrada/saída;
- alteração de custos;
- alteração de gate;
- falta de dados que invalide requisito;
- conflito de migration;
- remoção de dados;
- uso de short;
- integração com corretora;
- qualquer uso de dinheiro real.

## Entrega de cada release

Entregar:
- resumo;
- arquivos alterados;
- migrations;
- testes e resultados;
- exemplos manuais validados;
- divergências;
- decisões tomadas;
- limitações;
- riscos;
- commit hash;
- recomendação para gate da próxima release.
