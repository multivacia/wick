import type { ReactNode } from "react";
import "./shell.css";

export type MainContentRegionProps = {
  children: ReactNode;
};

export function MainContentRegion({ children }: MainContentRegionProps) {
  return (
    <main id="main-content" className="wick-main" tabIndex={-1}>
      {children}
    </main>
  );
}
