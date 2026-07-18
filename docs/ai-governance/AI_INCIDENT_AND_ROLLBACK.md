# Incidentes, Contenção e Rollback

## 1. Quando declarar incidente

Declarar incidente quando uma IA:

- altera arquivos fora do escopo;
- executa comando proibido;
- consulta efeito científico indevidamente;
- faz push ou merge não autorizado;
- sobrescreve dados;
- remove testes;
- introduz segredo;
- muda cutoff, freeze ou thresholds sem aprovação;
- implementa código MEDIUM/HIGH/CRITICAL sem impacto aprovado;
- declara `IMPLEMENTATION_AUTHORIZED=true` sem aprovação do impacto;
- declara conclusão com evidência falsa ou inexistente.

## 2. Contenção imediata

1. interromper novas ações;
2. não tentar “corrigir rápido” sem diagnóstico;
3. preservar logs e commits;
4. bloquear merge;
5. registrar branch, commit e comandos executados;
6. avaliar impacto científico e operacional.

## 3. Classificação

```text
SEVERITY_1 = documentação ou alteração local sem efeito
SEVERITY_2 = branch ou PR incorreta, sem merge
SEVERITY_3 = merge ou dados alterados, reversível
SEVERITY_4 = quebra científica, perda de dados ou exposição de segredo
```

## 4. Rollback

O rollback deve preferir:

- revert explícito;
- restauração de artefato versionado;
- branch corretiva;
- preservação do histórico.

Evitar:

- force-push;
- rebase destrutivo;
- exclusão de evidências.

## 5. Incidente científico

Se houver peeking ou execução indevida de validação:

```text
EFFECT_PEEKING_PERFORMED = true
SCIENTIFIC_REVIEW_REQUIRED = true
R3E_GATE = BLOCKED_PENDING_INCIDENT_REVIEW
```

A validade da amostra deve ser reavaliada formalmente.

## 6. Relatório mínimo

```text
INCIDENT_ID =
DETECTED_AT =
BRANCH =
COMMIT =
ACTION =
IMPACT =
CONTAINMENT =
ROLLBACK =
SCIENTIFIC_IMPACT =
FOLLOW_UP =
```
