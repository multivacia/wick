import { describe, expect, it } from "vitest";
import { explainReasonCode, REASON_CODES } from "../../src/viewmodels/reasons.js";
import { buildReadinessViewModel } from "../../src/viewmodels/buildReadinessViewModel.js";
import { sampleReadiness } from "./sampleInputs.js";

describe("reason taxonomy", () => {
  it("explains every stable reason code in plain language", () => {
    for (const code of REASON_CODES) {
      const text = explainReasonCode(code);
      expect(text.length).toBeGreaterThan(8);
      expect(text).not.toBe(code);
    }
  });

  it("keeps user-facing text separate from reason codes on readiness", () => {
    const vm = buildReadinessViewModel({
      readiness: sampleReadiness({
        blockingReasonCodes: ["WINDOW_DAYS_INSUFFICIENT"],
      }),
    });
    expect(vm.blockingReasonCodes).toEqual(["WINDOW_DAYS_INSUFFICIENT"]);
    expect(vm.presentation.primaryMessage.plainLanguage).not.toBe(
      "WINDOW_DAYS_INSUFFICIENT",
    );
    expect(vm.presentation.technicalDetail.reasonCode).toBe(
      "WINDOW_DAYS_INSUFFICIENT",
    );
  });
});
