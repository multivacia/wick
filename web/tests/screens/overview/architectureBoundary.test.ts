import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const testDir = dirname(fileURLToPath(import.meta.url));
const screensRoot = join(testDir, "../../../src/screens");

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

describe("Overview screen architecture boundaries", () => {
  it("does not import network clients, operational commands, or scientific modules", () => {
    const files = listFiles(screensRoot);
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

  it("Overview route wiring does not introduce network clients", () => {
    const routes = readFileSync(
      join(testDir, "../../../src/app/AppRoutes.tsx"),
      "utf8",
    );
    expect(routes).toMatch(/OverviewScreen/);
    expect(routes).not.toMatch(/\bfetch\s*\(/);
    expect(routes).not.toMatch(/axios/);
  });
});
