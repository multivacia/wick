import { describe, expect, it } from "vitest";
import {
  COLLECTION_DATA_QUALITY_FIXTURE_ID,
  COLLECTION_DATA_QUALITY_NOW_ISO,
  getCollectionDataQualityFixture,
} from "../../src/fixtures/collectionDataQuality";

describe("collectionDataQuality fixture", () => {
  it("uses the authorized fixture id and as-of timestamp", () => {
    const fixture = getCollectionDataQualityFixture();
    expect(fixture.metadata.fixtureId).toBe(COLLECTION_DATA_QUALITY_FIXTURE_ID);
    expect(COLLECTION_DATA_QUALITY_FIXTURE_ID).toBe(
      "collection_data_quality_current_state_illustrative",
    );
    expect(fixture.nowIso).toBe(COLLECTION_DATA_QUALITY_NOW_ISO);
    expect(fixture.domain.asOfIso).toBe(COLLECTION_DATA_QUALITY_NOW_ISO);
    expect(fixture.metadata.synthetic).toBe(true);
    expect(fixture.metadata.illustrative).toBe(true);
    expect(fixture.metadata.notOperationalEvidence).toBe(true);
  });

  it("covers all quality statuses illustratively", () => {
    const statuses = new Set(
      getCollectionDataQualityFixture().domain.series.map((s) => s.qualityStatus),
    );
    for (const required of [
      "SERIES_COMPLETE",
      "SERIES_PARTIAL",
      "GAPS_PRESENT",
      "DUPLICATES_PRESENT",
      "REJECTED_RECORDS_PRESENT",
      "OPEN_CANDLE_EXCLUDED",
      "SOURCE_UNAVAILABLE",
      "STALE_STATE",
      "UNKNOWN_STATE",
    ]) {
      expect(statuses.has(required as never)).toBe(true);
    }
  });

  it("keeps unknown counts as null/unknown rather than zero", () => {
    const unknown = getCollectionDataQualityFixture().domain.series.find(
      (s) => s.qualityStatus === "UNKNOWN_STATE",
    );
    expect(unknown).toBeDefined();
    expect(unknown?.gapCount.value).toBeNull();
    expect(unknown?.gapCount.availability).toBe("unknown");
    expect(unknown?.expectedRecords.value).toBeNull();
  });

  it("does not embed forbidden runtime/secret tokens", () => {
    const blob = JSON.stringify(getCollectionDataQualityFixture()).toLowerCase();
    expect(blob).not.toMatch(/process\.env/);
    expect(blob).not.toMatch(/api_key/);
    expect(blob).not.toMatch(/password/);
    expect(blob).not.toMatch(/future_unseen_payload/);
    expect(blob).not.toMatch(/\bpnl\b/);
  });
});
