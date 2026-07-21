import { describe, expect, it } from "vitest";
import {
  assertValidEvidenceSourcePath,
  buildEvidenceExplorerViewModel,
  clearEvidenceFilters,
  emptyEvidenceCriteria,
  filterEvidenceEntries,
  InvalidEvidenceSourcePathError,
  isValidEvidenceSourcePath,
  mapEvidenceStatusToDomain,
  presentEvidenceStatus,
  type EvidenceCatalogEntryInput,
  type EvidenceCatalogInput,
} from "../../src/viewmodels";

function entry(
  overrides: Partial<EvidenceCatalogEntryInput> &
    Pick<EvidenceCatalogEntryInput, "evidenceId" | "title">,
): EvidenceCatalogEntryInput {
  return {
    evidenceClass: "impact_assessment",
    release: "UX-R2",
    increment: "I1",
    experimentId: null,
    status: "AUTHORIZED_WITH_CONDITIONS",
    dataOrigin: "GOVERNANCE_RECORD",
    scientificStage: "NOT_APPLICABLE",
    createdAtOrUnknown: "2026-07-20T00:00:00.000Z",
    sourcePath: "docs/ai-impact/example.md",
    summary: "Resumo ilustrativo",
    supports: ["a"],
    limitations: ["b"],
    knownState: ["c"],
    unknownState: ["d"],
    governanceFlags: ["FLAG=true"],
    staleness: "CURRENT_AS_OF_FIXTURE",
    ...overrides,
  };
}

const SAMPLE_CATALOG: EvidenceCatalogInput = {
  entries: [
    entry({
      evidenceId: "ev-r3d",
      title: "Conclusão R3D",
      evidenceClass: "validation_report",
      release: "R3D",
      increment: null,
      experimentId: "R3D",
      status: "NO_MEASURABLE_EDGE",
      dataOrigin: "HISTORICAL_AUDITED",
      scientificStage: "AUDITED_COMPLETE",
      sourcePath: "docs/audits/R3D_AUDIT_RESULTS.md",
      summary: "R3D_RESULT=NO_MEASURABLE_EDGE distinto de R3E",
      governanceFlags: ["R3D_RESULT=NO_MEASURABLE_EDGE"],
      staleness: "HISTORICAL",
    }),
    entry({
      evidenceId: "ev-r3e",
      title: "Estado R3E",
      evidenceClass: "experiment_specification",
      release: "R3E",
      increment: null,
      experimentId: "R3E",
      status: "PENDING_FUTURE_UNSEEN_DATA",
      dataOrigin: "SYNTHETIC_ILLUSTRATIVE",
      scientificStage: "PENDING_FUTURE_UNSEEN",
      sourcePath: "docs/audits/R3E_AUDIT_RESULTS.md",
      summary: "R3E_GATE=PENDING_FUTURE_UNSEEN_DATA",
      governanceFlags: ["R3E_GATE=PENDING_FUTURE_UNSEEN_DATA"],
    }),
    entry({
      evidenceId: "ev-ux",
      title: "Avaliação UX-R2 I1",
      evidenceClass: "impact_assessment",
      release: "UX-R2",
      status: "AUTHORIZED_WITH_CONDITIONS",
      summary: "Evidence Explorer authorization",
    }),
    entry({
      evidenceId: "ev-ready",
      title: "Prontidão coleta",
      evidenceClass: "collection_readiness_evidence",
      release: "R3E-FU",
      status: "NOT_READY",
      scientificStage: "PENDING_FUTURE_UNSEEN",
      sourcePath: "reports/ai-implementation/R3E-READINESS-001_IMPLEMENTATION_REPORT.md",
      summary: "WINDOW_DAYS_INSUFFICIENT",
      staleness: "PENDING_REFRESH",
    }),
  ],
};

