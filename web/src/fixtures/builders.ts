/**
 * Internal helpers for building I6B domain inputs inside fixtures.
 * Fixed ISO timestamps only — no Date.now / Math.random.
 */

import type {
  CollectionRunInput,
  HostDiscoveryInput,
  OptionalIsoTimestamp,
  OptionalMetric,
  ReadinessAssessmentInput,
  R3eExperimentDomainInput,
  SchedulerStateInput,
  ValueAvailability,
} from "../viewmodels/index.js";

export function emptyMetric(): OptionalMetric {
  return { value: null, availability: "not_supplied" };
}

export function metric(value: number): OptionalMetric {
  return { value, availability: "available" };
}

export function ts(
  iso: string | null,
  availability: ValueAvailability = iso ? "available" : "not_supplied",
): OptionalIsoTimestamp {
  return { iso, availability };
}

export function run(
  overrides: Partial<CollectionRunInput> = {},
): CollectionRunInput {
  return {
    runId: "fx-run-1",
    state: "complete",
    startedAt: ts("2026-07-18T10:00:00.000Z"),
    finishedAt: ts("2026-07-18T11:00:00.000Z"),
    resultLabel: "accepted",
    acceptedCount: metric(10),
    rejectedCount: metric(1),
    storeBeforeCount: metric(100),
    storeAfterCount: metric(110),
    idempotencyResult: "applied",
    failureReason: null,
    failureReasonCode: null,
    evidence: [
      {
        label: "synthetic run log",
        reference: "fixtures/runs/fx-run-1",
        kind: "path",
      },
    ],
    ...overrides,
  };
}

export function readiness(
  overrides: Partial<ReadinessAssessmentInput> = {},
): ReadinessAssessmentInput {
  return {
    state: "not_ready",
    windowDays: metric(3),
    requiredWindowDays: metric(14),
    blockingReasonCodes: ["WINDOW_DAYS_INSUFFICIENT"],
    validationAuthorized: false,
    validationCommandExecuted: false,
    effectPeekingPerformed: false,
    explanationPlainLanguage: null,
    evidence: [],
    ...overrides,
  };
}

export function host(
  overrides: Partial<HostDiscoveryInput> = {},
): HostDiscoveryInput {
  return {
    state: "deferred",
    persistentHostPresent: null,
    discoveryNote: null,
    evidence: [],
    ...overrides,
  };
}

export function scheduler(
  overrides: Partial<SchedulerStateInput> = {},
): SchedulerStateInput {
  return {
    registered: false,
    active: false,
    activationAuthorized: false,
    state: "blocked",
    lastCycleState: "not_started",
    lastCycleAt: ts(null),
    operationalDebt: "open",
    evidence: [],
    ...overrides,
  };
}

/**
 * Dedicated explanatory R3E fixture defaults — synthetic / illustrative only.
 * No fabricated p-values, returns, or future-unseen outcomes.
 */
