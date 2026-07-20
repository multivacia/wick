import { NavLink } from "react-router-dom";
import type { NavItem, PlannedNavItem } from "./navigation";
import { isActiveNavItem } from "./navigation";
import "./shell.css";

export type NavigationItemProps = {
  item: NavItem | PlannedNavItem;
  onNavigate?: () => void;
};

export function NavigationItem({ item, onNavigate }: NavigationItemProps) {
  if (!isActiveNavItem(item)) {
    return (
      <li className="wick-nav-item wick-nav-item--planned">
        <span
          className="wick-nav-item__label"
          aria-disabled="true"
          title={item.note}
        >
          {item.label}
        </span>
        <span className="wick-nav-item__hint">{item.note}</span>
      </li>
    );
  }

  return (
    <li className="wick-nav-item">
      <NavLink
        to={item.path}
        className={({ isActive }) =>
          [
            "wick-nav-item__link",
            isActive ? "wick-nav-item__link--active" : "",
          ]
            .filter(Boolean)
            .join(" ")
        }
        end={item.path === "/overview"}
        onClick={onNavigate}
      >
        {({ isActive }) => (
          <>
            <span className="wick-nav-item__label">{item.label}</span>
            {isActive ? (
              <span className="wick-visually-hidden"> (página atual)</span>
            ) : null}
          </>
        )}
      </NavLink>
    </li>
  );
}
