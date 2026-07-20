import { Navigate, Route, Routes } from "react-router-dom";
import { ApplicationShell } from "../shell/ApplicationShell";
import { RoutePlaceholder } from "../shell/RoutePlaceholder";
import {
  NOT_FOUND_PLACEHOLDER,
  ROUTE_PLACEHOLDERS,
} from "../shell/navigation";
import { OverviewScreen } from "../screens/overview";

function PlaceholderPage({ path }: { path: keyof typeof ROUTE_PLACEHOLDERS }) {
  const model = ROUTE_PLACEHOLDERS[path];
  if (!model) {
    return <RoutePlaceholder model={NOT_FOUND_PLACEHOLDER} />;
  }
  return <RoutePlaceholder model={model} />;
}

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<ApplicationShell />}>
        <Route index element={<Navigate to="/overview" replace />} />
        <Route path="overview" element={<OverviewScreen />} />
        <Route
          path="future-collection/runs"
          element={<PlaceholderPage path="/future-collection/runs" />}
        />
        <Route
          path="future-collection/readiness"
          element={<PlaceholderPage path="/future-collection/readiness" />}
        />
        <Route
          path="operations/host-scheduler"
          element={<PlaceholderPage path="/operations/host-scheduler" />}
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
