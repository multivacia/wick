import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const testDir = dirname(fileURLToPath(import.meta.url));
const viewmodelsRoot = join(testDir, "../../src/viewmodels");

function listFiles(dir: string): string[] {
  const out: string[] = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) {
      out.push(...listFiles(full));
    } else if (full.endsWith(".ts")) {
      out.push(full);
    }
  }
  return out;
}

const FORBIDDEN = [
  /from\s+["']react["']/,
  /from\s+["']react\//,
  /from\s+["']react-dom/,
  /from\s+["']react-router/,
  /from\s+["']react-router-dom["']/,
  /\bfetch\s*\(/,
  /from\s+["'].*fixtures/,
  /from\s+["'].*\/shell\//,
  /from\s+["'].*\/components\//,
  /from\s+["'].*screens/,
];

describe("ViewModel architecture boundaries", () => {
  it("does not import react, router, fetch clients, fixtures, or screens", () => {
    const files = listFiles(viewmodelsRoot);
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
});
