import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import {
  DESIGN_TOKEN_CONTRACT_VERSION,
  FORBIDDEN_TOKEN_NAME_FRAGMENTS,
  MERGED_SPEC_STATUS_ALIASES,
  REQUIRED_FOCUS_TOKENS,
  REQUIRED_MOTION_TOKENS,
  REQUIRED_SEMANTIC_COLOR_TOKENS,
  REQUIRED_STATUS_TOKENS,
} from "../../src/theme/contract";

const here = dirname(fileURLToPath(import.meta.url));
const tokensDir = join(here, "../../src/styles/tokens");

function readTokenCss(): string {
  return [
    "raw.css",
    "semantic.css",
    "themes/light.css",
    "themes/dark.css",
    "motion.css",
    "index.css",
  ]
    .map((name) => readFileSync(join(tokensDir, name), "utf8"))
    .join("\n");
}

describe("design token contract", () => {
  const css = readTokenCss();

  it("ships DESIGN_TOKEN_CONTRACT_VERSION 1.0.0", () => {
    expect(DESIGN_TOKEN_CONTRACT_VERSION).toBe("1.0.0");
    expect(css).toContain('--wick-design-token-contract-version: "1.0.0"');
  });

  it("defines required semantic color tokens", () => {
    for (const token of REQUIRED_SEMANTIC_COLOR_TOKENS) {
      expect(css, `missing ${token}`).toContain(token);
    }
  });

  it("defines required operational status tokens", () => {
    for (const token of REQUIRED_STATUS_TOKENS) {
      expect(css, `missing ${token}`).toContain(token);
    }
  });

  it("keeps merged-spec status aliases", () => {
    for (const token of MERGED_SPEC_STATUS_ALIASES) {
      expect(css, `missing ${token}`).toContain(token);
    }
  });

  it("defines focus tokens", () => {
    for (const token of REQUIRED_FOCUS_TOKENS) {
      expect(css, `missing ${token}`).toContain(token);
    }
  });

  it("defines motion tokens and reduced-motion overrides", () => {
    for (const token of REQUIRED_MOTION_TOKENS) {
      expect(css, `missing ${token}`).toContain(token);
    }
    expect(css).toContain("@media (prefers-reduced-motion: reduce)");
    expect(css).toMatch(/--wick-motion-duration-fast:\s*0ms/);
    expect(css).toMatch(/--wick-motion-duration-normal:\s*0ms/);
  });

  it("activates light and dark themes via data-theme / classes", () => {
    expect(css).toContain('html[data-theme="light"]');
    expect(css).toContain('html[data-theme="dark"]');
    expect(css).toContain(".wick-theme-light");
    expect(css).toContain(".wick-theme-dark");
  });

  it("does not introduce forbidden financial or trading token names", () => {
    const lower = css.toLowerCase();
    for (const fragment of FORBIDDEN_TOKEN_NAME_FRAGMENTS) {
      const tokenIdHits = lower.match(
        new RegExp(`--wick-[\\w-]*${fragment}[\\w-]*`, "g"),
      );
      expect(tokenIdHits ?? [], `forbidden token id containing ${fragment}`).toEqual(
        [],
      );
    }
  });

  it("keeps raw and semantic layers (no component token layer)", () => {
    expect(css).toContain("--wick-raw-color-neutral-0");
    expect(css).toContain("--wick-color-text-primary");
    expect(css).not.toMatch(/--wick-button-/);
    expect(css).not.toMatch(/--wick-component-/);
  });
});
