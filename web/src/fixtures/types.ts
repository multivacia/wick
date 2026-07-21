import type {
  HostSchedulerDomainInput,
  OverviewDomainInput,
  ReadinessDomainInput,
  R3eExperimentDomainInput,
  RunsDomainInput,
} from "../viewmodels/index.js";
import type { FixtureMetadata } from "./metadata.js";

export type FixtureScenarioId =
  | "healthy_collection_not_ready"
  | "collection_in_progress"
  | "readiness_window_insufficient"
  | "host_discovery_deferred"
  | "scheduler_blocked_not_authorized"
  | "confirmed_collection_fault"
  | "partial_unknown_data"
  | "empty_no_runs"
  | "mixed_operational_blockers"
  | "current_project_state_illustrative"
  | "readiness_ready_illustrative"
  | "r3e_experiment_current_state_illustrative";

export type FixtureScenario = {
  metadata: FixtureMetadata;
  overview: OverviewDomainInput;
  runs: RunsDomainInput;
  readiness: ReadinessDomainInput;
  hostScheduler: HostSchedulerDomainInput;
  r3eExperiment: R3eExperimentDomainInput;
  /** Fixed now for ViewModel freshness demos. */
  nowIso: string;
};
