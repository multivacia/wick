/**
 * Pure fixture catalog API — framework-agnostic.
 * Calls I6B ViewModel builders only. No React/router/network.
 */

import {
  buildHostSchedulerViewModel,
  buildOverviewViewModel,
  buildReadinessViewModel,
  buildRunsViewModel,
  type HostSchedulerViewModel,
  type OverviewViewModel,
  type ReadinessViewModel,
  type RunsViewModel,
  type ViewModelClock,
} from "../viewmodels/index.js";
import { FIXTURE_SCENARIOS, FIXTURE_SCENARIO_IDS } from "./scenarios.js";
import type { FixtureScenario, FixtureScenarioId } from "./types.js";
import type { FixtureMetadata } from "./metadata.js";

export class UnknownFixtureError extends Error {
  readonly fixtureId: string;

  constructor(fixtureId: string) {
    super(`Unknown synthetic fixture id: ${fixtureId}`);
    this.name = "UnknownFixtureError";
    this.fixtureId = fixtureId;
  }
}

export function listFixtureScenarios(): FixtureMetadata[] {
  return FIXTURE_SCENARIO_IDS.map((id) => FIXTURE_SCENARIOS[id].metadata);
}

export function getFixtureScenario(id: string): FixtureScenario {
  if (!Object.prototype.hasOwnProperty.call(FIXTURE_SCENARIOS, id)) {
    throw new UnknownFixtureError(id);
  }
  return FIXTURE_SCENARIOS[id as FixtureScenarioId];
}

export type FixtureViewModels = {
  metadata: FixtureMetadata;
  overview: OverviewViewModel;
  runs: RunsViewModel;
  readiness: ReadinessViewModel;
  hostScheduler: HostSchedulerViewModel;
  nowIso: string;
};

export function buildFixtureViewModels(
  id: string,
  nowIso?: string,
): FixtureViewModels {
  const scenario = getFixtureScenario(id);
  const clock: ViewModelClock = {
    nowIso: nowIso ?? scenario.nowIso,
  };
  return {
    metadata: scenario.metadata,
    overview: buildOverviewViewModel(scenario.overview, clock),
    runs: buildRunsViewModel(scenario.runs, clock),
    readiness: buildReadinessViewModel(scenario.readiness, clock),
    hostScheduler: buildHostSchedulerViewModel(scenario.hostScheduler, clock),
    nowIso: clock.nowIso,
  };
}
