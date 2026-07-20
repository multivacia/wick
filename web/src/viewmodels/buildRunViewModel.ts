import type { CollectionRunInput, ViewModelClock } from "./inputs.js";
import type { RunViewModel } from "./outputs.js";
import {
  mapDomainStateToPresentation,
  type DomainLifecycleState,
} from "./status.js";
import { explainReasonCode } from "./reasons.js";
import { metricPresentation, presentTimestamp } from "./time.js";
import { toEvidenceLinks } from "./helpers.js";

export function buildRunViewModel(
  run: CollectionRunInput,
  clock: ViewModelClock | null = null,
): RunViewModel {
  const mapping = mapDomainStateToPresentation(run.state);
  const reasonCodes = run.failureReasonCode ? [run.failureReasonCode] : [];
  const plain =
    run.state === "fault"
      ? (run.failureReason ??
        (run.failureReasonCode
          ? explainReasonCode(run.failureReasonCode)
          : "A execução falhou."))
      : run.state === "complete"
        ? "Execução concluída."
        : run.state === "in_progress"
          ? "Execução em andamento."
          : run.state === "not_started"
            ? "Execução ainda não iniciada."
            : "Estado da execução indeterminado.";

  return {
    runId: run.runId,
    state: run.state,
    presentation: {
      status: mapping.status,
      severity: mapping.severity,
      primaryMessage: {
        plainLanguage: plain,
        technicalCode: run.state.toUpperCase(),
      },
      technicalDetail: {
        plainLanguage: run.failureReason ?? plain,
        technicalCode: run.failureReasonCode,
        reasonCode: run.failureReasonCode,
      },
      reasonCodes,
    },
    startedAt: presentTimestamp(run.startedAt, clock, { includeRelative: true }),
    finishedAt: presentTimestamp(run.finishedAt, clock, {
      includeRelative: true,
    }),
    resultLabel: run.resultLabel,
    acceptedCount: metricPresentation(
      "accepted",
      run.acceptedCount.value,
      run.acceptedCount.availability,
      "rows",
    ),
    rejectedCount: metricPresentation(
      "rejected",
      run.rejectedCount.value,
      run.rejectedCount.availability,
      "rows",
    ),
    storeBeforeCount: metricPresentation(
      "store_before",
      run.storeBeforeCount.value,
      run.storeBeforeCount.availability,
      "rows",
    ),
    storeAfterCount: metricPresentation(
      "store_after",
      run.storeAfterCount.value,
      run.storeAfterCount.availability,
      "rows",
    ),
    idempotencyResult: run.idempotencyResult,
    failureReason: run.failureReason,
    evidence: toEvidenceLinks(run.evidence),
  };
}

export function worstLifecycle(
  states: DomainLifecycleState[],
): DomainLifecycleState {
  const order: DomainLifecycleState[] = [
    "fault",
    "blocked",
    "deferred",
    "not_ready",
    "in_progress",
    "not_started",
    "not_available",
    "unknown",
    "ready",
    "complete",
  ];
  for (const candidate of order) {
    if (states.includes(candidate)) {
      return candidate;
    }
  }
  return "unknown";
}
