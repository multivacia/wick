/**
 * UX-R3 I1 — Collection Data Quality ViewModel types.
 * Framework-agnostic. No React / router / network / fixtures.
 */

import type {
  CollectionQualitySeverity,
  CollectionQualityStatus,
  CollectionSourceState,
} from "./collectionDataQualityEnums.js";
import type { ActionHint } from "./presentation.js";
import type {
  DomainLifecycleState,
  PresentationSeverity,
  PresentationStatus,
} from "./status.js";
import type { TimestampPresentation } from "./presentation.js";

export type OptionalCount = {
  value: number | null;
  availability: "available" | "unknown" | "not_supplied" | "not_available";
};

export type CollectionSeriesFindingInput = {
  code: string;
  severity: CollectionQualitySeverity;
  message: string;
};

export type CollectionSeriesInput = {
  seriesId: string;
  market: string;
  asset: string;
  interval: string;
  source: string;
  qualityStatus: CollectionQualityStatus;
  sourceState: CollectionSourceState;
  coverageWindowStartIso: string | null;
  coverageWindowEndIso: string | null;
  expectedRecords: OptionalCount;
  acceptedRecords: OptionalCount;
  rejectedRecords: OptionalCount;
  gapCount: OptionalCount;
  duplicateCount: OptionalCount;
  openCandleExclusionCount: OptionalCount;
  lastUpdateIso: string | null;
  findings: CollectionSeriesFindingInput[];
  limitations: string[];
  relatedEvidenceIds: string[];
};

export type CollectionDataQualityDomainInput = {
  asOfIso: string;
  illustrativeDisclosure: string;
  series: CollectionSeriesInput[];
  aggregateQualityStatus: CollectionQualityStatus;
  aggregateLimitations: string[];
  knownState: string[];
  unknownState: string[];
  nextSafeActionPlainLanguage: string;
  relatedEvidence: Array<{ evidenceId: string; label: string }>;
};

export type CollectionDataQualityFilters = {
  seriesId?: string;
  market?: string;
  interval?: string;
  qualityStatus?: CollectionQualityStatus;
  severity?: CollectionQualitySeverity;
};

export type CollectionDataQualityCriteria = {
  filters: CollectionDataQualityFilters;
};

export type CollectionFilterOption<T extends string = string> = {
  value: T;
  label: string;
};

export type CollectionDataQualityFilterOptions = {
  seriesIds: CollectionFilterOption[];
  markets: CollectionFilterOption[];
  intervals: CollectionFilterOption[];
  qualityStatuses: CollectionFilterOption<CollectionQualityStatus>[];
  severities: CollectionFilterOption<CollectionQualitySeverity>[];
};

export type QualityStatusPresentation = {
  qualityStatus: CollectionQualityStatus;
  qualityStatusLabel: string;
  qualitySeverity: CollectionQualitySeverity;
  qualitySeverityLabel: string;
  domainState: DomainLifecycleState;
  status: PresentationStatus;
  presentationSeverity: PresentationSeverity;
};

export type CountPresentation = {
  displayText: string;
  availability: OptionalCount["availability"];
  isUnknown: boolean;
  isZero: boolean;
};

export type CollectionSeriesViewModel = {
  seriesId: string;
  market: string;
  asset: string;
  interval: string;
  source: string;
  quality: QualityStatusPresentation;
  sourceState: CollectionSourceState;
  sourceStateLabel: string;
  coverageWindowLabel: string;
  expectedRecords: CountPresentation;
  acceptedRecords: CountPresentation;
  rejectedRecords: CountPresentation;
  gapCount: CountPresentation;
  duplicateCount: CountPresentation;
  openCandleExclusionCount: CountPresentation;
  lastUpdate: TimestampPresentation;
  findings: CollectionSeriesFindingInput[];
  limitations: string[];
  relatedEvidenceIds: string[];
};

export type CollectionDataQualityViewModel = {
  pageTitle: string;
  pageDescription: string;
  asOfIso: string;
  illustrativeDisclosure: string;
  freshnessDisclosure: string;
  aggregateQuality: QualityStatusPresentation;
  semanticSafeguards: readonly string[];
  knownState: readonly string[];
  unknownState: readonly string[];
  aggregateLimitations: readonly string[];
  nextSafeAction: ActionHint;
  relatedEvidence: readonly { evidenceId: string; label: string }[];
  filterOptions: CollectionDataQualityFilterOptions;
  series: CollectionSeriesViewModel[];
  resultCount: number;
  totalSeriesCount: number;
  emptyState: boolean;
  noResultsState: boolean;
  hasStaleSeries: boolean;
  hasUnknownCounts: boolean;
};
