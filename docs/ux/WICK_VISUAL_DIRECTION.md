# WICK — Direção Visual

```text
DOCUMENT = WICK_VISUAL_DIRECTION
VERSION = 1.0.0
RELEASE = UX-R1
STATUS = ACTIVE
EFFECTIVE_AT = 2026-07-19T03:13:15Z
```

## Posicionamento

```text
70_PERCENT = operations center
20_PERCENT = scientific laboratory
10_PERCENT = institutional financial product
0_PERCENT = casino or home broker
```

Leitura: a interface deve parecer um **centro de operações** com disciplina de laboratório científico e um toque institucional discreto. Nunca um terminal de trading especulativo.

## Temas

| Tema | Papel |
|------|-------|
| Light | Primário (default) |
| Dark | Suportado (paridade funcional, não “modo gamer”) |

## Paleta semântica

| Uso | Direção | Notas |
|-----|---------|-------|
| Institucional | Azul profundo / azul petróleo | Cor de marca e navegação |
| Destaque discreto | Ciano discreto | Links, foco, destaques não alarmistas |
| Concluído / saudável | Verde moderado | Conclusão operacional — **não** lucro |
| Atenção / não pronto | Âmbar | `NOT_READY`, atenção sem falha |
| Bloqueado | Roxo discreto ou cinza forte | Bloqueio de protocolo/gate |
| Falha real | Vermelho | Somente falha operacional/científica real |
| Indisponível / N/A | Cinza | Ausência ou não aplicável |

### Tokens nominais (fundação; valores finais no UX-B2)

```text
color.brand.petroleum
color.accent.cyan
color.status.complete
color.status.attention
color.status.blocked
color.status.failure
color.status.unavailable
color.surface.canvas
color.surface.panel
color.text.primary
color.text.secondary
color.border.subtle
```

## Tipografia

- Primária: tipografia legível de produto/operações (sem Inter/Roboto/Arial como default de marca).
- Secundária/técnica: monoespacada para `run_id`, hashes, códigos de status.
- Hierarquia clara: título de página → status em linguagem simples → detalhe técnico.

## Densidade e layout

- Densidade operacional média: tabelas legíveis, não dashboards congestionados.
- Uma composição por viewport principal; evitar “painel de widgets”.
- Evidências e auditoria têm espaço próprio (não escondidas em rodapé).

## Proibições visuais

```text
neon
preços piscando
estética de market-ticker
gauges decorativos
semântica verde/vermelho de lucro/prejuízo
badges flutuantes de “hot/profit”
cards decorativos sem função interativa na hero
efeitos glow agressivos
```

## Estados visuais (mapeamento)

| Estado | Cor | Ícone/linguagem |
|--------|-----|-----------------|
| Complete / healthy | Verde moderado | Neutro, sem confetti |
| Attention / not ready | Âmbar | “Atenção” / “Ainda não” |
| Blocked | Roxo/cinza forte | “Bloqueado” ≠ “Falhou” |
| Failed | Vermelho | Somente falha real |
| Unavailable | Cinza | “Indisponível” |

## Acessibilidade visual (baseline)

- Contraste WCAG AA mínimo em texto e componentes de status.
- Nunca transmitir status só por cor; sempre texto + (quando útil) ícone.
- Suportar `prefers-reduced-motion`.
- Foco de teclado sempre visível.