export function r3eExperiment(
  overrides: Partial<R3eExperimentDomainInput> = {},
): R3eExperimentDomainInput {
  return {
    experimentId: "R3E-CONTEXTUAL-EDGE-V1",
    parentExperimentId: "R3D-V1",
    title: "Experimento R3E",
    purpose:
      "Avaliar, de forma exploratória e auditável, se contexto de mercado e padrões de candle acrescentam valor incremental — sem declarar vantagem comprovada nem liberar dinheiro real.",
    hypothesis:
      "Hipótese principal (H2): o modelo contextual acrescido de padrão de candle (M5) supera o mesmo modelo sem candle (M4) de forma estável fora da amostra. Isso ainda não foi validado em dados futuros não vistos.",
    protocolVersion: "R3E_CONTEXTUAL_EDGE_SPECIFICATION",
    modelFamilies: [
      "baseline aleatório pareado",
      "contexto de mercado",
      "contexto + padrão de candle",
    ],
    modelStages: [
      {
        id: "M0",
        plainLanguage:
          "M0 é o baseline aleatório pareado — um ponto de comparação sem sinal estruturado.",
        technicalDefinition: "M0 = baseline aleatório pareado",
      },
      {
        id: "M1",
        plainLanguage:
          "M1 usa apenas tendência — direção e força do movimento recente.",
        technicalDefinition: "M1 = tendência",
      },
      {
        id: "M2",
        plainLanguage:
          "M2 combina tendência com volume — intensidade relativa das negociações.",
        technicalDefinition: "M2 = tendência + volume",
      },
      {
        id: "M3",
        plainLanguage:
          "M3 acrescenta volatilidade — o quão amplos estão os movimentos.",
        technicalDefinition: "M3 = tendência + volume + volatilidade",
      },
      {
        id: "M4",
        plainLanguage:
          "M4 é o melhor modelo contextual sem candle: tendência, volume, volatilidade e posição no range.",
        technicalDefinition:
          "M4 = tendência + volume + volatilidade + posição no range",
      },
      {
        id: "M5",
        plainLanguage:
          "M5 é M4 mais o padrão de candle — usado só para medir o incremento do candle.",
        technicalDefinition: "M5 = M4 + padrão de candle",
      },
    ],
    deltaCandleDefinition:
      "DELTA_CANDLE = M5 − M4. Em linguagem simples: é a diferença entre o modelo com candle e o mesmo modelo sem candle. A definição não afirma significância estatística nem lucratividade.",
    temporalValidationSummary:
      "Nested walk-forward: o desenvolvimento avança no tempo em janelas aninhadas. Treino, ajuste e teste externo respeitam a ordem temporal — sem embaralhar o passado com o futuro.",
    holdoutSummary:
      "Holdout é um conjunto reservado fora do desenvolvimento. O holdout já consumido da R3D não pode ser reutilizado como validação final da R3E.",
    leakageProtectionSummary:
      "Leakage (vazamento) é usar informação que ainda não estaria disponível no momento da decisão. Proteções: scaler, imputação, encoder e hiperparâmetros só no treino; sem features futuras.",
    bootstrapSummary:
      "Bootstrap é um método de reamostragem para avaliar a estabilidade de uma estimativa. Nesta tela não há resultados numéricos inventados — apenas a definição.",
    fdrSummary:
      "FDR (False Discovery Rate) controla quantas descobertas falsas se espera ao testar várias comparações. Aqui só se explica o conceito — sem p-valores fabricados.",
    currentScientificState:
      "EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA — exploração e auditoria concluídas; validação final com dados futuros não vistos ainda pendente.",
    r3dResult: "NO_MEASURABLE_EDGE",
    r3eGate: "PENDING_FUTURE_UNSEEN_DATA",
    collectionState: "IN_PROGRESS",
    readinessState: "NOT_READY",
    validationCommandExecuted: false,
    effectPeekingPerformed: false,
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    knownStatements: [
      {
        id: "r3d-closed",
        plainLanguage:
          "A R3D encerrou sem vantagem mensurável (NO_MEASURABLE_EDGE). Isso não significa que a R3E foi rejeitada.",
        technicalCode: "R3D_RESULT=NO_MEASURABLE_EDGE",
      },
      {
        id: "r3e-exploratory",
        plainLanguage:
          "A R3E concluiu a fase exploratória e a auditoria de código/processo. Exploração completa ≠ edge comprovado.",
        technicalCode: "R3E_STATUS=EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA",
      },
      {
        id: "gate-pending",
        plainLanguage:
          "O gate oficial permanece PENDING_FUTURE_UNSEEN_DATA. Pendente ≠ falhou.",
        technicalCode: "R3E_GATE=PENDING_FUTURE_UNSEEN_DATA",
      },
      {
        id: "r4-blocked",
        plainLanguage: "R4 permanece BLOCKED. R5 permanece NOT_STARTED.",
        technicalCode: "R4_STATUS=BLOCKED;R5_STATUS=NOT_STARTED",
      },
    ],
    unknownStatements: [
      {
        id: "future-unseen",
        plainLanguage:
          "Resultados da validação em dados futuros não vistos ainda não existem para esta tela e não são inspecionados.",
        technicalCode: "FUTURE_UNSEEN_RESULTS=ABSENT",
      },
      {
        id: "economic",
        plainLanguage:
          "Não há afirmação de lucratividade, Sharpe, taxa de acerto ou prontidão para dinheiro real.",
        technicalCode: "ECONOMIC_INTERPRETATION_ALLOWED=false",
      },
      {
        id: "approval",
        plainLanguage:
          "Não há aprovação de estratégia nem recomendação de compra ou venda.",
        technicalCode: "NO_TRADING_RECOMMENDATIONS",
      },
    ],
    nextSafeScientificActionPlain:
      "Continuar a coleta futura até a janela mínima; não executar validação nem effect peeking nesta tela; manter R4 bloqueado e R5 não iniciado.",
    evidence: [
      {
        label: "Especificação R3E",
        reference: "docs/experiments/R3E_CONTEXTUAL_EDGE_SPECIFICATION.md",
        kind: "path",
      },
      {
        label: "Estado oficial do projeto",
        reference: "docs/PROJECT.md",
        kind: "path",
      },
      {
        label: "Guardrails científicos e econômicos",
        reference: "docs/ux/UX-R1-SCIENTIFIC-AND-ECONOMIC-LANGUAGE-GUARDRAILS.md",
        kind: "path",
      },
    ],
    ...overrides,
    futureUnseenResultsPresent: false,
  };
}

/** Fixed clock for relative/freshness demos — never Date.now(). */
export const FIXTURE_NOW_ISO = "2026-07-20T12:00:00.000Z";
