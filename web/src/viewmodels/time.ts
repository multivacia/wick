/**
 * Explicit time presentation helpers. No implicit Date.now() in builders.
 */

import type {
  FreshnessClassification,
  TimestampPresentation,
  ValueAvailability,
} from "./presentation.js";
import type { OptionalIsoTimestamp, ViewModelClock } from "./inputs.js";

const DEFAULT_STALE_MS = 6 * 60 * 60 * 1000;

export function absentTimestamp(
  availability: ValueAvailability = "not_supplied",
): TimestampPresentation {
  return {
    rawIso: null,
    displayText: null,
    relativeText: null,
    freshness: availability === "not_available" ? "absent" : "absent",
    availability,
  };
}

export function presentTimestamp(
  input: OptionalIsoTimestamp,
  clock: ViewModelClock | null,
  options?: { includeRelative?: boolean },
): TimestampPresentation {
  if (input.iso === null || input.availability !== "available") {
    return absentTimestamp(
      input.availability === "unknown" ? "unknown" : input.availability,
    );
  }

  const rawIso = input.iso;
  const parsed = Date.parse(rawIso);
  if (Number.isNaN(parsed)) {
    return {
      rawIso,
      displayText: rawIso,
      relativeText: null,
      freshness: "unknown",
      availability: "available",
    };
  }

  let freshness: FreshnessClassification = "not_applicable";
  let relativeText: string | null = null;

  if (clock !== null) {
    const now = Date.parse(clock.nowIso);
    if (!Number.isNaN(now)) {
      const staleAfter = clock.staleAfterMs ?? DEFAULT_STALE_MS;
      const age = now - parsed;
      freshness = age > staleAfter ? "stale" : "current";
      if (options?.includeRelative) {
        relativeText = formatRelative(age);
      }
    } else {
      freshness = "unknown";
    }
  }

  return {
    rawIso,
    displayText: rawIso,
    relativeText,
    freshness,
    availability: "available",
  };
}

function formatRelative(ageMs: number): string {
  const abs = Math.abs(ageMs);
  const minutes = Math.round(abs / 60000);
  if (minutes < 1) {
    return ageMs >= 0 ? "agora" : "em breve";
  }
  if (minutes < 60) {
    return ageMs >= 0 ? `há ${minutes} min` : `em ${minutes} min`;
  }
  const hours = Math.round(minutes / 60);
  if (hours < 48) {
    return ageMs >= 0 ? `há ${hours} h` : `em ${hours} h`;
  }
  const days = Math.round(hours / 24);
  return ageMs >= 0 ? `há ${days} d` : `em ${days} d`;
}

export function metricPresentation(
  label: string,
  value: number | null,
  availability: ValueAvailability,
  unit: string | null = null,
): {
  label: string;
  value: number | null;
  unit: string | null;
  availability: ValueAvailability;
  displayText: string | null;
} {
  if (value === null || availability !== "available") {
    return {
      label,
      value: null,
      unit,
      availability: availability === "available" ? "not_supplied" : availability,
      displayText: null,
    };
  }
  return {
    label,
    value,
    unit,
    availability: "available",
    displayText: unit ? `${value} ${unit}` : String(value),
  };
}
