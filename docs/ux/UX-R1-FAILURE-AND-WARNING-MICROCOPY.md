# WICK — UX-R1 Failure and Warning Microcopy

```text
DOCUMENT = UX-R1-FAILURE-AND-WARNING-MICROCOPY
VERSION = 1.0.0
RELEASE = UX-R1
BACKLOG_ITEM = UX-B4
TASK_ID = OPERATIONAL-LANGUAGE-MICROCOPY-001
STATUS = ACTIVE
LOCALE = pt-BR
SOURCE_TAXONOMY = docs/operations/R3E_FUTURE_UNSEEN_FAILURE_TAXONOMY.md
UI_IMPLEMENTATION_AUTHORIZED = false
EFFECTIVE_AT = 2026-07-19T13:26:43Z
VALIDATE_AUTHORIZED = false
```

## Distinction rules

| Kind | UX treatment |
|------|----------------|
| Warning / attention | Amber family; not ERROR |
| Expected `NOT_READY` | NOT_READY; not failure |
| Expected lock skip | ATTENTION/INFO; not failure |
| Real operational failure | ERROR; red allowed |
| Integrity critical | ERROR/BLOCKED; freeze guidance; no validate |

Do not recommend retry when retry could worsen the condition.

Global invariants (unchanged):

```text
NO_CATEGORY_AUTHORIZES_VALIDATE = true
NO_CATEGORY_AUTHORIZES_EFFECT_PEEKING = true
NO_CATEGORY_AUTHORIZES_ECONOMIC_INTERPRETATION = true
NO_CATEGORY_UNBLOCKS_R4_OR_R5 = true
SCHEDULER_ACTIVATION_AUTHORIZED = false
```

## Failure category microcopy

### CONFIGURATION_MISSING

| Field | Value |
|-------|-------|
| failure code | `CONFIGURATION_MISSING` |
| plain-language title | Configuração ausente |
| plain-language explanation | Falta configuração necessária para o ciclo. |
| technical detail | Exit family CONFIG (10); não retentável até o operador fornecer config. |
| likely impact | Ciclos não avançam de forma segura. |
| safe next step | Criar config a partir dos exemplos; não inventar valores de host. |
| retry guidance | Não retentar até a config existir. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | env/config examples, preflight logs, `run_id` |

### CONFIGURATION_INVALID

| Field | Value |
|-------|-------|
| failure code | `CONFIGURATION_INVALID` |
| plain-language title | Configuração inválida |
| plain-language explanation | Há chaves, caminhos ou tipos inválidos. |
| technical detail | Exit family CONFIG (11). |
| likely impact | Fail-closed até correção. |
| safe next step | Corrigir config; reexecutar preflight. |
| retry guidance | Não retentar em loop automático sem correção. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | preflight report, config validation errors |

### NETWORK_UNAVAILABLE

| Field | Value |
|-------|-------|
| failure code | `NETWORK_UNAVAILABLE` |
| plain-language title | Rede indisponível |
| plain-language explanation | Não foi possível alcançar o provedor de dados. |
| technical detail | PROVIDER (30); retentável. |
| likely impact | Ciclo sem dados novos; store intacto se não houve escrita parcial insegura. |
| safe next step | Verificar conectividade; aguardar próximo ciclo. |
| retry guidance | Retry permitido no próximo ciclo. |
| escalation guidance | Alerta após ciclos repetidos. |
| evidence to inspect | provider logs, network error, `run_id` |

### PROVIDER_AUTHENTICATION_FAILED

| Field | Value |
|-------|-------|
| failure code | `PROVIDER_AUTHENTICATION_FAILED` |
| plain-language title | Autenticação do provedor falhou |
| plain-language explanation | Credenciais do provedor estão ausentes ou inválidas. |
| technical detail | PROVIDER (31); não retentável até reparo. |
| likely impact | Coleta bloqueada sem novos dados. |
| safe next step | Rotacionar/reparar credenciais fora do git; nunca commitar segredos. |
| retry guidance | Não retentar até credenciais corrigidas. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | auth error (redacted), secret presence check (not values) |

### PROVIDER_RATE_LIMITED

| Field | Value |
|-------|-------|
| failure code | `PROVIDER_RATE_LIMITED` |
| plain-language title | Limite de taxa do provedor |
| plain-language explanation | O provedor limitou temporariamente as chamadas. |
| technical detail | PROVIDER (32); retry com backoff. |
| likely impact | Atraso na coleta. |
| safe next step | Reduzir cadência ou aguardar. |
| retry guidance | Retry com backoff; evitar martelar a API. |
| escalation guidance | Opcional salvo persistência. |
| evidence to inspect | rate-limit headers/logs, cadence config |

