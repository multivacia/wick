import { describe, expect, it } from "vitest";
import {
  contrastRatio,
  WCAG_AA_NORMAL_TEXT,
  WCAG_AA_UI,
} from "../../src/theme/contrast";

/**
 * Contrast pairs use the same hex literals wired in raw.css / theme files.
 * Manual verification remains for edge cases; these pairs are the automated gate.
 */

const LIGHT = {
  canvas: "#f8fafc",
  panel: "#ffffff",
  textPrimary: "#0f172a",
  textSecondary: "#334155",
  focus: "#0e7490",
  status: {
    healthy: { fg: "#065f46", bg: "#ecfdf5" },
    completed: { fg: "#065f46", bg: "#ecfdf5" },
    attention: { fg: "#78350f", bg: "#fffbeb" },
    notReady: { fg: "#78350f", bg: "#fffbeb" },
    blocked: { fg: "#4c1d95", bg: "#f5f3ff" },
    deferred: { fg: "#5b21b6", bg: "#f5f3ff" },
    unknown: { fg: "#1e293b", bg: "#f1f5f9" },
    fault: { fg: "#991b1b", bg: "#fef2f2" },
    informational: { fg: "#164e63", bg: "#ecfeff" },
  },
} as const;

const DARK = {
  canvas: "#020617",
  panel: "#0f172a",
  textPrimary: "#f8fafc",
  textSecondary: "#cbd5e1",
  focus: "#67e8f9",
  status: {
    healthy: { fg: "#d1fae5", bg: "#064e3b" },
    completed: { fg: "#d1fae5", bg: "#064e3b" },
    attention: { fg: "#fef3c7", bg: "#78350f" },
    notReady: { fg: "#fef3c7", bg: "#78350f" },
    blocked: { fg: "#ede9fe", bg: "#4c1d95" },
    deferred: { fg: "#ede9fe", bg: "#4c1d95" },
    unknown: { fg: "#f1f5f9", bg: "#1e293b" },
    fault: { fg: "#fee2e2", bg: "#7f1d1d" },
    informational: { fg: "#cffafe", bg: "#164e63" },
  },
} as const;

function expectAa(fg: string, bg: string, min = WCAG_AA_NORMAL_TEXT): void {
  const ratio = contrastRatio(fg, bg);
  expect(ratio, `${fg} on ${bg}`).not.toBeNull();
  expect(ratio!, `${fg} on ${bg}`).toBeGreaterThanOrEqual(min);
}

describe("WCAG 2.2 AA contrast — light theme", () => {
  it("passes primary text on canvas and panel", () => {
    expectAa(LIGHT.textPrimary, LIGHT.canvas);
    expectAa(LIGHT.textPrimary, LIGHT.panel);
  });

  it("passes secondary text on canvas", () => {
    expectAa(LIGHT.textSecondary, LIGHT.canvas);
  });

  it("passes focus ring as UI non-text contrast on canvas", () => {
    expectAa(LIGHT.focus, LIGHT.canvas, WCAG_AA_UI);
  });

  it("passes status badge fg/bg pairs", () => {
    for (const [name, pair] of Object.entries(LIGHT.status)) {
      expectAa(pair.fg, pair.bg);
      expect(name.length).toBeGreaterThan(0);
    }
  });
});

describe("WCAG 2.2 AA contrast — dark theme", () => {
  it("passes primary text on canvas and panel", () => {
    expectAa(DARK.textPrimary, DARK.canvas);
    expectAa(DARK.textPrimary, DARK.panel);
  });

  it("passes secondary text on canvas", () => {
    expectAa(DARK.textSecondary, DARK.canvas);
  });

  it("passes focus ring as UI non-text contrast on canvas", () => {
    expectAa(DARK.focus, DARK.canvas, WCAG_AA_UI);
  });

  it("passes status badge fg/bg pairs", () => {
    for (const [name, pair] of Object.entries(DARK.status)) {
      expectAa(pair.fg, pair.bg);
      expect(name.length).toBeGreaterThan(0);
    }
  });
});
