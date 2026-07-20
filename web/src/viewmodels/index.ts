/**
 * UX-R1 I6B — pure, screen-agnostic ViewModel layer.
 * Do not import React, router, network clients, fixtures, or screens here.
 */

export {
  DOMAIN_LIFECYCLE_STATES,
  PRESENTATION_STATUSES,
  PRESENTATION_SEVERITIES,
  mapDomainStateToPresentation,
  isFaultPresentation,
  assertSemanticInequalities,
  type DomainLifecycleState,
  type PresentationStatus,
  type PresentationSeverity,
  type StatusSemanticMapping,
} from "./status.js";

export {
  REASON_CODES,
  explainReasonCode,
  type ReasonCode,
} from "./reasons.js";

export type {
  PrimaryMessage,
  TechnicalDetail,
  EvidenceLink,
  ActionHint,
  ActionHintCode,
  TimestampPresentation,
  FreshnessClassification,
  ValueAvailability,
  MetricPresentation,
  StateExplanation,
  PresentationBlock,
} from "./presentation.js";

export { ACTION_HINT_CODES } from "./presentation.js";

export type {
  OptionalMetric,
  OptionalIsoTimestamp,
  EvidenceReferenceInput,
  OperationalBlockerInput,
  CollectionRunInput,
  CollectionFreshnessInput,
  ReadinessAssessmentInput,
  HostDiscoveryInput,
  SchedulerStateInput,
  OverviewDomainInput,
  RunsDomainInput,
  ReadinessDomainInput,
  HostSchedulerDomainInput,
  ViewModelClock,
} from "./inputs.js";

export type {
  RunViewModel,
  RunsViewModel,
  ReadinessViewModel,
  HostSchedulerViewModel,
  OverviewViewModel,
} from "./outputs.js";

export { buildRunViewModel, worstLifecycle } from "./buildRunViewModel.js";
export { buildRunsViewModel } from "./buildRunsViewModel.js";
export { buildReadinessViewModel } from "./buildReadinessViewModel.js";
export { buildHostSchedulerViewModel } from "./buildHostSchedulerViewModel.js";
export { buildOverviewViewModel } from "./buildOverviewViewModel.js";
export {
  presentTimestamp,
  absentTimestamp,
  metricPresentation,
} from "./time.js";
