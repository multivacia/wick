import { NAV_GROUPS } from "./navigation";
import { NavigationGroup } from "./NavigationGroup";
import "./shell.css";

export type PrimarySidebarProps = {
  onNavigate?: () => void;
};

export function PrimarySidebar({ onNavigate }: PrimarySidebarProps) {
  return (
    <aside className="wick-sidebar" aria-label="Navegação principal">
      <div className="wick-sidebar__brand">
        <p className="wick-sidebar__product">Wick</p>
        <p className="wick-sidebar__tagline">Centro operacional</p>
      </div>
      <nav className="wick-sidebar__nav" aria-label="Principal">
        {NAV_GROUPS.map((group) => (
          <NavigationGroup
            key={group.id}
            group={group}
            onNavigate={onNavigate}
          />
        ))}
      </nav>
    </aside>
  );
}
