/**
 * Design token contract constants for tests and typed references.
 * Not a component token layer — I2 only.
 */

export const DESIGN_TOKEN_CONTRACT_VERSION = "1.0.0" as const;

export const THEME_ATTRIBUTE = "data-theme" as const;

export type ResolvedTheme = "light" | "dark";
export type ThemePreference = ResolvedTheme | "system";

/** Required semantic surface/text/border/interactive tokens (prompt + merged spec). */
export const REQUIRED_SEMANTIC_COLOR_TOKENS = [
  "--wick-color-background",
  "--wick-color-surface",
  "--wick-color-surface-elevated",
  "--wick-color-surface-muted",
  "--wick-color-surface-canvas",
  "--wick-color-surface-panel",
  "--wick-color-surface-subtle",
  "--wick-color-text-primary",
  "--wick-color-text-secondary",
  "--wick-color-text-muted",
  "--wick-color-text-inverse",
  "--wick-color-border",
  "--wick-color-border-subtle",
  "--wick-color-border-strong",
  "--wick-color-focus-ring",
  "--wick-color-interactive",
  "--wick-color-interactive-hover",
  "--wick-color-interactive-active",
  "--wick-color-interactive-disabled",
  "--wick-color-brand-petroleum",
  "--wick-color-accent-cyan",
] as const;

/** Operational status semantics required by I2 implementation authorization. */
export const REQUIRED_STATUS_TOKENS = [
  "--wick-color-status-healthy",
  "--wick-color-status-completed",
  "--wick-color-status-attention",
  "--wick-color-status-not-ready",
  "--wick-color-status-blocked",
  "--wick-color-status-deferred",
  "--wick-color-status-unknown",
  "--wick-color-status-fault",
  "--wick-color-status-informational",
] as const;

/** Merged assessment aliases that must remain present. */
export const MERGED_SPEC_STATUS_ALIASES = [
  "--wick-color-status-normal",
  "--wick-color-status-success",
  "--wick-color-status-error",
  "--wick-color-status-unavailable",
] as const;

export const REQUIRED_FOCUS_TOKENS = [
  "--wick-focus-ring-color",
  "--wick-focus-ring-width",
  "--wick-focus-ring-offset",
] as const;

export const REQUIRED_MOTION_TOKENS = [
  "--wick-motion-duration-fast",
  "--wick-motion-duration-normal",
  "--wick-motion-easing-standard",
] as const;

/** Names that must never appear as token identifiers (financial/trading semantics). */
export const FORBIDDEN_TOKEN_NAME_FRAGMENTS = [
  "profit",
  "pnl",
  "p-and-l",
  "sharpe",
  "ticker",
  "casino",
  "broker",
  "edge",
  "alpha",
] as const;

export const STATUS_BADGE_PAIRS = [
  "healthy",
  "completed",
  "attention",
  "not-ready",
  "blocked",
  "deferred",
  "unknown",
  "fault",
  "informational",
] as const;
