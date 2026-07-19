# WICK — Personas UX

```text
DOCUMENT = WICK_UX_PERSONAS
VERSION = 1.0.0
RELEASE = UX-R1
STATUS = ACTIVE
EFFECTIVE_AT = 2026-07-19T03:13:15Z
```

## Persona A — Usuário operacional

**Quem:** operador que mantém a coleta e a infraestrutura rodando.

**Precisa saber:**

- se a coleta está funcionando;
- qual ação está pendente;
- se há incidente;
- se a automação está ativa;
- o que pode ser feito com segurança.

**Não precisa:** interpretar edge econômico ou estatística avançada.

**Jornadas principais:** 1 (status), 2 (execução), 4 (automação).

---

## Persona B — Stakeholder não-economista

**Quem:** patrocinador, gestor ou interessado sem formação quantitativa.

**Precisa entender:**

- o que o experimento está perguntando;
- por que a validação está bloqueada;
- quanto de dados ainda falta;
- o significado dos termos em linguagem simples;
- que nenhum resultado está sendo escondido ou interpretado cedo demais.

**Não precisa:** operar o host ou ler logs brutos (pode expandir se quiser).

**Jornadas principais:** 1 (status), 3 (prontidão), 5 (experimento R3E).

---

## Persona C — Revisor técnico/científico

**Quem:** auditor, quant ou revisor de protocolo.

**Precisa de:**

- status técnico exato;
- `run_id`s;
- evidências;
- hashes;
- motivo de readiness;
- estado do protocolo;
- trilha de auditoria.

**Não aceita:** eufemismos que ocultem estado científico ou fixtures apresentados como resultado real.

**Jornadas principais:** 2 (execução), 3 (prontidão), 5 (experimento).

---

## Persona D — Administrador

**Quem:** responsável por host, permissões e ativação operacional.

**Precisa de:**

- host;
- scheduler;
- backups;
- incidentes;
- permissões;
- gates de ativação.

**Não deve:** ativar scheduler ou validate sem confirmação e gates explícitos.

**Jornadas principais:** 4 (automação), operação/backups/incidentes (pós-MVP core).

## Matriz resumida

| Necessidade | A | B | C | D |
|-------------|---|---|---|---|
| Status em linguagem simples | ● | ● | ○ | ○ |
| Termo técnico / evidência | ○ | ○ | ● | ○ |
| Próxima ação segura | ● | ● | ○ | ● |
| Host / scheduler / backup | ○ | — | ○ | ● |
| Explicação do experimento | ○ | ● | ● | ○ |
