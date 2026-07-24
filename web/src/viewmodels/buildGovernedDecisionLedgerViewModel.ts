/**
 * UX-R4 I2 — Governed Decision Ledger ViewModel builder.
 * Pure, screen-agnostic. No React / fixtures / network.
 */

import {
  LEDGER_DECISION_TYPE_LABELS,
  LEDGER_DISPOSITION_LABELS,
  LEDGER_DISPOSITION_MEANINGS,
  LEDGER_DOMAIN_LABELS,
  mapDispositionToPresentation,
  type LedgerDisposition,
} from "./governedDecisionLedgerEnums.js";
import type {
  GovernedDecisionLedgerCriteria,
  GovernedDecisionLedgerDomainInput,
  GovernedDecisionLedgerViewModel,
  GovernedDecisionRecordInput,
  GovernedDecisionRecordViewModel,
  LedgerDispositionPresentation,
  LedgerSummaryCounts,
} from "./governedDecisionLedgerTypes.js";
import {
  buildLedgerFilterOptions,
  filterAndSortLedgerRecords,
} from "./filterGovernedDecisionLedger.js";
import { deepFreeze } from "./helpers.js";
import { presentTimestamp } from "./time.js";

export const GOVERNED_DECISION_LEDGER_SECTION_TITLE = "Livro de decisões governadas";

export const GOVERNED_DECISION_LEDGER_SECTION_DESCRIPTION =
  "Registro ilustrativo, curado e somente leitura das decisões governadas — não é backlog, fluxo de aprovação nem resultado científico.";

export const GOVERNED_DECISION_LEDGER_SEMANTIC_SAFEGUARDS = [
  "ACCEPTED ≠ SCIENTIFIC_APPROVAL — aceitar escopo UX não aprova estratégia de trading.",
  "AUTHORIZED_WITH_CONDITIONS ≠ IMPLEMENTED — autorização condicionada não é implementação.",
  "BLOCKED ≠ SYSTEM_FAILURE — bloqueio de governança não é falha de sistema.",
  "DEFERRED ≠ REJECTED — adiamento consciente não é rejeição.",
  "REJECTED ≠ INVALID_FOREVER — rejeição neste contexto não invalida para sempre.",
  "SUPERSEDED ≠ DELETED — substituída permanece como histórico.",
  "UNKNOWN ≠ ZERO — desconhecido nunca é apresentado como zero.",
  "PENDING ≠ FAULT — pendente não é falha (vermelho só para falha genuína).",
  "ledger record ≠ scientific result — registro do livro ≠ resultado científico.",
  "evidence link ≠ validated edge — link de evidência ≠ vantagem validada.",
  "reassessment trigger ≠ permission — gatilho descritivo ≠ permissão automática.",
  "blocked scientific R4 ≠ UX failure — R4 científico bloqueado ≠ falha de UX.",
] as const;

export const GOVERNED_DECISION_LEDGER_FRESHNESS_DISCLOSURE =
  "Horários do livro são curados e ilustrativos (fixture_authored_at / catalog_curated_at). Não implicam atualização ao vivo nem polling do repositório.";

const DECISION_ID_PATTERN = /^dec-[a-z0-9-]+$/;

export class InvalidGovernedDecisionLedgerError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "InvalidGovernedDecisionLedgerError";
  }
}

export function assertValidDecisionId(decisionId: string): void {
  if (!DECISION_ID_PATTERN.test(decisionId)) {
    throw new InvalidGovernedDecisionLedgerError(
      `decision_id must match dec-*: ${decisionId}`,
    );
  }
}

export function assertValidEvidenceId(evidenceId: string): void {
  const trimmed = evidenceId.trim();
  if (!trimmed) {
    throw new InvalidGovernedDecisionLedgerError("evidenceId is empty");
  }
  if (/^https?:\/\//i.test(trimmed)) {
    throw new InvalidGovernedDecisionLedgerError(
      `external URL evidenceId forbidden: ${evidenceId}`,
    );
  }
  if (trimmed.includes("..") || trimmed.startsWith("/") || trimmed.startsWith("\\")) {
    throw new InvalidGovernedDecisionLedgerError(
      `unsafe evidenceId path: ${evidenceId}`,
    );
  }
}

export function presentDisposition(
  disposition: LedgerDisposition,
): LedgerDispositionPresentation {
  return {
    disposition,
    dispositionLabel: LEDGER_DISPOSITION_LABELS[disposition],
    dispositionMeaning: LEDGER_DISPOSITION_MEANINGS[disposition],
    status: mapDispositionToPresentation(disposition),
  };
}

function presentDecisionDate(decisionDate: string): {
  display: string;
  isUnknown: boolean;
} {
  if (decisionDate === "UNKNOWN") {
    return { display: "Desconhecida", isUnknown: true };
  }
  return { display: decisionDate, isUnknown: false };
}

