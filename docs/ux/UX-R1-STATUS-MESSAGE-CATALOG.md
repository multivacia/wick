# WICK — UX-R1 Status Message Catalog

```text
DOCUMENT = UX-R1-STATUS-MESSAGE-CATALOG
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B4
TASK_ID = OPERATIONAL-LANGUAGE-MICROCOPY-001
STATUS = ACTIVE
LOCALE = pt-BR
UI_IMPLEMENTATION_AUTHORIZED = false
EFFECTIVE_AT = 2026-07-19T13:26:43Z
```

## Mandatory rules

```text
NOT_READY is not an error
READY does not authorize validation
SUCCESS does not imply profit
BLOCKED does not always imply failure
red is reserved for real failure
green never means profitable
deferred debt must not look completed
```

Color is never the sole channel. Pair with label + technical code + icon meaning.

## Status entries

### NORMAL

| Field | Value |
|-------|-------|
| primary label | Normal |
| secondary technical label | `NORMAL` |
| one-line explanation | Operação dentro do esperado, sem alerta. |
| expanded explanation | Não há avisos, bloqueios nem falhas neste objeto. Continua sujeito às regras científicas vigentes. |
| recommended icon meaning | Neutral indicator / steady state |
| prohibited color implication | Do not use bright green that suggests profit or “all clear to trade”. |
| allowed next action | Continuar monitoramento; Ver detalhes |
| prohibited implication | Liberação de validate, R4 ou money |
| screen-reader text | Status normal. Código NORMAL. Sem alertas operacionais. |

### SUCCESS

| Field | Value |
|-------|-------|
| primary label | Concluído com sucesso |
| secondary technical label | `SUCCESS` / `COMPLETE` |
| one-line explanation | A operação pedida terminou sem falha dura. |
| expanded explanation | Sucesso operacional (ex.: ciclo completo, backup ok). Não significa edge, lucro nem autorização científica. |
| recommended icon meaning | Check for completion only |
| prohibited color implication | Green must not mean profitable or “model approved”. |
| allowed next action | Abrir evidência; Copiar identificador; Ver histórico |
| prohibited implication | Profit, accuracy guaranteed, validate authorized |
| screen-reader text | Sucesso operacional. Código SUCCESS. Não implica resultado econômico. |

### ATTENTION

| Field | Value |
|-------|-------|
| primary label | Atenção |
| secondary technical label | `ATTENTION` |
| one-line explanation | Há algo a observar, sem falha dura confirmada. |
| expanded explanation | Use para dados parciais, defasagem leve, avisos e estados que pedem olhar humano sem alarmismo. |
| recommended icon meaning | Amber caution mark |
| prohibited color implication | Not red; not success-green. |
| allowed next action | Ver detalhes; Ver bloqueios; Atualizar agora |
| prohibited implication | Crash, loss, or scientific failure |
| screen-reader text | Atenção. Código ATTENTION. Não é falha. |

### BLOCKED

| Field | Value |
|-------|-------|
| primary label | Bloqueado |
| secondary technical label | `BLOCKED` |
| one-line explanation | Impedido por regra, integridade ou falta de autorização. |
| expanded explanation | Bloqueio pode ser proteção correta. Distinto de erro. Mostre o motivo técnico. |
| recommended icon meaning | Shield / stop-barrier (not skull/crash) |
| prohibited color implication | Do not default to failure-red unless paired with a real failure category. Prefer distinct blocked token (e.g. purple per visual direction). |
| allowed next action | Ver bloqueios; Ver dados técnicos; Voltar |
| prohibited implication | “Quebrou”; always equivalent to ERROR |
| screen-reader text | Bloqueado. Código BLOCKED. Pode ser proteção, não necessariamente falha. |

### ERROR

| Field | Value |
|-------|-------|
| primary label | Falha |
| secondary technical label | `ERROR` / `FAILED` |
| one-line explanation | Ocorreu uma falha operacional real. |
| expanded explanation | Reserve vermelho. Inclua código da taxonomia, impacto e próximo passo seguro. |
| recommended icon meaning | Failure mark |
| prohibited color implication | Red only here (and true critical integrity failures). |
| allowed next action | Abrir evidência; Ver dados técnicos; Copiar identificador |
| prohibited implication | Retry when retry worsens condition; economic loss narrative |
| screen-reader text | Falha. Código ERROR. Consulte evidências e o código técnico. |

### UNAVAILABLE

