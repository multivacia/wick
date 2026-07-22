import { describe, expect, it } from "vitest";
import {
  buildCollectionDataQualityViewModel,
  clearCollectionFilters,
  emptyCollectionCriteria,
  filterAndSortCollectionSeries,
  mapQualityStatusToDomain,
  mapQualityStatusToSeverity,
  presentOptionalCount,
  presentQualityStatus,
  type CollectionDataQualityDomainInput,
  type CollectionSeriesInput,
} from "../../src/viewmodels";

function count(
  value: number | null,
  availability: CollectionSeriesInput["gapCount"]["availability"] = "available",
) {
  return { value, availability };
}

function series(
  overrides: Partial<CollectionSeriesInput> &
    Pick<CollectionSeriesInput, "seriesId" | "qualityStatus">,
): CollectionSeriesInput {
  return {
    market: "crypto",
    asset: "BTC-USDT",
    interval: "1h",
    source: "illustrative",
    sourceState: "available",
    coverageWindowStartIso: "2026-07-01T00:00:00.000Z",
    coverageWindowEndIso: "2026-07-10T00:00:00.000Z",
    expectedRecords: count(10),
    acceptedRecords: count(10),
    rejectedRecords: count(0),
    gapCount: count(0),
    duplicateCount: count(0),
    openCandleExclusionCount: count(1),
    lastUpdateIso: "2026-07-22T12:00:00.000Z",
    findings: [],
    limitations: [],
    relatedEvidenceIds: [],
    ...overrides,
  };
}

const DOMAIN: CollectionDataQualityDomainInput = {
  asOfIso: "2026-07-22T18:00:00.000Z",
  illustrativeDisclosure: "Ilustrativo",
  series: [
    series({
      seriesId: "a-complete",
      qualityStatus: "SERIES_COMPLETE",
      lastUpdateIso: "2026-07-22T10:00:00.000Z",
    }),
    series({
      seriesId: "b-gap",
      qualityStatus: "GAPS_PRESENT",
      gapCount: count(2),
      lastUpdateIso: "2026-07-22T16:00:00.000Z",
    }),
    series({
      seriesId: "c-fault",
      qualityStatus: "SOURCE_UNAVAILABLE",
      sourceState: "unavailable",
      lastUpdateIso: "2026-07-22T11:00:00.000Z",
    }),
    series({
      seriesId: "d-unknown",
      qualityStatus: "UNKNOWN_STATE",
      sourceState: "unknown",
      expectedRecords: count(null, "unknown"),
      acceptedRecords: count(null, "unknown"),
      rejectedRecords: count(null, "unknown"),
      gapCount: count(null, "unknown"),
      duplicateCount: count(null, "unknown"),
      openCandleExclusionCount: count(null, "unknown"),
      lastUpdateIso: null,
    }),
  ],
  aggregateQualityStatus: "SERIES_PARTIAL",
  aggregateLimitations: ["lim"],
  knownState: ["known"],
  unknownState: ["unknown"],
  nextSafeActionPlainLanguage: "Monitorar",
  relatedEvidence: [{ evidenceId: "ev-fu-collection-readiness", label: "Ready" }],
};

describe("collection data quality enums and presentation", () => {
  it("maps only SOURCE_UNAVAILABLE to fault severity (red reserved)", () => {
    expect(mapQualityStatusToSeverity("SOURCE_UNAVAILABLE")).toBe("fault");
    expect(mapQualityStatusToDomain("SOURCE_UNAVAILABLE")).toBe("fault");
    expect(presentQualityStatus("SOURCE_UNAVAILABLE").status).toBe("fault");

    expect(mapQualityStatusToSeverity("GAPS_PRESENT")).toBe("warning");
    expect(mapQualityStatusToDomain("GAPS_PRESENT")).toBe("not_ready");
    expect(presentQualityStatus("GAPS_PRESENT").status).not.toBe("fault");

    expect(mapQualityStatusToSeverity("OPEN_CANDLE_EXCLUDED")).toBe(
      "informational",
    );
    expect(mapQualityStatusToSeverity("UNKNOWN_STATE")).toBe("informational");
    expect(mapQualityStatusToDomain("UNKNOWN_STATE")).toBe("unknown");
  });

  it("never presents unknown counts as zero", () => {
    const unknown = presentOptionalCount({ value: null, availability: "unknown" });
    expect(unknown.isUnknown).toBe(true);
    expect(unknown.isZero).toBe(false);
    expect(unknown.displayText).toBe("Desconhecido");
    expect(unknown.displayText).not.toBe("0");

    const zero = presentOptionalCount({ value: 0, availability: "available" });
    expect(zero.isZero).toBe(true);
    expect(zero.displayText).toBe("0");
  });
});

