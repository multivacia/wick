import { describe, expect, it } from "vitest";
import {
  DOMAIN_LIFECYCLE_STATES,
  assertSemanticInequalities,
  isFaultPresentation,
  mapDomainStateToPresentation,
} from "../../src/viewmodels/status.js";

describe("status semantic mapping", () => {
  it("maps all domain states without throwing", () => {
    for (const state of DOMAIN_LIFECYCLE_STATES) {
      const mapping = mapDomainStateToPresentation(state);
      expect(mapping.status).toBeTruthy();
      assertSemanticInequalities(mapping, state);
    }
  });

  it("maps READY and COMPLETE to healthy/green", () => {
    expect(mapDomainStateToPresentation("ready")).toMatchObject({
      status: "healthy",
      colorTokenHint: "green",
    });
    expect(mapDomainStateToPresentation("complete")).toMatchObject({
      status: "completed",
      colorTokenHint: "green",
    });
  });

  it("maps IN_PROGRESS to informational/cyan", () => {
    expect(mapDomainStateToPresentation("in_progress")).toMatchObject({
      status: "informational",
      colorTokenHint: "cyan",
    });
  });

  it("maps NOT_READY to amber attention, not fault/red", () => {
    const m = mapDomainStateToPresentation("not_ready");
    expect(m.status).toBe("not_ready");
    expect(m.severity).toBe("attention");
    expect(m.colorTokenHint).toBe("amber");
    expect(isFaultPresentation(m.status)).toBe(false);
  });

  it("maps BLOCKED and DEFERRED without fault/red", () => {
    for (const state of ["blocked", "deferred"] as const) {
      const m = mapDomainStateToPresentation(state);
      expect(m.status).not.toBe("fault");
      expect(m.colorTokenHint).not.toBe("red");
      expect(isFaultPresentation(m.status)).toBe(false);
    }
  });

  it("maps FAULT to critical/red only", () => {
    const m = mapDomainStateToPresentation("fault");
    expect(m.status).toBe("fault");
    expect(m.severity).toBe("critical");
    expect(m.colorTokenHint).toBe("red");
  });

  it("maps UNKNOWN to neutral/gray", () => {
    expect(mapDomainStateToPresentation("unknown")).toMatchObject({
      status: "unknown",
      colorTokenHint: "gray",
    });
  });
});