### PROVIDER_DATA_UNAVAILABLE

| Field | Value |
|-------|-------|
| failure code | `PROVIDER_DATA_UNAVAILABLE` |
| plain-language title | Dados do provedor indisponíveis |
| plain-language explanation | O provedor não entregou dados utilizáveis agora. |
| technical detail | PROVIDER (33); retentável. |
| likely impact | Sem novas observações neste ciclo. |
| safe next step | Confirmar feriado/outage; manter política de coleta. |
| retry guidance | Retry no próximo ciclo. |
| escalation guidance | Alerta após repetições. |
| evidence to inspect | provider response metadata, series keys |

### STORE_NOT_WRITABLE

| Field | Value |
|-------|-------|
| failure code | `STORE_NOT_WRITABLE` |
| plain-language title | Armazenamento sem permissão de escrita |
| plain-language explanation | O store oficial não aceita gravação. |
| technical detail | STORAGE (20); crítico operacional. |
| likely impact | Ciclos fail-closed; risco de atraso de cobertura. |
| safe next step | Corrigir ownership/permissões/mount; preservar store existente. |
| retry guidance | Não retentar writes até permissão corrigida. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | path permissions, mount status, store path |

### STORE_CORRUPTION_SUSPECTED

| Field | Value |
|-------|-------|
| failure code | `STORE_CORRUPTION_SUSPECTED` |
| plain-language title | Suspeita de corrupção no armazenamento |
| plain-language explanation | Integridade do store está sob suspeita. |
| technical detail | STORAGE (21); não retentável; stop. |
| likely impact | Congelar writes; validação científica proibida. |
| safe next step | Preservar evidências; checar hash/manifest; restore só com autorização humana. |
| retry guidance | Não retentar coleta/escrita. |
| escalation guidance | Alerta imediato. |
| evidence to inspect | manifests, hashes, last good backup |

### DISK_SPACE_LOW

| Field | Value |
|-------|-------|
| failure code | `DISK_SPACE_LOW` |
| plain-language title | Pouco espaço em disco |
| plain-language explanation | O disco está abaixo do limiar seguro. |
| technical detail | STORAGE (22). |
| likely impact | Fail-closed até recuperar espaço. |
| safe next step | Liberar espaço com retention dry-run primeiro; nunca apagar último backup válido nem observações do store. |
| retry guidance | Não retentar até espaço recuperado. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | disk usage, retention dry-run report |

### LOCK_ACTIVE

| Field | Value |
|-------|-------|
| failure code | `LOCK_ACTIVE` |
| plain-language title | Travamento ativo |
| plain-language explanation | Outro ciclo mantém o lock; este ciclo foi ignorado com segurança. |
| technical detail | `SKIPPED_LOCKED` (4) / LOCK (40); severidade baixa. |
| likely impact | Um ciclo pulado; geralmente esperado. |
| safe next step | Confirmar sobreposição esperada; não forçar unlock. |
| retry guidance | Próximo ciclo ok; não force-unlock. |
| escalation guidance | Opcional salvo prolongado. |
| evidence to inspect | lock-status, owner pid, `run_id` ativo |

### LOCK_STALE

| Field | Value |
|-------|-------|
| failure code | `LOCK_STALE` |
| plain-language title | Travamento obsoleto |
| plain-language explanation | Há indício de lock órfão/stale. |
| technical detail | LOCK (41); remoção só com autorização humana. |
| likely impact | Ciclos podem ficar presos até recuperação segura. |
| safe next step | Rodar diagnóstico `lock-status`; remoção humana se owner morto. |
| retry guidance | Automação pode recuperar na aquisição; diagnóstico nunca apaga sozinho. |
| escalation guidance | Obrigatório se repetido. |
| evidence to inspect | lock file metadata, process liveness |

### BACKUP_FAILED

| Field | Value |
|-------|-------|
| failure code | `BACKUP_FAILED` |
| plain-language title | Falha na cópia de segurança |
| plain-language explanation | O backup não completou com verificação ok. |
| technical detail | STORAGE (23). |
| likely impact | Ativação de scheduler permanece fail-closed; coleta só se store saudável. |
| safe next step | Inspecionar logs de backup e disco; não ativar scheduler. |
| retry guidance | Retry após causa-raiz corrigida. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | backup logs, verification state |

### READINESS_NOT_READY