describe("buildEvidenceExplorerViewModel", () => {
  it("returns all entries sorted by evidenceId with empty criteria", () => {
    const vm = buildEvidenceExplorerViewModel(
      SAMPLE_CATALOG,
      emptyEvidenceCriteria(),
    );
    expect(vm.resultCount).toBe(4);
    expect(vm.summaries.map((s) => s.evidenceId)).toEqual([
      "ev-r3d",
      "ev-r3e",
      "ev-ready",
      "ev-ux",
    ]);
    expect(vm.emptyState).toBe(false);
    expect(vm.noResultsState).toBe(false);
    expect(vm.pageTitle).toBe("Evidências");
    expect(vm.safetyNotices.length).toBeGreaterThanOrEqual(3);
    expect(
      vm.safetyNotices.some((n) => n.includes("Evidence presence")),
    ).toBe(true);
    expect(vm.safetyNotices.some((n) => n.includes("Audited"))).toBe(true);
    expect(vm.safetyNotices.some((n) => n.includes("Source path"))).toBe(true);
  });

  it("searches case-insensitively across approved fields", () => {
    const vm = buildEvidenceExplorerViewModel(SAMPLE_CATALOG, {
      searchQuery: "  r3e_gate  ",
      filters: {},
    });
    expect(vm.summaries.map((s) => s.evidenceId)).toEqual(["ev-r3e"]);
    expect(vm.resultCount).toBe(1);
  });

  it("combines filters with AND logic", () => {
    const vm = buildEvidenceExplorerViewModel(SAMPLE_CATALOG, {
      searchQuery: "",
      filters: {
        evidenceClass: "validation_report",
        release: "R3D",
      },
    });
    expect(vm.summaries).toHaveLength(1);
    expect(vm.summaries[0]?.evidenceId).toBe("ev-r3d");
  });

  it("clears filters via helper and shows no-results when nothing matches", () => {
    expect(clearEvidenceFilters()).toEqual({});
    const filtered = filterEvidenceEntries(SAMPLE_CATALOG.entries, "zzzz-none", {});
    expect(filtered).toEqual([]);
    const vm = buildEvidenceExplorerViewModel(SAMPLE_CATALOG, {
      searchQuery: "zzzz-none",
      filters: {},
    });
    expect(vm.noResultsState).toBe(true);
    expect(vm.emptyState).toBe(false);
    expect(vm.resultCount).toBe(0);
  });

  it("keeps R3D NO_MEASURABLE_EDGE distinct from R3E pending gate", () => {
    const vm = buildEvidenceExplorerViewModel(SAMPLE_CATALOG, {
      searchQuery: "",
      filters: {},
      selectedEvidenceId: "ev-r3d",
    });
    expect(vm.selectedDetail?.status).toBe("NO_MEASURABLE_EDGE");
    expect(vm.selectedDetail?.governanceFlags).toContain(
      "R3D_RESULT=NO_MEASURABLE_EDGE",
    );
    expect(vm.selectedDetail?.summary).not.toMatch(/R3E.?rejected/i);

    const r3e = buildEvidenceExplorerViewModel(SAMPLE_CATALOG, {
      searchQuery: "",
      filters: {},
      selectedEvidenceId: "ev-r3e",
    });
    expect(r3e.selectedDetail?.status).toBe("PENDING_FUTURE_UNSEEN_DATA");
    expect(r3e.selectedDetail?.status).not.toBe("NO_MEASURABLE_EDGE");
  });

  it("validates sourcePath and rejects unsafe paths", () => {
    expect(() =>
      assertValidEvidenceSourcePath("docs/releases/ok.md"),
    ).not.toThrow();
    expect(() =>
      assertValidEvidenceSourcePath("reports/ai-implementation/ok.md"),
    ).not.toThrow();
    expect(isValidEvidenceSourcePath("../etc/passwd")).toBe(false);
    expect(isValidEvidenceSourcePath("/etc/passwd")).toBe(false);
    expect(isValidEvidenceSourcePath("https://example.com/x")).toBe(false);
    expect(isValidEvidenceSourcePath("docs/../secrets/x")).toBe(false);
    expect(isValidEvidenceSourcePath("docs/.env")).toBe(false);
    expect(isValidEvidenceSourcePath("reports/r3e_future_unseen/x.json")).toBe(
      false,
    );
    expect(() =>
      assertValidEvidenceSourcePath("src/code.ts"),
    ).toThrow(InvalidEvidenceSourcePathError);

    expect(() =>
      buildEvidenceExplorerViewModel(
        {
          entries: [
            entry({
              evidenceId: "bad",
              title: "Bad",
              sourcePath: "../../.env",
            }),
          ],
        },
        emptyEvidenceCriteria(),
      ),
    ).toThrow(InvalidEvidenceSourcePathError);
  });

  it("falls back when selection is invalid or filtered out", () => {
    const missing = buildEvidenceExplorerViewModel(SAMPLE_CATALOG, {
      searchQuery: "",
      filters: {},
      selectedEvidenceId: "does-not-exist",
    });
    expect(missing.selectedDetail).toBeNull();
    expect(missing.invalidSelectionFallback).toBe(true);

    const filteredOut = buildEvidenceExplorerViewModel(SAMPLE_CATALOG, {
      searchQuery: "",
      filters: { release: "R3D" },
      selectedEvidenceId: "ev-r3e",
    });
    expect(filteredOut.selectedDetail).toBeNull();
    expect(filteredOut.invalidSelectionFallback).toBe(true);
    expect(filteredOut.resultCount).toBe(1);
  });

  it("maps pending/blocked/not_ready away from fault presentation", () => {
    expect(mapEvidenceStatusToDomain("PENDING_FUTURE_UNSEEN_DATA")).toBe(
      "in_progress",
    );
    expect(mapEvidenceStatusToDomain("BLOCKED")).toBe("blocked");
    expect(mapEvidenceStatusToDomain("NOT_READY")).toBe("not_ready");
    expect(mapEvidenceStatusToDomain("DEFERRED")).toBe("deferred");
    expect(presentEvidenceStatus("NOT_READY").status).not.toBe("fault");
    expect(presentEvidenceStatus("BLOCKED").status).not.toBe("fault");
    expect(presentEvidenceStatus("PENDING_X").status).not.toBe("fault");
  });

  it("marks empty catalog state", () => {
    const vm = buildEvidenceExplorerViewModel(
      { entries: [] },
      emptyEvidenceCriteria(),
    );
    expect(vm.emptyState).toBe(true);
    expect(vm.noResultsState).toBe(false);
  });
});
