# Papéis e Responsabilidades

## 1. Humano responsável

Responsabilidades:

- aprovar especificações;
- aprovar análises de impacto HIGH/CRITICAL;
- autorizar `IMPLEMENTATION_AUTHORIZED` quando exigido;
- autorizar ações sensíveis;
- decidir merge;
- decidir execução científica;
- resolver conflitos de prioridade;
- assumir a decisão final sobre gates.

A IA não substitui essa autoridade.

## 2. Agente especificador

Responsabilidades:

- analisar contexto;
- definir escopo e não escopo;
- criar critérios de aceite;
- registrar riscos e `CHANGE_RISK` preliminar;
- gerar prompt de implementação somente após impacto aprovado;
- manter as restrições científicas explícitas.

Não deve aprovar automaticamente a própria especificação.

## 2.1 Agente de análise de impacto

Responsabilidades:

- produzir `docs/ai-impact/<TASK_ID>_IMPACT_ASSESSMENT.md` quando exigido;
- mapear componentes, contratos, persistência, concorrência, rollback e testes;
- manter `IMPLEMENTATION_AUTHORIZED = false` até aprovação;
- bloquear (`BLOCKED`) se houver ambiguidade material.

Não deve implementar código nesta fase.

## 3. Agente executor

Exemplos: Cursor, Codex.

Responsabilidades:

- confirmar impacto aprovado antes de codificar (MEDIUM+);
- implementar apenas o escopo aprovado;
- trabalhar em branch dedicada;
- executar testes;
- produzir relatório;
- abrir PR draft;
- parar antes do merge.

Não pode reescrever a especificação ou o impacto para acomodar a implementação.

## 4. Agente revisor

Responsabilidades:

- revisar diff e evidências;
- comparar implementação com especificação **e** impacto aprovado;
- verificar se o desenho aprovado foi seguido;
- verificar testes e CI;
- procurar violações de guardrails;
- emitir decisão fundamentada.

Idealmente, não deve ser o mesmo agente executor.

## 5. CI

Responsabilidades:

- executar verificações automatizadas;
- fornecer evidência objetiva;
- bloquear regressões detectáveis.

CI verde não equivale, sozinho, a aprovação técnica ou científica.

## 6. GitHub

Responsabilidades:

- manter histórico;
- registrar commits;
- armazenar PRs e discussões;
- preservar trilha de auditoria.

## 7. Matriz de autoridade

| Ação | Especificador | Analista de impacto | Executor | Revisor | Humano |
|---|---:|---:|---:|---:|---:|
| Criar spec | Sim | Pode | Não | Pode sugerir | Aprova |
| Criar impacto | Pode | Sim | Não | Pode revisar | Aprova HIGH/CRITICAL |
| Autorizar implementação | Não | Recomenda | Não | Pode | Decide |
| Implementar | Não recomendado | Não | Sim | Não | Pode |
| Executar testes | Pode | Pode | Sim | Pode | Pode |
| Abrir PR draft | Pode | Não (impacto-only) | Sim | Pode | Pode |
| Aprovar revisão | Não sozinho | Não | Não | Sim | Sim |
| Fazer merge | Não | Não | Não | Não | Sim |
| Executar validate | Não | Não | Não | Não | Sim, com autorização explícita |
| Alterar gate científico | Não | Não | Não | Recomenda | Decide |
