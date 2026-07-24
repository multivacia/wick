/**
 * Pure filter/sort helpers for Governed Decision Ledger.
 * Default sort: decision_date DESC, decision_id ASC — not severity-first.
 */

import {
  LEDGER_DECISION_TYPE_LABELS,
  LEDGER_DECISION_TYPES,
  LEDGER_DISPOSITION_LABELS,
  LEDGER_DISPOSITIONS,
  LEDGER_DOMAIN_LABELS,
  LEDGER_DOMAINS,
  LEDGER_REASSESSMENT_AVAILABILITY_LABELS,
  type LedgerDecisionType,
  type LedgerDisposition,
  type LedgerDomain,
  type LedgerReassessmentAvailability,
} from "./governedDecisionLedgerEnums.js";
import type {
  GovernedDecisionLedgerFilterOptions,
  GovernedDecisionLedgerFilters,
  GovernedDecisionRecordInput,
} from "./governedDecisionLedgerTypes.js";

export function hasReassessmentTrigger(
  record: GovernedDecisionRecordInput,
): boolean {
  return Boolean(record.reassessmentTrigger?.trim());
}

export function matchesLedgerFilters(
  record: GovernedDecisionRecordInput,
  filters: GovernedDecisionLedgerFilters,
): boolean {
  if (filters.disposition && record.disposition !== filters.disposition) {
    return false;
  }
  if (filters.domain && record.domain !== filters.domain) {
    return false;
  }
  if (filters.release && record.relatedRelease !== filters.release) {
    return false;
  }
  if (filters.decisionType && record.decisionType !== filters.decisionType) {
    return false;
  }
  if (filters.reassessmentAvailability) {
    const available = hasReassessmentTrigger(record);
    if (filters.reassessmentAvailability === "available" && !available) {
      return false;
    }
    if (filters.reassessmentAvailability === "none" && available) {
      return false;
    }
  }
  return true;
}

/**
 * Sort by decision_date DESC (UNKNOWN dates sort last), then decision_id ASC.
 * Intentionally not severity-first — blocked must not look “more scientific”.
 */
export function sortLedgerRecords(
  records: readonly GovernedDecisionRecordInput[],
): GovernedDecisionRecordInput[] {
  return records.slice().sort((a, b) => {
    const unknownA = a.decisionDate === "UNKNOWN";
    const unknownB = b.decisionDate === "UNKNOWN";
    if (unknownA !== unknownB) return unknownA ? 1 : -1;
    if (!unknownA && a.decisionDate !== b.decisionDate) {
      return b.decisionDate.localeCompare(a.decisionDate);
    }
    return a.decisionId.localeCompare(b.decisionId);
  });
}

export function filterAndSortLedgerRecords(
  records: readonly GovernedDecisionRecordInput[],
  filters: GovernedDecisionLedgerFilters,
): GovernedDecisionRecordInput[] {
  return sortLedgerRecords(
    records.filter((entry) => matchesLedgerFilters(entry, filters)),
  );
}

export function clearLedgerFilters(): GovernedDecisionLedgerFilters {
  return {};
}

export function emptyLedgerCriteria() {
  return { filters: clearLedgerFilters(), selectedDecisionId: null as string | null };
}

function uniqueSorted(values: readonly string[]): string[] {
  return Array.from(new Set(values.filter(Boolean))).sort((a, b) =>
    a.localeCompare(b),
  );
}

export function buildLedgerFilterOptions(
  records: readonly GovernedDecisionRecordInput[],
): GovernedDecisionLedgerFilterOptions {
  const releases = uniqueSorted(
    records.map((r) => r.relatedRelease).filter((v): v is string => Boolean(v)),
  );

  return {
    dispositions: LEDGER_DISPOSITIONS.map((value: LedgerDisposition) => ({
      value,
      label: LEDGER_DISPOSITION_LABELS[value],
    })),
    domains: LEDGER_DOMAINS.map((value: LedgerDomain) => ({
      value,
      label: LEDGER_DOMAIN_LABELS[value],
    })),
    releases: releases.map((value) => ({ value, label: value })),
    decisionTypes: LEDGER_DECISION_TYPES.map((value: LedgerDecisionType) => ({
      value,
      label: LEDGER_DECISION_TYPE_LABELS[value],
    })),
    reassessmentAvailability: (
      [
        "available",
        "none",
      ] as const satisfies readonly LedgerReassessmentAvailability[]
    ).map((value) => ({
      value,
      label: LEDGER_REASSESSMENT_AVAILABILITY_LABELS[value],
    })),
  };
}
