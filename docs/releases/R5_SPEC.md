# R5 — PWA

## Arquitetura

- React + TypeScript;
- PWA responsiva;
- FastAPI;
- módulos no mesmo repositório;
- polling;
- sem microserviços prematuros.

## Telas

1. Visão geral.
2. Gráfico do ativo.
3. Padrões detectados.
4. Estratégias validadas.
5. Paper trading.
6. Estatísticas.
7. Qualidade dos dados.
8. Alertas.

## Regras

- frontend não calcula padrões ou métricas;
- distinguir padrão, estratégia validada e paper trade;
- nenhum segredo no cliente;
- sem execução de ordens;
- alertas explicam horário, contexto e status;
- aviso educacional visível.

## Autenticação

Inicialmente:
- único usuário administrador;
- hash seguro;
- cookie seguro;
- sem autenticação social.

## Critérios

- uso confortável no celular;
- dados rastreáveis;
- atualização clara;
- alertas no momento executável;
- nenhum cálculo financeiro no cliente.
