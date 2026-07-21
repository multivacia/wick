/**
 * Evidence sourcePath allowlist validation (metadata display only).
 * Rejects traversal, absolute paths, URLs, secrets, and home paths.
 */

const FORBIDDEN_SUBSTRINGS = [
  "..",
  ".env",
  "secrets",
  "secret",
  "credentials",
  "credential",
  "/home/",
  "/Users/",
  "~",
] as const;

export class InvalidEvidenceSourcePathError extends Error {
  constructor(path: string, reason: string) {
    super(`Invalid evidence sourcePath "${path}": ${reason}`);
    this.name = "InvalidEvidenceSourcePathError";
  }
}

/**
 * Validate that sourcePath is relative metadata under docs/ or reports/.
 * Throws InvalidEvidenceSourcePathError on failure.
 */
export function assertValidEvidenceSourcePath(sourcePath: string): void {
  const path = sourcePath.trim();
  if (!path) {
    throw new InvalidEvidenceSourcePathError(sourcePath, "empty path");
  }
  if (!(path.startsWith("docs/") || path.startsWith("reports/"))) {
    throw new InvalidEvidenceSourcePathError(
      sourcePath,
      "must start with docs/ or reports/",
    );
  }
  if (path.startsWith("/") || /^[A-Za-z]:[\\/]/.test(path)) {
    throw new InvalidEvidenceSourcePathError(sourcePath, "absolute paths forbidden");
  }
  if (/^[a-z][a-z0-9+.-]*:\/\//i.test(path) || path.includes("://")) {
    throw new InvalidEvidenceSourcePathError(sourcePath, "URLs forbidden");
  }
  const lower = path.toLowerCase();
  for (const fragment of FORBIDDEN_SUBSTRINGS) {
    if (lower.includes(fragment.toLowerCase()) || path.includes(fragment)) {
      throw new InvalidEvidenceSourcePathError(
        sourcePath,
        `forbidden fragment "${fragment}"`,
      );
    }
  }
  if (path.startsWith("reports/r3e_future_unseen/")) {
    throw new InvalidEvidenceSourcePathError(
      sourcePath,
      "future-unseen result payloads forbidden",
    );
  }
}

export function isValidEvidenceSourcePath(sourcePath: string): boolean {
  try {
    assertValidEvidenceSourcePath(sourcePath);
    return true;
  } catch {
    return false;
  }
}
