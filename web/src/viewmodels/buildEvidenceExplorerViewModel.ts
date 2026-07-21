/**
 * UX-R2 I1 — Evidence Explorer ViewModel builder.
 * Pure, screen-agnostic. No React / fixtures / network.
 */

import {
  EVIDENCE_CLASS_LABELS,
  EVIDENCE_CLASSES,
  EVIDENCE_DATA_ORIGIN_LABELS,
  EVIDENCE_DATA_ORIGINS,
  EVIDENCE_SCIENTIFIC_STAGE_LABELS,
  EVIDENCE_SCIENTIFIC_STAGES,
  EVIDENCE_STALENESS_LABELS,
  EVIDENCE_STALENESS_VALUES,
  type EvidenceClass,
  type EvidenceDataOrigin,
  type EvidenceScientificStage,
  type EvidenceStaleness,
} from "./evidenceEnums.js";
import type {
  EvidenceCatalogEntryInput,
  EvidenceCatalogInput,
  EvidenceDetailViewModel,
  EvidenceExplorerCriteria,
  EvidenceExplorerFilterOptions,
  EvidenceExplorerViewModel,
  EvidenceStatusPresentation,
  EvidenceSummaryItem,
} from "./evidenceExplorerTypes.js";
import { assertValidEvidenceSourcePath } from "./evidenceSourcePath.js";
import { filterEvidenceEntries } from "./filterEvidenceCatalog.js";
import {
  mapDomainStateToPresentation,
  type DomainLifecycleState,
} from "./status.js";

export const EVIDENCE_EXPLORER_PAGE_TITLE = "Evidências";

export const EVIDENCE_EXPLORER_PAGE_DESCRIPTION =
  "Catálogo curado de evidências de governança — somente leitura, metadados e resumos, sem acesso a arquivos.";

export const EVIDENCE_CATALOG_DISCLOSURE =
  "Catálogo ilustrativo curado. Presença de evidência no catálogo não implica aprovação científica nem autorização operacional.";

export const EVIDENCE_SOURCE_PATH_DISCLAIMER =
  "O caminho de origem é metadado de exibição apenas. Não abre, baixa nem lê arquivos em tempo de execução.";

export const EVIDENCE_SAFETY_NOTICES = [
  "Evidence presence != scientific approval — presença de evidência não significa aprovação científica.",
  "Audited != future validated — auditado não significa validado em dados futuros não vistos.",
  "Source path display != file access — exibir sourcePath não concede acesso a arquivos.",
] as const;

/**
 * Map free-text evidence status to domain lifecycle for StatusBadge.
 * pending / blocked / not_ready must never become fault.
 */
export function mapEvidenceStatusToDomain(
  status: string,
): DomainLifecycleState {
  const normalized = status.trim().toLowerCase().replace(/[-\s]+/g, "_");

  if (
    normalized.includes("not_ready") ||
    normalized.includes("insufficient") ||
    normalized === "window_days_insufficient"
  ) {
    return "not_ready";
  }
  if (normalized.includes("blocked")) {
    return "blocked";
  }
  if (normalized.includes("deferred")) {
    return "deferred";
  }
  if (
    normalized.includes("pending") ||
    normalized.includes("in_progress") ||
    normalized.includes("authorized_with_conditions")
  ) {
    return "in_progress";
  }
  if (
    normalized.includes("complete") ||
    normalized.includes("accepted") ||
    normalized.includes("closed") ||
    normalized.includes("merged") ||
    normalized.includes("audited") ||
    normalized.includes("no_measurable_edge") ||
    normalized.includes("scope_recommended")
  ) {
    return "complete";
  }
  if (normalized.includes("fault") || normalized.includes("error")) {
    return "fault";
  }
  if (normalized.includes("ready") && !normalized.includes("not_ready")) {
    return "ready";
  }
  if (normalized.includes("not_started") || normalized.includes("absent")) {
    return "not_started";
  }
  return "unknown";
}

export function presentEvidenceStatus(status: string): EvidenceStatusPresentation {
  const domainState = mapEvidenceStatusToDomain(status);
  const mapping = mapDomainStateToPresentation(domainState);
  return {
    domainState,
    status: mapping.status,
    severity: mapping.severity,
    label: status,
  };
}

function toSummary(entry: EvidenceCatalogEntryInput): EvidenceSummaryItem {
  return {
    evidenceId: entry.evidenceId,
    title: entry.title,
    evidenceClass: entry.evidenceClass,
    evidenceClassLabel: EVIDENCE_CLASS_LABELS[entry.evidenceClass],
    release: entry.release,
    increment: entry.increment,
    experimentId: entry.experimentId,
    status: entry.status,
    statusPresentation: presentEvidenceStatus(entry.status),
    dataOrigin: entry.dataOrigin,
    dataOriginLabel: EVIDENCE_DATA_ORIGIN_LABELS[entry.dataOrigin],
    scientificStage: entry.scientificStage,
    scientificStageLabel:
      EVIDENCE_SCIENTIFIC_STAGE_LABELS[entry.scientificStage],
    staleness: entry.staleness,
    stalenessLabel: EVIDENCE_STALENESS_LABELS[entry.staleness],
    summary: entry.summary,
  };
}

