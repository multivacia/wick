/**
 * Minimal theme bootstrap — resolves and applies html[data-theme].
 * Not a CSS-in-JS theme engine / provider. No required persistence.
 */

import {
  type ResolvedTheme,
  type ThemePreference,
  THEME_ATTRIBUTE,
} from "./contract";

export {
  DESIGN_TOKEN_CONTRACT_VERSION,
  THEME_ATTRIBUTE,
  type ResolvedTheme,
  type ThemePreference,
} from "./contract";

const VALID_RESOLVED: ReadonlySet<string> = new Set(["light", "dark"]);
const VALID_PREFERENCE: ReadonlySet<string> = new Set(["light", "dark", "system"]);

export function isResolvedTheme(value: unknown): value is ResolvedTheme {
  return typeof value === "string" && VALID_RESOLVED.has(value);
}

export function isThemePreference(value: unknown): value is ThemePreference {
  return typeof value === "string" && VALID_PREFERENCE.has(value);
}

export function getSystemPrefersDark(
  media?: Pick<MediaQueryList, "matches"> | null,
): boolean {
  if (media) {
    return Boolean(media.matches);
  }
  if (typeof window === "undefined" || typeof window.matchMedia !== "function") {
    return false;
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

/**
 * Resolve a preference to light|dark.
 * Invalid / unknown inputs fall back to light.
 */
export function resolveTheme(
  preference: unknown,
  systemPrefersDark = false,
): ResolvedTheme {
  if (preference === "dark") {
    return "dark";
  }
  if (preference === "light") {
    return "light";
  }
  if (preference === "system") {
    return systemPrefersDark ? "dark" : "light";
  }
  return "light";
}

export function applyResolvedTheme(
  theme: ResolvedTheme,
  root: HTMLElement = document.documentElement,
): void {
  root.setAttribute(THEME_ATTRIBUTE, theme);
  root.classList.toggle("wick-theme-light", theme === "light");
  root.classList.toggle("wick-theme-dark", theme === "dark");
}

/**
 * Read an explicit preference from html[data-theme-preference] when present.
 * Absence means system (preserve browser/system defaults).
 */
export function readThemePreference(
  root: HTMLElement = document.documentElement,
): ThemePreference {
  const explicit = root.getAttribute("data-theme-preference");
  if (isThemePreference(explicit)) {
    return explicit;
  }
  const attr = root.getAttribute(THEME_ATTRIBUTE);
  if (attr === "light" || attr === "dark") {
    return attr;
  }
  return "system";
}

/** Apply theme before React render; safe to call repeatedly. */
export function bootstrapTheme(
  preference?: ThemePreference,
  options?: {
    root?: HTMLElement;
    systemPrefersDark?: boolean;
  },
): ResolvedTheme {
  const root = options?.root ?? document.documentElement;
  const resolvedPreference = preference ?? readThemePreference(root);
  const systemPrefersDark =
    options?.systemPrefersDark ?? getSystemPrefersDark();
  const theme = resolveTheme(resolvedPreference, systemPrefersDark);
  applyResolvedTheme(theme, root);
  return theme;
}
