# WICK — UX-R1 Operational Language Guide

```text
DOCUMENT = UX-R1-OPERATIONAL-LANGUAGE-GUIDE
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B4
TASK_ID = OPERATIONAL-LANGUAGE-MICROCOPY-001
STATUS = ACTIVE
PHASE = CONTENT_DESIGN_AND_GOVERNANCE
LOCALE = pt-BR
UI_IMPLEMENTATION_AUTHORIZED = false
UX_B4_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
EFFECTIVE_AT = 2026-07-19T13:26:43Z
SUPERSEDES_PARTIAL = docs/ux/WICK_UX_LANGUAGE_AND_TERMINOLOGY_GUIDE.md
```

## 1. Purpose

Official language, terminology and microcopy system for the WICK operational experience.

This guide governs **user-facing wording**. It does not implement UI, APIs or runtime behavior.

Companion catalogs:

| Catalog | Path |
|---------|------|
| Status messages | `docs/ux/UX-R1-STATUS-MESSAGE-CATALOG.md` |
| Empty states | `docs/ux/UX-R1-EMPTY-STATE-CATALOG.md` |
| Failures and warnings | `docs/ux/UX-R1-FAILURE-AND-WARNING-MICROCOPY.md` |
| Scientific and economic guardrails | `docs/ux/UX-R1-SCIENTIFIC-AND-ECONOMIC-LANGUAGE-GUARDRAILS.md` |

Foundation still in force: `docs/ux/WICK_UX_LANGUAGE_AND_TERMINOLOGY_GUIDE.md` (two-layer model). Where this guide and the foundation differ on operational MVP wording, **this guide wins** for UX-R1 screens.

## 1.1 Parallel UX tracks (do not duplicate)

| Track | Owns | Does not own |
|-------|------|--------------|
| UX-B2 | Future design-system and frontend architecture | Terminology / screen contracts |
| UX-B3 | Operational screen / data / state contracts | Design tokens / microcopy glossary |
| UX-B4 (this package) | Official terminology and microcopy | UI components / DS tokens / screen schemas |

Future implementation must consume the approved outputs of **all three** tracks. This package does not duplicate B2 or B3 content.

## 2. Core language principle

Every important concept uses two layers:

```text
PLAIN_LANGUAGE   (primary, always visible first)
TECHNICAL_TERM   (secondary, always visible, searchable, copyable)
```

Example:

```text
Ainda não há dados suficientes
Technical term: NOT_READY
```

Rules:

1. Plain language comes first.
2. The technical term remains visible (badge, subtitle, expandable row or “Detalhes técnicos”).
3. Never hide blockers behind soft marketing copy.
4. Never present a technical code without a plain explanation on the same surface.

## 3. Language goals

Must be:

```text
clear
direct
non-alarmist
scientifically precise
operationally actionable
non-financially-promotional
accessible
consistent
traceable
```

Avoid:

```text
casino language
trading hype
guaranteed-result language
anthropomorphic claims
false certainty
hidden blockers
ambiguous success wording
technical jargon without explanation
```

## 4. Brazilian Portuguese standard

```text
LOCALE = pt-BR
DATE_FORMAT = DD/MM/YYYY
TIME_FORMAT = HH:mm:ss
TIMEZONE_ALWAYS_VISIBLE = true
DECIMAL_SEPARATOR = comma
THOUSANDS_SEPARATOR = dot
```

Examples:

| Value | Display |
|-------|---------|
| Timestamp | `19/07/2026 13:26:43 UTC` |
| Window days | `12,45 dias` |
| Count | `1.250 observações` |
| Percentage | `87,5%` (with plain meaning) |

Technical identifiers (`run_id`, reason codes, paths) remain unchanged ASCII.

## 5. English technical terms policy

| Term | Decision | Official Portuguese label | Display pattern |
|------|----------|---------------------------|-----------------|
| readiness | bilingual | Prontidão | `Prontidão (readiness)` on first use; then `Prontidão` + badge `READY`/`NOT_READY`/`BLOCKED` |
| scheduler | bilingual | Agendamento automático | `Agendamento automático (scheduler)` |
| host | bilingual | Host / máquina | `Host` kept; expand as `máquina operacional (host)` in help |
| lock | bilingual | Travamento | `Travamento (lock)` |
| run | keep English in IDs; translate concept | Ciclo / execução | `Ciclo de coleta` + `run_id=…` |
| artifact | bilingual | Artefato / evidência | Prefer `evidência` for operators; `artifact` in technical layer |
| store | keep English in technical layer | Armazenamento oficial | `Armazenamento (store)` |
| future-unseen | bilingual | Dados futuros ainda não vistos | Primary Portuguese; badge `FUTURE_UNSEEN` |
| validate | keep command English | Validação científica | `Validação científica (validate)` |
| backup | translate concept | Cópia de segurança | `Cópia de segurança (backup)` |
| incident | translate | Incidente | Portuguese primary |
| coverage | bilingual | Cobertura | `Cobertura (coverage)` |
| freshness | bilingual | Atualidade | `Atualidade dos dados (freshness)` |
| gap | bilingual | Lacuna | `Lacuna (gap)` |
| duplicate | translate | Duplicata | Portuguese + code `DUPLICATES_PRESENT` |
| integrity | bilingual | Integridade | `Integridade (integrity)` |
| idempotency | bilingual | Idempotência | Keep technical term; explain once |
| trigger | bilingual | Disparo | `Disparo (trigger)` |

## 6. Official glossary

