import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  FIXTURE_SCENARIO_IDS,
  FIXTURE_SCENARIOS,
  UnknownFixtureError,
  buildFixtureViewModels,
  getFixtureScenario,
  listFixtureScenarios,
} from "../../src/fixtures/index.js";

const fixturesRoot = join(
  dirname(fileURLToPath(import.meta.url)),
  "../../src/fixtures",
);

function listTsFiles(dir: string): string[] {
  const out: string[] = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      out.push(...listTsFiles(full));
    } else if (full.endsWith(".ts")) {
      out.push(full);
    }
  }
  return out;
}

describe("fixture catalog", () => {
  it("lists unique synthetic fixtures", () => {
    const listed = listFixtureScenarios();
    const ids = listed.map((m) => m.fixtureId);
    expect(new Set(ids).size).toBe(ids.length);
    expect(ids.sort()).toEqual([...FIXTURE_SCENARIO_IDS].sort());
    for (const meta of listed) {
      expect(meta.synthetic).toBe(true);
      expect(meta.illustrative).toBe(true);
      expect(meta.notOperationalEvidence).toBe(true);
      expect(meta.exampleLabel).toBe("Dados ilustrativos");
      expect(meta.technicalLabel).toBe("Synthetic fixture");
    }
  });

  it("looks up scenarios and rejects unknown ids", () => {
    const s = getFixtureScenario("current_project_state_illustrative");
    expect(s.metadata.fixtureId).toBe("current_project_state_illustrative");
    expect(() => getFixtureScenario("does_not_exist")).toThrow(
      UnknownFixtureError,
    );
  });

  it("is deterministic and serializable", () => {
    for (const id of FIXTURE_SCENARIO_IDS) {
      const a = getFixtureScenario(id);
      const b = getFixtureScenario(id);
      expect(a).toEqual(b);
      const json = JSON.stringify(a);
      expect(JSON.parse(json)).toEqual(JSON.parse(JSON.stringify(b)));
    }
  });

  it("uses valid fixed ISO-8601 timestamps when present", () => {
    const isoRe =
      /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{3})?(?:Z|[+-]\d{2}:\d{2})$/;
    for (const id of FIXTURE_SCENARIO_IDS) {
      const scenario = FIXTURE_SCENARIOS[id];
      expect(scenario.nowIso).toMatch(isoRe);
      expect(Number.isNaN(Date.parse(scenario.nowIso))).toBe(false);
      for (const run of scenario.runs.runs) {
        for (const stamp of [run.startedAt.iso, run.finishedAt.iso]) {
          if (stamp !== null) {
            expect(stamp).toMatch(isoRe);
            expect(Number.isNaN(Date.parse(stamp))).toBe(false);
          }
        }
      }
    }
  });

  it("does not mutate fixture inputs when building view models", () => {
    const before = JSON.stringify(
      getFixtureScenario("current_project_state_illustrative"),
    );
    buildFixtureViewModels("current_project_state_illustrative");
    const after = JSON.stringify(
      getFixtureScenario("current_project_state_illustrative"),
    );
    expect(after).toBe(before);
  });
});

