import type { ThemePreference } from "../theme/theme";

const CYCLE: ThemePreference[] = ["system", "light", "dark"];

export const THEME_PREFERENCE_LABELS: Record<ThemePreference, string> = {
  system: "Sistema",
  light: "Claro",
  dark: "Escuro",
};

export function resolveNextThemePreference(
  current: ThemePreference,
): ThemePreference {
  const index = CYCLE.indexOf(current);
  return CYCLE[(index + 1) % CYCLE.length] ?? "system";
}

export { CYCLE as THEME_PREFERENCE_CYCLE };
