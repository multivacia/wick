# Regras de Segurança Científica para IA

## 1. Finalidade

Proteger a validade científica dos experimentos do Wick contra leakage, peeking, tuning retrospectivo e decisões orientadas pelo resultado observado.

## 2. Estado atual protegido

Enquanto a R3E estiver aguardando dados future unseen:

```text
R3E_FUTURE_DATA_COLLECTION = IN_PROGRESS
R3E_GATE = PENDING_FUTURE_UNSEEN_DATA
ECONOMIC_INTERPRETATION_ALLOWED = false
R4_STATUS = BLOCKED
R5_STATUS = NOT_STARTED
VALIDATION_COMMAND_EXECUTED = false
EFFECT_PEEKING_PERFORMED = false
```

## 3. Ações permitidas

São permitidas, desde que não revelem efeito:

- coleta incremental;
- dry-run;
- validação estrutural do store;
- contagem de barras;
- cobertura temporal;
- gaps;
- duplicidades;
- barras abertas rejeitadas;
- disponibilidade de séries;
- integridade de schema;
- idempotência;
- auditoria operacional.

## 4. Ações proibidas antes da autorização

- executar o comando científico `validate`;
- calcular retorno, hit rate, Sharpe, PnL ou equivalente;
- comparar M0–M5 em future unseen;
- inspecionar labels de resultado;
- consultar significância ou intervalos de confiança;
- alterar thresholds após observar efeito;
- escolher data de validação com base em desempenho;
- alterar universo, custos ou grids para melhorar resultado;
- liberar interpretação econômica;
- iniciar R4.

## 5. Readiness sem efeito

Um comando de readiness deve mostrar apenas maturidade operacional.

Exemplo permitido:

```text
series_complete = 12/20
bars_total = 1500
coverage_days = 45
duplicates = 0
open_bars_rejected = 5
readiness = NOT_READY
```

Exemplo proibido:

```text
delta_return = +2.4%
p_value = 0.03
best_model = M5
```

## 6. Imutabilidade

Cutoff, freeze, thresholds, custos, grids e critérios de gate devem ser definidos antes da validação e não podem mudar silenciosamente.

Qualquer alteração deve:

1. ser proposta formalmente;
2. justificar por que não depende do efeito;
3. passar por revisão;
4. gerar novo versionamento;
5. preservar os artefatos anteriores.

## 7. Validação oficial

A validação oficial exige:

- protocolo de readiness aprovado;
- checklist pré-validação aprovado;
- commit congelado;
- CI verde;
- store íntegro;
- autorização humana explícita;
- registro de que não houve peeking.

## 8. Resultado ruim não autoriza repetição

É proibido repetir validações, alterar critérios ou ajustar modelo apenas porque o resultado não foi favorável.

A repetição somente é permitida se existir razão técnica pré-definida e auditável, independente do efeito observado.
