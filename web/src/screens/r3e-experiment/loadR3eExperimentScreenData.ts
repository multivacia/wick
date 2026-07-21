/**
 * UX-R1 I6M — Experimento R3E screen data assembly.
 * Fixture-backed only. No network / filesystem / validation / effect peeking.
 */

import {
  buildFixtureViewModels,
  type FixtureMetadata,
  type FixtureScenarioId,
  type FixtureViewModels,
} from "../../fixtures";
import type { R3eExperimentViewModel } from "../../viewmodels";

export const R3E_EXPERIMENT_FIXTURE_ID =
  "r3e_experiment_current_state_illustrative" as const;

export const SYNTHETIC_EVIDENCE_DISCLAIMER =
  "Não representa evidência científica operacional real";

export const R3E_SYNTHETIC_SCIENCE_DISCLAIMER =
  "Dados sintéticos ilustrativos — não comprovam edge, não mostram resultados futuros não vistos e não autorizam trading nem dinheiro real.";

export type R3eExperimentScreenData = {
  fixtureId: FixtureScenarioId;
  metadata: FixtureMetadata;
  r3eExperiment: R3eExperimentViewModel;
  nowIso: string;
};

/**
 * Product route always uses R3E_EXPERIMENT_FIXTURE_ID.
 * Tests may pass another catalog id only when that scenario includes R3E fields.
 */
export function loadR3eExperimentScreenData(
  fixtureId: FixtureScenarioId = R3E_EXPERIMENT_FIXTURE_ID,
): R3eExperimentScreenData {
  const packed: FixtureViewModels = buildFixtureViewModels(fixtureId);
  return {
    fixtureId,
    metadata: packed.metadata,
    r3eExperiment: packed.r3eExperiment,
    nowIso: packed.nowIso,
  };
}
