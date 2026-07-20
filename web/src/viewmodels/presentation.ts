/**
 * Shared presentation contracts — plain language first, technical evidence second.
 */

import type { PresentationSeverity, PresentationStatus } from "./status.js";
import type { ReasonCode } from "./reasons.js";

export type PrimaryMessage = {
  plainLanguage: string;
  technicalCode: string | null;
};

export type TechnicalDetail = {
  plainLanguage: string;
  technicalCode: string | null;
  reasonCode: ReasonCode | null;
};

export type EvidenceLink = {
  label: string;
  reference: string;
  kind: "path" | "uri" | "run_id" | "artifact" | "note";
};

export type ActionHint = {
  code: ActionHintCode;
  plainLanguage: string;
  /** Advisory only — never implies automatic execution. */
  advisoryOnly: true;
};

export const ACTION_HINT_CODES = [
  "continue_collecting",
  "review_blocker_evidence",
  "complete_host_discovery",
  "wait_for_sufficient_future_window",
  "request_separate_activation_authorization",
  "investigate_failed_run",
  "monitor_collection",
  "do_not_validate",
  "no_action_available",
] as const;

export type ActionHintCode = (typeof ACTION_HINT_CODES)[number];

export type TimestampPresentation = {
  rawIso: string | null;
  displayText: string | null;
  relativeText: string | null;
  freshness: FreshnessClassification;
  availability: ValueAvailability;
};

export type FreshnessClassification =
  | "current"
  | "stale"
  | "absent"
  | "unknown"
  | "not_applicable";

export type ValueAvailability =
  | "available"
  | "unknown"
  | "not_available"
  | "not_supplied";

export type MetricPresentation = {
  label: string;
  /** Never invent zeroes — null when missing. */
  value: number | null;
  unit: string | null;
  availability: ValueAvailability;
  displayText: string | null;
};

export type StateExplanation = {
  status: PresentationStatus;
  severity: PresentationSeverity;
  primaryMessage: PrimaryMessage;
  technicalDetail: TechnicalDetail;
  reasonCodes: ReasonCode[];
};

export type PresentationBlock = {
  explanation: StateExplanation;
  evidence: EvidenceLink[];
  actionHint: ActionHint | null;
  observedAt: TimestampPresentation | null;
};
