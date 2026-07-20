/**
 * Normalized operational-domain inputs (not API payloads).
 * Missing facts stay explicit — never invent status or metrics.
 */

import type { DomainLifecycleState } from "./status.js";
import type { ReasonCode } from "./reasons.js";
import type { ValueAvailability } from "./presentation.js";

export type OptionalMetric = {
  value: number | null;
  availability: ValueAvailability;
};

export type OptionalIsoTimestamp = {
  iso: string | null;
  availability: ValueAvailability;
};

export type EvidenceReferenceInput = {
  label: string;
  reference: string;
  kind: "path" | "uri" | "run_id" | "artifact" | "note";
};

export type OperationalBlockerInput = {
  reasonCode: ReasonCode;
  plainLanguage: string;
  evidence: EvidenceReferenceInput[];
};

export type CollectionRunInput = {
  runId: string | null;
  state: DomainLifecycleState;
  startedAt: OptionalIsoTimestamp;
  finishedAt: OptionalIsoTimestamp;
  resultLabel: string | null;
  acceptedCount: OptionalMetric;
  rejectedCount: OptionalMetric;
  storeBeforeCount: OptionalMetric;
  storeAfterCount: OptionalMetric;
  idempotencyResult: string | null;
  failureReason: string | null;
  failureReasonCode: ReasonCode | null;
  evidence: EvidenceReferenceInput[];
};

export type CollectionFreshnessInput = {
  state: DomainLifecycleState;
  lastObservationAt: OptionalIsoTimestamp;
  observationCount: OptionalMetric;
  futureUnseenCutoff: OptionalIsoTimestamp;
};

export type ReadinessAssessmentInput = {
  state: DomainLifecycleState;
  windowDays: OptionalMetric;
  requiredWindowDays: OptionalMetric;
  blockingReasonCodes: ReasonCode[];
  validationAuthorized: boolean;
  validationCommandExecuted: boolean;
  effectPeekingPerformed: boolean;
  explanationPlainLanguage: string | null;
  evidence: EvidenceReferenceInput[];
};

export type HostDiscoveryInput = {
  state: DomainLifecycleState;
  persistentHostPresent: boolean | null;
  discoveryNote: string | null;
  evidence: EvidenceReferenceInput[];
};

export type SchedulerStateInput = {
  registered: boolean | null;
  active: boolean | null;
  activationAuthorized: boolean;
  state: DomainLifecycleState;
  lastCycleState: DomainLifecycleState;
  lastCycleAt: OptionalIsoTimestamp;
  operationalDebt: "open" | "none" | "unknown";
  evidence: EvidenceReferenceInput[];
};

export type OverviewDomainInput = {
  collection: CollectionFreshnessInput;
  lastCompletedRun: CollectionRunInput | null;
  lastFailedRun: CollectionRunInput | null;
  readiness: ReadinessAssessmentInput;
  host: HostDiscoveryInput;
  scheduler: SchedulerStateInput;
  blockers: OperationalBlockerInput[];
  scientificGate: string;
  r4Status: string;
  r5Status: string;
  evidence: EvidenceReferenceInput[];
};

export type RunsDomainInput = {
  runs: CollectionRunInput[];
};

export type ReadinessDomainInput = {
  readiness: ReadinessAssessmentInput;
};

export type HostSchedulerDomainInput = {
  host: HostDiscoveryInput;
  scheduler: SchedulerStateInput;
  blockers: OperationalBlockerInput[];
};

/** Optional clock for freshness / relative time — never read implicitly. */
export type ViewModelClock = {
  nowIso: string;
  /** Staleness threshold in milliseconds (default applied by builders when omitted). */
  staleAfterMs?: number;
};
