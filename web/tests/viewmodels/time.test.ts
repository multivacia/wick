import { describe, expect, it } from "vitest";
import { presentTimestamp, metricPresentation } from "../../src/viewmodels/time.js";

describe("explicit time and metrics", () => {
  it("does not invent timestamps when missing", () => {
    const ts = presentTimestamp(
      { iso: null, availability: "not_supplied" },
      { nowIso: "2026-07-20T12:00:00Z" },
    );
    expect(ts.rawIso).toBeNull();
    expect(ts.displayText).toBeNull();
    expect(ts.freshness).toBe("absent");
  });

  it("uses explicit now for freshness", () => {
    const current = presentTimestamp(
      { iso: "2026-07-20T10:00:00Z", availability: "available" },
      { nowIso: "2026-07-20T12:00:00Z", staleAfterMs: 6 * 60 * 60 * 1000 },
      { includeRelative: true },
    );
    expect(current.freshness).toBe("current");
    expect(current.relativeText).toBeTruthy();

    const stale = presentTimestamp(
      { iso: "2026-07-19T10:00:00Z", availability: "available" },
      { nowIso: "2026-07-20T12:00:00Z", staleAfterMs: 6 * 60 * 60 * 1000 },
    );
    expect(stale.freshness).toBe("stale");
  });

  it("without clock, does not invent relative freshness as current", () => {
    const ts = presentTimestamp(
      { iso: "2026-07-20T10:00:00Z", availability: "available" },
      null,
    );
    expect(ts.freshness).toBe("not_applicable");
    expect(ts.relativeText).toBeNull();
  });

  it("does not convert missing metrics to zero", () => {
    const m = metricPresentation("accepted", null, "not_supplied", "rows");
    expect(m.value).toBeNull();
    expect(m.displayText).toBeNull();
    expect(m.availability).not.toBe("available");
  });

  it("preserves explicit zero when supplied", () => {
    const m = metricPresentation("accepted", 0, "available", "rows");
    expect(m.value).toBe(0);
    expect(m.displayText).toBe("0 rows");
  });
});
