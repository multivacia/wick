/**
 * Closed enums for Evidence Explorer (UX-R2 I1).
 * Framework-agnostic. No React / router / network imports.
 */

export const EVIDENCE_CLASSES = [
  "release_record",
  "implementation_handoff",
  "impact_assessment",
  "technical_scientific_review",
  "experiment_specification",
  "validation_report",
  "collection_readiness_evidence",
  "operational_debt_record",
] as const;

export type EvidenceClass = (typeof EVIDENCE_CLASSES)[number];

export const EVIDENCE_STALENESS_VALUES = [
  "CURRENT_AS_OF_FIXTURE",
  "HISTORICAL",
  "PENDING_REFRESH",
  "DATE_UNKNOWN",
] as const;

export type EvidenceStaleness = (typeof EVIDENCE_STALENESS_VALUES)[number];

export const EVIDENCE_DATA_ORIGINS = [
  "SYNTHETIC_ILLUSTRATIVE",
  "HISTORICAL_AUDITED",
  "EXPLORATORY_RECORDED",
  "GOVERNANCE_RECORD",
] as const;

export type EvidenceDataOrigin = (typeof EVIDENCE_DATA_ORIGINS)[number];

export const EVIDENCE_SCIENTIFIC_STAGES = [
  "NOT_APPLICABLE",
  "AUDITED_COMPLETE",
  "EXPLORATORY_COMPLETE",
  "PENDING_FUTURE_UNSEEN",
  "BLOCKED",
] as const;

export type EvidenceScientificStage =
  (typeof EVIDENCE_SCIENTIFIC_STAGES)[number];

/** Portuguese labels for UI-facing enum values. */
export const EVIDENCE_CLASS_LABELS: Record<EvidenceClass, string> = {
  release_record: "Registro de release",
  implementation_handoff: "Handoff de implementação",
  impact_assessment: "Avaliação de impacto",
  technical_scientific_review: "Revisão técnico-científica",
  experiment_specification: "Especificação de experimento",
  validation_report: "Relatório de validação",
  collection_readiness_evidence: "Evidência de prontidão de coleta",
  operational_debt_record: "Registro de dívida operacional",
};

export const EVIDENCE_STALENESS_LABELS: Record<EvidenceStaleness, string> = {
  CURRENT_AS_OF_FIXTURE: "Atual conforme fixture",
  HISTORICAL: "Histórico",
  PENDING_REFRESH: "Pendente de atualização",
  DATE_UNKNOWN: "Data desconhecida",
};

export const EVIDENCE_DATA_ORIGIN_LABELS: Record<EvidenceDataOrigin, string> = {
  SYNTHETIC_ILLUSTRATIVE: "Sintético ilustrativo",
  HISTORICAL_AUDITED: "Histórico auditado",
  EXPLORATORY_RECORDED: "Exploratório registrado",
  GOVERNANCE_RECORD: "Registro de governança",
};

export const EVIDENCE_SCIENTIFIC_STAGE_LABELS: Record<
  EvidenceScientificStage,
  string
> = {
  NOT_APPLICABLE: "Não aplicável",
  AUDITED_COMPLETE: "Auditado completo",
  EXPLORATORY_COMPLETE: "Exploratório completo",
  PENDING_FUTURE_UNSEEN: "Pendente dados futuros não vistos",
  BLOCKED: "Bloqueado",
};

export function isEvidenceClass(value: string): value is EvidenceClass {
  return (EVIDENCE_CLASSES as readonly string[]).includes(value);
}

export function isEvidenceStaleness(value: string): value is EvidenceStaleness {
  return (EVIDENCE_STALENESS_VALUES as readonly string[]).includes(value);
}

export function isEvidenceDataOrigin(
  value: string,
): value is EvidenceDataOrigin {
  return (EVIDENCE_DATA_ORIGINS as readonly string[]).includes(value);
}

export function isEvidenceScientificStage(
  value: string,
): value is EvidenceScientificStage {
  return (EVIDENCE_SCIENTIFIC_STAGES as readonly string[]).includes(value);
}
