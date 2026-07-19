# WICK — Guia de Linguagem e Terminologia

```text
DOCUMENT = WICK_UX_LANGUAGE_AND_TERMINOLOGY_GUIDE
VERSION = 1.0.0
RELEASE = UX-R1
STATUS = ACTIVE
EFFECTIVE_AT = 2026-07-19T03:13:15Z
```

## Modelo em duas camadas

### Camada primária (sempre visível)

Explicação em linguagem simples.

```text
A coleta ainda não está pronta para validação.
```

### Camada secundária (sempre disponível)

Termo formal do setor + detalhe técnico.

```text
Status técnico: READINESS_NOT_READY
Motivo: WINDOW_DAYS_INSUFFICIENT
```

### Regras de exibição

| Situação | Camada primária | Camada secundária |
|----------|-----------------|-------------------|
| Banner / resumo | Obrigatória | Link “Detalhes técnicos” ou tooltip |
| Lista / tabela | Primária + badge técnico curto | Expansão por linha |
| Tela de evidência | Primária + IDs | Primária e secundária lado a lado |
| Confirmação crítica | Primária explícita do efeito | Código técnico do gate/ação |

## Glossário

### readiness

| Campo | Valor |
|-------|-------|
| Termo simples | Prontidão da coleta |
| Termo técnico | `READINESS` / `READY` / `NOT_READY` / `BLOCKED` |
| Quando exibir | Visão geral, Prontidão, Host |
| Tooltip / ajuda | “Prontidão diz se os critérios mínimos para validação futura foram atendidos. Não é resultado do experimento.” |
| Proibido | “Pronto para lucrar”, “aprovado”, “passou no teste” |

### future-unseen data

| Campo | Valor |
|-------|-------|
| Termo simples | Dados futuros ainda não vistos |
| Termo técnico | `FUTURE_UNSEEN` / cutoff pós-`FUTURE_UNSEEN_CUTOFF` |
| Quando exibir | Coleta, Experimento R3E |
| Tooltip / ajuda | “Barras coletadas depois do corte oficial. Servem para a validação final; não misturar com histórico antigo.” |
| Proibido | “dados novos de mercado para trading”, “sinais ao vivo” |

### window days

| Campo | Valor |
|-------|-------|
| Termo simples | Dias de janela já acumulados |
| Termo técnico | `WINDOW_DAYS` / `WINDOW_DAYS_INSUFFICIENT` |
| Quando exibir | Prontidão (progresso 90 dias) |
| Tooltip / ajuda | “Contagem de dias calendário cobertos após o cutoff. A validação exige a janela mínima definida no protocolo.” |
| Proibido | “quase pronto para investir”, progresso sem rótulo de requisito |

### store observations

| Campo | Valor |
|-------|-------|
| Termo simples | Observações guardadas |
| Termo técnico | store observations / `OBSERVATIONS_ACCEPTED` |
| Quando exibir | Dados coletados, detalhe de execução |
| Tooltip / ajuda | “Cada observação é um candle fechado aceito no armazenamento oficial da coleta.” |
| Proibido | “trades”, “ordens”, “posições” |

### lock

| Campo | Valor |
|-------|-------|
| Termo simples | Travamento / bloqueio de execução |
| Termo técnico | lock / `SKIPPED_LOCKED` / scientific locks |
| Quando exibir | Execuções, Host, confirmações |
| Tooltip / ajuda | “Impede duas execuções ao mesmo tempo ou protege regras científicas (ex.: validate não autorizado).” |
| Proibido | “sistema travou / crashou” quando o lock é intencional |

### run cycle

| Campo | Valor |
|-------|-------|
| Termo simples | Ciclo de coleta |
| Termo técnico | `run-cycle` / `run_id` |
| Quando exibir | Execuções, Visão geral (últimos ciclos) |
| Tooltip / ajuda | “Sequência automatizada: checagens → coleta incremental → prontidão. Cada ciclo tem um identificador único (`run_id`).” |
| Proibido | “backtest”, “trade automático” |

### scheduler

| Campo | Valor |
|-------|-------|
| Termo simples | Agendamento automático |
| Termo técnico | scheduler / systemd timer / cron |
| Quando exibir | Host e Automação |
| Tooltip / ajuda | “Dispara ciclos em horário definido. Enquanto não ativado, a coleta depende de execução manual autorizada.” |
| Proibido | “robô de trading”, “bot ativo no mercado” |

### backup

