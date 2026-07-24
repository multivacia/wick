/**
 * UX-R4 I2 — Governed Decision Ledger enums and Portuguese labels.
 * Framework-agnostic. No React / router / network / fixtures.
 */

import type { PresentationStatus } from "./status.js";

export const LEDGER_DISPOSITIONS = [
  "ACCEPTED",
  "AUTHORIZED_WITH_CONDITIONS",
  "BLOCKED",
  "DEFERRED",
  "REJECTED",
  "SUPERSEDED",
  "UNKNOWN",
] as const;

export type LedgerDisposition = (typeof LEDGER_DISPOSITIONS)[number];

export const LEDGER_DOMAINS = [
  "UX_GOVERNANCE",
  "SCIENTIFIC_GOVERNANCE",
  "DATA_QUALITY",
  "OPERATIONAL_GOVERNANCE",
  "RELEASE_GOVERNANCE",
  "ARCHITECTURE",
  "SECURITY",
] as const;

export type LedgerDomain = (typeof LEDGER_DOMAINS)[number];

export const LEDGER_DECISION_TYPES = [
  "SCOPE_DECISION",
  "AUTHORIZATION_DECISION",
  "IMPLEMENTATION_DECISION",
  "REVIEW_DECISION",
  "MERGE_DECISION",
  "RELEASE_ACCEPTANCE_DECISION",
  "DEFERRAL_DECISION",
  "BLOCKING_DECISION",
  "REASSESSMENT_DECISION",
] as const;

export type LedgerDecisionType = (typeof LEDGER_DECISION_TYPES)[number];

export const LEDGER_REASSESSMENT_AVAILABILITY = [
  "available",
  "none",
] as const;

export type LedgerReassessmentAvailability =
  (typeof LEDGER_REASSESSMENT_AVAILABILITY)[number];

export const LEDGER_DISPOSITION_LABELS: Record<LedgerDisposition, string> = {
  ACCEPTED: "Aceita",
  AUTHORIZED_WITH_CONDITIONS: "Autorizada com condições",
  BLOCKED: "Bloqueada",
  DEFERRED: "Adiada",
  REJECTED: "Rejeitada",
  SUPERSEDED: "Substituída",
  UNKNOWN: "Desconhecida",
};

export const LEDGER_DISPOSITION_MEANINGS: Record<LedgerDisposition, string> = {
  ACCEPTED:
    "Escopo ou decisão aceita no limite declarado. Não significa aprovação científica de estratégia.",
  AUTHORIZED_WITH_CONDITIONS:
    "Autorizada com condições explícitas. Não significa implementação concluída.",
  BLOCKED:
    "Bloqueada por dependência ou estado. Não significa falha de sistema.",
  DEFERRED:
    "Adiada conscientemente. Não significa rejeição definitiva.",
  REJECTED:
    "Rejeitada neste contexto. Não significa inválida para sempre.",
  SUPERSEDED:
    "Substituída por decisão posterior. O registro histórico permanece.",
  UNKNOWN:
    "Indisponível ou não inventado. Desconhecido nunca é zero.",
};

export const LEDGER_DOMAIN_LABELS: Record<LedgerDomain, string> = {
  UX_GOVERNANCE: "Governança UX",
  SCIENTIFIC_GOVERNANCE: "Governança científica",
  DATA_QUALITY: "Qualidade de dados",
  OPERATIONAL_GOVERNANCE: "Governança operacional",
  RELEASE_GOVERNANCE: "Governança de release",
  ARCHITECTURE: "Arquitetura",
  SECURITY: "Segurança",
};

export const LEDGER_DECISION_TYPE_LABELS: Record<LedgerDecisionType, string> = {
  SCOPE_DECISION: "Decisão de escopo",
  AUTHORIZATION_DECISION: "Decisão de autorização",
  IMPLEMENTATION_DECISION: "Decisão de implementação",
  REVIEW_DECISION: "Decisão de revisão",
  MERGE_DECISION: "Decisão de merge",
  RELEASE_ACCEPTANCE_DECISION: "Aceitação de release",
  DEFERRAL_DECISION: "Decisão de adiamento",
  BLOCKING_DECISION: "Decisão de bloqueio",
  REASSESSMENT_DECISION: "Decisão de reavaliação",
};

export const LEDGER_REASSESSMENT_AVAILABILITY_LABELS: Record<
  LedgerReassessmentAvailability,
  string
> = {
  available: "Com gatilho de reavaliação",
  none: "Sem gatilho de reavaliação",
};

/**
 * Disposition → StatusBadge presentation.
 * Red/fault is never used for process dispositions.
 */
export function mapDispositionToPresentation(
  disposition: LedgerDisposition,
): PresentationStatus {
  switch (disposition) {
    case "ACCEPTED":
      return "completed";
    case "AUTHORIZED_WITH_CONDITIONS":
    case "SUPERSEDED":
      return "informational";
    case "BLOCKED":
      return "blocked";
    case "DEFERRED":
      return "deferred";
    case "REJECTED":
      return "attention";
    case "UNKNOWN":
    default:
      return "unknown";
  }
}

export function isLedgerDisposition(value: string): value is LedgerDisposition {
  return (LEDGER_DISPOSITIONS as readonly string[]).includes(value);
}

export function isLedgerDomain(value: string): value is LedgerDomain {
  return (LEDGER_DOMAINS as readonly string[]).includes(value);
}

export function isLedgerDecisionType(value: string): value is LedgerDecisionType {
  return (LEDGER_DECISION_TYPES as readonly string[]).includes(value);
}
