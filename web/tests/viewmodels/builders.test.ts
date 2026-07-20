import { describe, expect, it } from "vitest";
import { buildOverviewViewModel } from "../../src/viewmodels/buildOverviewViewModel.js";
import { buildRunsViewModel } from "../../src/viewmodels/buildRunsViewModel.js";
import { buildReadinessViewModel } from "../../src/viewmodels/buildReadinessViewModel.js";
import { buildHostSchedulerViewModel } from "../../src/viewmodels/buildHostSchedulerViewModel.js";
import {
  currentProjectOverviewInput,
  emptyMetric,
  sampleHost,
  sampleReadiness,
  sampleRun,
  sampleScheduler,
  ts,
} from "./sampleInputs.js";

const NOW = { nowIso: "2026-07-20T12:00:00Z" };

describe("buildOverviewViewModel", () => {
  it("aggregates current project operational truth without inventing readiness/fault", () => {
    const vm = buildOverviewViewModel(currentProjectOverviewInput(), NOW);
    expect(vm.readinessSummary.explanation.status).toBe("not_ready");
    expect(vm.readinessSummary.explanation.status).not.toBe("fault");
    expect(vm.hostSchedulerSummary.explanation.status).not.toBe("fault");
    expect(vm.scientificGate).toBe("PENDING_FUTURE_UNSEEN_DATA");
    expect(vm.r4Status).toBe("BLOCKED");
    expect(vm.r5Status).toBe("NOT_STARTED");
    expect(vm.generatedWithNow).toBe(NOW.nowIso);
    expect(vm.activeBlockers.length).toBeGreaterThan(0);
    expect(vm.nextSafeAction.advisoryOnly).toBe(true);
  });

  it("is deterministic for identical inputs", () => {
    const input = currentProjectOverviewInput();
    const a = buildOverviewViewModel(input, NOW);
    const b = buildOverviewViewModel(input, NOW);
    expect(a).toEqual(b);
  });

  it("freezes outputs (immutable result)", () => {
    const vm = buildOverviewViewModel(currentProjectOverviewInput(), NOW);
    expect(Object.isFrozen(vm)).toBe(true);
    expect(() => {
      (vm as { overallState: string }).overallState = "fault";
    }).toThrow();
  });
});

describe("buildRunsViewModel", () => {
  it("maps run fields and preserves missing metrics as null", () => {
    const vm = buildRunsViewModel(
      {
        runs: [
          sampleRun({
            acceptedCount: emptyMetric(),
            rejectedCount: emptyMetric(),
            storeBeforeCount: emptyMetric(),
            storeAfterCount: emptyMetric(),
            idempotencyResult: null,
          }),
        ],
      },
      NOW,
    );
    expect(vm.runs[0]?.acceptedCount.value).toBeNull();
    expect(vm.runs[0]?.acceptedCount.value).not.toBe(0);
    expect(vm.runs[0]?.idempotencyResult).toBeNull();
  });

  it("maps failed run to fault presentation", () => {
    const vm = buildRunsViewModel(
      {
        runs: [
          sampleRun({
            state: "fault",
            failureReason: "store write failed",
            failureReasonCode: "LAST_RUN_FAILED",
            finishedAt: ts("2026-07-19T12:00:00Z"),
          }),
        ],
      },
      NOW,
    );
    expect(vm.summaryStatus).toBe("fault");
    expect(vm.runs[0]?.presentation.status).toBe("fault");
    expect(vm.actionHint?.code).toBe("investigate_failed_run");
  });
});

describe("buildReadinessViewModel", () => {
  it("maps not-ready with window reason and does not authorize validation", () => {
    const vm = buildReadinessViewModel(
      { readiness: sampleReadiness() },
      NOW,
    );
    expect(vm.state).toBe("not_ready");
    expect(vm.presentation.status).toBe("not_ready");
    expect(vm.presentation.severity).toBe("attention");
    expect(vm.blockingReasonCodes).toContain("WINDOW_DAYS_INSUFFICIENT");
    expect(vm.validationAuthorized).toBe(false);
    expect(vm.validationCommandExecuted).toBe(false);
    expect(vm.effectPeekingPerformed).toBe(false);
    expect(vm.nextSafeAction.code).toBe("wait_for_sufficient_future_window");
    expect(vm.windowDays.value).toBe(3);
    expect(vm.requiredWindowDays.value).toBe(14);
  });

  it("keeps unknown metrics null when readiness numbers absent", () => {
    const vm = buildReadinessViewModel({
      readiness: sampleReadiness({
        windowDays: emptyMetric(),
        requiredWindowDays: emptyMetric(),
        state: "unknown",
        blockingReasonCodes: ["DATA_UNAVAILABLE"],
      }),
    });
    expect(vm.windowDays.value).toBeNull();
    expect(vm.requiredWindowDays.value).toBeNull();
    expect(vm.presentation.status).toBe("unknown");
  });
});

describe("buildHostSchedulerViewModel", () => {
  it("preserves deferred host and blocked scheduler without implying activation", () => {
    const vm = buildHostSchedulerViewModel(
      {
        host: sampleHost(),
        scheduler: sampleScheduler(),
        blockers: [
          {
            reasonCode: "SCHEDULER_BLOCKED",
            plainLanguage: "Bloqueado",
            evidence: [],
          },
        ],
      },
      NOW,
    );
    expect(vm.hostDiscoveryState).toBe("deferred");
    expect(vm.hostPresentation.status).toBe("deferred");
    expect(vm.schedulerState).toBe("blocked");
    expect(vm.schedulerPresentation.status).toBe("blocked");
    expect(vm.schedulerActive).toBe(false);
    expect(vm.activationAuthorized).toBe(false);
    expect(vm.operationalDebt).toBe("open");
    expect(vm.lastCycleAt.rawIso).toBeNull();
    expect(vm.nextSafeAction.code).toBe("complete_host_discovery");
  });
});
