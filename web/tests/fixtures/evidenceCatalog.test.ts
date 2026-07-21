import { describe, expect, it } from "vitest";
import {
  EVIDENCE_CATALOG_FIXTURE_ID,
  getEvidenceCatalogFixture,
} from "../../src/fixtures";
import {
  assertValidEvidenceSourcePath,
  isEvidenceClass,
  isEvidenceDataOrigin,
  isEvidenceScientificStage,
  isEvidenceStaleness,
} from "../../src/viewmodels";

describe("evidenceCatalog fixture", () => {
  it("exposes the required fixture id and metadata disclosure", () => {
    const fixture = getEvidenceCatalogFixture();
    expect(EVIDENCE_CATALOG_FIXTURE_ID).toBe(
      "evidence_catalog_current_state_illustrative",
    );
    expect(fixture.metadata.fixtureId).toBe(EVIDENCE_CATALOG_FIXTURE_ID);
    expect(fixture.metadata.synthetic).toBe(true);
    expect(fixture.metadata.illustrative).toBe(true);
    expect(fixture.metadata.notOperationalEvidence).toBe(true);
    expect(fixture.nowIso).toMatch(/Z$/);
  });

  it("includes at least seven curated entries covering required themes", () => {
    const { catalog } = getEvidenceCatalogFixture();
    expect(catalog.entries.length).toBeGreaterThanOrEqual(7);

    const joined = catalog.entries
      .map((e) => `${e.title} ${e.summary} ${e.governanceFlags.join(" ")}`)
      .join("\n");

    expect(joined).toMatch(/UX-R1/);
    expect(joined).toMatch(/UX-R2/);
    expect(joined).toMatch(/R3D_RESULT=NO_MEASURABLE_EDGE/);
    expect(joined).toMatch(/R3E_GATE=PENDING_FUTURE_UNSEEN_DATA/);
    expect(joined).toMatch(/WINDOW_DAYS_INSUFFICIENT/);
    expect(joined).toMatch(/HOST_DISCOVERY=DEFERRED/);
    expect(joined).toMatch(/SCHEDULER_ACTIVATION=BLOCKED/);
    expect(joined).not.toMatch(/\bR3E was rejected\b/i);
    expect(joined).not.toMatch(/\bR3E foi rejeitado\b/i);
  });

  it("validates enums, allowed paths, and forbids secrets/FU payloads", () => {
    const { catalog } = getEvidenceCatalogFixture();
    const ids = new Set<string>();

    for (const entry of catalog.entries) {
      expect(ids.has(entry.evidenceId)).toBe(false);
      ids.add(entry.evidenceId);

      expect(isEvidenceClass(entry.evidenceClass)).toBe(true);
      expect(isEvidenceDataOrigin(entry.dataOrigin)).toBe(true);
      expect(isEvidenceScientificStage(entry.scientificStage)).toBe(true);
      expect(isEvidenceStaleness(entry.staleness)).toBe(true);
      expect(["SYNTHETIC_ILLUSTRATIVE", "GOVERNANCE_RECORD", "HISTORICAL_AUDITED", "EXPLORATORY_RECORDED"]).toContain(
        entry.dataOrigin,
      );

      assertValidEvidenceSourcePath(entry.sourcePath);
      expect(
        entry.sourcePath.startsWith("docs/") ||
          entry.sourcePath.startsWith("reports/"),
      ).toBe(true);
      expect(entry.sourcePath).not.toMatch(/\.\./);
      expect(entry.sourcePath).not.toMatch(/\.env|secret|credential/i);
      expect(entry.sourcePath).not.toMatch(/^reports\/r3e_future_unseen\//);

      const blob = JSON.stringify(entry).toLowerCase();
      expect(blob).not.toMatch(/futureunseenresultspresent=true/);
      expect(blob).not.toMatch(/sharpe\s*=/);
      expect(blob).not.toMatch(/p\s*=\s*0\./);
      expect(blob).not.toMatch(/"pnl"\s*:/);
      expect(entry.sourcePath).not.toMatch(/^https?:\/\//i);
    }
  });

  it("marks readiness as NOT_READY without fabricating FU result payloads", () => {
    const readiness = getEvidenceCatalogFixture().catalog.entries.find(
      (e) => e.evidenceClass === "collection_readiness_evidence",
    );
    expect(readiness).toBeDefined();
    expect(readiness?.status).toBe("NOT_READY");
    expect(readiness?.governanceFlags.join(" ")).toMatch(/FU_RESULT_PAYLOADS=absent/);
    expect(JSON.stringify(readiness)).not.toMatch(/futureUnseenResults\s*:/i);
  });
});