describe("filterAndSortCollectionSeries", () => {
  it("sorts by severity then lastUpdate descending", () => {
    const sorted = filterAndSortCollectionSeries(DOMAIN.series, {});
    expect(sorted.map((s) => s.seriesId)).toEqual([
      "c-fault",
      "b-gap",
      "a-complete",
      "d-unknown",
    ]);
  });

  it("filters by market/interval/status/severity", () => {
    const bySeverity = filterAndSortCollectionSeries(DOMAIN.series, {
      severity: "fault",
    });
    expect(bySeverity.map((s) => s.seriesId)).toEqual(["c-fault"]);

    const byStatus = filterAndSortCollectionSeries(DOMAIN.series, {
      qualityStatus: "GAPS_PRESENT",
    });
    expect(byStatus.map((s) => s.seriesId)).toEqual(["b-gap"]);
  });
});

describe("buildCollectionDataQualityViewModel", () => {
  it("builds VM with empty/no-results flags and semantic safeguards", () => {
    const vm = buildCollectionDataQualityViewModel(
      DOMAIN,
      emptyCollectionCriteria(),
      { nowIso: "2026-07-22T18:00:00.000Z" },
    );
    expect(vm.pageTitle).toBe("Dados Coletados");
    expect(vm.emptyState).toBe(false);
    expect(vm.noResultsState).toBe(false);
    expect(vm.resultCount).toBe(4);
    expect(vm.series[0]?.seriesId).toBe("c-fault");
    expect(vm.semanticSafeguards.some((s) => s.includes("UNKNOWN ≠ ZERO"))).toBe(
      true,
    );
    expect(vm.nextSafeAction.advisoryOnly).toBe(true);
    expect(vm.nextSafeAction.code).toBe("monitor_collection");
    expect(vm.hasUnknownCounts).toBe(true);

    const unknownSeries = vm.series.find((s) => s.seriesId === "d-unknown");
    expect(unknownSeries?.gapCount.displayText).toBe("Desconhecido");
    expect(unknownSeries?.gapCount.isZero).toBe(false);
  });

  it("sets noResultsState when filters exclude all series", () => {
    const vm = buildCollectionDataQualityViewModel(
      DOMAIN,
      { filters: { seriesId: "does-not-exist" } },
      null,
    );
    expect(vm.emptyState).toBe(false);
    expect(vm.noResultsState).toBe(true);
    expect(vm.resultCount).toBe(0);
  });

  it("sets emptyState when catalog has no series", () => {
    const vm = buildCollectionDataQualityViewModel(
      { ...DOMAIN, series: [] },
      { filters: clearCollectionFilters() },
      null,
    );
    expect(vm.emptyState).toBe(true);
    expect(vm.noResultsState).toBe(false);
  });

  it("marks stale freshness when last update is old relative to clock", () => {
    const vm = buildCollectionDataQualityViewModel(
      {
        ...DOMAIN,
        series: [
          series({
            seriesId: "stale-one",
            qualityStatus: "STALE_STATE",
            lastUpdateIso: "2026-07-01T00:00:00.000Z",
          }),
        ],
      },
      emptyCollectionCriteria(),
      { nowIso: "2026-07-22T18:00:00.000Z" },
    );
    expect(vm.hasStaleSeries).toBe(true);
    expect(vm.series[0]?.lastUpdate.freshness).toBe("stale");
  });
});
