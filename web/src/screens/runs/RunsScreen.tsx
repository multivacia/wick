import { loadRunsScreenData } from "./loadRunsScreenData";
import { RunsScreenView } from "./RunsScreenView";

/**
 * Execuções — Runs product screen (I6G).
 * Read-only, fixture-backed, no operational controls.
 * Product route always uses RUNS_FIXTURE_ID.
 */
export function RunsScreen() {
  return <RunsScreenView data={loadRunsScreenData()} />;
}
