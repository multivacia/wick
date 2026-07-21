import { describe, expect, it } from "vitest";
import {
  buildEvidenceExplorerHref,
  EVIDENCE_EXPLORER_PATH,
  parseEvidenceIdParam,
} from "../../src/viewmodels/evidenceDeepLink.js";

describe("evidenceDeepLink", () => {
  it("builds internal evidence explorer hrefs", () => {
    expect(EVIDENCE_EXPLORER_PATH).toBe("/governance/evidence");
    expect(buildEvidenceExplorerHref("ev-r3d")).toBe(
      "/governance/evidence?evidenceId=ev-r3d",
    );
    expect(buildEvidenceExplorerHref("ev has spaces")).toBe(
      "/governance/evidence?evidenceId=ev%20has%20spaces",
    );
  });

  it("parses valid evidenceId params and rejects unsafe values", () => {
    expect(
      parseEvidenceIdParam(new URLSearchParams("evidenceId=ev-ok")),
    ).toBe("ev-ok");
    expect(parseEvidenceIdParam(new URLSearchParams(""))).toBeNull();
    expect(
      parseEvidenceIdParam(new URLSearchParams("evidenceId=")),
    ).toBeNull();
    expect(
      parseEvidenceIdParam(
        new URLSearchParams("evidenceId=https://evil.example"),
      ),
    ).toBeNull();
    expect(
      parseEvidenceIdParam(new URLSearchParams("evidenceId=../secrets")),
    ).toBeNull();
    expect(
      parseEvidenceIdParam(new URLSearchParams("evidenceId=/etc/passwd")),
    ).toBeNull();
  });

  it("never produces external http(s) hrefs", () => {
    const href = buildEvidenceExplorerHref("ev-host-scheduler-operational-debt");
    expect(href.startsWith("/governance/evidence")).toBe(true);
    expect(href).not.toMatch(/^https?:/i);
  });
});
