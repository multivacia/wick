import { useState } from "react";
import { Outlet } from "react-router-dom";
import { SkipLink } from "./SkipLink";
import { TopBar } from "./TopBar";
import { PrimarySidebar } from "./PrimarySidebar";
import { MainContentRegion } from "./MainContentRegion";
import { MobileNavigationDrawer } from "./MobileNavigationDrawer";
import "./shell.css";

export function ApplicationShell() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="wick-shell">
      <SkipLink />
      <TopBar menuOpen={menuOpen} onMenuToggle={() => setMenuOpen((v) => !v)} />
      <div className="wick-shell__body">
        <div className="wick-shell__sidebar-slot">
          <PrimarySidebar />
        </div>
        <MainContentRegion>
          <Outlet />
        </MainContentRegion>
      </div>
      <MobileNavigationDrawer open={menuOpen} onOpenChange={setMenuOpen} />
    </div>
  );
}