For each term: Portuguese label, technical term, short/long description, when to use / not use, related terms, confusion risk, scientific and economic safety notes.

### collection

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Coleta |
| TECHNICAL_TERM | `collection` / `collect` / `R3E_FUTURE_DATA_COLLECTION` |
| SHORT_DESCRIPTION | Processo de obter candles fechados após o cutoff oficial. |
| LONG_DESCRIPTION | Ingestão append-only de observações no store `future_unseen`, sem look-ahead e sem misturar backfill histórico como futuro. |
| WHEN_TO_USE | Execuções, Visão Geral, Dados Coletados. |
| WHEN_NOT_TO_USE | Não usar como sinônimo de validação científica ou trading. |
| RELATED_TERMS | execution, store, future-unseen, artifact |
| CONFUSION_RISK | Operador pode achar que “coleta ok” = experimento aprovado. |
| SCIENTIFIC_SAFETY_NOTE | Coleta bem-sucedida não autoriza `validate`. |
| ECONOMIC_SAFETY_NOTE | Não falar em lucro ou retorno da coleta. |

### execution

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Execução / ciclo de coleta |
| TECHNICAL_TERM | `run` / `run-cycle` / `run_id` |
| SHORT_DESCRIPTION | Uma corrida auditável do ciclo operacional. |
| LONG_DESCRIPTION | Sequência com `run_id`: pré-checagens, coleta incremental quando autorizada, prontidão e evidências. |
| WHEN_TO_USE | Lista e detalhe de Execuções. |
| WHEN_NOT_TO_USE | Não chamar de “trade” ou “ordem”. |
| RELATED_TERMS | collection, trigger, artifact, lock |
| CONFUSION_RISK | “Execução” pode soar como ordem enviada. |
| SCIENTIFIC_SAFETY_NOTE | Sucesso operacional ≠ gate científico. |
| ECONOMIC_SAFETY_NOTE | Proibido P&L por execução. |

### future-unseen data

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Dados futuros ainda não vistos |
| TECHNICAL_TERM | `FUTURE_UNSEEN` / `FUTURE_UNSEEN_CUTOFF` |
| SHORT_DESCRIPTION | Barras coletadas estritamente depois do corte oficial. |
| LONG_DESCRIPTION | Conjunto reservado para validação final; não reutiliza holdout R3D nem histórico pré-cutoff. |
| WHEN_TO_USE | Coleta, Prontidão, Experimento R3E. |
| WHEN_NOT_TO_USE | Não rotular dados de demonstração como future-unseen reais. |
| RELATED_TERMS | store, window days, validation |
| CONFUSION_RISK | Confundir com “dados ao vivo para trading”. |
| SCIENTIFIC_SAFETY_NOTE | Peeking de efeitos / resultados científicos proibido antes do gate. |
| ECONOMIC_SAFETY_NOTE | Sem interpretação econômica nestes dados até autorização. |

### store

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Armazenamento oficial |
| TECHNICAL_TERM | `store` / `data/future_unseen` |
| SHORT_DESCRIPTION | Local canônico das observações aceitas. |
| LONG_DESCRIPTION | Persistência append-only com manifests, hashes e trilha de auditoria. |
| WHEN_TO_USE | Dados Coletados, Host, falhas de storage. |
| WHEN_NOT_TO_USE | Não chamar de “carteira” ou “portfólio”. |
| RELATED_TERMS | integrity, duplicates, gaps, backup |
| CONFUSION_RISK | “Store” em inglês sem explicação. |
| SCIENTIFIC_SAFETY_NOTE | Integridade do store é pré-requisito operacional, não resultado do modelo. |
| ECONOMIC_SAFETY_NOTE | Tamanho do store ≠ performance financeira. |

### readiness

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Prontidão |
| TECHNICAL_TERM | `READINESS` / `READY` / `NOT_READY` / `BLOCKED` |
| SHORT_DESCRIPTION | Critérios mínimos do store para uma futura validação. |
| LONG_DESCRIPTION | Gate operacional separado do gate científico. `READY` não executa nem autoriza `validate`. |
| WHEN_TO_USE | Visão Geral, Prontidão, Host. |
| WHEN_NOT_TO_USE | Não usar como “aprovado para produção” ou “edge confirmado”. |
| RELATED_TERMS | window days, coverage, validation, scientific gate |
| CONFUSION_RISK | `NOT_READY` tratado como falha; `READY` tratado como liberação. |
| SCIENTIFIC_SAFETY_NOTE | `READY` ≠ autorização de validação. |
| ECONOMIC_SAFETY_NOTE | Prontidão não mede lucro. |

### window days

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Dias de janela |
| TECHNICAL_TERM | `WINDOW_DAYS` / `WINDOW_DAYS_INSUFFICIENT` |
| SHORT_DESCRIPTION | Dias decorridos após o cutoff até `as_of`. |
| LONG_DESCRIPTION | Progresso em direção à janela mínima do protocolo (ex.: 90 dias). Insuficiência gera `NOT_READY`, não erro. |
| WHEN_TO_USE | Banner de prontidão, checklist. |
| WHEN_NOT_TO_USE | Não apresentar como countdown de investimento. |
| RELATED_TERMS | readiness, coverage, freshness |
| CONFUSION_RISK | “Faltam X dias” lido como falha. |
| SCIENTIFIC_SAFETY_NOTE | Janela incompleta bloqueia interpretação prematura. |
| ECONOMIC_SAFETY_NOTE | Progresso de janela ≠ retorno esperado. |

