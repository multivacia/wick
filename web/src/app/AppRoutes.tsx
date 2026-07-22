import { Navigate, Route, Routes } from "react-router-dom";
import { ApplicationShell } from "../shell/ApplicationShell";
import { RoutePlaceholder } from "../shell/RoutePlaceholder";
import { NOT_FOUND_PLACEHOLDER } from "../shell/navigation";
import { CollectedDataScreen } from "../screens/collected-data";
import { EvidenceExplorerScreen } from "../screens/evidence-explorer";
import { HostSchedulerScreen } from "../screens/host-scheduler";
import { OverviewScreen } from "../screens/overview";
import { ReadinessScreen } from "../screens/readiness";
import { R3eExperimentScreen } from "../screens/r3e-experiment";
import { RunsScreen } from "../screens/runs";

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<ApplicationShell />}>
        <Route index element={<Navigate to="/overview" replace />} />
        <Route path="overview" element={<OverviewScreen />} />
        <Route path="future-collection/runs" element={<RunsScreen />} />
        <Route
          path="future-collection/readiness"
          element={<ReadinessScreen />}
        />
        <Route
          path="future-collection/collected-data"
          element={<CollectedDataScreen />}
        />
        <Route
          path="operations/host-scheduler"
          element={<HostSchedulerScreen />}
        />
        <Route path="experiments/r3e" element={<R3eExperimentScreen />} />
        <Route
          path="governance/evidence"
          element={<EvidenceExplorerScreen />}
        />
        <Route
          path="not-found"
          element={<RoutePlaceholder model={NOT_FOUND_PLACEHOLDER} />}
        />
        <Route
          path="*"
          element={<RoutePlaceholder model={NOT_FOUND_PLACEHOLDER} />}
        />
      </Route>
    </Routes>
  );
}
