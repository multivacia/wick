import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const testDir = dirname(fileURLToPath(import.meta.url));
const runsRoot = join(testDir, "../../../src/screens/runs");

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
  /from\s+["'].*wick\.operational/,
  /from\s+["'].*r3e/,
  /scheduler\.activate/,
  /activateScheduler/,
  /runCollection/,
  /validate_future/,
  /from\s+["']fs["']/,
  /from\s+["']node:fs["']/,
  /from\s+["']node:child_process["']/,
];

describe("Runs screen architecture boundaries", () => {
  it("does not import network clients, operational commands, or scientific modules", () => {
    const files = listFiles(runsRoot);
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
  });

  it("does not include a visible fixture selector control", () => {
    const files = listFiles(runsRoot);
    const joined = files.map((f) => readFileSync(f, "utf8")).join("\n");
    expect(joined).not.toMatch(/<select/i);
    expect(joined).not.toMatch(/fixture-selector/i);
    expect(joined).not.toMatch(/FixtureSelector/);
  });
});
