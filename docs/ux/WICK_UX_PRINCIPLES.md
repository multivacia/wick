# WICK — Princípios de UX

```text
DOCUMENT = WICK_UX_PRINCIPLES
VERSION = 1.0.0
RELEASE = UX-R1
STATUS = ACTIVE
EFFECTIVE_AT = 2026-07-19T03:13:15Z
```

Qualquer alteração nestes princípios exige **nova versão** deste documento e registro no log de decisões de `docs/PROJECT.md`.

## Princípios

| ID | Princípio | Significado operacional |
|----|-----------|-------------------------|
| UX_PRINCIPLE_1 | Plain language first | A mensagem principal de cada tela usa linguagem cotidiana. |
| UX_PRINCIPLE_2 | Technical term always available | O termo técnico formal está sempre acessível (expansão, tooltip ou painel secundário). |
| UX_PRINCIPLE_3 | No trading-casino visual language | Proibido neon, ticker de preços, gauges decorativos e estética de home broker. |
| UX_PRINCIPLE_4 | Blocked does not mean failed | Bloqueio/prontidão incompleta é estado esperado, não erro. |
| UX_PRINCIPLE_5 | Every screen must show the next action | Cada tela indica a próxima ação segura (ou “nenhuma ação necessária”). |
| UX_PRINCIPLE_6 | Scientific state must never be hidden | Estado científico (gates, readiness, locks) permanece visível e auditável. |
| UX_PRINCIPLE_7 | Critical actions require explicit confirmation | Ações com efeito operacional ou científico exigem confirmação explícita. |
| UX_PRINCIPLE_8 | Mobile is a designed experience, not compressed desktop | Mobile tem IA própria; não é desktop encolhido. |
| UX_PRINCIPLE_9 | Accessibility and contrast are mandatory | Contraste, teclado, leitores de tela e motion reduzido são requisitos, não extras. |
| UX_PRINCIPLE_10 | Evidence and auditability are first-class UI elements | `run_id`, hashes, evidências e trilhas de auditoria são elementos de primeira classe. |

## Aplicação

- Violação de qualquer princípio bloqueia aceite de protótipo ou release UX.
- Em conflito entre clareza e jargão: priorizar clareza na camada primária e expor jargão na secundária.
- Em conflito entre estética e segurança científica: priorizar segurança científica.