### coverage

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Cobertura |
| TECHNICAL_TERM | `coverage` / `COVERAGE_INSUFFICIENT` / series completeness |
| SHORT_DESCRIPTION | Quanto das séries esperadas está presente e utilizável. |
| LONG_DESCRIPTION | Inclui séries completas vs parciais/ausentes e barras mínimas por série. No código, razões próximas incluem `SERIES_INSUFFICIENT` e `BARS_INSUFFICIENT`. |
| WHEN_TO_USE | Prontidão, Dados Coletados. |
| WHEN_NOT_TO_USE | Não confundir com acurácia do modelo. |
| RELATED_TERMS | gaps, window days, store |
| CONFUSION_RISK | Cobertura operacional ≠ acerto preditivo. |
| SCIENTIFIC_SAFETY_NOTE | Cobertura insuficiente impede validação honesta. |
| ECONOMIC_SAFETY_NOTE | Sem mapear cobertura para edge. |

### freshness

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Atualidade |
| TECHNICAL_TERM | `freshness` / `DATA_STALE` |
| SHORT_DESCRIPTION | Quão recentes estão as últimas observações aceitas. |
| LONG_DESCRIPTION | Dados defasados em relação ao esperado operacionalmente. Staleness é atenção operacional, não prova científica. |
| WHEN_TO_USE | Visão Geral, Dados Coletados, avisos. |
| WHEN_NOT_TO_USE | Não alarmar como “crash do mercado”. |
| RELATED_TERMS | collection, scheduler, host |
| CONFUSION_RISK | Stale confundido com falha científica. |
| SCIENTIFIC_SAFETY_NOTE | Não inventar barras para “atualizar”. |
| ECONOMIC_SAFETY_NOTE | Sem linguagem de oportunidade de trade. |

### gaps

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Lacunas |
| TECHNICAL_TERM | `gaps` / `GAPS_PRESENT` |
| SHORT_DESCRIPTION | Intervalos faltantes na série temporal. |
| LONG_DESCRIPTION | Buracos entre candles esperados. Devem ser visíveis e auditáveis; não preenchidos artificialmente na UI. |
| WHEN_TO_USE | Dados Coletados, Prontidão. |
| WHEN_NOT_TO_USE | Não chamar de “perda financeira”. |
| RELATED_TERMS | coverage, integrity, duplicates |
| CONFUSION_RISK | Lacuna vs. mercado fechado vs. falha de provider. |
| SCIENTIFIC_SAFETY_NOTE | Preencher lacunas sem regra versionada é proibido. |
| ECONOMIC_SAFETY_NOTE | Lacuna ≠ prejuízo. |

### duplicates

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Duplicatas |
| TECHNICAL_TERM | `DUPLICATES_PRESENT` |
| SHORT_DESCRIPTION | Observações repetidas no store. |
| LONG_DESCRIPTION | Problema de integridade; no readiness atual, duplicatas elevam para `BLOCKED`. |
| WHEN_TO_USE | Prontidão, Incidentes, falhas de storage. |
| WHEN_NOT_TO_USE | Não tratar como “mais dados = melhor”. |
| RELATED_TERMS | integrity, store, idempotency |
| CONFUSION_RISK | Duplicata vista como sucesso de coleta. |
| SCIENTIFIC_SAFETY_NOTE | Não validar sobre store com duplicatas. |
| ECONOMIC_SAFETY_NOTE | Sem linguagem de “sinal reforçado”. |

### integrity

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Integridade |
| TECHNICAL_TERM | `integrity` / `STORE_INTEGRITY_FAILURE` |
| SHORT_DESCRIPTION | Consistência e confiabilidade do store e manifests. |
| LONG_DESCRIPTION | Inclui corrupção suspeita, manifests órfãos, mistura com backfill proibido. |
| WHEN_TO_USE | Falhas críticas, Host, Governança. |
| WHEN_NOT_TO_USE | Não usar “integridade” como eufemismo de performance. |
| RELATED_TERMS | store, duplicates, backup, failure |
| CONFUSION_RISK | Integridade operacional ≠ honestidade científica do edge. |
| SCIENTIFIC_SAFETY_NOTE | Falha de integridade congela writes e proíbe validate. |
| ECONOMIC_SAFETY_NOTE | Sem P&L. |

### idempotency

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Idempotência |
| TECHNICAL_TERM | `idempotency` |
| SHORT_DESCRIPTION | Reexecutar o mesmo comando não duplica efeito indevido. |
| LONG_DESCRIPTION | Coleta e ciclos devem ser seguros para repetir; evidências registram o resultado real. |
| WHEN_TO_USE | Execuções, tooltips técnicos, Governança. |
| WHEN_NOT_TO_USE | Não afirmar idempotência se o fluxo não for. |
| RELATED_TERMS | execution, duplicates, lock |
| CONFUSION_RISK | Termo opaco para não-engenheiros. |
| SCIENTIFIC_SAFETY_NOTE | Idempotência protege o store; não gera resultado científico. |
| ECONOMIC_SAFETY_NOTE | N/A econômico. |

### scheduler

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Agendamento automático |
| TECHNICAL_TERM | `scheduler` / systemd timer / cron |
| SHORT_DESCRIPTION | Disparo automático de ciclos em horário definido. |
| LONG_DESCRIPTION | Enquanto `SCHEDULER_ACTIVATION = BLOCKED`, a UI diz que o agendamento **não está ativo**. |
| WHEN_TO_USE | Host e Scheduler. |
| WHEN_NOT_TO_USE | Não chamar de “robô de trading”. |
| RELATED_TERMS | host, trigger, lock, deferred dependency |
| CONFUSION_RISK | Scheduler ausente lido como sistema morto ou falha. |
| SCIENTIFIC_SAFETY_NOTE | Ativação não autoriza validate. |
| ECONOMIC_SAFETY_NOTE | Automação ≠ lucro automático. |

