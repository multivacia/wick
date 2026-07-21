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

export type R3eModelStageId = "M0" | "M1" | "M2" | "M3" | "M4" | "M5";

export type R3eModelStageDefinition = {
  id: R3eModelStageId;
  plainLanguage: string;
  technicalDefinition: string;
};

export type R3eExplanatoryStatement = {
  id: string;
  plainLanguage: string;
  technicalCode: string | null;
};

/**
 * Explanatory R3E experiment domain input — definitions and governed status
 * codes only. Never invent p-values, returns, or future-unseen outcomes.
 */
export type R3eExperimentDomainInput = {
  experimentId: string;
  parentExperimentId: string;
  title: string;
  purpose: string;
  hypothesis: string;
  protocolVersion: string;
  modelFamilies: string[];
  modelStages: R3eModelStageDefinition[];
  deltaCandleDefinition: string;
  temporalValidationSummary: string;
  holdoutSummary: string;
  leakageProtectionSummary: string;
  bootstrapSummary: string;
  fdrSummary: string;
  currentScientificState: string;
  r3dResult: string;
  r3eGate: string;
  collectionState: string;
  readinessState: string;
  validationCommandExecuted: boolean;
  effectPeekingPerformed: boolean;
  /** Always false for authorized explanatory fixtures. */
  futureUnseenResultsPresent: false;
  r4Status: string;
  r5Status: string;
  knownStatements: R3eExplanatoryStatement[];
  unknownStatements: R3eExplanatoryStatement[];
  nextSafeScientificActionPlain: string;
  evidence: EvidenceReferenceInput[];
};

/** Optional clock for freshness / relative time — never read implicitly. */
export type ViewModelClock = {
  nowIso: string;
  /** Staleness threshold in milliseconds (default applied by builders when omitted). */
  staleAfterMs?: number;
};
