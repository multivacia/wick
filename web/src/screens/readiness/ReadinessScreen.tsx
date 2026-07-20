import { loadReadinessScreenData } from "./loadReadinessScreenData";
import { ReadinessScreenView } from "./ReadinessScreenView";

/**
 * Prontidão — Readiness product screen (I6I).
 * Read-only, fixture-backed, no operational controls.
 * Product route always uses READINESS_FIXTURE_ID.
 */
export function ReadinessScreen() {
  return <ReadinessScreenView data={loadReadinessScreenData()} />;
}
