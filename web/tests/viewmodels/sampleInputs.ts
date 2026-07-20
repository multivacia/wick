import type {
  CollectionRunInput,
  HostDiscoveryInput,
  OverviewDomainInput,
  ReadinessAssessmentInput,
  SchedulerStateInput,
} from "../../src/viewmodels/inputs.js";

/** Test-only sample inputs representing current project operational truth. Not executable fixtures. */

export function emptyMetric() {
  return { value: null as number | null, availability: "not_supplied" as const };
}

export function metric(value: number) {
  return { value, availability: "available" as const };
}

export function ts(iso: string | null, availability: "available" | "not_supplied" | "unknown" = iso ? "available" : "not_supplied") {
  return { iso, availability };
}

export function sampleRun(
  overrides: Partial<CollectionRunInput> = {},
): CollectionRunInput {
  return {
    runId: "run-1",
    state: "complete",
    startedAt: ts("2026-07-18T10:00:00Z"),
    finishedAt: ts("2026-07-18T11:00:00Z"),
    resultLabel: "accepted",
    acceptedCount: metric(10),
    rejectedCount: metric(1),
    storeBeforeCount: metric(100),
    storeAfterCount: metric(110),
    idempotencyResult: "applied",
    failureReason: null,
    failureReasonCode: null,
    evidence: [{ label: "run log", reference: "runs/run-1", kind: "path" }],
    ...overrides,
  };
}

export function sampleReadiness(
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

export function sampleHost(
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

export function sampleScheduler(
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

/** Current project operational truth for tests/examples only. */
export function currentProjectOverviewInput(): OverviewDomainInput {
  return {
    collection: {
      state: "in_progress",
      lastObservationAt: ts("2026-07-20T08:00:00Z"),
      observationCount: metric(42),
      futureUnseenCutoff: ts("2026-07-20T00:00:00Z"),
    },
    lastCompletedRun: sampleRun(),
    lastFailedRun: null,
    readiness: sampleReadiness(),
    host: sampleHost(),
    scheduler: sampleScheduler(),
    blockers: [
      {
        reasonCode: "HOST_DISCOVERY_DEFERRED",
        plainLanguage: "Descoberta de host adiada.",
        evidence: [],
      },
      {
        reasonCode: "SCHEDULER_BLOCKED",
        plainLanguage: "Ativação do agendador bloqueada.",
        evidence: [],
      },
      {
        reasonCode: "WINDOW_DAYS_INSUFFICIENT",
        plainLanguage: "Janela futura insuficiente.",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [
      {
        label: "project state",
        reference: "docs/PROJECT.md",
        kind: "path",
      },
    ],
  };
}
