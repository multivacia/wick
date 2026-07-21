/**
 * UX-R1 I6C — executable synthetic fixtures for I6B ViewModels.
 * Do not import React, router, network clients, or screens here.
 * Do not treat fixtures as live operational evidence.
 */

export {
  EXAMPLE_LABEL,
  TECHNICAL_LABEL,
  fixtureMetadata,
  type FixtureMetadata,
} from "./metadata.js";

export {
  FIXTURE_NOW_ISO,
  emptyMetric,
  metric,
  ts,
  run,
  readiness,
  host,
  scheduler,
  r3eExperiment,
} from "./builders.js";

export type { FixtureScenario, FixtureScenarioId } from "./types.js";

export {
  FIXTURE_SCENARIOS,
  FIXTURE_SCENARIO_IDS,
} from "./scenarios.js";

export {
  listFixtureScenarios,
  getFixtureScenario,
  buildFixtureViewModels,
  UnknownFixtureError,
  type FixtureViewModels,
} from "./catalog.js";

export {
  EVIDENCE_CATALOG_FIXTURE_ID,
  EVIDENCE_CATALOG_NOW_ISO,
  getEvidenceCatalogFixture,
  type EvidenceCatalogFixture,
} from "./evidenceCatalog.js";
