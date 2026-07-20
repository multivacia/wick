/**
 * UX-R1 I6G — Execuções screen data assembly.
 * Fixture-backed only. No network / filesystem / operational sources.
 */

import {
  buildFixtureViewModels,
  type FixtureMetadata,
  type FixtureScenarioId,
  type FixtureViewModels,
} from "../../fixtures";
import type { RunsViewModel } from "../../viewmodels";

export const RUNS_FIXTURE_ID = "current_project_state_illustrative" as const;

export const SYNTHETIC_EVIDENCE_DISCLAIMER =
  "Não representa evidência operacional real";

export type RunsScreenData = {
  fixtureId: FixtureScenarioId;
  metadata: FixtureMetadata;
  runs: RunsViewModel;
  nowIso: string;
};

/**
 * Product route always uses RUNS_FIXTURE_ID.
 * Tests may pass another catalog id to cover required scenarios.
 */
export function loadRunsScreenData(
  fixtureId: FixtureScenarioId = RUNS_FIXTURE_ID,
): RunsScreenData {
  const packed: FixtureViewModels = buildFixtureViewModels(fixtureId);
  return {
    fixtureId,
    metadata: packed.metadata,
    runs: packed.runs,
    nowIso: packed.nowIso,
  };
}
