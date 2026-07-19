# WICK — UX-R1 Empty-State Catalog

```text
DOCUMENT = UX-R1-EMPTY-STATE-CATALOG
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B4
TASK_ID = OPERATIONAL-LANGUAGE-MICROCOPY-001
STATUS = ACTIVE
LOCALE = pt-BR
UI_IMPLEMENTATION_AUTHORIZED = false
EFFECTIVE_AT = 2026-07-19T13:26:43Z
```

## Rules

1. Empty is not failure by default.
2. Explain why empty can be legitimate.
3. Offer only safe next actions (read-only / refresh / navigate).
4. Never imply profit, validate authorization, or scheduler activation.
5. Always expose a technical context line.

## Catalog

### no executions

| Field | Value |
|-------|-------|
| headline | Ainda não há execuções |
| explanation | Nenhum ciclo de coleta foi registrado nesta visão. |
| technical context | `runs=[]` · sem `run_id` disponível |
| next safe action | Atualizar agora · Ver Host e Scheduler |
| prohibited implication | Sistema quebrado; coleta “falhou”; automação ativa |

### no failures

| Field | Value |
|-------|-------|
| headline | Nenhuma falha registrada |
| explanation | Não há ciclos classificados como falha operacional neste período. |
| technical context | `failure_category=null` nos ciclos listados |
| next safe action | Ver execuções · Ver prontidão |
| prohibited implication | Estratégia lucrativa; experimento aprovado; ausência de `NOT_READY` |

### no incidents

| Field | Value |
|-------|-------|
| headline | Nenhum incidente registrado |
| explanation | Não há problemas operacionais abertos nesta lista. |
| technical context | `incidents=[]` |
| next safe action | Voltar à Visão Geral · Atualizar agora |
| prohibited implication | Host pronto; scheduler ativo; débito operacional fechado |

### no readiness history

| Field | Value |
|-------|-------|
| headline | Ainda sem histórico de prontidão |
| explanation | Nenhuma avaliação de prontidão foi armazenada para exibir. |
| technical context | readiness history absent · gate reports not listed |
| next safe action | Ver Dados Coletados · Atualizar agora |
| prohibited implication | Validação já ocorreu; critérios impossíveis |

### no host discovery

| Field | Value |
|-------|-------|
| headline | Discovery de host ainda não disponível |
| explanation | A descoberta no host real está adiada ou ainda não foi registrada. |
| technical context | `HOST_DISCOVERY=DEFERRED` · result file ausente |
| next safe action | Ver detalhes do débito · Ver Governança |
| prohibited implication | Host ready; preparation docs = discovery complete |

### no scheduler registration

| Field | Value |
|-------|-------|
| headline | Agendamento não registrado |
| explanation | Não há timer/scheduler ativo ou registrado neste ambiente. |
| technical context | `SCHEDULER_ACTIVATION=BLOCKED` · timer not enabled |
| next safe action | Ver Host e Scheduler · Ver débito aberto |
| prohibited implication | Activation complete; auto-trading on |

### no backups

| Field | Value |
|-------|-------|
| headline | Nenhuma cópia de segurança listada |
| explanation | Ainda não há backups verificáveis nesta visão. |
| technical context | `backups=[]` |
| next safe action | Ver Host · Atualizar agora |
| prohibited implication | Dados perdidos com certeza; restore automático disponível na UI |

### no collection artifacts

| Field | Value |
|-------|-------|
| headline | Sem evidências de coleta |
| explanation | Não há artefatos/relatórios de coleta para abrir. |
| technical context | artifact paths absent for selected scope |
| next safe action | Ver execuções · Voltar |
| prohibited implication | Experimento sem valor; lucro ausente |

### no available metadata

| Field | Value |
|-------|-------|
| headline | Metadados indisponíveis |
| explanation | Os metadados necessários para esta vista não estão acessíveis. |
| technical context | `UNAVAILABLE` / metadata null |
| next safe action | Atualizar agora · Ver dados técnicos (se houver) |
| prohibited implication | Remoção silenciosa de evidência; sucesso oculto |

## Shared empty-state footer (optional)

```text
Estados vazios legítimos não são falhas.
Códigos técnicos permanecem auditáveis quando existirem.
```
