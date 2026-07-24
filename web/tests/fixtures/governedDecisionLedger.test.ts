import { describe, expect, it } from "vitest";
import {
  GOVERNED_DECISION_LEDGER_FIXTURE_ID,
  GOVERNED_DECISION_LEDGER_FIXTURE_VERSION,
  getGovernedDecisionLedgerFixture,
} from "../../src/fixtures";

describe("governedDecisionLedger fixture", () => {
  it("exports the authorized fixture id/version and nine grounded seeds", () => {
    const packed = getGovernedDecisionLedgerFixture();
    expect(packed.metadata.fixtureId).toBe(GOVERNED_DECISION_LEDGER_FIXTURE_ID);
    expect(packed.metadata.illustrative).toBe(true);
    expect(packed.metadata.notOperationalEvidence).toBe(true);
    expect(packed.domain.fixtureVersion).toBe(
      GOVERNED_DECISION_LEDGER_FIXTURE_VERSION,
    );
    expect(packed.domain.records).toHaveLength(9);
    expect(
      packed.domain.records.every((r) => r.decisionId.startsWith("dec-")),
    ).toBe(true);
    expect(packed.domain.records.every((r) => r.isIllustrative)).toBe(true);
  });

  it("covers the required seed themes without fabricating scientific unlocks", () => {
    const ids = getGovernedDecisionLedgerFixture().domain.records.map(
      (r) => r.decisionId,
    );
    expect(ids).toEqual(
      expect.arrayContaining([
        "dec-ux-r1-fixture-backed-read-only-acceptance",
        "dec-ux-r2-evidence-audit-exploration-acceptance",
        "dec-ux-r3-collection-quality-coherence-acceptance",
        "dec-r3d-no-measurable-edge",
        "dec-r3e-pending-future-unseen",
        "dec-host-discovery-deferred",
        "dec-scheduler-activation-blocked",
        "dec-scientific-r4-blocked",
        "dec-r5-not-started",
      ]),
    );
    const joined = JSON.stringify(getGovernedDecisionLedgerFixture());
    expect(joined).not.toMatch(/R4_STATUS\s*=\s*UNLOCKED/i);
    expect(joined).not.toMatch(/EFFECT_PEEKING_PERFORMED\s*=\s*true/);
  });
});
