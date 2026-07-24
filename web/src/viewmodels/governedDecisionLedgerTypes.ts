/**
 * UX-R4 I2 — Governed Decision Ledger types.
 * Framework-agnostic. No React / router / network / fixtures.
 */

import type {
  LedgerDecisionType,
  LedgerDisposition,
  LedgerDomain,
  LedgerReassessmentAvailability,
} from "./governedDecisionLedgerEnums.js";
import type { PresentationStatus } from "./status.js";

export type LedgerEvidenceRefInput = {
  evidenceId: string;
  label: string;
};

export type GovernedDecisionRecordInput = {
  decisionId: string;
  title: string;
  summary: string;
  domain: LedgerDomain;
  decisionType: LedgerDecisionType;
  disposition: LedgerDisposition;
  /** ISO date (YYYY-MM-DD) or the sentinel "UNKNOWN". */
  decisionDate: string;
  scope: string;
  rationale: string;
  evidenceRefs: LedgerEvidenceRefInput[];
  mustNotInfer: string[];
  reassessmentTrigger: string | null;
  nextGovernedAction: string;
  isIllustrative: true;
  fixtureAuthoredAt: string;
  catalogCuratedAt: string;
  effectiveDate?: string;
  conditions?: string[];
  relatedRelease?: string;
  relatedIncrement?: string;
  scientificBoundary?: string;
  operationalBoundary?: string;
  supersedes?: string;
  supersededBy?: string;
  sourceArtifact?: string;
  primaryEvidenceRef?: LedgerEvidenceRefInput;
};

export type GovernedDecisionLedgerDomainInput = {
  fixtureVersion: 1;
  catalogCuratedAt: string;
  fixtureAuthoredAt: string;
  /** Explicit curated freshness — never implies live polling. */
  freshness: "current" | "stale";
  staleDisclosure: string;
  illustrativeDisclosure: string;
  records: GovernedDecisionRecordInput[];
};

export type GovernedDecisionLedgerFilters = {
  disposition?: LedgerDisposition;
  domain?: LedgerDomain;
  release?: string;
  decisionType?: LedgerDecisionType;
  reassessmentAvailability?: LedgerReassessmentAvailability;
};

export type GovernedDecisionLedgerCriteria = {
  filters: GovernedDecisionLedgerFilters;
  selectedDecisionId?: string | null;
};

export type LedgerFilterOption<T extends string = string> = {
  value: T;
  label: string;
};

export type GovernedDecisionLedgerFilterOptions = {
  dispositions: LedgerFilterOption<LedgerDisposition>[];
  domains: LedgerFilterOption<LedgerDomain>[];
  releases: LedgerFilterOption[];
  decisionTypes: LedgerFilterOption<LedgerDecisionType>[];
  reassessmentAvailability: LedgerFilterOption<LedgerReassessmentAvailability>[];
};

export type LedgerDispositionPresentation = {
  disposition: LedgerDisposition;
  dispositionLabel: string;
  dispositionMeaning: string;
  status: PresentationStatus;
};

export type LedgerSummaryCounts = {
  /** Accepted UX/governance decisions — not approved trading strategies. */
  acceptedCount: number;
  /** Blocked governance decisions — not system failure count. */
  blockedCount: number;
  /** Records with reassessment triggers — not automatic actions. */
  triggerCount: number;
  /** Unknown disposition/date presentations — never coerced to zero. */
  unknownDispositionCount: number;
  totalCount: number;
  resultCount: number;
};

export type GovernedDecisionRecordViewModel = {
  decisionId: string;
  title: string;
  summary: string;
  domain: LedgerDomain;
  domainLabel: string;
  decisionType: LedgerDecisionType;
  decisionTypeLabel: string;
  disposition: LedgerDispositionPresentation;
  decisionDateDisplay: string;
  decisionDateIsUnknown: boolean;
  scope: string;
  rationale: string;
  evidenceRefs: LedgerEvidenceRefInput[];
  primaryEvidenceRef: LedgerEvidenceRefInput | null;
  mustNotInfer: string[];
  reassessmentTrigger: string | null;
  hasReassessmentTrigger: boolean;
  nextGovernedAction: string;
  conditions: string[];
  hasConditions: boolean;
  relatedRelease: string | null;
  relatedIncrement: string | null;
  scientificBoundary: string | null;
  operationalBoundary: string | null;
  supersedes: string | null;
  supersededBy: string | null;
  isSuperseded: boolean;
  sourceArtifact: string | null;
  fixtureAuthoredAtDisplay: string;
  catalogCuratedAtDisplay: string;
  effectiveDateDisplay: string | null;
  isIllustrative: true;
};

export type GovernedDecisionLedgerViewModel = {
  sectionTitle: string;
  sectionDescription: string;
  illustrativeDisclosure: string;
  freshnessDisclosure: string;
  staleFixtureState: boolean;
  staleDisclosure: string | null;
  unknownStateNotice: string | null;
  semanticSafeguards: readonly string[];
  counts: LedgerSummaryCounts;
  filterOptions: GovernedDecisionLedgerFilterOptions;
  records: GovernedDecisionRecordViewModel[];
  selectedRecord: GovernedDecisionRecordViewModel | null;
  emptyState: boolean;
  noResultsState: boolean;
  catalogCuratedAtDisplay: string;
  fixtureAuthoredAtDisplay: string;
  fixtureVersion: 1;
};
