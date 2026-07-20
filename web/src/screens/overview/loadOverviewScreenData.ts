/**
 * UX-R1 I6E — Visão Geral screen data assembly.
 * Fixture-backed only. No network / filesystem / operational sources.
 */

import {
  buildFixtureViewModels,
  type FixtureMetadata,
  type FixtureViewModels,
} from "../../fixtures";
import type { OverviewViewModel } from "../../viewmodels";

export const OVERVIEW_FIXTURE_ID = "current_project_state_illustrative" as const;

export const SYNTHETIC_EVIDENCE_DISCLAIMER =
  "Não representa evidência operacional real";

export type OverviewScreenData = {
  fixtureId: typeof OVERVIEW_FIXTURE_ID;
  metadata: FixtureMetadata;
  overview: OverviewViewModel;
  nowIso: string;
};

export function loadOverviewScreenData(): OverviewScreenData {
  const packed: FixtureViewModels = buildFixtureViewModels(OVERVIEW_FIXTURE_ID);
  return {
    fixtureId: OVERVIEW_FIXTURE_ID,
    metadata: packed.metadata,
    overview: packed.overview,
    nowIso: packed.nowIso,
  };
}