function buildRecordViewModel(
  record: GovernedDecisionRecordInput,
): GovernedDecisionRecordViewModel {
  assertValidDecisionId(record.decisionId);
  if (!record.isIllustrative) {
    throw new InvalidGovernedDecisionLedgerError(
      `is_illustrative must be true: ${record.decisionId}`,
    );
  }
  for (const ref of record.evidenceRefs) {
    assertValidEvidenceId(ref.evidenceId);
  }
  if (record.primaryEvidenceRef) {
    assertValidEvidenceId(record.primaryEvidenceRef.evidenceId);
  }

  const date = presentDecisionDate(record.decisionDate);
  const conditions = record.conditions ?? [];
  const trigger = record.reassessmentTrigger?.trim()
    ? record.reassessmentTrigger.trim()
    : null;

  return {
    decisionId: record.decisionId,
    title: record.title,
    summary: record.summary,
    domain: record.domain,
    domainLabel: LEDGER_DOMAIN_LABELS[record.domain],
    decisionType: record.decisionType,
    decisionTypeLabel: LEDGER_DECISION_TYPE_LABELS[record.decisionType],
    disposition: presentDisposition(record.disposition),
    decisionDateDisplay: date.display,
    decisionDateIsUnknown: date.isUnknown,
    scope: record.scope,
    rationale: record.rationale,
    evidenceRefs: record.evidenceRefs.map((r) => ({ ...r })),
    primaryEvidenceRef: record.primaryEvidenceRef
      ? { ...record.primaryEvidenceRef }
      : record.evidenceRefs[0]
        ? { ...record.evidenceRefs[0] }
        : null,
    mustNotInfer: [...record.mustNotInfer],
    reassessmentTrigger: trigger,
    hasReassessmentTrigger: trigger !== null,
    nextGovernedAction: record.nextGovernedAction,
    conditions: [...conditions],
    hasConditions: conditions.length > 0,
    relatedRelease: record.relatedRelease ?? null,
    relatedIncrement: record.relatedIncrement ?? null,
    scientificBoundary: record.scientificBoundary ?? null,
    operationalBoundary: record.operationalBoundary ?? null,
    supersedes: record.supersedes ?? null,
    supersededBy: record.supersededBy ?? null,
    isSuperseded:
      record.disposition === "SUPERSEDED" || Boolean(record.supersededBy),
    sourceArtifact: record.sourceArtifact ?? null,
    fixtureAuthoredAtDisplay:
      presentTimestamp(
        { iso: record.fixtureAuthoredAt, availability: "available" },
        { nowIso: record.catalogCuratedAt },
      ).displayText ?? record.fixtureAuthoredAt,
    catalogCuratedAtDisplay:
      presentTimestamp(
        { iso: record.catalogCuratedAt, availability: "available" },
        { nowIso: record.catalogCuratedAt },
      ).displayText ?? record.catalogCuratedAt,
    effectiveDateDisplay: record.effectiveDate
      ? presentDecisionDate(record.effectiveDate).display
      : null,
    isIllustrative: true,
  };
}

function buildCounts(
  all: readonly GovernedDecisionRecordInput[],
  filtered: readonly GovernedDecisionRecordInput[],
): LedgerSummaryCounts {
  return {
    acceptedCount: all.filter((r) => r.disposition === "ACCEPTED").length,
    blockedCount: all.filter((r) => r.disposition === "BLOCKED").length,
    triggerCount: all.filter((r) => Boolean(r.reassessmentTrigger?.trim()))
      .length,
    unknownDispositionCount: all.filter((r) => r.disposition === "UNKNOWN")
      .length,
    totalCount: all.length,
    resultCount: filtered.length,
  };
}

export function buildGovernedDecisionLedgerViewModel(
  input: GovernedDecisionLedgerDomainInput,
  criteria: GovernedDecisionLedgerCriteria,
): GovernedDecisionLedgerViewModel {
  const filtered = filterAndSortLedgerRecords(input.records, criteria.filters);
  const recordVms = filtered.map(buildRecordViewModel);
  const selectedId = criteria.selectedDecisionId ?? null;
  const selectedRecord =
    selectedId === null
      ? null
      : (recordVms.find((r) => r.decisionId === selectedId) ?? null);

  const hasUnknownDisposition = input.records.some(
    (r) => r.disposition === "UNKNOWN",
  );
  const hasUnknownDate = input.records.some((r) => r.decisionDate === "UNKNOWN");

  const vm: GovernedDecisionLedgerViewModel = {
    sectionTitle: GOVERNED_DECISION_LEDGER_SECTION_TITLE,
    sectionDescription: GOVERNED_DECISION_LEDGER_SECTION_DESCRIPTION,
    illustrativeDisclosure: input.illustrativeDisclosure,
    freshnessDisclosure: GOVERNED_DECISION_LEDGER_FRESHNESS_DISCLOSURE,
    staleFixtureState: input.freshness === "stale",
    staleDisclosure:
      input.freshness === "stale" ? input.staleDisclosure : null,
    unknownStateNotice:
      hasUnknownDisposition || hasUnknownDate
        ? "Há disposições ou datas desconhecidas no livro. Desconhecido ≠ zero e não é inventado."
        : null,
    semanticSafeguards: GOVERNED_DECISION_LEDGER_SEMANTIC_SAFEGUARDS,
    counts: buildCounts(input.records, filtered),
    filterOptions: buildLedgerFilterOptions(input.records),
    records: recordVms,
    selectedRecord,
    emptyState: input.records.length === 0,
    noResultsState: input.records.length > 0 && filtered.length === 0,
    catalogCuratedAtDisplay:
      presentTimestamp(
        { iso: input.catalogCuratedAt, availability: "available" },
        { nowIso: input.catalogCuratedAt },
      ).displayText ?? input.catalogCuratedAt,
    fixtureAuthoredAtDisplay:
      presentTimestamp(
        { iso: input.fixtureAuthoredAt, availability: "available" },
        { nowIso: input.catalogCuratedAt },
      ).displayText ?? input.fixtureAuthoredAt,
    fixtureVersion: 1,
  };

  return deepFreeze(vm);
}
