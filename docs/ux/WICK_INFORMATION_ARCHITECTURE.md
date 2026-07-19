# WICK — Arquitetura de Informação

```text
DOCUMENT = WICK_INFORMATION_ARCHITECTURE
VERSION = 1.0.0
RELEASE = UX-R1
STATUS = ACTIVE
EFFECTIVE_AT = 2026-07-19T03:13:15Z
```

## Navegação desktop

```text
WICK
├── Visão Geral
├── Coleta Futura
│   ├── Execuções
│   ├── Dados Coletados
│   └── Prontidão
├── Operação
│   ├── Host e Automação
│   ├── Backups
│   └── Incidentes
├── Experimentos
│   └── R3E
└── Governança
    ├── Backlog
    ├── Aprovações
    └── Evidências
```

## Navegação mobile

```text
Início
Coleta
Prontidão
Operação
Mais
```

### Mapeamento mobile → desktop

| Aba mobile | Destinos |
|------------|----------|
| Início | Visão Geral |
| Coleta | Execuções (+ Dados Coletados via subnavegação) |
| Prontidão | Prontidão |
| Operação | Host e Automação (Backups/Incidentes em “Mais” se fora do MVP) |
| Mais | Experimentos, Governança, tema, ajuda |

## Inventário de páginas (MVP UX-R1)

| # | Página | Persona primária | Objetivo único |
|---|--------|------------------|----------------|
| 1 | Visão Geral | A, B | Status global + próxima ação |
| 2 | Execuções da Coleta | A, C | Investigar ciclos e evidências |
| 3 | Prontidão | B, C | Entender por que validação está bloqueada/não pronta |
| 4 | Host e Automação | A, D | Preparar automação com segurança |
| 5 | Experimento R3E | B, C | Explicar o experimento sem economia prematura |

Páginas fora do MVP inicial (backlog posterior): Dados Coletados, Backups, Incidentes, Governança completa.

## Elementos globais (shell)

- Marca WICK + contexto da release/experimento
- Status global em linguagem simples + código técnico
- Indicador de automação (ativa / não ativa)
- Acesso a evidências recentes
- Seletor de tema (claro/escuro)
- Em mobile: bottom nav das 5 abas

## Regras de IA

1. Cada tela tem **um** objetivo principal.
2. Toda tela mostra **próxima ação** (ou ausência segura de ação).
3. Estado científico nunca fica só no menu; aparece no conteúdo.
4. Bloqueado ≠ falha (rótulos e cores distintos).
5. Dados de demonstração sempre rotulados `DEMONSTRATION DATA`.
6. Nenhuma página de P&L, ordens ou paper trading nesta release.

## Jornadas (resumo)

Ver `docs/ai-specs/UX-R1-EXPERIENCE-FOUNDATION_SPEC.md` § User journeys.

| ID | Nome | Entrada → Saída |
|----|------|-----------------|
| J1 | Entender status atual | Visão Geral → próxima ação clara |
| J2 | Investigar execução | Execuções → evidência técnica |
| J3 | Entender bloqueio de validação | Prontidão → critérios incompletos sem alarmismo |
| J4 | Preparar automação | Host → stepper + gates restantes |
| J5 | Entender R3E | Experimento → pergunta + fase + sem resultado econômico |
