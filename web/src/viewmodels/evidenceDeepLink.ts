/**
 * Evidence Explorer deep-link helpers (UX-R2 I4).
 * No React / router imports — pure URL helpers.
 */

export const EVIDENCE_EXPLORER_PATH = "/governance/evidence";

/**
 * Build an internal href for a specific evidence entry.
 * Uses ?evidenceId= query param; no external URLs or filesystem paths.
 */
export function buildEvidenceExplorerHref(evidenceId: string): string {
  return `${EVIDENCE_EXPLORER_PATH}?evidenceId=${encodeURIComponent(evidenceId)}`;
}

/**
 * Extract and validate the evidenceId param from URLSearchParams.
 * Rejects empty values, URLs, and paths containing "..".
 */
export function parseEvidenceIdParam(
  params: URLSearchParams,
): string | null {
  const raw = params.get("evidenceId");
  if (!raw) return null;
  const trimmed = raw.trim();
  if (!trimmed) return null;
  if (/^https?:\/\//i.test(trimmed)) return null;
  if (trimmed.includes("..")) return null;
  if (trimmed.startsWith("/") || trimmed.startsWith("\\")) return null;
  return trimmed;
}
