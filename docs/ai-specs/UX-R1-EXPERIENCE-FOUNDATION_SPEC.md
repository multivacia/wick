# UX-R1 — Experience Foundation Specification

```text
RELEASE = UX-R1
RELEASE_NAME = WICK OPERATIONAL EXPERIENCE
BACKLOG_ITEM = UX-B1
TASK_ID = UX-RELEASE-FOUNDATION-001
PHASE = RELEASE_DEFINITION_AND_DESIGN_FOUNDATION
CHANGE_RISK = MEDIUM
IMPLEMENTATION_AUTHORIZED = false
UI_IMPLEMENTATION_AUTHORIZED = false
R3E_SCIENTIFIC_STATE_CHANGE = false
SPEC_VERSION = 1.0.0
CREATED_AT = 2026-07-19T03:13:15Z
```

## 1. Objetivo da release

Transformar o WICK em uma experiência operacional compreensível, segura e auditável para não-economistas, mantendo terminologia financeira/estatística/científica formal como camada explicativa secundária.

Esta release **não** altera o estado científico de R3E.

## 2. Personas

Ver `docs/ux/WICK_UX_PERSONAS.md`.

| ID | Nome |
|----|------|
| A | Usuário operacional |
| B | Stakeholder não-economista |
| C | Revisor técnico/científico |
| D | Administrador |

## 3. User journeys

### Journey 1 — Entender status atual

```text
Open WICK
→ Read plain-language global status
→ See technical state
→ Understand next required action
```

**Aceite:** usuário B explica o status e a próxima ação sem jargão obrigatório.

### Journey 2 — Investigar uma execução de coleta

```text
Open collection executions
→ Filter
→ Open run
→ Read outcome in plain language
→ Expand technical evidence
```

**Aceite:** usuário A/C localiza `run_id`, outcome e evidências.

### Journey 3 — Entender por que a validação está bloqueada

```text
Open readiness
→ See incomplete criteria
→ Understand 90-day requirement
→ See that blocked is not failure
```

**Aceite:** usuário B distingue “ainda não pronto / bloqueado” de “falhou”.

### Journey 4 — Preparar automação com segurança

```text
Open host and scheduler
→ See current host state
→ Follow activation stepper
→ Understand which gates remain
```

**Aceite:** usuário D vê gates restantes e não consegue “ativar” sem confirmação (quando UI existir).

### Journey 5 — Entender R3E sem background econômico

```text
Open experiment
→ Read experiment question
→ See current phase
→ Expand technical concepts
→ Confirm final result is not available yet
```

**Aceite:** usuário B resume a pergunta do experimento e afirma que não há conclusão econômica.

## 4. Inventário de páginas (MVP)

| Página | Objetivo |
|--------|----------|
| Visão Geral | Status + próxima ação + timeline recente |
| Execuções da Coleta | Lista/filtro/detalhe de ciclos |
| Prontidão | Progresso 90d + checklist + expansão técnica |
| Host e Automação | Host, scheduler, stepper, confirmações |
| Experimento R3E | Pergunta, fase, protocolo, glossário |

IA completa: `docs/ux/WICK_INFORMATION_ARCHITECTURE.md`.

## 5. Navegação

Desktop e mobile definidos em `docs/ux/WICK_INFORMATION_ARCHITECTURE.md`.

## 6. Terminologia

Duas camadas obrigatórias — guia completo em `docs/ux/WICK_UX_LANGUAGE_AND_TERMINOLOGY_GUIDE.md`.

Cobertura mínima: readiness, future-unseen data, window days, store observations, lock, run cycle, scheduler, backup, validation, holdout, walk-forward, bootstrap, FDR, economic interpretation, incident, operational health.

## 7. Regras visuais

`docs/ux/WICK_VISUAL_DIRECTION.md`

```text
70% operations center / 20% scientific lab / 10% institutional / 0% casino
```

Light primary; dark supported; azul petróleo + ciano discreto; semântica de status sem P&L.

## 8. Inventário de componentes (fundação → UX-B2)

| Componente | Uso inicial |
|------------|-------------|
| App shell | Sidebar/header/mobile nav |
| Status banner | Global + readiness |
| Status badge | READY / NOT_READY / BLOCKED / FAILED / N/A |
| Next-action card | Toda tela MVP |
| Summary card | Visão geral (somente se interação/resumo necessário) |
| Data table | Execuções |
| Alert / confirmation | Ações críticas |
| Progress (90d) | Prontidão |
| Stepper | Host/scheduler |
| Evidence panel | run_id, hashes, links |
| Glossary expand | Experimento R3E |
| Demo-data label | Fixtures |

## 9. Accessibility baseline

- WCAG 2.2 AA contraste mínimo
- Navegação completa por teclado
- Foco visível
- Nomes acessíveis em status (não só cor)
- Semântica de headings / landmarks
- Zoom até 200% sem perda de função crítica
- `prefers-reduced-motion`
- Rótulos em português claros; códigos técnicos em mono

Detalhamento e auditoria: UX-B10.

## 10. Responsive rules

| Breakpoint | Comportamento |
|------------|---------------|
| Desktop | Sidebar + conteúdo |
| Tablet | Sidebar colapsável ou rail |
| Mobile | Bottom nav (Início / Coleta / Prontidão / Operação / Mais) |

Mobile é experiência desenhada (princípio 8), não desktop comprimido.

## 11. Fronteira MVP

`docs/ux/UX-R1_BACKLOG.md`

REQUIRED: B1–B6, B9, B10; B11 antes do fechamento; B7/B8 opcionais após o core.

## 12. Critérios de aceite (UX-B1)

1. UX-R1 formalmente registrado (`docs/releases/UX-R1_SPEC.md`);
2. owner e status definidos;
3. princípios versionados;
4. personas documentadas;
5. language guide existe;
6. visual direction existe;
7. information architecture existe;
8. backlog completo existe;
9. MVP boundary explícita;
10. impact assessment existe;
11. UX spec existe (este documento);
12. nenhuma implementação de tela ocorreu;
13. estado científico permanece inalterado;
14. revisão independente completa.

## 13. Padrões proibidos

```text
Neon / flashing prices / market ticker
Decorative gauges
Green/red profit-loss semantics
Fabricated scientific results as real
Fake profit / invented model performance as real
Implying readiness, scheduler activation, or validate execution
Hiding scientific state
Treating BLOCKED/NOT_READY as FAILED
Trading-casino copy or visuals
Real-money / broker integration UI
```

## 14. Fora de escopo desta tarefa

- Implementação de frontend/UI
- Design system tokens em código
- Alteração de código Python/R3E
- Execução de collect/validate/readiness
- Ativação de scheduler
- Mudança de gates R3E/R4/R5