### host

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Host (máquina operacional) |
| TECHNICAL_TERM | `host` / `host_id` |
| SHORT_DESCRIPTION | Ambiente onde coleta/automação deve rodar de forma persistente. |
| LONG_DESCRIPTION | Discovery real ainda pode estar adiada (`HOST_DISCOVERY = DEFERRED`). |
| WHEN_TO_USE | Host e Scheduler, Incidentes. |
| WHEN_NOT_TO_USE | Não inventar hostname/IP na UI. |
| RELATED_TERMS | scheduler, lock, backup, operational debt |
| CONFUSION_RISK | Host “preparado em docs” ≠ host descoberto. |
| SCIENTIFIC_SAFETY_NOTE | Sem host real, não fingir ativação. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### lock

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Travamento |
| TECHNICAL_TERM | `lock` / `LOCK_ACTIVE` / `LOCK_STALE` / `SKIPPED_LOCKED` |
| SHORT_DESCRIPTION | Proteção contra ciclos sobrepostos ou remoção insegura. |
| LONG_DESCRIPTION | Lock ativo esperado não é crash. Lock stale exige diagnóstico humano. |
| WHEN_TO_USE | Execuções, Host, falhas. |
| WHEN_NOT_TO_USE | Não dizer “sistema travou” para lock intencional. |
| RELATED_TERMS | execution, scheduler, incident |
| CONFUSION_RISK | Lock vs falha vs bloqueio científico. |
| SCIENTIFIC_SAFETY_NOTE | Force-unlock sem autorização é proibido. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### backup

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Cópia de segurança |
| TECHNICAL_TERM | `backup` |
| SHORT_DESCRIPTION | Cópia verificável do estado operacional. |
| LONG_DESCRIPTION | Não altera resultado científico; falha de backup é alerta operacional. |
| WHEN_TO_USE | Host, Incidentes, Governança. |
| WHEN_NOT_TO_USE | Não chamar de snapshot de performance. |
| RELATED_TERMS | integrity, host, failure |
| CONFUSION_RISK | Backup ok ≠ estratégia validada. |
| SCIENTIFIC_SAFETY_NOTE | Restore só com autorização humana. |
| ECONOMIC_SAFETY_NOTE | Sem “salvou o lucro”. |

### incident

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Incidente |
| TECHNICAL_TERM | `incident` |
| SHORT_DESCRIPTION | Problema operacional que merece registro e acompanhamento. |
| LONG_DESCRIPTION | Diferente de `NOT_READY` esperado durante a coleta. |
| WHEN_TO_USE | Incidentes, Visão Geral. |
| WHEN_NOT_TO_USE | Não classificar janela incompleta como incidente. |
| RELATED_TERMS | warning, failure, blocked |
| CONFUSION_RISK | Todo aviso virar incidente. |
| SCIENTIFIC_SAFETY_NOTE | Incidente não autoriza atalho científico. |
| ECONOMIC_SAFETY_NOTE | Sem linguagem de perda financeira. |

### warning

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Aviso |
| TECHNICAL_TERM | `warning` / ATTENTION |
| SHORT_DESCRIPTION | Atenção sem falha dura. |
| LONG_DESCRIPTION | Inclui `NOT_READY`, dados parciais, scheduler inativo esperado. |
| WHEN_TO_USE | Banners âmbar, tooltips. |
| WHEN_NOT_TO_USE | Não usar vermelho. |
| RELATED_TERMS | failure, not ready, deferred |
| CONFUSION_RISK | Aviso lido como erro. |
| SCIENTIFIC_SAFETY_NOTE | Aviso não esconde bloqueio. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### failure

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Falha |
| TECHNICAL_TERM | `failure` / `FAILED` / failure category codes |
| SHORT_DESCRIPTION | Ciclo ou componente que não completou de forma saudável. |
| LONG_DESCRIPTION | Mapeado pela taxonomia operacional; vermelho reservado. |
| WHEN_TO_USE | Execuções com exit failure, Incidentes. |
| WHEN_NOT_TO_USE | Não rotular `NOT_READY` ou `SKIPPED_LOCKED` esperado como falha. |
| RELATED_TERMS | warning, blocked, incident |
| CONFUSION_RISK | Falha operacional confundida com rejeição científica de edge. |
| SCIENTIFIC_SAFETY_NOTE | Falha não autoriza validate nem peeking. |
| ECONOMIC_SAFETY_NOTE | Falha ≠ prejuízo de estratégia. |

### blocked

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Bloqueado |
| TECHNICAL_TERM | `BLOCKED` |
| SHORT_DESCRIPTION | Impedido por regra, integridade ou autorização. |
| LONG_DESCRIPTION | Bloqueio pode ser proteção correta. Nem todo bloqueio é falha. |
| WHEN_TO_USE | Prontidão, ações desabilitadas, Host. |
| WHEN_NOT_TO_USE | Não dizer “quebrou” quando o bloqueio é intencional. |
| RELATED_TERMS | not ready, failure, scientific gate |
| CONFUSION_RISK | `BLOCKED` = `ERROR`. |
| SCIENTIFIC_SAFETY_NOTE | Bloqueios científicos/operacionais protegem o protocolo. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### not ready

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Ainda não pronto |
| TECHNICAL_TERM | `NOT_READY` |
| SHORT_DESCRIPTION | Critérios mínimos ainda não atendidos. |
| LONG_DESCRIPTION | Estado esperado durante acumulação de janela/cobertura. **Não é erro.** |
| WHEN_TO_USE | Prontidão, Visão Geral. |
| WHEN_NOT_TO_USE | Não usar vermelho; não dizer “falhou”. |
| RELATED_TERMS | ready, window days, coverage |
| CONFUSION_RISK | Tratado como incident/failure. |
| SCIENTIFIC_SAFETY_NOTE | Continuar coleta; não validar. |
| ECONOMIC_SAFETY_NOTE | Sem urgência de trade. |

