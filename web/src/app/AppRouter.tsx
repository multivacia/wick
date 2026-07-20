import { BrowserRouter, MemoryRouter } from "react-router-dom";
import type { ReactNode } from "react";
import { AppRoutes } from "./AppRoutes";

export type AppRouterProps = {
  /** When set, use MemoryRouter (tests). Otherwise BrowserRouter. */
  initialEntries?: string[];
  children?: ReactNode;
};

export function AppRouter({ initialEntries }: AppRouterProps) {
  if (initialEntries) {
    return (
      <MemoryRouter initialEntries={initialEntries}>
        <AppRoutes />
      </MemoryRouter>
    );
  }

  return (
    <BrowserRouter>
      <AppRoutes />
    </BrowserRouter>
  );
}
