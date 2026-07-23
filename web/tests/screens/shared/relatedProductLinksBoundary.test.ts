import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const testDir = dirname(fileURLToPath(import.meta.url));
const sharedRoot = join(testDir, "../../../src/screens/shared");

function listFiles(dir: string): string[] {
  const out: string[] = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      out.push(...listFiles(full));
    } else if (/\.(ts|tsx|css)$/.test(full)) {
      out.push(full);
    }
  }
  return out;
}

const FORBIDDEN = [
  /\bfetch\s*\(/,
  /from\s+["']axios["']/,
  /XMLHttpRequest/,
  /WebSocket/,
  /localStorage/,
  /sessionStorage/,
  /from\s+["']fs["']/,
  /from\s+["']node:fs["']/,
  /from\s+["']node:child_process["']/,
  /dangerouslySetInnerHTML/,
  /process\.env/,
];

describe("RelatedProductLinks architecture boundaries", () => {
  it("uses react-router Link only and forbids network/fs/unsafe HTML", () => {
    const files = listFiles(sharedRoot);
    expect(files.length).toBeGreaterThan(0);
    const violations: string[] = [];
    for (const file of files) {
      const source = readFileSync(file, "utf8");
      for (const pattern of FORBIDDEN) {
        if (pattern.test(source)) {
          violations.push(`${file} matches ${pattern}`);
        }
      }
    }
    expect(violations).toEqual([]);

    const productLinks = readFileSync(
      join(sharedRoot, "RelatedProductLinks.tsx"),
      "utf8",
    );
    const collectedTarget = readFileSync(
      join(sharedRoot, "collectedDataRelatedLink.ts"),
      "utf8",
    );
    expect(productLinks).toMatch(/from\s+["']react-router-dom["']/);
    expect(productLinks).toMatch(/<Link\b/);
    expect(productLinks).not.toMatch(/href=["']https?:/i);
    expect(collectedTarget).toContain("/future-collection/collected-data");
  });
});
