/**
 * UX-R3 I1 — Collection Data Quality ViewModel builder.
 * Pure, screen-agnostic. No React / fixtures / network.
 */

import {
  COLLECTION_QUALITY_SEVERITY_LABELS,
  COLLECTION_QUALITY_STATUS_LABELS,
  COLLECTION_SOURCE_STATE_LABELS,
  mapQualityStatusToSeverity,
  type CollectionQualityStatus,
} from "./collectionDataQualityEnums.js";
import type {
  CollectionDataQualityCriteria,
  CollectionDataQualityDomainInput,
  CollectionDataQualityViewModel,
  CollectionSeriesInput,
  CollectionSeriesViewModel,
  CountPresentation,
  OptionalCount,
  QualityStatusPresentation,
} from "./collectionDataQualityTypes.js";
import {
  buildCollectionFilterOptions,
  filterAndSortCollectionSeries,
} from "./filterCollectionDataQuality.js";
import { actionHint, deepFreeze } from "./helpers.js";
import type { DomainLifecycleState } from "./status.js";
import { mapDomainStateToPresentation } from "./status.js";
import { presentTimestamp } from "./time.js";
import type { ViewModelClock } from "./inputs.js";

export const COLLECTION_DATA_QUALITY_PAGE_TITLE = "Dados Coletados";

export const COLLECTION_DATA_QUALITY_PAGE_DESCRIPTION =
  "Monitoramento ilustrativo de cobertura e qualidade dos dados coletados — sem aprovar cientificamente, validar ou ativar operações.";

export const COLLECTION_DATA_QUALITY_SEMANTIC_SAFEGUARDS = [
  "DATA_QUALITY ≠ SCIENTIFIC_APPROVAL — qualidade de dados não implica aprovação científica.",
  "COVERAGE_COMPLETE ≠ FUTURE_WINDOW_COMPLETE — cobertura de série não completa a janela futura.",
  "COLLECTION_HEALTHY ≠ VALIDATION_READY — saúde da coleta não significa prontidão para validação.",
  "GAP_PRESENT ≠ COLLECTION_FAILED — lacuna presente não significa falha da coleta.",
  "OPEN_CANDLE_EXCLUDED ≠ DATA_CORRUPTION — exclusão de candle aberto não é corrupção.",
  "PENDING ≠ FAULT — pendente/parcial não é falha (vermelho só para falha genuína).",
  "UNKNOWN ≠ ZERO — desconhecido nunca é apresentado como zero.",
] as const;

export const COLLECTION_DATA_QUALITY_FRESHNESS_DISCLOSURE =
  "Horários e atualizações são ilustrativos (fixture-backed). Desatualizado não implica validação científica nem ativação operacional.";

/**
 * Map quality status → domain lifecycle for shared StatusBadge presentation.
 * SOURCE_UNAVAILABLE is the only status that becomes fault (red).
 */
export function mapQualityStatusToDomain(
  status: CollectionQualityStatus,
): DomainLifecycleState {
  switch (status) {
    case "SOURCE_UNAVAILABLE":
      return "fault";
    case "SERIES_COMPLETE":
      return "complete";
    case "SERIES_PARTIAL":
    case "OPEN_CANDLE_EXCLUDED":
      return "in_progress";
    case "GAPS_PRESENT":
    case "DUPLICATES_PRESENT":
    case "REJECTED_RECORDS_PRESENT":
    case "STALE_STATE":
      return "not_ready";
    case "UNKNOWN_STATE":
    default:
      return "unknown";
  }
}

export function presentQualityStatus(
  status: CollectionQualityStatus,
): QualityStatusPresentation {
  const qualitySeverity = mapQualityStatusToSeverity(status);
  const domainState = mapQualityStatusToDomain(status);
  const mapping = mapDomainStateToPresentation(domainState);
  return {
    qualityStatus: status,
    qualityStatusLabel: COLLECTION_QUALITY_STATUS_LABELS[status],
    qualitySeverity,
    qualitySeverityLabel: COLLECTION_QUALITY_SEVERITY_LABELS[qualitySeverity],
    domainState,
    status: mapping.status,
    presentationSeverity: mapping.severity,
  };
}

