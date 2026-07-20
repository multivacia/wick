import { AppRouter } from "./app/AppRouter";

export function App() {
  return <AppRouter />;
}

/** Test helper — MemoryRouter with optional start path. */
export function AppForTest({ initialEntry = "/overview" }: { initialEntry?: string }) {
  return <AppRouter initialEntries={[initialEntry]} />;
}
