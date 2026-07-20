/**
 * UX-R1 I6B — shared presentation status semantics.
 * Framework-agnostic. No React / router / network imports.
 */

export const DOMAIN_LIFECYCLE_STATES = [
  "unknown",
  "not_available",
  "not_started",
  "in_progress",
  "complete",
  "not_ready",
  "ready",
  "blocked",
  "fault",
  "deferred",
] as const;

export type DomainLifecycleState = (typeof DOMAIN_LIFECYCLE_STATES)[number];

/** Presentation status aligned with I2 StatusBadge semantics. */
export const PRESENTATION_STATUSES = [
  "healthy",
  "completed",
  "informational",
  "attention",
  "not_ready",
  "blocked",
  "deferred",
  "unknown",
  "fault",
] as const;

export type PresentationStatus = (typeof PRESENTATION_STATUSES)[number];

export const PRESENTATION_SEVERITIES = [
  "healthy",
  "informational",
  "attention",
  "blocked",
  "neutral",
  "critical",
] as const;

export type PresentationSeverity = (typeof PRESENTATION_SEVERITIES)[number];

export type StatusSemanticMapping = {
  status: PresentationStatus;
  severity: PresentationSeverity;
  colorTokenHint:
    | "green"
    | "cyan"
    | "amber"
    | "purple_or_gray"
    | "gray"
    | "red";
};

/**
 * Map domain lifecycle → presentation semantics.
 * Critical: NOT_READY / BLOCKED / DEFERRED are never FAULT (red).
 */
export function mapDomainStateToPresentation(
  state: DomainLifecycleState,
): StatusSemanticMapping {
  switch (state) {
    case "ready":
      return { status: "healthy", severity: "healthy", colorTokenHint: "green" };
    case "complete":
      return {
        status: "completed",
        severity: "healthy",
        colorTokenHint: "green",
      };
    case "in_progress":
      return {
        status: "informational",
        severity: "informational",
        colorTokenHint: "cyan",
      };
    case "not_ready":
      return {
        status: "not_ready",
        severity: "attention",
        colorTokenHint: "amber",
      };
    case "blocked":
      return {
        status: "blocked",
        severity: "blocked",
        colorTokenHint: "purple_or_gray",
      };
    case "deferred":
      return {
        status: "deferred",
        severity: "blocked",
        colorTokenHint: "purple_or_gray",
      };
    case "fault":
      return { status: "fault", severity: "critical", colorTokenHint: "red" };
    case "not_started":
      return {
        status: "unknown",
        severity: "neutral",
        colorTokenHint: "gray",
      };
    case "not_available":
      return {
        status: "unknown",
        severity: "neutral",
        colorTokenHint: "gray",
      };
    case "unknown":
    default:
      return {
        status: "unknown",
        severity: "neutral",
        colorTokenHint: "gray",
      };
  }
}

export function isFaultPresentation(status: PresentationStatus): boolean {
  return status === "fault";
}

export function assertSemanticInequalities(
  mapping: StatusSemanticMapping,
  domain: DomainLifecycleState,
): void {
  if (domain === "not_ready" && mapping.status === "fault") {
    throw new Error("NOT_READY must not map to FAULT");
  }
  if (domain === "blocked" && mapping.status === "fault") {
    throw new Error("BLOCKED must not map to FAULT");
  }
  if (domain === "deferred" && mapping.status === "fault") {
    throw new Error("DEFERRED must not map to FAULT");
  }
  if (mapping.colorTokenHint === "red" && domain !== "fault") {
    throw new Error("Red is reserved for confirmed fault only");
  }
}
