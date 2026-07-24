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

export {
  COLLECTION_QUALITY_STATUSES,
  COLLECTION_QUALITY_SEVERITIES,
  COLLECTION_SOURCE_STATES,
  COLLECTION_QUALITY_STATUS_LABELS,
  COLLECTION_QUALITY_SEVERITY_LABELS,
  COLLECTION_SOURCE_STATE_LABELS,
  QUALITY_SEVERITY_RANK,
  mapQualityStatusToSeverity,
  isCollectionQualityStatus,
  isCollectionQualitySeverity,
  isCollectionSourceState,
  type CollectionQualityStatus,
  type CollectionQualitySeverity,
  type CollectionSourceState,
} from "./collectionDataQualityEnums.js";

export type {
  OptionalCount,
  CollectionSeriesFindingInput,
  CollectionSeriesInput,
  CollectionDataQualityDomainInput,
  CollectionDataQualityFilters,
  CollectionDataQualityCriteria,
  CollectionFilterOption,
  CollectionDataQualityFilterOptions,
  QualityStatusPresentation,
  CountPresentation,
  CollectionSeriesViewModel,
  CollectionDataQualityViewModel,
} from "./collectionDataQualityTypes.js";

export {
  matchesCollectionFilters,
  sortCollectionSeries,
  filterAndSortCollectionSeries,
  clearCollectionFilters,
  emptyCollectionCriteria,
  buildCollectionFilterOptions,
} from "./filterCollectionDataQuality.js";

export {
  buildCollectionDataQualityViewModel,
  mapQualityStatusToDomain,
  presentQualityStatus,
  presentOptionalCount,
  COLLECTION_DATA_QUALITY_PAGE_TITLE,
  COLLECTION_DATA_QUALITY_PAGE_DESCRIPTION,
  COLLECTION_DATA_QUALITY_SEMANTIC_SAFEGUARDS,
  COLLECTION_DATA_QUALITY_FRESHNESS_DISCLOSURE,
} from "./buildCollectionDataQualityViewModel.js";

export {
  LEDGER_DISPOSITIONS,
  LEDGER_DOMAINS,
  LEDGER_DECISION_TYPES,
  LEDGER_REASSESSMENT_AVAILABILITY,
  LEDGER_DISPOSITION_LABELS,
  LEDGER_DISPOSITION_MEANINGS,
  LEDGER_DOMAIN_LABELS,
  LEDGER_DECISION_TYPE_LABELS,
  LEDGER_REASSESSMENT_AVAILABILITY_LABELS,
  mapDispositionToPresentation,
  isLedgerDisposition,
  isLedgerDomain,
  isLedgerDecisionType,
  type LedgerDisposition,
  type LedgerDomain,
  type LedgerDecisionType,
  type LedgerReassessmentAvailability,
} from "./governedDecisionLedgerEnums.js";

export type {
  LedgerEvidenceRefInput,
  GovernedDecisionRecordInput,
  GovernedDecisionLedgerDomainInput,
  GovernedDecisionLedgerFilters,
  GovernedDecisionLedgerCriteria,
  LedgerFilterOption,
  GovernedDecisionLedgerFilterOptions,
  LedgerDispositionPresentation,
  LedgerSummaryCounts,
  GovernedDecisionRecordViewModel,
  GovernedDecisionLedgerViewModel,
} from "./governedDecisionLedgerTypes.js";

export {
  hasReassessmentTrigger,
  matchesLedgerFilters,
  sortLedgerRecords,
  filterAndSortLedgerRecords,
  clearLedgerFilters,
  emptyLedgerCriteria,
  buildLedgerFilterOptions,
} from "./filterGovernedDecisionLedger.js";

export {
  buildGovernedDecisionLedgerViewModel,
  presentDisposition,
  assertValidDecisionId,
  assertValidEvidenceId,
  InvalidGovernedDecisionLedgerError,
  GOVERNED_DECISION_LEDGER_SECTION_TITLE,
  GOVERNED_DECISION_LEDGER_SECTION_DESCRIPTION,
  GOVERNED_DECISION_LEDGER_SEMANTIC_SAFEGUARDS,
  GOVERNED_DECISION_LEDGER_FRESHNESS_DISCLOSURE,
} from "./buildGovernedDecisionLedgerViewModel.js";
