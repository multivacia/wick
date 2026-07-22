/**
 * UX-R3 I1 — standalone curated Collection Data Quality fixture.
 * Synthetic/illustrative metadata only. No runtime FS / network / FU payloads.
 */

import { fixtureMetadata, type FixtureMetadata } from "./metadata.js";
import type { CollectionDataQualityDomainInput } from "../viewmodels/collectionDataQualityTypes.js";
import {
  isCollectionQualitySeverity,
  isCollectionQualityStatus,
  isCollectionSourceState,
} from "../viewmodels/collectionDataQualityEnums.js";

export const COLLECTION_DATA_QUALITY_FIXTURE_ID =
  "collection_data_quality_current_state_illustrative" as const;

export const COLLECTION_DATA_QUALITY_NOW_ISO = "2026-07-22T18:00:00.000Z";

const SERIES: CollectionDataQualityDomainInput["series"] = [
  {
    seriesId: "btc-usdt-1h-binance",
    market: "crypto",
    asset: "BTC-USDT",
    interval: "1h",
    source: "binance-public-illustrative",
    qualityStatus: "SERIES_COMPLETE",
    sourceState: "available",
    coverageWindowStartIso: "2026-07-01T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-21T23:00:00.000Z",
    expectedRecords: { value: 504, availability: "available" },
    acceptedRecords: { value: 504, availability: "available" },
    rejectedRecords: { value: 0, availability: "available" },
    gapCount: { value: 0, availability: "available" },
    duplicateCount: { value: 0, availability: "available" },
    openCandleExclusionCount: { value: 1, availability: "available" },
    lastUpdateIso: "2026-07-22T17:05:00.000Z",
    findings: [
      {
        code: "COVERAGE_OK",
        severity: "informational",
        message:
          "Cobertura ilustrativa completa para a janela representada. Não implica janela futura científica completa.",
      },
    ],
    limitations: [
      "Cobertura completa ≠ FUTURE_WINDOW_COMPLETE",
      "Não autoriza validação científica",
    ],
    relatedEvidenceIds: ["ev-fu-collection-readiness"],
  },
  {
    seriesId: "eth-usdt-1h-binance",
    market: "crypto",
    asset: "ETH-USDT",
    interval: "1h",
    source: "binance-public-illustrative",
    qualityStatus: "SERIES_PARTIAL",
    sourceState: "available",
    coverageWindowStartIso: "2026-07-01T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-18T12:00:00.000Z",
    expectedRecords: { value: 420, availability: "available" },
    acceptedRecords: { value: 390, availability: "available" },
    rejectedRecords: { value: 4, availability: "available" },
    gapCount: { value: 0, availability: "available" },
    duplicateCount: { value: 0, availability: "available" },
    openCandleExclusionCount: { value: 1, availability: "available" },
    lastUpdateIso: "2026-07-22T16:40:00.000Z",
    findings: [
      {
        code: "PARTIAL_COVERAGE",
        severity: "warning",
        message:
          "Série parcial: cobertura ilustrativa incompleta. Parcial ≠ falha da coleta.",
      },
    ],
    limitations: ["Série parcial não bloqueia monitoramento ilustrativo"],
    relatedEvidenceIds: ["ev-fu-collection-readiness"],
  },
  {
    seriesId: "btc-usdt-15m-binance",
    market: "crypto",
    asset: "BTC-USDT",
    interval: "15m",
    source: "binance-public-illustrative",
    qualityStatus: "GAPS_PRESENT",
    sourceState: "degraded",
    coverageWindowStartIso: "2026-07-10T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-22T12:00:00.000Z",
    expectedRecords: { value: 1200, availability: "available" },
    acceptedRecords: { value: 1172, availability: "available" },
    rejectedRecords: { value: 0, availability: "available" },
    gapCount: { value: 3, availability: "available" },
    duplicateCount: { value: 0, availability: "available" },
    openCandleExclusionCount: { value: 1, availability: "available" },
    lastUpdateIso: "2026-07-22T15:10:00.000Z",
    findings: [
      {
        code: "GAP_PRESENT",
        severity: "warning",
        message:
          "Lacunas ilustrativas detectadas. GAP_PRESENT ≠ COLLECTION_FAILED.",
      },
    ],
    limitations: ["Lacunas ilustrativas não implicam corrupção de dados"],
    relatedEvidenceIds: ["ev-r3e-pending-future-unseen"],
  },
  {
    seriesId: "sol-usdt-1h-binance",
    market: "crypto",
    asset: "SOL-USDT",
    interval: "1h",
    source: "binance-public-illustrative",
    qualityStatus: "DUPLICATES_PRESENT",
    sourceState: "available",
    coverageWindowStartIso: "2026-07-05T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-21T00:00:00.000Z",
    expectedRecords: { value: 384, availability: "available" },
    acceptedRecords: { value: 382, availability: "available" },
    rejectedRecords: { value: 0, availability: "available" },
    gapCount: { value: 0, availability: "available" },
    duplicateCount: { value: 2, availability: "available" },
    openCandleExclusionCount: { value: 1, availability: "available" },
    lastUpdateIso: "2026-07-22T14:20:00.000Z",
    findings: [
      {
        code: "DUPLICATES_PRESENT",
        severity: "warning",
        message: "Duplicatas ilustrativas presentes — atenção, não falha vermelha.",
      },
    ],
    limitations: ["Duplicatas ilustrativas exigem revisão, não ativação"],
    relatedEvidenceIds: ["ev-fu-collection-readiness"],
  },
  {
    seriesId: "ada-usdt-1h-binance",
    market: "crypto",
    asset: "ADA-USDT",
    interval: "1h",
    source: "binance-public-illustrative",
    qualityStatus: "REJECTED_RECORDS_PRESENT",
    sourceState: "available",
    coverageWindowStartIso: "2026-07-08T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-20T00:00:00.000Z",
    expectedRecords: { value: 288, availability: "available" },
    acceptedRecords: { value: 275, availability: "available" },
    rejectedRecords: { value: 13, availability: "available" },
    gapCount: { value: 0, availability: "available" },
    duplicateCount: { value: 0, availability: "available" },
    openCandleExclusionCount: { value: 1, availability: "available" },
    lastUpdateIso: "2026-07-22T13:55:00.000Z",
    findings: [
      {
        code: "REJECTED_RECORDS",
        severity: "warning",
        message:
          "Registros rejeitados ilustrativos. Rejeição ≠ corrupção automática.",
      },
    ],
    limitations: ["Rejeições ilustrativas não autorizam correção operacional aqui"],
    relatedEvidenceIds: ["ev-fu-collection-readiness"],
  },
  {
    seriesId: "xrp-usdt-1h-binance",
    market: "crypto",
    asset: "XRP-USDT",
    interval: "1h",
    source: "binance-public-illustrative",
    qualityStatus: "OPEN_CANDLE_EXCLUDED",
    sourceState: "available",
    coverageWindowStartIso: "2026-07-12T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-22T16:00:00.000Z",
    expectedRecords: { value: 256, availability: "available" },
    acceptedRecords: { value: 255, availability: "available" },
    rejectedRecords: { value: 0, availability: "available" },
    gapCount: { value: 0, availability: "available" },
    duplicateCount: { value: 0, availability: "available" },
    openCandleExclusionCount: { value: 1, availability: "available" },
    lastUpdateIso: "2026-07-22T17:00:00.000Z",
    findings: [
      {
        code: "OPEN_CANDLE_EXCLUDED",
        severity: "informational",
        message:
          "Candle aberto excluído por política (somente fechados). OPEN_CANDLE_EXCLUDED ≠ DATA_CORRUPTION.",
      },
    ],
    limitations: ["Somente candles fechados entram na série ilustrativa"],
    relatedEvidenceIds: ["ev-r3e-pending-future-unseen"],
  },
  {
    seriesId: "dot-usdt-1h-kraken",
    market: "crypto",
    asset: "DOT-USDT",
    interval: "1h",
    source: "kraken-public-illustrative",
    qualityStatus: "SOURCE_UNAVAILABLE",
    sourceState: "unavailable",
    coverageWindowStartIso: "2026-07-01T00:00:00.000Z",
    coverageWindowEndIso: null,
    expectedRecords: { value: 200, availability: "available" },
    acceptedRecords: { value: 120, availability: "available" },
    rejectedRecords: { value: 0, availability: "available" },
    gapCount: { value: 8, availability: "available" },
    duplicateCount: { value: 0, availability: "available" },
    openCandleExclusionCount: { value: 0, availability: "available" },
    lastUpdateIso: "2026-07-20T09:00:00.000Z",
    findings: [
      {
        code: "SOURCE_UNAVAILABLE",
        severity: "fault",
        message:
          "Fonte ilustrativa indisponível — única severidade de falha (vermelho) neste modelo.",
      },
    ],
    limitations: [
      "Falha de fonte ilustrativa ≠ prontidão científica",
      "Não aciona coleta nem scheduler nesta tela",
    ],
    relatedEvidenceIds: ["ev-r3e-pending-future-unseen"],
  },
  {
    seriesId: "link-usdt-4h-binance",
    market: "crypto",
    asset: "LINK-USDT",
    interval: "4h",
    source: "binance-public-illustrative",
    qualityStatus: "STALE_STATE",
    sourceState: "degraded",
    coverageWindowStartIso: "2026-06-01T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-15T00:00:00.000Z",
    expectedRecords: { value: 270, availability: "available" },
    acceptedRecords: { value: 270, availability: "available" },
    rejectedRecords: { value: 0, availability: "available" },
    gapCount: { value: 0, availability: "available" },
    duplicateCount: { value: 0, availability: "available" },
    openCandleExclusionCount: { value: 1, availability: "available" },
    lastUpdateIso: "2026-07-15T08:00:00.000Z",
    findings: [
      {
        code: "STALE_STATE",
        severity: "warning",
        message:
          "Estado ilustrativo desatualizado. STALE ≠ VALIDATION_READY e ≠ FAULT.",
      },
    ],
    limitations: ["Freshness ilustrativa não autoriza validação"],
    relatedEvidenceIds: ["ev-fu-collection-readiness"],
  },
  {
    seriesId: "matic-usdt-1h-unknown",
    market: "crypto",
    asset: "MATIC-USDT",
    interval: "1h",
    source: "unknown-illustrative",
    qualityStatus: "UNKNOWN_STATE",
    sourceState: "unknown",
    coverageWindowStartIso: null,
    coverageWindowEndIso: null,
    expectedRecords: { value: null, availability: "unknown" },
    acceptedRecords: { value: null, availability: "unknown" },
    rejectedRecords: { value: null, availability: "unknown" },
    gapCount: { value: null, availability: "unknown" },
    duplicateCount: { value: null, availability: "unknown" },
    openCandleExclusionCount: { value: null, availability: "unknown" },
    lastUpdateIso: null,
    findings: [
      {
        code: "UNKNOWN_STATE",
        severity: "informational",
        message:
          "Estado desconhecido ilustrativo. UNKNOWN ≠ ZERO — contagens não são apresentadas como 0.",
      },
    ],
    limitations: ["Desconhecido permanece explícito; sem coercão para zero"],
    relatedEvidenceIds: ["ev-r3e-pending-future-unseen"],
  },
];

