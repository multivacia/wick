import type { NavGroup } from "./navigation";
import { NavigationItem } from "./NavigationItem";
import "./shell.css";

export type NavigationGroupProps = {
  group: NavGroup;
  onNavigate?: () => void;
};

export function NavigationGroup({ group, onNavigate }: NavigationGroupProps) {
  return (
    <div className="wick-nav-group">
      <h2 className="wick-nav-group__label" id={`nav-group-${group.id}`}>
        {group.label}
      </h2>
      <ul
        className="wick-nav-group__list"
        aria-labelledby={`nav-group-${group.id}`}
      >
        {group.items.map((item) => (
          <NavigationItem key={item.id} item={item} onNavigate={onNavigate} />
        ))}
      </ul>
    </div>
  );
}
