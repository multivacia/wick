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
  R3eModelStageId,
  R3eModelStageDefinition,
  R3eExplanatoryStatement,
  R3eExperimentDomainInput,
  ViewModelClock,
} from "./inputs.js";

export type {
  RunViewModel,
  RunsViewModel,
  ReadinessViewModel,
  HostSchedulerViewModel,
  OverviewViewModel,
  R3eValidationExecutionState,
  R3eEffectPeekingState,
  R3eExperimentViewModel,
} from "./outputs.js";

export { buildRunViewModel, worstLifecycle } from "./buildRunViewModel.js";
export { buildRunsViewModel } from "./buildRunsViewModel.js";
export { buildReadinessViewModel } from "./buildReadinessViewModel.js";
export { buildHostSchedulerViewModel } from "./buildHostSchedulerViewModel.js";
export { buildOverviewViewModel } from "./buildOverviewViewModel.js";
export { buildR3eExperimentViewModel } from "./buildR3eExperimentViewModel.js";
export {
  presentTimestamp,
  absentTimestamp,
  metricPresentation,
} from "./time.js";

export {
  EVIDENCE_CLASSES,
  EVIDENCE_STALENESS_VALUES,
  EVIDENCE_DATA_ORIGINS,
  EVIDENCE_SCIENTIFIC_STAGES,
  EVIDENCE_CATALOG_STANDINGS,
  EVIDENCE_CLASS_LABELS,
  EVIDENCE_STALENESS_LABELS,
  EVIDENCE_DATA_ORIGIN_LABELS,
  EVIDENCE_SCIENTIFIC_STAGE_LABELS,
  EVIDENCE_CATALOG_STANDING_LABELS,
  isEvidenceClass,
  isEvidenceStaleness,
  isEvidenceDataOrigin,
  isEvidenceScientificStage,
  isEvidenceCatalogStanding,
  type EvidenceClass,
  type EvidenceStaleness,
  type EvidenceDataOrigin,
  type EvidenceScientificStage,
  type EvidenceCatalogStanding,
} from "./evidenceEnums.js";

export {
  assertValidEvidenceSourcePath,
  isValidEvidenceSourcePath,
  InvalidEvidenceSourcePathError,
} from "./evidenceSourcePath.js";

export type {
  EvidenceCatalogEntryInput,
  EvidenceCatalogInput,
  EvidenceExplorerFilters,
  EvidenceExplorerCriteria,
  EvidenceFilterOption,
  EvidenceStatusPresentation,
  EvidenceSummaryItem,
  EvidenceDetailViewModel,
  EvidenceExplorerFilterOptions,
  EvidenceExplorerViewModel,
} from "./evidenceExplorerTypes.js";

export {
  matchesEvidenceSearch,
  matchesEvidenceFilters,
  filterEvidenceEntries,
  clearEvidenceFilters,
  emptyEvidenceCriteria,
} from "./filterEvidenceCatalog.js";

export {
  buildEvidenceExplorerViewModel,
  mapEvidenceStatusToDomain,
  presentEvidenceStatus,
  EVIDENCE_EXPLORER_PAGE_TITLE,
  EVIDENCE_EXPLORER_PAGE_DESCRIPTION,
  EVIDENCE_CATALOG_DISCLOSURE,
  EVIDENCE_SOURCE_PATH_DISCLAIMER,
  EVIDENCE_SAFETY_NOTICES,
} from "./buildEvidenceExplorerViewModel.js";

export {
  EVIDENCE_EXPLORER_PATH,
  buildEvidenceExplorerHref,
  parseEvidenceIdParam,
} from "./evidenceDeepLink.js";