const DOMAIN: CollectionDataQualityDomainInput = {
  asOfIso: COLLECTION_DATA_QUALITY_NOW_ISO,
  illustrativeDisclosure:
    "Dados ilustrativos de monitoramento de coleta e qualidade. Não são evidência operacional ao vivo, não aprovam cientificamente e não autorizam validação, ativação ou dinheiro real.",
  series: SERIES,
  aggregateQualityStatus: "SERIES_PARTIAL",
  aggregateLimitations: [
    "Qualidade de dados ilustrativa ≠ aprovação científica",
    "Coleta saudável ilustrativa ≠ VALIDATION_READY",
    "Janela futura permanece insuficiente no estado científico oficial",
  ],
  knownState: [
    "Várias séries ilustrativas com estados de qualidade distintos",
    "Severidade vermelha reservada apenas a SOURCE_UNAVAILABLE",
    "Somente candles fechados são considerados na série ilustrativa",
  ],
  unknownState: [
    "Estado real da coleta no host operacional",
    "Resultados future-unseen (não acessados)",
    "Pronto para validação científica (permanece NOT_READY)",
  ],
  nextSafeActionPlainLanguage:
    "Continuar monitorando a coleta ilustrativa e a prontidão; não executar validação nem ativar scheduler a partir desta tela.",
  relatedEvidence: [
    {
      evidenceId: "ev-fu-collection-readiness",
      label: "Prontidão da coleta futura (evidência curada)",
    },
    {
      evidenceId: "ev-r3e-pending-future-unseen",
      label: "R3E pendente de dados futuros não vistos",
    },
  ],
};

