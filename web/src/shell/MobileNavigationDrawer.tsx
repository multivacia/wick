import {
  Drawer,
  DrawerClose,
  DrawerContent,
} from "../components/primitives";
import { NAV_GROUPS } from "./navigation";
import { NavigationGroup } from "./NavigationGroup";
import "./shell.css";

export type MobileNavigationDrawerProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

export function MobileNavigationDrawer({
  open,
  onOpenChange,
}: MobileNavigationDrawerProps) {
  return (
    <Drawer open={open} onOpenChange={onOpenChange}>
      <DrawerContent
        id="mobile-navigation-drawer"
        className="wick-mobile-nav-drawer"
        title="Navegação"
        description="Menu principal do centro operacional Wick"
        aria-describedby={undefined}
      >
        <nav aria-label="Principal móvel" className="wick-mobile-nav">
          {NAV_GROUPS.map((group) => (
            <NavigationGroup
              key={group.id}
              group={group}
              onNavigate={() => onOpenChange(false)}
            />
          ))}
        </nav>
        <div className="wick-mobile-nav__footer">
          <DrawerClose className="wick-button wick-button--secondary wick-button--sm">
            Fechar menu
          </DrawerClose>
        </div>
      </DrawerContent>
    </Drawer>
  );
}