### ready

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Critérios operacionais atendidos |
| TECHNICAL_TERM | `READY` |
| SHORT_DESCRIPTION | Store atende critérios do gate de prontidão. |
| LONG_DESCRIPTION | Exige revisão humana. **Não autoriza** `validate`, R4, R5 nem interpretação econômica. |
| WHEN_TO_USE | Transição de prontidão, notificação operacional. |
| WHEN_NOT_TO_USE | Não dizer “pode validar agora” sem autorização explícita. |
| RELATED_TERMS | not ready, validation, scientific gate |
| CONFUSION_RISK | Verde = lucro / liberação. |
| SCIENTIFIC_SAFETY_NOTE | `VALIDATE_AUTHORIZED` permanece false até decisão humana. |
| ECONOMIC_SAFETY_NOTE | Verde nunca significa lucrativo. |

### validation

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Validação científica |
| TECHNICAL_TERM | `validate` / `R3E_GATE` |
| SHORT_DESCRIPTION | Avaliação do protocolo em dados future-unseen. |
| LONG_DESCRIPTION | Só com autorização humana explícita e critérios atendidos. Fora do escopo de UI até autorização. |
| WHEN_TO_USE | Experimento, Prontidão (como ação bloqueada explicada). |
| WHEN_NOT_TO_USE | Não apresentar botão ativo sem autorização. |
| RELATED_TERMS | scientific gate, readiness, future-unseen |
| CONFUSION_RISK | “Validação” genérica = qualquer check. |
| SCIENTIFIC_SAFETY_NOTE | Sem peeking; sem reuso de holdout. |
| ECONOMIC_SAFETY_NOTE | Resultado de validate não implica promoção econômica automática. |

### scientific gate

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Gate científico |
| TECHNICAL_TERM | `R3E_GATE` / mechanical gates |
| SHORT_DESCRIPTION | Decisão metodológica versionada sobre evidência. |
| LONG_DESCRIPTION | Separado de sucesso operacional e de prontidão. |
| WHEN_TO_USE | Experimento, Governança. |
| WHEN_NOT_TO_USE | Não usar para status de host/scheduler. |
| RELATED_TERMS | validation, economic interpretation |
| CONFUSION_RISK | Gate científico vs readiness operacional. |
| SCIENTIFIC_SAFETY_NOTE | Estado atual permanece `PENDING_FUTURE_UNSEEN_DATA` até evidência futura. |
| ECONOMIC_SAFETY_NOTE | Gate mecânico ≠ autorização econômica. |

### economic interpretation

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Interpretação econômica |
| TECHNICAL_TERM | `ECONOMIC_INTERPRETATION_ALLOWED` |
| SHORT_DESCRIPTION | Conclusão sobre valor econômico ou edge negociável. |
| LONG_DESCRIPTION | Enquanto `false`, a UI não afirma vantagem financeira. |
| WHEN_TO_USE | Experimento, avisos de governança. |
| WHEN_NOT_TO_USE | Não inventar P&L ilustrativo “só para demonstração” sem rótulo e proibição clara. |
| RELATED_TERMS | scientific gate, operational success |
| CONFUSION_RISK | Sucesso de coleta lido como edge. |
| SCIENTIFIC_SAFETY_NOTE | Interpretação só com gate e autorização. |
| ECONOMIC_SAFETY_NOTE | Default: proibida. |

### operational debt

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Débito técnico-operacional |
| TECHNICAL_TERM | `OPERATIONAL_DEBT` / `OPEN` |
| SHORT_DESCRIPTION | Dependência aceita e registrada, ainda não concluída. |
| LONG_DESCRIPTION | O projeto segue em frentes não dependentes **sem** considerar a ativação concluída. Ver §7. |
| WHEN_TO_USE | Host, Visão Geral, relatórios, auditoria. |
| WHEN_NOT_TO_USE | Não apresentar como item concluído ou “ok”. |
| RELATED_TERMS | deferred dependency, host discovery, scheduler |
| CONFUSION_RISK | Débito aberto parecer done. |
| SCIENTIFIC_SAFETY_NOTE | Débito não altera estado científico. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### deferred dependency

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Dependência adiada |
| TECHNICAL_TERM | `DEFERRED` (ex.: `HOST_DISCOVERY`) |
| SHORT_DESCRIPTION | Trabalho intencionalmente postergado com registro explícito. |
| LONG_DESCRIPTION | Não é esquecimento; não é conclusão. |
| WHEN_TO_USE | Host discovery, ativações futuras. |
| WHEN_NOT_TO_USE | Não usar para esconder falha. |
| RELATED_TERMS | operational debt, blocked |
| CONFUSION_RISK | Deferred = resolvido. |
| SCIENTIFIC_SAFETY_NOTE | Adiar discovery não autoriza atalhos. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### manual execution

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Execução manual |
| TECHNICAL_TERM | `manual execution` |
| SHORT_DESCRIPTION | Ciclo disparado por operador autorizado. |
| LONG_DESCRIPTION | Modo atual enquanto scheduler não está ativo. |
| WHEN_TO_USE | Host, Execuções. |
| WHEN_NOT_TO_USE | Não incentivar execução não autorizada na UI. |
| RELATED_TERMS | automated execution, trigger |
| CONFUSION_RISK | Manual = informal / sem auditoria. |
| SCIENTIFIC_SAFETY_NOTE | Manual ainda exige `run_id` e evidências. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### automated execution

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Execução automatizada |
| TECHNICAL_TERM | `automated execution` / scheduler-triggered |
| SHORT_DESCRIPTION | Ciclo disparado pelo agendamento. |
| LONG_DESCRIPTION | Indisponível enquanto ativação estiver bloqueada. |
| WHEN_TO_USE | Host (estado desabilitado explicado). |
| WHEN_NOT_TO_USE | Não afirmar automação ativa sem evidência. |
| RELATED_TERMS | scheduler, trigger |
| CONFUSION_RISK | Docs de preparação = automação ligada. |
| SCIENTIFIC_SAFETY_NOTE | Automação ≠ validate automático. |
| ECONOMIC_SAFETY_NOTE | Proibido “bot lucrando”. |

