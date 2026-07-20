import type { MetricPresentation, TimestampPresentation } from "../../viewmodels";

export function formatMetric(metric: MetricPresentation): string {
  if (metric.value === null || metric.availability !== "available") {
    return "indisponível";
  }
  return metric.displayText ?? String(metric.value);
}

export function formatTimestamp(ts: TimestampPresentation): string {
  if (ts.availability !== "available" || (!ts.displayText && !ts.rawIso)) {
    return "indisponível";
  }
  return ts.displayText ?? ts.rawIso ?? "indisponível";
}
