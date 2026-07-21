import { describe, expect, it } from "vitest";
import { buildOverviewViewModel } from "../../src/viewmodels/buildOverviewViewModel.js";
import { buildRunsViewModel } from "../../src/viewmodels/buildRunsViewModel.js";
import { buildReadinessViewModel } from "../../src/viewmodels/buildReadinessViewModel.js";
import { buildHostSchedulerViewModel } from "../../src/viewmodels/buildHostSchedulerViewModel.js";
import { buildR3eExperimentViewModel } from "../../src/viewmodels/buildR3eExperimentViewModel.js";
import type { R3eExperimentDomainInput } from "../../src/viewmodels/inputs.js";
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

describe("buildR3eExperimentViewModel", () => {
  it("maps explanatory R3E fields without inventing future-unseen outcomes", () => {
    const input: R3eExperimentDomainInput = {
      experimentId: "R3E-TEST",
      parentExperimentId: "R3D-V1",
      title: "Experimento R3E",
      purpose: "Explicativo",
      hypothesis: "H2 ilustrativa",
      protocolVersion: "R3E_SPEC",
      modelFamilies: ["baseline", "contexto", "contexto+candle"],
      modelStages: [
        {
          id: "M0",
          plainLanguage: "baseline",
          technicalDefinition: "M0 = baseline",
        },
        {
          id: "M4",
          plainLanguage: "contexto",
          technicalDefinition: "M4 = contexto",
        },
        {
          id: "M5",
          plainLanguage: "contexto + candle",
          technicalDefinition: "M5 = M4 + candle",
        },
      ],
      deltaCandleDefinition: "DELTA_CANDLE = M5 − M4",
      temporalValidationSummary: "nested walk-forward",
      holdoutSummary: "holdout",
      leakageProtectionSummary: "leakage",
      bootstrapSummary: "bootstrap",
      fdrSummary: "FDR",
      currentScientificState: "EXPLORATORY_COMPLETE_PENDING_FUTURE_UNSEEN_DATA",
      r3dResult: "NO_MEASURABLE_EDGE",
      r3eGate: "PENDING_FUTURE_UNSEEN_DATA",
      collectionState: "IN_PROGRESS",
      readinessState: "NOT_READY",
      validationCommandExecuted: false,
      effectPeekingPerformed: false,
      futureUnseenResultsPresent: false,
      r4Status: "BLOCKED",
      r5Status: "NOT_STARTED",
      knownStatements: [],
      unknownStatements: [],
      nextSafeScientificActionPlain: "Aguardar dados futuros não vistos.",
      evidence: [],
    };
    const vm = buildR3eExperimentViewModel(input, NOW);
    expect(vm.r3dResult).toBe("NO_MEASURABLE_EDGE");
    expect(vm.r3eGate).toBe("PENDING_FUTURE_UNSEEN_DATA");
    expect(vm.futureUnseenResultsPresent).toBe(false);
    expect(vm.validationExecutionState.executed).toBe(false);
    expect(vm.effectPeekingState.performed).toBe(false);
    expect(vm.r4Status).toBe("BLOCKED");
    expect(vm.r5Status).toBe("NOT_STARTED");
    expect(vm.nextSafeScientificAction.advisoryOnly).toBe(true);
    expect(vm.nextSafeScientificAction.code).toBe("await_future_unseen_data");
    expect(vm.deltaCandleDefinition).toMatch(/DELTA_CANDLE/);
    expect(Object.isFrozen(vm)).toBe(true);
  });
});
