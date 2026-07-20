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

/** Fixed clock for relative/freshness demos — never Date.now(). */
export const FIXTURE_NOW_ISO = "2026-07-20T12:00:00.000Z";
