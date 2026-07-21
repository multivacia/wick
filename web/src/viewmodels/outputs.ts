import type {
  ActionHint,
  EvidenceLink,
  MetricPresentation,
  PresentationBlock,
  StateExplanation,
  TimestampPresentation,
} from "./presentation.js";
import type {
  CollectionRunInput,
  HostSchedulerDomainInput,
  OverviewDomainInput,
  ReadinessDomainInput,
  R3eExplanatoryStatement,
  R3eExperimentDomainInput,
  R3eModelStageDefinition,
  RunsDomainInput,
  ViewModelClock,
} from "./inputs.js";
import type { ReasonCode } from "./reasons.js";
import type { DomainLifecycleState, PresentationStatus } from "./status.js";

export type RunViewModel = {
  runId: string | null;
  state: DomainLifecycleState;
  presentation: StateExplanation;
  startedAt: TimestampPresentation;
  finishedAt: TimestampPresentation;
  resultLabel: string | null;
  acceptedCount: MetricPresentation;
  rejectedCount: MetricPresentation;
  storeBeforeCount: MetricPresentation;
  storeAfterCount: MetricPresentation;
  idempotencyResult: string | null;
  failureReason: string | null;
  evidence: EvidenceLink[];
};

export type RunsViewModel = {
  runs: RunViewModel[];
  summaryStatus: PresentationStatus;
  primaryMessage: { plainLanguage: string; technicalCode: string | null };
  actionHint: ActionHint | null;
};

export type ReadinessViewModel = {
  state: DomainLifecycleState;
  presentation: StateExplanation;
  windowDays: MetricPresentation;
  requiredWindowDays: MetricPresentation;
  blockingReasonCodes: ReasonCode[];
  validationAuthorized: boolean;
  validationCommandExecuted: boolean;
  effectPeekingPerformed: boolean;
  nextSafeAction: ActionHint;
  evidence: EvidenceLink[];
};

export type HostSchedulerViewModel = {
  hostDiscoveryState: DomainLifecycleState;
  hostPresentation: StateExplanation;
  persistentHostPresent: boolean | null;
  schedulerRegistered: boolean | null;
  schedulerActive: boolean | null;
  schedulerState: DomainLifecycleState;
  schedulerPresentation: StateExplanation;
  lastCycleState: DomainLifecycleState;
  lastCycleAt: TimestampPresentation;
  operationalDebt: "open" | "none" | "unknown";
  activationAuthorized: boolean;
  blockers: Array<{
    reasonCode: ReasonCode;
    plainLanguage: string;
    evidence: EvidenceLink[];
  }>;
  nextSafeAction: ActionHint;
  evidence: EvidenceLink[];
};

export type OverviewViewModel = {
  overallState: DomainLifecycleState;
  overallPresentation: StateExplanation;
  collectionSummary: PresentationBlock;
  readinessSummary: PresentationBlock;
  hostSchedulerSummary: PresentationBlock;
  activeBlockers: Array<{
    reasonCode: ReasonCode;
    plainLanguage: string;
    evidence: EvidenceLink[];
  }>;
  lastCompletedRun: RunViewModel | null;
  lastFailedRun: RunViewModel | null;
  lastKnownEvidence: EvidenceLink[];
  nextSafeAction: ActionHint;
  scientificGate: string;
  r4Status: string;
  r5Status: string;
  generatedWithNow: string | null;
};

export type R3eValidationExecutionState = {
  executed: boolean;
  label: string;
  /** Explicit inequality: not executed ≠ failed. */
  distinctFromFailed: string;
};

export type R3eEffectPeekingState = {
  performed: boolean;
  label: string;
  /** Explicit inequality: false ≠ not reported. */
  distinctFromNotReported: string;
};

export type R3eExperimentViewModel = {
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
  validationExecutionState: R3eValidationExecutionState;
  effectPeekingState: R3eEffectPeekingState;
  futureUnseenResultsPresent: false;
  r4Status: string;
  r5Status: string;
  knownStatements: R3eExplanatoryStatement[];
  unknownStatements: R3eExplanatoryStatement[];
  nextSafeScientificAction: ActionHint;
  evidence: EvidenceLink[];
};

export type {
  OverviewDomainInput,
  RunsDomainInput,
  ReadinessDomainInput,
  HostSchedulerDomainInput,
  R3eExperimentDomainInput,
  CollectionRunInput,
  ViewModelClock,
};
