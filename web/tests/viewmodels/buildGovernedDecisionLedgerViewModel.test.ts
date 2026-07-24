import { describe, expect, it } from "vitest";
import {
  buildGovernedDecisionLedgerViewModel,
  clearLedgerFilters,
  mapDispositionToPresentation,
  type GovernedDecisionLedgerDomainInput,
  type GovernedDecisionRecordInput,
} from "../../src/viewmodels";
import { getGovernedDecisionLedgerFixture } from "../../src/fixtures";

function baseDomain(
  overrides: Partial<GovernedDecisionLedgerDomainInput> = {},
): GovernedDecisionLedgerDomainInput {
  const packed = getGovernedDecisionLedgerFixture();
  return { ...packed.domain, ...overrides };
}

function sampleRecord(
  overrides: Partial<GovernedDecisionRecordInput> = {},
): GovernedDecisionRecordInput {
  const first = baseDomain().records[0];
  if (!first) {
    throw new Error("expected seeded ledger records");
  }
  return { ...first, ...overrides };
}

describe("buildGovernedDecisionLedgerViewModel", () => {
  it("builds the curated ledger with nine grounded seeds", () => {
    const vm = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: clearLedgerFilters(),
    });
    expect(vm.records).toHaveLength(9);
    expect(vm.fixtureVersion).toBe(1);
    expect(vm.emptyState).toBe(false);
    expect(vm.staleFixtureState).toBe(false);
    expect(vm.counts.acceptedCount).toBe(3);
    expect(vm.counts.blockedCount).toBe(3);
    expect(vm.counts.triggerCount).toBeGreaterThan(0);
    expect(vm.counts.unknownDispositionCount).toBe(0);
  });

  it("sorts by decision_date DESC then decision_id ASC (not severity-first)", () => {
    const vm = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: clearLedgerFilters(),
    });
    const ids = vm.records.map((r) => r.decisionId);
    expect(ids[0]).toBe("dec-ux-r3-collection-quality-coherence-acceptance");
    expect(ids[ids.length - 1]).toBe("dec-r5-not-started");
    const last = vm.records[ids.length - 1];
    expect(last?.decisionDateIsUnknown).toBe(true);
  });

  it("filters by disposition/domain/release/type/reassessment", () => {
    const blocked = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: { disposition: "BLOCKED" },
    });
    expect(
      blocked.records.every((r) => r.disposition.disposition === "BLOCKED"),
    ).toBe(true);
    expect(blocked.noResultsState).toBe(false);

    const none = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: { disposition: "SUPERSEDED" },
    });
    expect(none.records).toHaveLength(0);
    expect(none.noResultsState).toBe(true);

    const withTrigger = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: { reassessmentAvailability: "available" },
    });
    expect(withTrigger.records.every((r) => r.hasReassessmentTrigger)).toBe(
      true,
    );

    const withoutTrigger = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: { reassessmentAvailability: "none" },
    });
    expect(
      withoutTrigger.records.every((r) => !r.hasReassessmentTrigger),
    ).toBe(true);
  });

  it("supports empty fixture state", () => {
    const vm = buildGovernedDecisionLedgerViewModel(
      baseDomain({ records: [] }),
      { filters: clearLedgerFilters() },
    );
    expect(vm.emptyState).toBe(true);
    expect(vm.counts.totalCount).toBe(0);
    expect(vm.counts.resultCount).toBe(0);
  });

  it("exposes stale fixture state without implying live freshness", () => {
    const vm = buildGovernedDecisionLedgerViewModel(
      baseDomain({ freshness: "stale" }),
      { filters: clearLedgerFilters() },
    );
    expect(vm.staleFixtureState).toBe(true);
    expect(vm.staleDisclosure).toMatch(/desatualizado/i);
    expect(vm.freshnessDisclosure).toMatch(/não implicam atualização ao vivo/i);
  });

  it("presents UNKNOWN disposition and date without inventing zero", () => {
    const unknownRecord = sampleRecord({
      decisionId: "dec-unknown-example",
      disposition: "UNKNOWN",
      decisionDate: "UNKNOWN",
      reassessmentTrigger: null,
      conditions: undefined,
    });
    const vm = buildGovernedDecisionLedgerViewModel(
      baseDomain({ records: [unknownRecord] }),
      {
        filters: clearLedgerFilters(),
        selectedDecisionId: "dec-unknown-example",
      },
    );
    expect(vm.unknownStateNotice).toMatch(/Desconhecido/);
    expect(vm.counts.unknownDispositionCount).toBe(1);
    expect(vm.selectedRecord?.decisionDateIsUnknown).toBe(true);
    expect(vm.selectedRecord?.decisionDateDisplay).toBe("Desconhecida");
    expect(vm.selectedRecord?.disposition.status).toBe("unknown");
  });

  it("distinguishes conditions / reassessment / superseded detail states", () => {
    const withConditions = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: clearLedgerFilters(),
      selectedDecisionId: "dec-r3e-pending-future-unseen",
    });
    expect(withConditions.selectedRecord?.hasConditions).toBe(true);
    expect(withConditions.selectedRecord?.hasReassessmentTrigger).toBe(true);

    const without = buildGovernedDecisionLedgerViewModel(baseDomain(), {
      filters: clearLedgerFilters(),
      selectedDecisionId: "dec-ux-r1-fixture-backed-read-only-acceptance",
    });
    expect(without.selectedRecord?.hasConditions).toBe(false);
    expect(without.selectedRecord?.hasReassessmentTrigger).toBe(false);

    const superseded = sampleRecord({
      decisionId: "dec-superseded-example",
      disposition: "SUPERSEDED",
      supersededBy: "dec-ux-r1-fixture-backed-read-only-acceptance",
    });
    const supersededVm = buildGovernedDecisionLedgerViewModel(
      baseDomain({ records: [superseded] }),
      {
        filters: clearLedgerFilters(),
        selectedDecisionId: "dec-superseded-example",
      },
    );
    expect(supersededVm.selectedRecord?.isSuperseded).toBe(true);
    expect(mapDispositionToPresentation("SUPERSEDED")).toBe("informational");
    expect(mapDispositionToPresentation("BLOCKED")).toBe("blocked");
    expect(mapDispositionToPresentation("REJECTED")).toBe("attention");
  });

  it("rejects unsafe evidence ids and non-illustrative records", () => {
    expect(() =>
      buildGovernedDecisionLedgerViewModel(
        baseDomain({
          records: [
            sampleRecord({
              evidenceRefs: [
                { evidenceId: "https://evil.example", label: "bad" },
              ],
            }),
          ],
        }),
        { filters: clearLedgerFilters() },
      ),
    ).toThrow(/external URL/i);

    expect(() =>
      buildGovernedDecisionLedgerViewModel(
        baseDomain({
          records: [
            sampleRecord({
              isIllustrative: false as true,
            }),
          ],
        }),
        { filters: clearLedgerFilters() },
      ),
    ).toThrow(/is_illustrative/i);
  });

  it("never maps process dispositions to fault/red", () => {
    for (const disposition of [
      "ACCEPTED",
      "AUTHORIZED_WITH_CONDITIONS",
      "BLOCKED",
      "DEFERRED",
      "REJECTED",
      "SUPERSEDED",
      "UNKNOWN",
    ] as const) {
      expect(mapDispositionToPresentation(disposition)).not.toBe("fault");
    }
  });
});
