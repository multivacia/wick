/**
 * Pure filter/sort helpers for Collection Data Quality.
 * Severity fault > warning > informational, then lastUpdate descending.
 */

import {
  COLLECTION_QUALITY_SEVERITIES,
  COLLECTION_QUALITY_SEVERITY_LABELS,
  COLLECTION_QUALITY_STATUS_LABELS,
  COLLECTION_QUALITY_STATUSES,
  QUALITY_SEVERITY_RANK,
  mapQualityStatusToSeverity,
  type CollectionQualitySeverity,
  type CollectionQualityStatus,
} from "./collectionDataQualityEnums.js";
import type {
  CollectionDataQualityFilterOptions,
  CollectionDataQualityFilters,
  CollectionSeriesInput,
} from "./collectionDataQualityTypes.js";

export function matchesCollectionFilters(
  series: CollectionSeriesInput,
  filters: CollectionDataQualityFilters,
): boolean {
  if (filters.seriesId && series.seriesId !== filters.seriesId) {
    return false;
  }
  if (filters.market && series.market !== filters.market) {
    return false;
  }
  if (filters.interval && series.interval !== filters.interval) {
    return false;
  }
  if (filters.qualityStatus && series.qualityStatus !== filters.qualityStatus) {
    return false;
  }
  if (
    filters.severity &&
    mapQualityStatusToSeverity(series.qualityStatus) !== filters.severity
  ) {
    return false;
  }
  return true;
}

export function sortCollectionSeries(
  series: readonly CollectionSeriesInput[],
): CollectionSeriesInput[] {
  return series.slice().sort((a, b) => {
    const sevA = QUALITY_SEVERITY_RANK[mapQualityStatusToSeverity(a.qualityStatus)];
    const sevB = QUALITY_SEVERITY_RANK[mapQualityStatusToSeverity(b.qualityStatus)];
    if (sevA !== sevB) return sevA - sevB;
    const dateA = a.lastUpdateIso ?? "";
    const dateB = b.lastUpdateIso ?? "";
    if (dateA !== dateB) return dateB.localeCompare(dateA);
    return a.seriesId.localeCompare(b.seriesId);
  });
}

export function filterAndSortCollectionSeries(
  series: readonly CollectionSeriesInput[],
  filters: CollectionDataQualityFilters,
): CollectionSeriesInput[] {
  return sortCollectionSeries(
    series.filter((entry) => matchesCollectionFilters(entry, filters)),
  );
}

export function clearCollectionFilters(): CollectionDataQualityFilters {
  return {};
}

export function emptyCollectionCriteria() {
  return { filters: clearCollectionFilters() };
}

function uniqueSorted(values: readonly string[]): string[] {
  return Array.from(new Set(values)).sort((a, b) => a.localeCompare(b));
}

export function buildCollectionFilterOptions(
  series: readonly CollectionSeriesInput[],
): CollectionDataQualityFilterOptions {
  return {
    seriesIds: uniqueSorted(series.map((s) => s.seriesId)).map((value) => ({
      value,
      label: value,
    })),
    markets: uniqueSorted(series.map((s) => s.market)).map((value) => ({
      value,
      label: value,
    })),
    intervals: uniqueSorted(series.map((s) => s.interval)).map((value) => ({
      value,
      label: value,
    })),
    qualityStatuses: COLLECTION_QUALITY_STATUSES.map(
      (value: CollectionQualityStatus) => ({
        value,
        label: COLLECTION_QUALITY_STATUS_LABELS[value],
      }),
    ),
    severities: COLLECTION_QUALITY_SEVERITIES.map(
      (value: CollectionQualitySeverity) => ({
        value,
        label: COLLECTION_QUALITY_SEVERITY_LABELS[value],
      }),
    ),
  };
}
