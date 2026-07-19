# Wick — Pacote de Especificações para Execução Autônoma

Este pacote consolida as decisões técnicas e metodológicas para o Cursor implementar o projeto Wick por releases, com autonomia alta dentro de cada release e interação humana apenas quando uma dúvida impedir a continuidade ou puder alterar regra de negócio, metodologia quantitativa, segurança, custos ou risco financeiro.

## Ordem recomendada

1. Ler `CLAUDE.md`.
2. Ler `docs/PROJECT.md`.
3. Ler os documentos de arquitetura.
4. Executar `prompts/PROMPT_BUILD_R1.md`.
5. Executar `prompts/PROMPT_AUDIT_R1.md`.
6. Corrigir achados críticos/altos.
7. Repetir para R2 e R3.
8. R4 e R5 só começam depois dos gates definidos.

## Regra de autonomia

O agente pode decidir sem interação humana:
- organização interna de módulos;
- nomes de funções privadas;
- helpers;
- refatorações locais;
- implementação de testes;
- correções de lint e formatação;
- escolhas técnicas equivalentes que não alterem comportamento.

O agente deve interromper e solicitar decisão humana quando:
- houver ambiguidade de regra de negócio;
- uma escolha puder alterar resultado quantitativo;
- a fonte não puder atender requisito obrigatório;
- for necessário apagar, recriar ou invalidar dados;
- houver risco de look-ahead ou vazamento temporal;
- custos, entrada, saída, short, amostra mínima ou gate precisarem mudar;
- alguma decisão envolver dinheiro real, corretora ou ordem;
- a implementação divergir estruturalmente das decisões registradas.

## Princípios inegociáveis

- Nenhum dinheiro real até R3 e R4 estarem concluídas e auditadas.
- Detectar padrão não é recomendar compra ou venda.
- Resultados devem ser auditáveis e reproduzíveis.
- Dados incompletos nunca podem ser tratados como completos.
- O conjunto final de teste não pode ser usado para calibração.
- A confirmação não pode usar informação futura para simular entrada anterior.
- Sinal bearish não equivale automaticamente a operação short executável.
- Um resultado inconclusivo é um resultado válido.

## Estrutura

- `CLAUDE.md`: regras operacionais permanentes para o agente.
- `docs/PROJECT.md`: visão, roadmap, decisões e gates.
- `docs/architecture`: dados, qualidade e metodologia quantitativa.
- `docs/patterns`: contrato matemático para detectores.
- `docs/releases`: especificações detalhadas R1–R5 e UX-R1.
- `docs/ux`: fundação de experiência (trilha paralela à ciência R3E).
- `docs/audits`: checklists independentes.
- `prompts`: prompts prontos para Cursor/Claude Code.
