/**
 * UX-R3 I1 — Collection Data Quality enums and labels.
 * Framework-agnostic. No React / router / network / fixtures.
 */

export const COLLECTION_QUALITY_STATUSES = [
  "SERIES_COMPLETE",
  "SERIES_PARTIAL",
  "GAPS_PRESENT",
  "DUPLICATES_PRESENT",
  "REJECTED_RECORDS_PRESENT",
  "OPEN_CANDLE_EXCLUDED",
  "SOURCE_UNAVAILABLE",
  "STALE_STATE",
  "UNKNOWN_STATE",
] as const;

export type CollectionQualityStatus =
  (typeof COLLECTION_QUALITY_STATUSES)[number];

export const COLLECTION_QUALITY_SEVERITIES = [
  "informational",
  "warning",
  "fault",
] as const;

export type CollectionQualitySeverity =
  (typeof COLLECTION_QUALITY_SEVERITIES)[number];

export const COLLECTION_SOURCE_STATES = [
  "available",
  "degraded",
  "unavailable",
  "unknown",
] as const;

export type CollectionSourceState = (typeof COLLECTION_SOURCE_STATES)[number];

export const COLLECTION_QUALITY_STATUS_LABELS: Record<
  CollectionQualityStatus,
  string
> = {
  SERIES_COMPLETE: "Série completa (cobertura ilustrativa)",
  SERIES_PARTIAL: "Série parcial",
  GAPS_PRESENT: "Lacunas presentes",
  DUPLICATES_PRESENT: "Duplicatas presentes",
  REJECTED_RECORDS_PRESENT: "Registros rejeitados",
  OPEN_CANDLE_EXCLUDED: "Candle aberto excluído",
  SOURCE_UNAVAILABLE: "Fonte indisponível",
  STALE_STATE: "Estado desatualizado",
  UNKNOWN_STATE: "Estado desconhecido",
};

export const COLLECTION_QUALITY_SEVERITY_LABELS: Record<
  CollectionQualitySeverity,
  string
> = {
  informational: "Informativo",
  warning: "Atenção",
  fault: "Falha",
};

export const COLLECTION_SOURCE_STATE_LABELS: Record<
  CollectionSourceState,
  string
> = {
  available: "Disponível",
  degraded: "Degradado",
  unavailable: "Indisponível",
  unknown: "Desconhecido",
};

/**
 * Auth severity model: red (fault) only for genuine source unavailability.
 * Gaps, duplicates, rejected, open-candle, partial, stale, unknown ≠ fault.
 */
export function mapQualityStatusToSeverity(
  status: CollectionQualityStatus,
): CollectionQualitySeverity {
  switch (status) {
    case "SOURCE_UNAVAILABLE":
      return "fault";
    case "GAPS_PRESENT":
    case "DUPLICATES_PRESENT":
    case "REJECTED_RECORDS_PRESENT":
    case "STALE_STATE":
    case "SERIES_PARTIAL":
      return "warning";
    case "SERIES_COMPLETE":
    case "OPEN_CANDLE_EXCLUDED":
      return "informational";
    case "UNKNOWN_STATE":
    default:
      return "informational";
  }
}

export const QUALITY_SEVERITY_RANK: Record<CollectionQualitySeverity, number> =
  {
    fault: 0,
    warning: 1,
    informational: 2,
  };

export function isCollectionQualityStatus(
  value: string,
): value is CollectionQualityStatus {
  return (COLLECTION_QUALITY_STATUSES as readonly string[]).includes(value);
}

export function isCollectionQualitySeverity(
  value: string,
): value is CollectionQualitySeverity {
  return (COLLECTION_QUALITY_SEVERITIES as readonly string[]).includes(value);
}

export function isCollectionSourceState(
  value: string,
): value is CollectionSourceState {
  return (COLLECTION_SOURCE_STATES as readonly string[]).includes(value);
}