| Field | Value |
|-------|-------|
| failure code | `READINESS_NOT_READY` |
| plain-language title | Prontidão ainda não alcançada |
| plain-language explanation | Critérios de prontidão ainda não foram atendidos. |
| technical detail | Severidade INFO; exit OK (0) se o ciclo estiver saudável. **Não é falha.** |
| likely impact | Validação científica permanece não autorizada. |
| safe next step | Continuar coleta autorizada; não interpretar como liberação científica. |
| retry guidance | N/A como falha; continuar acumulação. |
| escalation guidance | Sem alerta de falha. |
| evidence to inspect | readiness report, `WINDOW_DAYS`, series counts |

### READINESS_TRANSITION_READY

| Field | Value |
|-------|-------|
| failure code | `READINESS_TRANSITION_READY` |
| plain-language title | Transição operacional para READY |
| plain-language explanation | A prontidão operacional passou a READY. Isso exige revisão humana. |
| technical detail | Milestone operacional; exit OK (0); **não** autoriza validate. |
| likely impact | Notificação operacional; estado científico inalterado. |
| safe next step | Emitir notificação contratual; revisão humana; não rodar validate. |
| retry guidance | N/A. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | readiness transition notification, readiness report |

### UNEXPECTED_EXCEPTION

| Field | Value |
|-------|-------|
| failure code | `UNEXPECTED_EXCEPTION` |
| plain-language title | Exceção inesperada |
| plain-language explanation | Ocorreu um erro não classificado previamente. |
| technical detail | UNEXPECTED (90) / FAILED (1). |
| likely impact | Depende do ponto de falha; preservar evidências. |
| safe next step | Preservar logs/`run` dir; classificar; escalar se desconhecido. |
| retry guidance | Condicional; parar se houver risco ao store. |
| escalation guidance | Alerta humano obrigatório. |
| evidence to inspect | stack traces (sanitized), run directory, store health |

## Warning-only microcopy (non-failure)

| Warning code | Plain title | Plain explanation | Safe next step |
|--------------|-------------|-------------------|----------------|
| `WINDOW_DAYS_INSUFFICIENT` | Janela ainda insuficiente | Ainda faltam dias após o cutoff. | Continuar coleta; não validar |
| `SERIES_INSUFFICIENT` | Séries incompletas | Menos séries completas que o mínimo. | Continuar coleta; ver cobertura |
| `BARS_INSUFFICIENT` | Barras insuficientes | Séries parciais abaixo do mínimo de barras. | Continuar coleta |
| `NO_OBSERVATIONS` | Sem observações | Store sem observações aceitas. | Verificar coleta/config |
| `DATA_STALE` | Dados desatualizados | Última observação mais antiga que o esperado. | Ver última execução; não inventar barras |
| `GAPS_PRESENT` | Lacunas presentes | Há buracos temporais nas séries. | Inspecionar cobertura; sem fill artificial |
| `COVERAGE_INSUFFICIENT` | Cobertura insuficiente | Cobertura abaixo do critério operacional. | Ver séries faltantes |
| `OPEN_DEBT` | Débito operacional aberto | Dependências adiadas registradas. | Ver Host; não tratar como concluído |
| `SCHEDULER_INACTIVE` | Agendamento inativo | Timer não ativado. | Manter execução manual autorizada apenas |

## Readiness language (blocking vs not)

| Code | What happened | Why it matters | Blocking? | Remains safe | Remains unauthorized |
|------|---------------|----------------|-----------|--------------|----------------------|
| `WINDOW_DAYS_INSUFFICIENT` | Janela < mínima | Validação precoce seria inválida | NOT_READY (not ERROR) | Continuar coleta | validate, economic claims |
| `SERIES_INCOMPLETE` / `SERIES_INSUFFICIENT` | Séries incompletas | Cobertura insuficiente | NOT_READY | Monitorar séries | validate |
| `COVERAGE_INSUFFICIENT` | Cobertura baixa | Amostra operacional incompleta | NOT_READY / ATTENTION | Inspeção | validate |
| `DATA_STALE` | Dados velhos | Operação pode estar parada | ATTENTION | Diagnóstico | fingir freshness |
| `GAPS_PRESENT` | Lacunas | Qualidade temporal | ATTENTION / NOT_READY | Inspeção | fill artificial |
| `DUPLICATES_PRESENT` | Duplicatas | Integridade | BLOCKED | Freeze writes / inspect | validate |
| `STORE_INTEGRITY_FAILURE` | Integridade falhou | Store não confiável | BLOCKED/ERROR | Preserve evidence | validate, unsafe restore |
| `READY` | Critérios ok | Milestone operacional | No (ready) | Human review | validate until explicit auth |
