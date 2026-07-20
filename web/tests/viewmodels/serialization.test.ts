import { describe, expect, it } from "vitest";
import { buildOverviewViewModel } from "../../src/viewmodels/buildOverviewViewModel.js";
import { buildRunsViewModel } from "../../src/viewmodels/buildRunsViewModel.js";
import { buildReadinessViewModel } from "../../src/viewmodels/buildReadinessViewModel.js";
import { buildHostSchedulerViewModel } from "../../src/viewmodels/buildHostSchedulerViewModel.js";
import {
  currentProjectOverviewInput,
  sampleHost,
  sampleReadiness,
  sampleRun,
  sampleScheduler,
} from "./sampleInputs.js";

describe("serializable ViewModel outputs", () => {
  it("round-trips through JSON for all builders", () => {
    const now = { nowIso: "2026-07-20T12:00:00Z" };
    const payloads = [
      buildOverviewViewModel(currentProjectOverviewInput(), now),
      buildRunsViewModel({ runs: [sampleRun()] }, now),
      buildReadinessViewModel({ readiness: sampleReadiness() }, now),
      buildHostSchedulerViewModel(
        {
          host: sampleHost(),
          scheduler: sampleScheduler(),
          blockers: [],
        },
        now,
      ),
    ];

    for (const payload of payloads) {
      const json = JSON.stringify(payload);
      expect(json).toBeTypeOf("string");
      const parsed = JSON.parse(json) as unknown;
      expect(parsed).toEqual(JSON.parse(JSON.stringify(payload)));
    }
  });
});

describe("immutable inputs", () => {
  it("does not mutate input objects", () => {
    const input = currentProjectOverviewInput();
    const snapshot = JSON.stringify(input);
    buildOverviewViewModel(input, { nowIso: "2026-07-20T12:00:00Z" });
    expect(JSON.stringify(input)).toBe(snapshot);
  });
});
