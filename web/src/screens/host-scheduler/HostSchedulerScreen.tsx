import { loadHostSchedulerScreenData } from "./loadHostSchedulerScreenData";
import { HostSchedulerScreenView } from "./HostSchedulerScreenView";

/**
 * Host e Automação — Host/Scheduler product screen (I6K).
 * Read-only, fixture-backed, no operational controls.
 * Product route always uses HOST_SCHEDULER_FIXTURE_ID.
 */
export function HostSchedulerScreen() {
  return <HostSchedulerScreenView data={loadHostSchedulerScreenData()} />;
}