function toDetail(entry: EvidenceCatalogEntryInput): EvidenceDetailViewModel {
  return {
    ...toSummary(entry),
    createdAtOrUnknown: entry.createdAtOrUnknown,
    sourcePath: entry.sourcePath,
    supports: [...entry.supports],
    limitations: [...entry.limitations],
    knownState: [...entry.knownState],
    unknownState: [...entry.unknownState],
    governanceFlags: [...entry.governanceFlags],
  };
}

function buildFilterOptions(
  catalog: EvidenceCatalogInput,
): EvidenceExplorerFilterOptions {
  const releases = [
    ...new Set(catalog.entries.map((e) => e.release)),
  ].sort((a, b) => a.localeCompare(b));
  const statuses = [
    ...new Set(catalog.entries.map((e) => e.status)),
  ].sort((a, b) => a.localeCompare(b));

  const presentClasses = new Set(
    catalog.entries.map((e) => e.evidenceClass),
  );
  const presentOrigins = new Set(catalog.entries.map((e) => e.dataOrigin));
  const presentStages = new Set(
    catalog.entries.map((e) => e.scientificStage),
  );
  const presentStaleness = new Set(catalog.entries.map((e) => e.staleness));

  return {
    evidenceClasses: EVIDENCE_CLASSES.filter((c) => presentClasses.has(c)).map(
      (value: EvidenceClass) => ({
        value,
        label: EVIDENCE_CLASS_LABELS[value],
      }),
    ),
    releases: releases.map((value) => ({ value, label: value })),
    statuses: statuses.map((value) => ({ value, label: value })),
    dataOrigins: EVIDENCE_DATA_ORIGINS.filter((o) =>
      presentOrigins.has(o),
    ).map((value: EvidenceDataOrigin) => ({
      value,
      label: EVIDENCE_DATA_ORIGIN_LABELS[value],
    })),
    scientificStages: EVIDENCE_SCIENTIFIC_STAGES.filter((s) =>
      presentStages.has(s),
    ).map((value: EvidenceScientificStage) => ({
      value,
      label: EVIDENCE_SCIENTIFIC_STAGE_LABELS[value],
    })),
    stalenessValues: EVIDENCE_STALENESS_VALUES.filter((s) =>
      presentStaleness.has(s),
    ).map((value: EvidenceStaleness) => ({
      value,
      label: EVIDENCE_STALENESS_LABELS[value],
    })),
  };
}

function validateCatalogPaths(catalog: EvidenceCatalogInput): void {
  for (const entry of catalog.entries) {
    assertValidEvidenceSourcePath(entry.sourcePath);
  }
}

/**
 * Build the Evidence Explorer ViewModel from a curated catalog + criteria.
 */
export function buildEvidenceExplorerViewModel(
  catalog: EvidenceCatalogInput,
  criteria: EvidenceExplorerCriteria,
): EvidenceExplorerViewModel {
  validateCatalogPaths(catalog);

  const normalized: EvidenceExplorerCriteria = {
    searchQuery: criteria.searchQuery ?? "",
    filters: { ...(criteria.filters ?? {}) },
    selectedEvidenceId: criteria.selectedEvidenceId ?? null,
  };

  const filtered = filterEvidenceEntries(
    catalog.entries,
    normalized.searchQuery,
    normalized.filters,
  );
  const summaries = filtered.map(toSummary);
  const resultCount = summaries.length;
  const catalogEmpty = catalog.entries.length === 0;
  const emptyState = catalogEmpty;
  const noResultsState = !catalogEmpty && resultCount === 0;

  let selectedDetail: EvidenceDetailViewModel | null = null;
  let invalidSelectionFallback = false;
  const selectedId = normalized.selectedEvidenceId;

  if (selectedId) {
    const inFiltered = filtered.find((e) => e.evidenceId === selectedId);
    if (inFiltered) {
      selectedDetail = toDetail(inFiltered);
    } else {
      const inCatalog = catalog.entries.find(
        (e) => e.evidenceId === selectedId,
      );
      if (inCatalog) {
        // Selected id exists but is filtered out — clear selection gracefully.
        invalidSelectionFallback = true;
        selectedDetail = null;
      } else {
        invalidSelectionFallback = true;
        selectedDetail = null;
      }
    }
  }

  return {
    pageTitle: EVIDENCE_EXPLORER_PAGE_TITLE,
    pageDescription: EVIDENCE_EXPLORER_PAGE_DESCRIPTION,
    catalogDisclosure: EVIDENCE_CATALOG_DISCLOSURE,
    sourcePathDisclaimer: EVIDENCE_SOURCE_PATH_DISCLAIMER,
    safetyNotices: [...EVIDENCE_SAFETY_NOTICES],
    filterOptions: buildFilterOptions(catalog),
    activeCriteria: normalized,
    summaries,
    selectedDetail,
    emptyState,
    noResultsState,
    invalidSelectionFallback,
    resultCount,
  };
}