### artifact

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Evidência / artefato |
| TECHNICAL_TERM | `artifact` / report paths |
| SHORT_DESCRIPTION | Arquivo ou registro auditável gerado por um ciclo. |
| LONG_DESCRIPTION | Relatórios JSON, logs, manifests, hashes — rastreáveis por `run_id`. |
| WHEN_TO_USE | Execuções, Governança. |
| WHEN_NOT_TO_USE | Não chamar de “prova de lucro”. |
| RELATED_TERMS | evidence, run, integrity |
| CONFUSION_RISK | Artefato de demo sem rótulo. |
| SCIENTIFIC_SAFETY_NOTE | Evidência operacional ≠ evidência de edge. |
| ECONOMIC_SAFETY_NOTE | Sem P&L embutido. |

### evidence

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Evidência |
| TECHNICAL_TERM | `evidence` |
| SHORT_DESCRIPTION | Material que permite auditar o que ocorreu. |
| LONG_DESCRIPTION | Preferir este termo na UI para operadores; `artifact` na camada técnica. |
| WHEN_TO_USE | Botões “Abrir evidência”, detalhe de execução. |
| WHEN_NOT_TO_USE | Não usar para marketing de resultado. |
| RELATED_TERMS | artifact, run |
| CONFUSION_RISK | Evidência = verdade científica final. |
| SCIENTIFIC_SAFETY_NOTE | Cadeia de evidência deve permanecer intacta. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### run

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Ciclo (`run`) |
| TECHNICAL_TERM | `run` / `run_id` |
| SHORT_DESCRIPTION | Identidade única de uma execução. |
| LONG_DESCRIPTION | Sempre copyable; aparece em listas e detalhes. |
| WHEN_TO_USE | Todas as telas com histórico. |
| WHEN_NOT_TO_USE | Não omitir `run_id` em superfícies de auditoria. |
| RELATED_TERMS | execution, trigger, artifact |
| CONFUSION_RISK | Run de coleta vs run de experimento científico. |
| SCIENTIFIC_SAFETY_NOTE | Sempre amarrar a versões quando for run científico. |
| ECONOMIC_SAFETY_NOTE | N/A. |

### trigger

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Disparo |
| TECHNICAL_TERM | `trigger` |
| SHORT_DESCRIPTION | O que iniciou o ciclo (manual, timer, API). |
| LONG_DESCRIPTION | Deve ser explícito na UI de detalhe. |
| WHEN_TO_USE | Detalhe de execução. |
| WHEN_NOT_TO_USE | Não inventar trigger se desconhecido — dizer “não disponível”. |
| RELATED_TERMS | scheduler, manual execution |
| CONFUSION_RISK | Trigger = sinal de compra. |
| SCIENTIFIC_SAFETY_NOTE | N/A operacional. |
| ECONOMIC_SAFETY_NOTE | Proibido jargão de sinal. |

### health

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Saúde operacional |
| TECHNICAL_TERM | `health` / operational health |
| SHORT_DESCRIPTION | Se coleta, host e automação estão saudáveis. |
| LONG_DESCRIPTION | Não mede desempenho de estratégia. |
| WHEN_TO_USE | Visão Geral, Host. |
| WHEN_NOT_TO_USE | Não usar “saúde do portfólio”. |
| RELATED_TERMS | status, incident, warning |
| CONFUSION_RISK | Verde de saúde = lucrativo. |
| SCIENTIFIC_SAFETY_NOTE | Saúde operacional ≠ gate científico. |
| ECONOMIC_SAFETY_NOTE | Verde nunca = profit. |

### status

| Field | Value |
|-------|-------|
| OFFICIAL_PORTUGUESE_LABEL | Status |
| TECHNICAL_TERM | status codes (see status catalog) |
| SHORT_DESCRIPTION | Estado atual de um objeto (ciclo, host, prontidão). |
| LONG_DESCRIPTION | Sempre duas camadas; cor não é o único significado. |
| WHEN_TO_USE | Badges, banners, tabelas. |
| WHEN_NOT_TO_USE | Não usar status ambíguo (“ok”, “tudo bem”) sem código. |
| RELATED_TERMS | health, ready, blocked, failure |
| CONFUSION_RISK | Status operacional vs científico. |
| SCIENTIFIC_SAFETY_NOTE | Separar claramente. |
| ECONOMIC_SAFETY_NOTE | Sem status de “lucro”. |

