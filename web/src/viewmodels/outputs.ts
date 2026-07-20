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

export type {
  OverviewDomainInput,
  RunsDomainInput,
  ReadinessDomainInput,
  HostSchedulerDomainInput,
  CollectionRunInput,
  ViewModelClock,
};