function assertFixtureIntegrity(domain: CollectionDataQualityDomainInput): void {
  for (const series of domain.series) {
    if (!isCollectionQualityStatus(series.qualityStatus)) {
      throw new Error(`Invalid qualityStatus: ${series.qualityStatus}`);
    }
    if (!isCollectionSourceState(series.sourceState)) {
      throw new Error(`Invalid sourceState: ${series.sourceState}`);
    }
    for (const finding of series.findings) {
      if (!isCollectionQualitySeverity(finding.severity)) {
        throw new Error(`Invalid finding severity: ${finding.severity}`);
      }
    }
  }
  if (!isCollectionQualityStatus(domain.aggregateQualityStatus)) {
    throw new Error("Invalid aggregateQualityStatus");
  }
  const blob = JSON.stringify(domain).toLowerCase();
  const forbidden = [
    "future_unseen_payload",
    "process_env_access",
    "password",
    "api_key",
    "secret_token",
    "pnl",
    "profit",
  ];
  for (const token of forbidden) {
    if (blob.includes(token)) {
      throw new Error(`Fixture contains forbidden token: ${token}`);
    }
  }
}

assertFixtureIntegrity(DOMAIN);

export type CollectionDataQualityFixture = {
  metadata: FixtureMetadata;
  domain: CollectionDataQualityDomainInput;
  nowIso: string;
};