## 7. Operational debt language

Accepted debt (current official state):

```text
HOST_DISCOVERY = DEFERRED
OPERATIONAL_DEBT = OPEN
SCHEDULER_ACTIVATION = BLOCKED
```

Canonical concept:

```text
Débito técnico-operacional aceito e registrado.
O projeto segue nas frentes não dependentes,
sem considerar a ativação concluída.
```

### Variants

| Surface | Microcopy |
|---------|-----------|
| Dashboard / Visão Geral | `Débito operacional aberto: descoberta de host adiada; agendamento não ativado.` |
| Detail page | `Há um débito técnico-operacional aceito e registrado: HOST_DISCOVERY=DEFERRED. O agendamento automático permanece BLOCKED. As frentes não dependentes podem avançar; a ativação não está concluída.` |
| Tooltip | `Débito aberto ≠ concluído. Scheduler não está ativo.` |
| Badge | Primary: `Débito aberto` · Technical: `OPERATIONAL_DEBT=OPEN` |
| Audit record | `OPERATIONAL_DEBT=OPEN; HOST_DISCOVERY=DEFERRED; SCHEDULER_ACTIVATION=BLOCKED; activation_complete=false` |
| Project report | `Estado operacional: débito técnico-operacional aberto. Host discovery adiada. Ativação do scheduler bloqueada. Sem implicação de prontidão de host nem de validação científica.` |
| Incident context | `Este contexto não fecha o débito operacional. Scheduler permanece não ativado.` |
| Mobile compact view | `Débito aberto · scheduler off` |

### Prohibited implications

Do not imply:

```text
host ready
scheduler active
activation complete
operational validation complete
```

## 8. Action language

### Allowed read-only actions

| Label | Technical intent |
|-------|------------------|
| Ver detalhes | Open detail |
| Abrir evidência | Open artifact/evidence |
| Copiar identificador | Copy `run_id` / code |
| Atualizar agora | Manual refresh of read model |
| Baixar relatório | Download evidence pack |
| Ver execução | Navigate to run |
| Ver bloqueios | Show blockers list |
| Ver dados técnicos | Expand technical layer |
| Ver histórico | Open history |
| Voltar | Navigate back |

### Prohibited as active actions (until explicit operational authorization)

```text
Ativar scheduler
Executar coleta
Validar modelo
Liberar R4
Executar automaticamente
```

These may appear only as **disabled** controls or explanatory references when the screen must teach why they are unavailable.

Disabled pattern:

```text
Validar modelo — indisponível
Motivo: autorização humana e gate científico ainda não liberados
Technical: VALIDATE_AUTHORIZED=false
```

## 9. Screen-level microcopy catalog

Shared labels for all screens:

| Key | Label |
|-----|-------|
| technical details | Detalhes técnicos |
| evidence | Evidências |
| last updated | Atualizado em |
| manual refresh | Atualizar agora |
| copy ID | Copiar identificador |
| download evidence | Baixar relatório |

Timezone always shown with timestamps.

### Visão Geral

| Field | Copy |
|-------|------|
| screen title | Visão Geral |
| screen subtitle | Estado operacional do WICK, em linguagem simples e códigos técnicos. |
| primary explanation | Veja se a coleta, a prontidão e o host estão saudáveis — e qual é a próxima ação segura. |
| empty state | Ainda não há resumo operacional para mostrar. |
| loading state | Carregando o estado operacional… |
| partial-data state | Parte dos painéis ainda não tem dados. Os disponíveis estão abaixo. |
| stale-data state | Este resumo pode estar desatualizado. Atualize ou confira a última execução. |
| unavailable state | O resumo operacional está temporariamente indisponível. |
| blocked state | Há bloqueios registrados. Bloqueado não significa necessariamente falha. |
| error state | Não foi possível montar a visão geral. Preserve evidências e tente atualizar. |

### Execuções

| Field | Copy |
|-------|------|
| screen title | Execuções |
| screen subtitle | Ciclos de coleta com `run_id`, status e evidências. |
| primary explanation | Investigue o que cada ciclo fez, sem confundir sucesso operacional com resultado científico. |
| empty state | Ainda não há execuções registradas. |
| loading state | Carregando execuções… |
| partial-data state | Algumas execuções têm metadados incompletos. |
| stale-data state | A lista pode estar defasada em relação ao host. |
| unavailable state | Histórico de execuções indisponível no momento. |
| blocked state | Há ciclos bloqueados por regra ou travamento. Veja o motivo técnico. |
| error state | Falha ao carregar execuções. |

### Readiness (Prontidão)

| Field | Copy |
|-------|------|
| screen title | Prontidão |
| screen subtitle | Critérios operacionais do store future-unseen. |
| primary explanation | A prontidão diz se a janela e a cobertura mínimas foram atendidas. Não é validação científica. |
| empty state | Ainda não há histórico de prontidão. |
| loading state | Avaliando critérios de prontidão… |
| partial-data state | Critérios parciais disponíveis; lista completa pode estar incompleta. |
| stale-data state | Avaliação de prontidão desatualizada em relação ao store. |
| unavailable state | Gate de prontidão indisponível. |
| blocked state | Prontidão bloqueada por integridade ou regra de proteção. |
| error state | Não foi possível obter o status de prontidão. |

### Host e Scheduler

