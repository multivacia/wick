# Governança de IA do Wick

Este diretório define as regras permanentes para uso de agentes de IA no projeto Wick.

As regras se aplicam a ChatGPT, Codex, Cursor, GitHub Copilot e qualquer outro agente capaz de analisar, editar, testar, versionar ou revisar o repositório.

## Objetivos

- reduzir risco de alterações incorretas ou não auditáveis;
- separar especificação, implementação, revisão e autorização;
- preservar a integridade científica do Wick;
- impedir ações destrutivas ou irreversíveis sem autorização humana;
- criar uma trilha objetiva de evidências para cada mudança.

## Documentos obrigatórios

1. `AI_AGENT_GUARDRAILS.md`
   Regras gerais e ações proibidas.

2. `AI_CHANGE_WORKFLOW.md`
   Fluxo oficial para especificar, implementar, revisar e aprovar mudanças.

3. `AI_SCIENTIFIC_SAFETY_RULES.md`
   Regras especiais para experimentos, gates, dados future unseen e interpretação econômica.

4. `AI_REVIEW_CHECKLIST.md`
   Checklist mínimo para revisão de qualquer implementação feita por IA.

5. `AI_ROLES_AND_RESPONSIBILITIES.md`
   Responsabilidades de cada participante do fluxo.

6. `AI_INCIDENT_AND_ROLLBACK.md`
   Procedimento para falhas, comportamento inesperado e reversão.

7. `AI_REVIEW_IDENTITY_AND_RECONCILIATION.md`
   Identidade Git obrigatória, validade por HEAD e reconciliação de tip.

Enforcement offline: `scripts/validate_ai_governance_artifacts.py`.

## Regra soberana

Nenhuma IA possui autoridade final para alterar o estado oficial do projeto.

A autoridade final para merge, execução científica sensível e mudança de gate permanece humana.
