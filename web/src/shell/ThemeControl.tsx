import { useEffect, useState } from "react";
import {
  applyResolvedTheme,
  readThemePreference,
  resolveTheme,
  type ThemePreference,
} from "../theme/theme";
import { Button } from "../components/primitives";
import {
  resolveNextThemePreference,
  THEME_PREFERENCE_LABELS,
} from "./themePreference";
import "./shell.css";

export function ThemeControl() {
  const [preference, setPreference] = useState<ThemePreference>(() =>
    typeof document === "undefined"
      ? "system"
      : readThemePreference(document.documentElement),
  );

  useEffect(() => {
    const root = document.documentElement;
    root.setAttribute("data-theme-preference", preference);
    const media =
      typeof window !== "undefined" && typeof window.matchMedia === "function"
        ? window.matchMedia("(prefers-color-scheme: dark)")
        : null;
    const apply = () => {
      applyResolvedTheme(
        resolveTheme(preference, Boolean(media?.matches)),
        root,
      );
    };
    apply();
    if (preference !== "system" || !media) {
      return;
    }
    media.addEventListener("change", apply);
    return () => media.removeEventListener("change", apply);
  }, [preference]);

  function cycleTheme() {
    setPreference((current) => resolveNextThemePreference(current));
  }

  return (
    <Button
      type="button"
      variant="quiet"
      size="sm"
      className="wick-theme-control"
      onClick={cycleTheme}
      aria-label={`Tema: ${THEME_PREFERENCE_LABELS[preference]}. Alternar tema`}
    >
      Tema: {THEME_PREFERENCE_LABELS[preference]}
    </Button>
  );
}
