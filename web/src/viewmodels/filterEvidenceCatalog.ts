/**
 * Pure filter/search helpers for Evidence Explorer.
 * Case-insensitive trim search; closed filters combine with AND; no regex.
 */

import type { EvidenceCatalogStanding } from "./evidenceEnums.js";
import type {
  EvidenceCatalogEntryInput,
  EvidenceExplorerFilters,
} from "./evidenceExplorerTypes.js";

const STANDING_RANK: Record<EvidenceCatalogStanding, number> = {
  current: 0,
  pending: 1,
  historical: 2,
  superseded: 3,
};

const SEARCH_FIELDS: Array<keyof EvidenceCatalogEntryInput> = [
  "title",
  "evidenceClass",
  "release",
  "increment",
  "experimentId",
  "status",
  "dataOrigin",
  "scientificStage",
  "summary",
];

function fieldText(
  entry: EvidenceCatalogEntryInput,
  field: keyof EvidenceCatalogEntryInput,
): string {
  const value = entry[field];
  if (value === null || value === undefined) {
    return "";
  }
  if (Array.isArray(value)) {
    return value.join(" ");
  }
  return String(value);
}

export function matchesEvidenceSearch(
  entry: EvidenceCatalogEntryInput,
  searchQuery: string,
): boolean {
  const needle = searchQuery.trim().toLowerCase();
  if (!needle) {
    return true;
  }
  return SEARCH_FIELDS.some((field) =>
    fieldText(entry, field).toLowerCase().includes(needle),
  );
}

export function matchesEvidenceFilters(
  entry: EvidenceCatalogEntryInput,
  filters: EvidenceExplorerFilters,
): boolean {
  if (filters.evidenceClass && entry.evidenceClass !== filters.evidenceClass) {
    return false;
  }
  if (filters.release && entry.release !== filters.release) {
    return false;
  }
  if (filters.status && entry.status !== filters.status) {
    return false;
  }
  if (filters.dataOrigin && entry.dataOrigin !== filters.dataOrigin) {
    return false;
  }
  if (
    filters.scientificStage &&
    entry.scientificStage !== filters.scientificStage
  ) {
    return false;
  }
  if (filters.staleness && entry.staleness !== filters.staleness) {
    return false;
  }
  if (
    filters.catalogStanding &&
    entry.catalogStanding !== filters.catalogStanding
  ) {
    return false;
  }
  return true;
}

export function filterEvidenceEntries(
  entries: readonly EvidenceCatalogEntryInput[],
  searchQuery: string,
  filters: EvidenceExplorerFilters,
): EvidenceCatalogEntryInput[] {
  return entries
    .filter(
      (entry) =>
        matchesEvidenceSearch(entry, searchQuery) &&
        matchesEvidenceFilters(entry, filters),
    )
    .slice()
    .sort((a, b) => {
      const rankA = STANDING_RANK[a.catalogStanding] ?? 99;
      const rankB = STANDING_RANK[b.catalogStanding] ?? 99;
      if (rankA !== rankB) return rankA - rankB;
      const dateA = a.createdAtOrUnknown ?? "";
      const dateB = b.createdAtOrUnknown ?? "";
      if (dateA !== dateB) return dateB.localeCompare(dateA);
      return a.evidenceId.localeCompare(b.evidenceId);
    });
}

export function clearEvidenceFilters(): EvidenceExplorerFilters {
  return {};
}

export function emptyEvidenceCriteria(selectedEvidenceId?: string | null) {
  return {
    searchQuery: "",
    filters: clearEvidenceFilters(),
    selectedEvidenceId: selectedEvidenceId ?? null,
  };
}
