# R3 — Validação Quantitativa

## Estrutura

### R3A — Motor auditável
- entrada e saída;
- retorno bruto;
- custos;
- retorno líquido;
- exemplos manuais;
- testes por índice.

### R3B — Estatística
- treino/holdout;
- walk-forward;
- baselines;
- block bootstrap;
- FDR;
- sobreposição;
- cenários de custo.

### R3C — Relatório e gate
- relatório técnico;
- relatório executivo;
- classificação;
- promoção para R4.

## Invariantes

- sem confirmação: `entry=t+1`;
- com confirmação: `entry=t+2`;
- saída: `entry+N-1`;
- long-only executável;
- bearish como previsão;
- dados futuros insuficientes = não avaliável;
- seed reproduzível;
- experimento congelado.

## Exemplos manuais mínimos

Criar fixtures onde:
- entrada 100;
- saída 103;
- bruto 3%;
- custos conhecidos;
- líquido esperado exato.

Criar caso de confirmação que prove que `open[t+1]` não é utilizado.

## Gate

Usar o gate registrado em `PROJECT.md`.

## Interação humana obrigatória

- alteração de fórmula;
- mudança em custos;
- mudança de amostra mínima;
- mudança de short/long;
- mudança de gate;
- necessidade de reutilizar holdout.
