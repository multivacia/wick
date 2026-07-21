/**
 * Evidence Explorer domain inputs and ViewModel outputs (UX-R2 I1).
 */

import type {
  EvidenceClass,
  EvidenceDataOrigin,
  EvidenceScientificStage,
  EvidenceStaleness,
} from "./evidenceEnums.js";
import type {
  DomainLifecycleState,
  PresentationStatus,
  PresentationSeverity,
} from "./status.js";

export type EvidenceCatalogEntryInput = {
  evidenceId: string;
  title: string;
  evidenceClass: EvidenceClass;
  release: string;
  increment: string | null;
  experimentId: string | null;
  status: string;
  dataOrigin: EvidenceDataOrigin;
  scientificStage: EvidenceScientificStage;
  createdAtOrUnknown: string;
  sourcePath: string;
  summary: string;
  supports: string[];
  limitations: string[];
  knownState: string[];
  unknownState: string[];
  governanceFlags: string[];
  staleness: EvidenceStaleness;
};

export type EvidenceCatalogInput = {
  entries: EvidenceCatalogEntryInput[];
};

export type EvidenceExplorerFilters = {
  evidenceClass?: EvidenceClass;
  release?: string;
  status?: string;
  dataOrigin?: EvidenceDataOrigin;
  scientificStage?: EvidenceScientificStage;
  staleness?: EvidenceStaleness;
};

export type EvidenceExplorerCriteria = {
  searchQuery: string;
  filters: EvidenceExplorerFilters;
  selectedEvidenceId?: string | null;
};

export type EvidenceFilterOption<T extends string = string> = {
  value: T;
  label: string;
};

export type EvidenceStatusPresentation = {
  domainState: DomainLifecycleState;
  status: PresentationStatus;
  severity: PresentationSeverity;
  label: string;
};

export type EvidenceSummaryItem = {
  evidenceId: string;
  title: string;
  evidenceClass: EvidenceClass;
  evidenceClassLabel: string;
  release: string;
  increment: string | null;
  experimentId: string | null;
  status: string;
  statusPresentation: EvidenceStatusPresentation;
  dataOrigin: EvidenceDataOrigin;
  dataOriginLabel: string;
  scientificStage: EvidenceScientificStage;
  scientificStageLabel: string;
  staleness: EvidenceStaleness;
  stalenessLabel: string;
  summary: string;
};

export type EvidenceDetailViewModel = EvidenceSummaryItem & {
  createdAtOrUnknown: string;
  sourcePath: string;
  supports: string[];
  limitations: string[];
  knownState: string[];
  unknownState: string[];
  governanceFlags: string[];
};

export type EvidenceExplorerFilterOptions = {
  evidenceClasses: EvidenceFilterOption<EvidenceClass>[];
  releases: EvidenceFilterOption[];
  statuses: EvidenceFilterOption[];
  dataOrigins: EvidenceFilterOption<EvidenceDataOrigin>[];
  scientificStages: EvidenceFilterOption<EvidenceScientificStage>[];
  stalenessValues: EvidenceFilterOption<EvidenceStaleness>[];
};

export type EvidenceExplorerViewModel = {
  pageTitle: string;
  pageDescription: string;
  catalogDisclosure: string;
  sourcePathDisclaimer: string;
  safetyNotices: string[];
  filterOptions: EvidenceExplorerFilterOptions;
  activeCriteria: EvidenceExplorerCriteria;
  summaries: EvidenceSummaryItem[];
  selectedDetail: EvidenceDetailViewModel | null;
  emptyState: boolean;
  noResultsState: boolean;
  invalidSelectionFallback: boolean;
  resultCount: number;
};
