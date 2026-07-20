import { Button } from "../components/primitives";
import { ThemeControl } from "./ThemeControl";
import "./shell.css";

export type TopBarProps = {
  menuOpen: boolean;
  onMenuToggle: () => void;
};

export function TopBar({ menuOpen, onMenuToggle }: TopBarProps) {
  return (
    <header className="wick-topbar" role="banner">
      <div className="wick-topbar__start">
        <Button
          type="button"
          variant="secondary"
          size="sm"
          className="wick-topbar__menu"
          aria-expanded={menuOpen}
          aria-controls="mobile-navigation-drawer"
          onClick={onMenuToggle}
        >
          Menu
        </Button>
        <p className="wick-topbar__product">Wick</p>
      </div>
      <div className="wick-topbar__end">
        <ThemeControl />
      </div>
    </header>
  );
}
