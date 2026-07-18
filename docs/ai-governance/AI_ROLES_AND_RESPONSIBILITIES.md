# Papéis e Responsabilidades

## 1. Humano responsável

Responsabilidades:

- aprovar especificações;
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
- registrar riscos;
- gerar prompt de implementação;
- manter as restrições científicas explícitas.

Não deve aprovar automaticamente a própria especificação.

## 3. Agente executor

Exemplos: Cursor, Codex.

Responsabilidades:

- implementar apenas o escopo aprovado;
- trabalhar em branch dedicada;
- executar testes;
- produzir relatório;
- abrir PR draft;
- parar antes do merge.

Não pode reescrever a especificação para acomodar a implementação.

## 4. Agente revisor

Responsabilidades:

- revisar diff e evidências;
- comparar implementação com especificação;
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

| Ação | Especificador | Executor | Revisor | Humano |
|---|---:|---:|---:|---:|
| Criar spec | Sim | Não | Pode sugerir | Aprova |
| Implementar | Não recomendado | Sim | Não | Pode |
| Executar testes | Pode | Sim | Pode | Pode |
| Abrir PR draft | Pode | Sim | Pode | Pode |
| Aprovar revisão | Não sozinho | Não | Sim | Sim |
| Fazer merge | Não | Não | Não | Sim |
| Executar validate | Não | Não | Não | Sim, com autorização explícita |
| Alterar gate científico | Não | Não | Recomenda | Decide |
