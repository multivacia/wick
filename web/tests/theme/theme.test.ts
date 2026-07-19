import { describe, expect, it } from "vitest";
import {
  applyResolvedTheme,
  bootstrapTheme,
  getSystemPrefersDark,
  isResolvedTheme,
  isThemePreference,
  readThemePreference,
  resolveTheme,
} from "../../src/theme/theme";

describe("theme resolution", () => {
  it("resolves explicit light and dark", () => {
    expect(resolveTheme("light")).toBe("light");
    expect(resolveTheme("dark")).toBe("dark");
  });

  it("resolves system from prefers-color-scheme", () => {
    expect(resolveTheme("system", false)).toBe("light");
    expect(resolveTheme("system", true)).toBe("dark");
  });

  it("falls back to light for invalid preferences", () => {
    expect(resolveTheme("bogus")).toBe("light");
    expect(resolveTheme(undefined)).toBe("light");
    expect(resolveTheme(null)).toBe("light");
    expect(resolveTheme(42)).toBe("light");
  });

  it("validates preference and resolved theme guards", () => {
    expect(isThemePreference("system")).toBe(true);
    expect(isThemePreference("hc")).toBe(false);
    expect(isResolvedTheme("dark")).toBe(true);
    expect(isResolvedTheme("system")).toBe(false);
  });

  it("reads system preference from media query matches", () => {
    expect(getSystemPrefersDark({ matches: true })).toBe(true);
    expect(getSystemPrefersDark({ matches: false })).toBe(false);
    expect(getSystemPrefersDark(null)).toBe(false);
  });
});

describe("theme application", () => {
  it("applies light theme attribute and class", () => {
    const root = document.createElement("html");
    applyResolvedTheme("light", root);
    expect(root.getAttribute("data-theme")).toBe("light");
    expect(root.classList.contains("wick-theme-light")).toBe(true);
    expect(root.classList.contains("wick-theme-dark")).toBe(false);
  });

  it("applies dark theme attribute and class", () => {
    const root = document.createElement("html");
    applyResolvedTheme("dark", root);
    expect(root.getAttribute("data-theme")).toBe("dark");
    expect(root.classList.contains("wick-theme-dark")).toBe(true);
    expect(root.classList.contains("wick-theme-light")).toBe(false);
  });

  it("bootstraps from data-theme-preference=system", () => {
    const root = document.createElement("html");
    root.setAttribute("data-theme-preference", "system");
    const theme = bootstrapTheme(undefined, {
      root,
      systemPrefersDark: true,
    });
    expect(theme).toBe("dark");
    expect(root.getAttribute("data-theme")).toBe("dark");
  });

  it("bootstraps explicit preference argument over attributes", () => {
    const root = document.createElement("html");
    root.setAttribute("data-theme-preference", "dark");
    const theme = bootstrapTheme("light", { root });
    expect(theme).toBe("light");
    expect(root.getAttribute("data-theme")).toBe("light");
  });

  it("readThemePreference defaults to system when unset", () => {
    const root = document.createElement("html");
    expect(readThemePreference(root)).toBe("system");
  });
});
