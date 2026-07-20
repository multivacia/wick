/**
 * Named synthetic fixture scenarios feeding I6B ViewModel inputs.
 * CLEARLY_SYNTHETIC — not live operational evidence.
 */

import type { OverviewDomainInput } from "../viewmodels/index.js";
import { fixtureMetadata } from "./metadata.js";
import {
  FIXTURE_NOW_ISO,
  emptyMetric,
  host,
  metric,
  readiness,
  run,
  scheduler,
  ts,
} from "./builders.js";
import type { FixtureScenario, FixtureScenarioId } from "./types.js";

function pack(
  id: FixtureScenarioId,
  label: string,
  purpose: string,
  overview: OverviewDomainInput,
): FixtureScenario {
  return {
    metadata: fixtureMetadata(id, label, purpose),
    overview,
    runs: {
      runs: [
        ...(overview.lastCompletedRun ? [overview.lastCompletedRun] : []),
        ...(overview.lastFailedRun ? [overview.lastFailedRun] : []),
      ],
    },
    readiness: { readiness: overview.readiness },
    hostScheduler: {
      host: overview.host,
      scheduler: overview.scheduler,
      blockers: overview.blockers,
    },
    nowIso: FIXTURE_NOW_ISO,
  };
}

const healthyCollectionNotReady = pack(
  "healthy_collection_not_ready",
  "Coleta saudável / prontidão insuficiente",
  "Exercise healthy collection with NOT_READY readiness (amber, not fault).",
  {
    collection: {
      state: "complete",
      lastObservationAt: ts("2026-07-20T08:00:00.000Z"),
      observationCount: metric(120),
      futureUnseenCutoff: ts("2026-07-20T00:00:00.000Z"),
    },
    lastCompletedRun: run({ runId: "fx-healthy-1" }),
    lastFailedRun: null,
    readiness: readiness(),
    host: host({ state: "unknown" }),
    scheduler: scheduler({ state: "blocked" }),
    blockers: [
      {
        reasonCode: "WINDOW_DAYS_INSUFFICIENT",
        plainLanguage: "Janela futura ilustrativa insuficiente.",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [
      {
        label: "synthetic overview note",
        reference: "fixtures/healthy_collection_not_ready",
        kind: "note",
      },
    ],
  },
);

const collectionInProgress = pack(
  "collection_in_progress",
  "Coleta em andamento",
  "Exercise IN_PROGRESS collection informational semantics.",
  {
    collection: {
      state: "in_progress",
      lastObservationAt: ts("2026-07-20T11:30:00.000Z"),
      observationCount: metric(42),
      futureUnseenCutoff: ts("2026-07-20T00:00:00.000Z"),
    },
    lastCompletedRun: run({ runId: "fx-progress-prev" }),
    lastFailedRun: null,
    readiness: readiness({ state: "not_ready" }),
    host: host(),
    scheduler: scheduler(),
    blockers: [],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

const readinessWindowInsufficient = pack(
  "readiness_window_insufficient",
  "Prontidão — janela insuficiente",
  "Focus readiness NOT_READY with WINDOW_DAYS_INSUFFICIENT.",
  {
    collection: {
      state: "in_progress",
      lastObservationAt: ts("2026-07-19T12:00:00.000Z"),
      observationCount: metric(20),
      futureUnseenCutoff: ts("2026-07-19T00:00:00.000Z"),
    },
    lastCompletedRun: null,
    lastFailedRun: null,
    readiness: readiness({
      windowDays: metric(2),
      requiredWindowDays: metric(14),
      blockingReasonCodes: ["WINDOW_DAYS_INSUFFICIENT"],
    }),
    host: host({ state: "unknown" }),
    scheduler: scheduler({ state: "unknown", operationalDebt: "unknown" }),
    blockers: [
      {
        reasonCode: "WINDOW_DAYS_INSUFFICIENT",
        plainLanguage: "Janela futura ilustrativa abaixo do requisito.",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

const hostDiscoveryDeferred = pack(
  "host_discovery_deferred",
  "Host — descoberta adiada",
  "Exercise DEFERRED host discovery without implying fault.",
  {
    collection: {
      state: "in_progress",
      lastObservationAt: ts("2026-07-20T09:00:00.000Z"),
      observationCount: metric(15),
      futureUnseenCutoff: ts(null),
    },
    lastCompletedRun: run({ runId: "fx-host-1" }),
    lastFailedRun: null,
    readiness: readiness(),
    host: host({
      state: "deferred",
      discoveryNote: "Descoberta de host ilustrativa adiada.",
    }),
    scheduler: scheduler(),
    blockers: [
      {
        reasonCode: "HOST_DISCOVERY_DEFERRED",
        plainLanguage: "Descoberta de host ilustrativa adiada.",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

const schedulerBlockedNotAuthorized = pack(
  "scheduler_blocked_not_authorized",
  "Agendador bloqueado / sem autorização",
  "Exercise BLOCKED scheduler with activation not authorized.",
  {
    collection: {
      state: "complete",
      lastObservationAt: ts("2026-07-20T07:00:00.000Z"),
      observationCount: metric(80),
      futureUnseenCutoff: ts("2026-07-20T00:00:00.000Z"),
    },
    lastCompletedRun: run({ runId: "fx-sched-1" }),
    lastFailedRun: null,
    readiness: readiness({ state: "not_ready" }),
    host: host({ state: "unknown" }),
    scheduler: scheduler({
      registered: false,
      active: false,
      activationAuthorized: false,
      state: "blocked",
    }),
    blockers: [
      {
        reasonCode: "SCHEDULER_BLOCKED",
        plainLanguage: "Ativação do agendador ilustrativa bloqueada.",
        evidence: [],
      },
      {
        reasonCode: "ACTIVATION_NOT_AUTHORIZED",
        plainLanguage: "Sem autorização humana separada (ilustrativo).",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

const confirmedCollectionFault = pack(
  "confirmed_collection_fault",
  "Falha confirmada de coleta",
  "Only confirmed FAULT scenario for red/critical severity.",
  {
    collection: {
      state: "fault",
      lastObservationAt: ts("2026-07-19T18:00:00.000Z"),
      observationCount: metric(5),
      futureUnseenCutoff: ts(null),
    },
    lastCompletedRun: run({ runId: "fx-ok-before-fault" }),
    lastFailedRun: run({
      runId: "fx-fault-1",
      state: "fault",
      resultLabel: "failed",
      acceptedCount: emptyMetric(),
      rejectedCount: emptyMetric(),
      storeBeforeCount: metric(100),
      storeAfterCount: emptyMetric(),
      idempotencyResult: null,
      failureReason: "Falha ilustrativa de escrita no store.",
      failureReasonCode: "LAST_RUN_FAILED",
      finishedAt: ts("2026-07-19T18:05:00.000Z"),
    }),
    readiness: readiness({ state: "not_ready" }),
    host: host(),
    scheduler: scheduler(),
    blockers: [
      {
        reasonCode: "LAST_RUN_FAILED",
        plainLanguage: "Última execução ilustrativa falhou.",
        evidence: [
          {
            label: "synthetic fault artifact",
            reference: "fixtures/confirmed_collection_fault",
            kind: "artifact",
          },
        ],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

const partialUnknownData = pack(
  "partial_unknown_data",
  "Dados parciais / desconhecidos",
  "Missing metrics, timestamps, evidence; unknown host/scheduler.",
  {
    collection: {
      state: "unknown",
      lastObservationAt: ts(null, "unknown"),
      observationCount: emptyMetric(),
      futureUnseenCutoff: ts(null, "not_available"),
    },
    lastCompletedRun: null,
    lastFailedRun: null,
    readiness: readiness({
      state: "unknown",
      windowDays: emptyMetric(),
      requiredWindowDays: emptyMetric(),
      blockingReasonCodes: ["DATA_UNAVAILABLE"],
      explanationPlainLanguage: "Relatório de prontidão ilustrativo ausente.",
      evidence: [],
    }),
    host: host({
      state: "unknown",
      persistentHostPresent: null,
    }),
    scheduler: scheduler({
      registered: null,
      active: null,
      state: "unknown",
      lastCycleState: "unknown",
      lastCycleAt: ts(null, "unknown"),
      operationalDebt: "unknown",
    }),
    blockers: [
      {
        reasonCode: "DATA_UNAVAILABLE",
        plainLanguage: "Dados ilustrativos indisponíveis.",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

const emptyNoRuns = pack(
  "empty_no_runs",
  "Sem execuções",
  "Empty run list and null last runs.",
  {
    collection: {
      state: "not_started",
      lastObservationAt: ts(null),
      observationCount: metric(0),
      futureUnseenCutoff: ts(null),
    },
    lastCompletedRun: null,
    lastFailedRun: null,
    readiness: readiness({
      state: "not_ready",
      windowDays: metric(0),
      requiredWindowDays: metric(14),
    }),
    host: host(),
    scheduler: scheduler(),
    blockers: [],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

// Override runs family to be explicitly empty even if overview has no runs
emptyNoRuns.runs = { runs: [] };

const mixedOperationalBlockers = pack(
  "mixed_operational_blockers",
  "Bloqueios operacionais mistos",
  "Multiple non-fault blockers: deferred host, blocked scheduler, not-ready.",
  {
    collection: {
      state: "in_progress",
      lastObservationAt: ts("2026-07-20T10:00:00.000Z"),
      observationCount: metric(55),
      futureUnseenCutoff: ts("2026-07-20T00:00:00.000Z"),
    },
    lastCompletedRun: run({ runId: "fx-mixed-1" }),
    lastFailedRun: null,
    readiness: readiness(),
    host: host({ state: "deferred" }),
    scheduler: scheduler({ state: "blocked", activationAuthorized: false }),
    blockers: [
      {
        reasonCode: "HOST_DISCOVERY_DEFERRED",
        plainLanguage: "Host ilustrativo adiado.",
        evidence: [],
      },
      {
        reasonCode: "SCHEDULER_BLOCKED",
        plainLanguage: "Agendador ilustrativo bloqueado.",
        evidence: [],
      },
      {
        reasonCode: "WINDOW_DAYS_INSUFFICIENT",
        plainLanguage: "Janela ilustrativa insuficiente.",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [],
  },
);

const currentProjectStateIllustrative = pack(
  "current_project_state_illustrative",
  "Estado atual do projeto (ilustrativo)",
  "Illustrative mirror of known project operational posture — not runtime truth.",
  {
    collection: {
      state: "in_progress",
      lastObservationAt: ts("2026-07-20T08:00:00.000Z"),
      observationCount: metric(42),
      futureUnseenCutoff: ts("2026-07-20T00:00:00.000Z"),
    },
    lastCompletedRun: run({ runId: "fx-current-last-ok" }),
    lastFailedRun: null,
    readiness: readiness({
      state: "not_ready",
      windowDays: metric(3),
      requiredWindowDays: metric(14),
      blockingReasonCodes: ["WINDOW_DAYS_INSUFFICIENT"],
      validationAuthorized: false,
      validationCommandExecuted: false,
      effectPeekingPerformed: false,
    }),
    host: host({ state: "deferred" }),
    scheduler: scheduler({
      state: "blocked",
      activationAuthorized: false,
      active: false,
      operationalDebt: "open",
    }),
    blockers: [
      {
        reasonCode: "HOST_DISCOVERY_DEFERRED",
        plainLanguage: "Descoberta de host adiada (ilustrativo).",
        evidence: [],
      },
      {
        reasonCode: "SCHEDULER_BLOCKED",
        plainLanguage: "Ativação do agendador bloqueada (ilustrativo).",
        evidence: [],
      },
      {
        reasonCode: "WINDOW_DAYS_INSUFFICIENT",
        plainLanguage: "Janela futura insuficiente (ilustrativo).",
        evidence: [],
      },
    ],
    scientificGate: "PENDING_FUTURE_UNSEEN_DATA",
    r4Status: "BLOCKED",
    r5Status: "NOT_STARTED",
    evidence: [
      {
        label: "illustrative project state",
        reference: "docs/PROJECT.md",
        kind: "note",
      },
    ],
  },
);

export const FIXTURE_SCENARIOS: Record<FixtureScenarioId, FixtureScenario> = {
  healthy_collection_not_ready: healthyCollectionNotReady,
  collection_in_progress: collectionInProgress,
  readiness_window_insufficient: readinessWindowInsufficient,
  host_discovery_deferred: hostDiscoveryDeferred,
  scheduler_blocked_not_authorized: schedulerBlockedNotAuthorized,
  confirmed_collection_fault: confirmedCollectionFault,
  partial_unknown_data: partialUnknownData,
  empty_no_runs: emptyNoRuns,
  mixed_operational_blockers: mixedOperationalBlockers,
  current_project_state_illustrative: currentProjectStateIllustrative,
};

export const FIXTURE_SCENARIO_IDS = Object.keys(
  FIXTURE_SCENARIOS,
) as FixtureScenarioId[];