describe("fixture ViewModel execution", () => {
  it("builds ViewModels for every scenario", () => {
    for (const id of FIXTURE_SCENARIO_IDS) {
      const vms = buildFixtureViewModels(id);
      expect(vms.metadata.synthetic).toBe(true);
      expect(vms.overview).toBeTruthy();
      expect(vms.runs).toBeTruthy();
      expect(vms.readiness).toBeTruthy();
      expect(vms.hostScheduler).toBeTruthy();
    }
  });

  it("keeps current project illustrative posture", () => {
    const vms = buildFixtureViewModels("current_project_state_illustrative");
    expect(vms.metadata.fixtureId).toBe("current_project_state_illustrative");
    expect(vms.readiness.state).toBe("not_ready");
    expect(vms.readiness.presentation.status).toBe("not_ready");
    expect(vms.readiness.blockingReasonCodes).toContain(
      "WINDOW_DAYS_INSUFFICIENT",
    );
    expect(vms.readiness.validationCommandExecuted).toBe(false);
    expect(vms.readiness.effectPeekingPerformed).toBe(false);
    expect(vms.hostScheduler.hostDiscoveryState).toBe("deferred");
    expect(vms.hostScheduler.schedulerState).toBe("blocked");
    expect(vms.hostScheduler.operationalDebt).toBe("open");
    expect(vms.overview.scientificGate).toBe("PENDING_FUTURE_UNSEEN_DATA");
    expect(vms.overview.r4Status).toBe("BLOCKED");
    expect(vms.overview.r5Status).toBe("NOT_STARTED");
    expect(vms.overview.collectionSummary.explanation.status).toBe(
      "informational",
    );
  });

  it("maps not-ready / blocked / deferred without fault", () => {
    const notReady = buildFixtureViewModels("readiness_window_insufficient");
    expect(notReady.readiness.presentation.status).toBe("not_ready");
    expect(notReady.readiness.presentation.status).not.toBe("fault");

    const blocked = buildFixtureViewModels("scheduler_blocked_not_authorized");
    expect(blocked.hostScheduler.schedulerPresentation.status).toBe("blocked");
    expect(blocked.hostScheduler.schedulerPresentation.status).not.toBe(
      "fault",
    );

    const deferred = buildFixtureViewModels("host_discovery_deferred");
    expect(deferred.hostScheduler.hostPresentation.status).toBe("deferred");
    expect(deferred.hostScheduler.hostPresentation.status).not.toBe("fault");
  });

  it("maps confirmed fault to fault severity", () => {
    const fault = buildFixtureViewModels("confirmed_collection_fault");
    expect(fault.runs.summaryStatus).toBe("fault");
    expect(fault.overview.lastFailedRun?.presentation.status).toBe("fault");
  });

  it("keeps partial data null without inventing zeroes", () => {
    const partial = buildFixtureViewModels("partial_unknown_data");
    expect(partial.readiness.windowDays.value).toBeNull();
    expect(partial.readiness.requiredWindowDays.value).toBeNull();
    expect(partial.hostScheduler.lastCycleAt.rawIso).toBeNull();
    expect(partial.runs.runs).toEqual([]);
  });

  it("supports empty runs scenario", () => {
    const empty = buildFixtureViewModels("empty_no_runs");
    expect(empty.runs.runs).toEqual([]);
    expect(empty.overview.lastCompletedRun).toBeNull();
    expect(empty.overview.lastFailedRun).toBeNull();
  });

  it("accepts explicit now override", () => {
    const vms = buildFixtureViewModels(
      "collection_in_progress",
      "2026-07-21T00:00:00.000Z",
    );
    expect(vms.nowIso).toBe("2026-07-21T00:00:00.000Z");
    expect(vms.overview.generatedWithNow).toBe("2026-07-21T00:00:00.000Z");
  });
});

describe("fixture architecture boundaries", () => {
  it("does not import react, router, network, or screens", () => {
    const files = listTsFiles(fixturesRoot);
    expect(files.length).toBeGreaterThan(0);
    const forbidden = [
      /from\s+["']react["']/,
      /from\s+["']react-dom/,
      /from\s+["']react-router/,
      /\bfetch\s*\(/,
      /from\s+["'].*\/shell\//,
      /from\s+["'].*\/components\//,
      /from\s+["'].*screens/,
    ];
    const violations: string[] = [];
    for (const file of files) {
      const source = readFileSync(file, "utf8");
      for (const pattern of forbidden) {
        if (pattern.test(source)) {
          violations.push(`${file} ${pattern}`);
        }
      }
    }
    expect(violations).toEqual([]);
  });

  it("does not use Date.now or Math.random", () => {
    const files = listTsFiles(fixturesRoot);
    const violations: string[] = [];
    for (const file of files) {
      const source = readFileSync(file, "utf8")
        .replace(/\/\*[\s\S]*?\*\//g, "")
        .replace(/\/\/.*$/gm, "");
      if (/\bDate\.now\s*\(/.test(source) || /\bMath\.random\s*\(/.test(source)) {
        violations.push(file);
      }
      if (/\bnew\s+Date\s*\(\s*\)/.test(source)) {
        violations.push(`${file} new Date()`);
      }
    }
    expect(violations).toEqual([]);
  });
});