| Campo | Valor |
|-------|-------|
| Termo simples | Cópia de segurança |
| Termo técnico | backup / verification state |
| Quando exibir | Backups, Operação |
| Tooltip / ajuda | “Cópia verificável do estado operacional. Não altera o resultado científico.” |
| Proibido | “salvou o lucro”, “snapshot de performance” |

### validation

| Campo | Valor |
|-------|-------|
| Termo simples | Validação científica final |
| Termo técnico | `validate` / `R3E_GATE` |
| Quando exibir | Prontidão, Experimento (sempre com estado de autorização) |
| Tooltip / ajuda | “Comando que avalia o protocolo em dados futuros. Só pode rodar com autorização humana explícita e critérios atendidos.” |
| Proibido | “já validado”, “aprovado para operar” sem gate |

### holdout

| Campo | Valor |
|-------|-------|
| Termo simples | Reserva de teste final (já consumida no R3D) |
| Termo técnico | holdout |
| Quando exibir | Experimento / glossário |
| Tooltip / ajuda | “Conjunto de dados separado para teste único. O holdout do R3D já foi usado e não pode ser reutilizado.” |
| Proibido | “vamos testar de novo no holdout” |

### walk-forward

| Campo | Valor |
|-------|-------|
| Termo simples | Avaliação em janelas sucessivas no tempo |
| Termo técnico | walk-forward / nested walk-forward |
| Quando exibir | Experimento R3E (camada secundária) |
| Tooltip / ajuda | “O modelo é avaliado avançando no tempo, sem usar o futuro daquela janela.” |
| Proibido | “previsão garantida”, “otimização mágica” |

### bootstrap

| Campo | Valor |
|-------|-------|
| Termo simples | Reamostragem para medir incerteza |
| Termo técnico | bootstrap |
| Quando exibir | Experimento / glossário técnico |
| Tooltip / ajuda | “Técnica estatística que reamostra resultados para estimar intervalos de confiança.” |
| Proibido | “prova definitiva de lucro” |

### FDR

| Campo | Valor |
|-------|-------|
| Termo simples | Controle de falsos positivos em muitos testes |
| Termo técnico | FDR (False Discovery Rate) |
| Quando exibir | Experimento / glossário técnico |
| Tooltip / ajuda | “Quando muitos padrões são testados juntos, o FDR limita descobertas falsas por acaso.” |
| Proibido | “taxa de acerto do robô” |

### economic interpretation

| Campo | Valor |
|-------|-------|
| Termo simples | Interpretação econômica (ainda não autorizada) |
| Termo técnico | `ECONOMIC_INTERPRETATION_ALLOWED` |
| Quando exibir | Experimento, Visão geral (quando relevante) |
| Tooltip / ajuda | “Conclusão sobre valor econômico ou edge negociável. Enquanto `false`, a interface não afirma vantagem financeira.” |
| Proibido | “estratégia lucrativa”, “edge confirmado”, P&L fictício |

### incident

| Campo | Valor |
|-------|-------|
| Termo simples | Incidente operacional |
| Termo técnico | incident |
| Quando exibir | Incidentes, Visão geral |
| Tooltip / ajuda | “Problema operacional (host, backup, coleta). Diferente de bloqueio científico esperado.” |
| Proibido | Confundir incidente com `NOT_READY` |

### operational health

| Campo | Valor |
|-------|-------|
| Termo simples | Saúde operacional |
| Termo técnico | operational health |
| Quando exibir | Visão geral, Host |
| Tooltip / ajuda | “Indica se coleta, host e automação estão saudáveis. Não mede desempenho de estratégia.” |
| Proibido | “saúde do portfólio”, cores verde/vermelho de lucro/prejuízo |

## Frases padrão recomendadas

| Contexto | Preferir | Evitar |
|----------|----------|--------|
| NOT_READY | “Ainda não dá para validar — faltam critérios.” | “Falhou a validação.” |
| BLOCKED | “Bloqueado por regra de segurança/protocolo.” | “Quebrou.” |
| READY sem authorize | “Critérios operacionais ok; validação ainda exige autorização humana.” | “Pode validar agora.” |
| Scheduler off | “Agendamento ainda não está ativo.” | “Automação desligada = sistema morto.” |
| Sem interpretação econômica | “Ainda não há conclusão econômica autorizada.” | “Sem resultados” (ambíguo: pode sugerir ocultação) |

## Palavras e padrões proibidos na UI

```text
lucro garantido
sinal de compra/venda
ordem enviada
P&L / profit
cassino / jackpot / hot streak
aprovado para dinheiro real
edge confirmado (sem gate)
dados inventados apresentados como reais
```
