/**
 * UX-R1 I6I — Prontidão screen data assembly.
 * Fixture-backed only. No network / filesystem / operational sources.
 */

import {
  buildFixtureViewModels,
  type FixtureMetadata,
  type FixtureScenarioId,
  type FixtureViewModels,
} from "../../fixtures";
import type { ReadinessViewModel } from "../../viewmodels";

export const READINESS_FIXTURE_ID =
  "current_project_state_illustrative" as const;

export const SYNTHETIC_EVIDENCE_DISCLAIMER =
  "Não representa evidência operacional real";

export const ILLUSTRATIVE_WINDOW_DISCLOSURE =
  "Valores de janela são ilustrativos (fixture sintético). Não representam o protocolo operacional completo nem comprovam vantagem preditiva.";

export type ReadinessScreenData = {
  fixtureId: FixtureScenarioId;
  metadata: FixtureMetadata;
  readiness: ReadinessViewModel;
  nowIso: string;
};

/**
 * Product route always uses READINESS_FIXTURE_ID.
 * Tests may pass another catalog id to cover required scenarios.
 */
export function loadReadinessScreenData(
  fixtureId: FixtureScenarioId = READINESS_FIXTURE_ID,
): ReadinessScreenData {
  const packed: FixtureViewModels = buildFixtureViewModels(fixtureId);
  return {
    fixtureId,
    metadata: packed.metadata,
    readiness: packed.readiness,
    nowIso: packed.nowIso,
  };
}
