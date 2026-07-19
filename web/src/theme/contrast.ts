/**
 * Minimal WCAG relative-luminance / contrast helpers for token tests.
 * No external color dependency.
 */

function parseHex(hex: string): { r: number; g: number; b: number } | null {
  const cleaned = hex.trim().replace(/^#/, "");
  if (/^[0-9a-fA-F]{6}$/.test(cleaned)) {
    return {
      r: Number.parseInt(cleaned.slice(0, 2), 16),
      g: Number.parseInt(cleaned.slice(2, 4), 16),
      b: Number.parseInt(cleaned.slice(4, 6), 16),
    };
  }
  if (/^[0-9a-fA-F]{3}$/.test(cleaned)) {
    return {
      r: Number.parseInt(cleaned[0]! + cleaned[0]!, 16),
      g: Number.parseInt(cleaned[1]! + cleaned[1]!, 16),
      b: Number.parseInt(cleaned[2]! + cleaned[2]!, 16),
    };
  }
  return null;
}

function parseRgb(value: string): { r: number; g: number; b: number } | null {
  const match = value
    .trim()
    .match(
      /^rgba?\(\s*([\d.]+)\s*[, ]\s*([\d.]+)\s*[, ]\s*([\d.]+)(?:\s*[,/]\s*[\d.]+%?)?\s*\)$/i,
    );
  if (!match) {
    return null;
  }
  return {
    r: Number(match[1]),
    g: Number(match[2]),
    b: Number(match[3]),
  };
}

/** Resolve a computed CSS color string to sRGB 0–255 channels. */
export function parseCssColor(value: string): { r: number; g: number; b: number } | null {
  const trimmed = value.trim();
  if (trimmed.startsWith("#")) {
    return parseHex(trimmed);
  }
  return parseRgb(trimmed);
}

function channelToLinear(channel: number): number {
  const c = channel / 255;
  return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
}

export function relativeLuminance(color: { r: number; g: number; b: number }): number {
  const r = channelToLinear(color.r);
  const g = channelToLinear(color.g);
  const b = channelToLinear(color.b);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export function contrastRatio(foreground: string, background: string): number | null {
  const fg = parseCssColor(foreground);
  const bg = parseCssColor(background);
  if (!fg || !bg) {
    return null;
  }
  const l1 = relativeLuminance(fg);
  const l2 = relativeLuminance(bg);
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

export const WCAG_AA_NORMAL_TEXT = 4.5;
export const WCAG_AA_UI = 3;
