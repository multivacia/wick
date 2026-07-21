import { describe, expect, it } from "vitest";
import { readFileSync, readdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const testDir = dirname(fileURLToPath(import.meta.url));
const screenRoot = join(testDir, "../../../src/screens/evidence-explorer");
const viewmodelEvidenceFiles = [
  join(testDir, "../../../src/viewmodels/buildEvidenceExplorerViewModel.ts"),
  join(testDir, "../../../src/viewmodels/filterEvidenceCatalog.ts"),
  join(testDir, "../../../src/viewmodels/evidenceEnums.ts"),
  join(testDir, "../../../src/viewmodels/evidenceExplorerTypes.ts"),
  join(testDir, "../../../src/viewmodels/evidenceSourcePath.ts"),
];

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
  /\bprocess\.env\b/,
  /dangerouslySetInnerHTML/,
  /react-markdown/,
  /from\s+["']marked["']/,
  /from\s+["']remark/,
  /from\s+["']rehype/,
  /innerHTML\s*=/,
];

describe("Evidence Explorer architecture boundaries", () => {
  it("does not import network, filesystem, markdown renderers, or unsafe HTML", () => {
    const files = [...listFiles(screenRoot), ...viewmodelEvidenceFiles];
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
    const files = listFiles(screenRoot);
    const joined = files.map((f) => readFileSync(f, "utf8")).join("\n");
    expect(joined).not.toMatch(/fixture-selector/i);
    expect(joined).not.toMatch(/FixtureSelector/);
    expect(joined).not.toMatch(/selecionar fixture/i);
    expect(joined).not.toMatch(/getFixtureScenario\s*\(/);
  });

  it("does not offer download or open-file actions", () => {
    const files = listFiles(screenRoot);
    const joined = files.map((f) => readFileSync(f, "utf8")).join("\n");
    expect(joined).not.toMatch(/\bdownload\b/i);
    expect(joined).not.toMatch(/href=["']https?:/i);
    expect(joined).not.toMatch(/window\.open/);
    expect(joined).not.toMatch(/<a[^>]+download/i);
  });
});
