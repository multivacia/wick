# WICK — UX-R1 Scientific and Economic Language Guardrails

```text
DOCUMENT = UX-R1-SCIENTIFIC-AND-ECONOMIC-LANGUAGE-GUARDRAILS
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B4
TASK_ID = OPERATIONAL-LANGUAGE-MICROCOPY-001
STATUS = ACTIVE
LOCALE = pt-BR
ECONOMIC_INTERPRETATION_ALLOWED = false
UI_IMPLEMENTATION_AUTHORIZED = false
EFFECTIVE_AT = 2026-07-19T13:26:43Z
```

## 1. Purpose

Prevent operational UI copy from overstating scientific certainty or implying financial performance.

Operational success and economic success are **different concepts**.

## 2. Prohibited language patterns

Prohibited unless supported by the exact scientific gate **and** explicitly authorized interpretation:

```text
modelo vencedor
estratégia lucrativa
resultado garantido
pronto para produção
validação concluída
edge confirmado
retorno esperado positivo
lucro provável
sinal de compra
sinal de venda
ordem enviada
P&L
profit
cassino / jackpot / hot streak
aprovado para dinheiro real
robô lucrando
quase pronto para investir
```

Also prohibited as unqualified claims:

```text
passou no teste (sem dizer qual gate)
aprovado (sem objeto)
ok para operar
melhor estratégia
```

## 3. Safe replacements

| Prohibited / risky | Safe replacement |
|--------------------|------------------|
| modelo vencedor | Experimento em andamento; sem promoção |
| estratégia lucrativa | Interpretação econômica não autorizada |
| resultado garantido | Resultado incerto; sem garantia |
| pronto para produção | Critérios operacionais/parciais descritos sem “produção” |
| validação concluída | Validação científica não executada / não autorizada |
| edge confirmado | Sem conclusão de edge autorizada |
| retorno esperado positivo | Sem projeção de retorno |
| lucro provável | Sem afirmação de lucro |
| passou no teste | Informe o gate exato e o status (`PENDING_FUTURE_UNSEEN_DATA`, etc.) |
| pronto para validar (após READY) | Critérios operacionais atendidos; validação exige autorização humana |
| automação desligada = morto | Agendamento automático ainda não está ativo |
| falhou a validação (para NOT_READY) | Ainda não há dados/critérios suficientes (`NOT_READY`) |

## 4. Economic interpretation safety rules

| Concept | Allowed wording | Forbidden wording |
|---------|-----------------|-------------------|
| profit | Only if authorized economic interpretation and labeled methodology | Any profit claim while `ECONOMIC_INTERPRETATION_ALLOWED=false` |
| return | Methodological discussion in docs only, not MVP ops UI | “retorno esperado”, “roi” |
| cost | Cost model version as metadata when relevant | “barato/lucrativo após custo” sem gate |
| performance | “desempenho operacional do ciclo” (latency, success) | performance financeira |
| accuracy | Só com métrica nomeada e contexto científico autorizado | “alta acurácia” solto |
| edge | “sem edge autorizado” / gate pendente | “edge confirmado” |
| economic significance | Bloqueada na UI operacional atual | qualquer significância econômica afirmada |
| statistical significance | Só em superfície científica com métricas e versões | p-hack / “estatisticamente garantido” |
| operational success | “ciclo concluído”, “backup ok” | “sucesso” sem qualificador operacional |

Rule:

```text
operational success ≠ economic success
```

Default banner for Experimentos / Visão Geral when relevant:

```text
Interpretação econômica não autorizada.
Technical: ECONOMIC_INTERPRETATION_ALLOWED=false
```

## 5. Scientific safety rules

1. Never hide scientific locks.
2. Never imply `validate` ran if it did not.
3. Never treat readiness `READY` as scientific approval.
4. Never reuse holdout language as available again.
5. Never present demonstration fixtures as real scientific outcomes.
6. Demonstration data must show: `DEMONSTRATION DATA`.
7. Every scientific claim needs: plain language + technical status + version/`run_id` when applicable.

## 6. Color and success semantics (language-facing)

| Cue | Meaning allowed | Meaning forbidden |
|-----|-----------------|-------------------|
| Green / SUCCESS | Operação concluída | Lucro, edge, production-ready |
| Amber / NOT_READY | Critérios incompletos | Falha científica |
| Purple / BLOCKED | Bloqueio / proteção | Sempre crash |
| Red / ERROR | Falha operacional real | Prejuízo de estratégia |

## 7. Enforcement checklist (content review)

Before approving any screen copy:

- [ ] Plain language first + technical code present
- [ ] No prohibited economic phrase
- [ ] No false validate/readiness/scheduler implication
- [ ] Empty/warning/error distinguishable
- [ ] Deferred debt does not look complete
- [ ] `DEMONSTRATION DATA` if fixture
- [ ] Timezone visible on timestamps
- [ ] Screen-reader text not color-only