export function getCollectionDataQualityFixture(): CollectionDataQualityFixture {
  return {
    metadata: fixtureMetadata(
      COLLECTION_DATA_QUALITY_FIXTURE_ID,
      "Monitoramento ilustrativo de dados coletados e qualidade",
      "Fixture estática para a tela Dados Coletados (UX-R3 I1). Somente leitura; sem dados reais, validação ou ativação.",
    ),
    domain: {
      ...DOMAIN,
      series: DOMAIN.series.map((s) => ({
        ...s,
        findings: s.findings.map((f) => ({ ...f })),
        limitations: [...s.limitations],
        relatedEvidenceIds: [...s.relatedEvidenceIds],
        expectedRecords: { ...s.expectedRecords },
        acceptedRecords: { ...s.acceptedRecords },
        rejectedRecords: { ...s.rejectedRecords },
        gapCount: { ...s.gapCount },
        duplicateCount: { ...s.duplicateCount },
        openCandleExclusionCount: { ...s.openCandleExclusionCount },
      })),
      aggregateLimitations: [...DOMAIN.aggregateLimitations],
      knownState: [...DOMAIN.knownState],
      unknownState: [...DOMAIN.unknownState],
      relatedEvidence: DOMAIN.relatedEvidence.map((r) => ({ ...r })),
    },
    nowIso: COLLECTION_DATA_QUALITY_NOW_ISO,
  };
}