export function presentOptionalCount(count: OptionalCount): CountPresentation {
  if (count.availability === "unknown" || count.value === null) {
    return {
      displayText: "Desconhecido",
      availability: count.availability === "unknown" ? "unknown" : count.availability,
      isUnknown: true,
      isZero: false,
    };
  }
  if (
    count.availability === "not_supplied" ||
    count.availability === "not_available"
  ) {
    return {
      displayText: "Não informado",
      availability: count.availability,
      isUnknown: true,
      isZero: false,
    };
  }
  return {
    displayText: String(count.value),
    availability: "available",
    isUnknown: false,
    isZero: count.value === 0,
  };
}

function coverageWindowLabel(series: CollectionSeriesInput): string {
  if (!series.coverageWindowStartIso && !series.coverageWindowEndIso) {
    return "Janela de cobertura desconhecida";
  }
  const start = series.coverageWindowStartIso ?? "—";
  const end = series.coverageWindowEndIso ?? "—";
  return `${start} → ${end}`;
}

function toSeriesViewModel(
  series: CollectionSeriesInput,
  clock: ViewModelClock | null,
): CollectionSeriesViewModel {
  return {
    seriesId: series.seriesId,
    market: series.market,
    asset: series.asset,
    interval: series.interval,
    source: series.source,
    quality: presentQualityStatus(series.qualityStatus),
    sourceState: series.sourceState,
    sourceStateLabel: COLLECTION_SOURCE_STATE_LABELS[series.sourceState],
    coverageWindowLabel: coverageWindowLabel(series),
    expectedRecords: presentOptionalCount(series.expectedRecords),
    acceptedRecords: presentOptionalCount(series.acceptedRecords),
    rejectedRecords: presentOptionalCount(series.rejectedRecords),
    gapCount: presentOptionalCount(series.gapCount),
    duplicateCount: presentOptionalCount(series.duplicateCount),
    openCandleExclusionCount: presentOptionalCount(
      series.openCandleExclusionCount,
    ),
    lastUpdate: presentTimestamp(
      {
        iso: series.lastUpdateIso,
        availability: series.lastUpdateIso ? "available" : "unknown",
      },
      clock,
      { includeRelative: true },
    ),
    findings: series.findings.map((f) => ({ ...f })),
    limitations: [...series.limitations],
    relatedEvidenceIds: [...series.relatedEvidenceIds],
  };
}

export function buildCollectionDataQualityViewModel(
  input: CollectionDataQualityDomainInput,
  criteria: CollectionDataQualityCriteria,
  clock: ViewModelClock | null = null,
): CollectionDataQualityViewModel {
  const filtered = filterAndSortCollectionSeries(
    input.series,
    criteria.filters,
  );
  const seriesVm = filtered.map((entry) => toSeriesViewModel(entry, clock));
  const emptyState = input.series.length === 0;
  const noResultsState = !emptyState && seriesVm.length === 0;
  const hasStaleSeries = seriesVm.some(
    (s) =>
      s.quality.qualityStatus === "STALE_STATE" ||
      s.lastUpdate.freshness === "stale",
  );
  const hasUnknownCounts = seriesVm.some(
    (s) =>
      s.expectedRecords.isUnknown ||
      s.acceptedRecords.isUnknown ||
      s.rejectedRecords.isUnknown ||
      s.gapCount.isUnknown ||
      s.duplicateCount.isUnknown ||
      s.openCandleExclusionCount.isUnknown,
  );

  return deepFreeze({
    pageTitle: COLLECTION_DATA_QUALITY_PAGE_TITLE,
    pageDescription: COLLECTION_DATA_QUALITY_PAGE_DESCRIPTION,
    asOfIso: input.asOfIso,
    illustrativeDisclosure: input.illustrativeDisclosure,
    freshnessDisclosure: COLLECTION_DATA_QUALITY_FRESHNESS_DISCLOSURE,
    aggregateQuality: presentQualityStatus(input.aggregateQualityStatus),
    semanticSafeguards: COLLECTION_DATA_QUALITY_SEMANTIC_SAFEGUARDS,
    knownState: [...input.knownState],
    unknownState: [...input.unknownState],
    aggregateLimitations: [...input.aggregateLimitations],
    nextSafeAction: actionHint(
      "monitor_collection",
      input.nextSafeActionPlainLanguage,
    ),
    relatedEvidence: input.relatedEvidence.map((r) => ({ ...r })),
    filterOptions: buildCollectionFilterOptions(input.series),
    series: seriesVm,
    resultCount: seriesVm.length,
    totalSeriesCount: input.series.length,
    emptyState,
    noResultsState,
    hasStaleSeries,
    hasUnknownCounts,
  });
}
