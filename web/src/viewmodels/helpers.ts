import type { ActionHint, ActionHintCode, EvidenceLink } from "./presentation.js";
import type { EvidenceReferenceInput } from "./inputs.js";
import { explainReasonCode, type ReasonCode } from "./reasons.js";

export function toEvidenceLinks(
  refs: EvidenceReferenceInput[],
): EvidenceLink[] {
  return refs.map((r) => ({
    label: r.label,
    reference: r.reference,
    kind: r.kind,
  }));
}

export function actionHint(
  code: ActionHintCode,
  plainLanguage: string,
): ActionHint {
  return { code, plainLanguage, advisoryOnly: true };
}

export function reasonDetail(
  code: ReasonCode,
  plainOverride: string | null = null,
): { plainLanguage: string; technicalCode: string; reasonCode: ReasonCode } {
  return {
    plainLanguage: plainOverride ?? explainReasonCode(code),
    technicalCode: code,
    reasonCode: code,
  };
}

export function deepFreeze<T>(value: T): T {
  if (value === null || typeof value !== "object") {
    return value;
  }
  Object.freeze(value);
  for (const key of Object.keys(value as object)) {
    const child = (value as Record<string, unknown>)[key];
    if (child !== null && typeof child === "object" && !Object.isFrozen(child)) {
      deepFreeze(child);
    }
  }
  return value;
}