| Field | Value |
|-------|-------|
| primary label | Indisponível |
| secondary technical label | `UNAVAILABLE` |
| one-line explanation | A informação ou serviço não está acessível agora. |
| expanded explanation | Diferente de vazio legítimo e de bloqueio por regra. Pode ser outage temporário de leitura. |
| recommended icon meaning | Offline / unavailable |
| prohibited color implication | Not success; not necessarily failure-red. |
| allowed next action | Atualizar agora; Voltar |
| prohibited implication | Data deleted; scientific rejection |
| screen-reader text | Indisponível. Código UNAVAILABLE. |

### INFORMATIONAL

| Field | Value |
|-------|-------|
| primary label | Informação |
| secondary technical label | `INFORMATIONAL` / `INFO` |
| one-line explanation | Contexto útil sem exigir alarme. |
| expanded explanation | Ex.: lembrete de que interpretação econômica está desligada; débito registrado. |
| recommended icon meaning | Info mark |
| prohibited color implication | Not error-red; not profit-green. |
| allowed next action | Ver detalhes; Ver dados técnicos |
| prohibited implication | Hidden blocker disguised as info-only when action is blocked |
| screen-reader text | Informação. Código INFORMATIONAL. |

### NOT_READY

| Field | Value |
|-------|-------|
| primary label | Ainda não pronto |
| secondary technical label | `NOT_READY` |
| one-line explanation | Critérios mínimos ainda não foram atendidos. |
| expanded explanation | Estado esperado durante acumulação. Não é erro. Continuar coleta quando autorizada; não validar. |
| recommended icon meaning | Amber progress / hourglass |
| prohibited color implication | Never red. Never success-green. |
| allowed next action | Ver bloqueios (critérios faltantes); Ver execução; Atualizar agora |
| prohibited implication | Failure; “falhou a validação”; profit delay narrative |
| screen-reader text | Ainda não pronto. Código NOT_READY. Não é uma falha. |

### READY

| Field | Value |
|-------|-------|
| primary label | Critérios operacionais atendidos |
| secondary technical label | `READY` |
| one-line explanation | O store atende os critérios de prontidão operacional. |
| expanded explanation | Exige revisão humana. Não autoriza `validate`, R4, R5 nem interpretação econômica. |
| recommended icon meaning | Ready check with explicit “operacional” qualifier |
| prohibited color implication | Green never means profitable or “validate now”. |
| allowed next action | Ver detalhes; Ver dados técnicos; (validate only as disabled explanation) |
| prohibited implication | Validate authorized; production ready; edge confirmed |
| screen-reader text | Pronto no sentido operacional. Código READY. Validação científica ainda não autorizada. |

### DEFERRED

| Field | Value |
|-------|-------|
| primary label | Adiado |
| secondary technical label | `DEFERRED` |
| one-line explanation | Dependência intencionalmente postergada e registrada. |
| expanded explanation | Ex.: `HOST_DISCOVERY=DEFERRED`. Não está concluído; não está esquecido. |
| recommended icon meaning | Pause / deferred queue |
| prohibited color implication | Must not look like SUCCESS/completed. |
| allowed next action | Ver detalhes; Ver histórico |
| prohibited implication | Host ready; activation complete |
| screen-reader text | Adiado. Código DEFERRED. Não concluído. |

### OPEN_DEBT

| Field | Value |
|-------|-------|
| primary label | Débito aberto |
| secondary technical label | `OPERATIONAL_DEBT=OPEN` |
| one-line explanation | Débito técnico-operacional aceito e ainda aberto. |
| expanded explanation | O projeto pode seguir em frentes não dependentes sem considerar ativação concluída. |
| recommended icon meaning | Open ledger / unfinished mark |
| prohibited color implication | Not completed-green; not hidden as NORMAL. |
| allowed next action | Ver detalhes; Ver bloqueios |
| prohibited implication | Scheduler active; operational validation complete |
| screen-reader text | Débito operacional aberto. Código OPERATIONAL_DEBT OPEN. Ativação não concluída. |

## Cross-status mapping (operational → UX)

| Runtime / domain signal | UX status family |
|-------------------------|------------------|
| Healthy cycle `COMPLETE` / `NO_NEW_DATA` | SUCCESS or NORMAL + INFORMATIONAL |
| `NOT_READY` / `WINDOW_DAYS_INSUFFICIENT` | NOT_READY (ATTENTION family) |
| Readiness `BLOCKED` / integrity | BLOCKED |
| Taxonomy `FAILED` categories | ERROR |
| `SKIPPED_LOCKED` expected | ATTENTION or INFORMATIONAL (not ERROR) |
| Scheduler not activated | DEFERRED / OPEN_DEBT / BLOCKED (activation) |
| Missing read API | UNAVAILABLE |