| Field | Copy |
|-------|------|
| screen title | Host e Scheduler |
| screen subtitle | Máquina operacional e agendamento automático. |
| primary explanation | Discovery de host pode estar adiada; agendamento permanece bloqueado até autorização. |
| empty state | Sem dados de host ou scheduler para exibir. |
| loading state | Carregando estado de host e agendamento… |
| partial-data state | Informações parciais: discovery ainda não concluída. |
| stale-data state | Estado do host pode estar desatualizado. |
| unavailable state | Status de host/scheduler indisponível. |
| blocked state | Ativação do scheduler bloqueada. Débito operacional permanece aberto. |
| error state | Falha ao ler estado de host/scheduler. |

### Dados Coletados

| Field | Copy |
|-------|------|
| screen title | Dados Coletados |
| screen subtitle | Observações aceitas no armazenamento oficial. |
| primary explanation | Consulte cobertura, lacunas e atualidade — sem inventar barras. |
| empty state | Ainda não há observações no store. |
| loading state | Carregando observações… |
| partial-data state | Cobertura parcial: algumas séries incompletas. |
| stale-data state | Última observação mais antiga que o esperado. |
| unavailable state | Metadados do store indisponíveis. |
| blocked state | Leitura bloqueada por integridade ou permissão. |
| error state | Falha ao carregar dados coletados. |

### Incidentes

| Field | Copy |
|-------|------|
| screen title | Incidentes |
| screen subtitle | Problemas operacionais registrados. |
| primary explanation | Incidentes são distintos de `NOT_READY` esperado durante a coleta. |
| empty state | Nenhum incidente registrado. |
| loading state | Carregando incidentes… |
| partial-data state | Lista parcial de incidentes. |
| stale-data state | Feed de incidentes pode estar defasado. |
| unavailable state | Módulo de incidentes indisponível. |
| blocked state | Registro de incidentes temporariamente bloqueado. |
| error state | Falha ao carregar incidentes. |

### Governança

| Field | Copy |
|-------|------|
| screen title | Governança |
| screen subtitle | Aprovações, débitos, evidências e trilha de decisão. |
| primary explanation | Transparência de autorizações e do que ainda está bloqueado. |
| empty state | Sem itens de governança para listar. |
| loading state | Carregando governança… |
| partial-data state | Parte dos registros de aprovação ainda não está disponível. |
| stale-data state | Painel de governança desatualizado. |
| unavailable state | Governança indisponível no momento. |
| blocked state | Ação de governança bloqueada até autorização humana. |
| error state | Falha ao carregar governança. |

### Experimentos

| Field | Copy |
|-------|------|
| screen title | Experimentos |
| screen subtitle | Contexto do experimento R3E sem interpretação econômica. |
| primary explanation | Explique a pergunta científica e a fase atual. Não afirme edge ou lucro. |
| empty state | Nenhum experimento listado nesta visão. |
| loading state | Carregando experimentos… |
| partial-data state | Metadados parciais do experimento. |
| stale-data state | Informações do experimento podem estar desatualizadas. |
| unavailable state | Detalhes do experimento indisponíveis. |
| blocked state | Validação científica bloqueada / não autorizada. |
| error state | Falha ao carregar experimentos. |

## 10. Accessibility and comprehension

| Rule | Standard |
|------|----------|
| Maximum sentence complexity | Prefer one idea per sentence; max ~25 words for primary UI sentences. |
| Abbreviation expansion | Expand on first use per screen (`FDR (False Discovery Rate)`). |
| Technical-term first-use | Portuguese first, then technical badge/code. |
| Tooltip usage | Clarify secondary layer; never be the only place a blocker appears. |
| Screen-reader wording | State name + plain meaning + technical code; do not rely on color alone. |
| Numeric formatting | pt-BR separators; units explicit (`dias`, `observações`). |
| Date/time | `DD/MM/YYYY HH:mm:ss` + timezone visible. |
| Percentage | `87,5%` + plain meaning (“da janela mínima”). |
| Error identification | Include failure code copyable. |
| Non-color meaning | Icon + text label mandatory for status. |

Reading level: clear professional Portuguese — no infantilization, no unexplained jargon.

## 11. Readiness wording (summary)

Full detail in status + failure catalogs. Official codes for UX:

| Code | Plain primary |
|------|---------------|
| `WINDOW_DAYS_INSUFFICIENT` | Ainda faltam dias na janela mínima. |
| `SERIES_INCOMPLETE` / `SERIES_INSUFFICIENT` | Ainda faltam séries completas. |
| `COVERAGE_INSUFFICIENT` | Cobertura ainda insuficiente. |
| `DATA_STALE` | Os dados estão desatualizados em relação ao esperado. |
| `GAPS_PRESENT` | Há lacunas nas séries. |
| `DUPLICATES_PRESENT` | Há duplicatas no armazenamento. |
| `STORE_INTEGRITY_FAILURE` | Integridade do armazenamento comprometida. |
| `READY` | Critérios operacionais atendidos; validação ainda exige autorização humana. |

Code alignment note: runtime readiness today emits `SERIES_INSUFFICIENT` / `BARS_INSUFFICIENT`. UX may show `SERIES_INCOMPLETE` as plain synonym only when paired with the exact runtime code in the technical layer.

## 12. Implementation boundary

```text
THIS_PACKAGE = documentation and governance only
UI_CODE = forbidden
FRONTEND_ROUTES = forbidden
DESIGN_TOKENS_CODE = forbidden
API_RUNTIME = forbidden
R3E_SCIENTIFIC_STATE_CHANGE = false
```
