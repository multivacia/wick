import type { OverviewDomainInput, ViewModelClock } from "./inputs.js";
import type { OverviewViewModel } from "./outputs.js";
import { buildRunViewModel, worstLifecycle } from "./buildRunViewModel.js";
import { buildReadinessViewModel } from "./buildReadinessViewModel.js";
import { buildHostSchedulerViewModel } from "./buildHostSchedulerViewModel.js";
import { mapDomainStateToPresentation } from "./status.js";
import { presentTimestamp } from "./time.js";
import { actionHint, deepFreeze, toEvidenceLinks } from "./helpers.js";
import type { PresentationBlock } from "./presentation.js";

export function buildOverviewViewModel(
  input: OverviewDomainInput,
  clock: ViewModelClock | null = null,
): OverviewViewModel {
  const readinessVm = buildReadinessViewModel(
    { readiness: input.readiness },
    clock,
  );
  const hostSchedVm = buildHostSchedulerViewModel(
    {
      host: input.host,
      scheduler: input.scheduler,
      blockers: input.blockers,
    },
    clock,
  );

  const overallState = worstLifecycle([
    input.collection.state,
    input.readiness.state,
    input.host.state,
    input.scheduler.state,
    ...(input.lastFailedRun ? [input.lastFailedRun.state] : []),
    ...input.blockers.map(() => "blocked" as const),
  ]);
  const overallMap = mapDomainStateToPresentation(overallState);

  const collectionBlock: PresentationBlock = {
    explanation: {
      status: mapDomainStateToPresentation(input.collection.state).status,
      severity: mapDomainStateToPresentation(input.collection.state).severity,
      primaryMessage: {
        plainLanguage:
          input.collection.state === "in_progress"
            ? "Coleta em andamento."
            : input.collection.state === "complete"
              ? "Coleta concluída para o intervalo conhecido."
              : "Estado da coleta indeterminado ou indisponível.",
        technicalCode: input.collection.state.toUpperCase(),
      },
      technicalDetail: {
        plainLanguage: "Resumo de frescor e observações do store.",
        technicalCode: "COLLECTION_SUMMARY",
        reasonCode: null,
      },
      reasonCodes: [],
    },
    evidence: [],
    actionHint:
      input.collection.state === "in_progress"
        ? actionHint("continue_collecting", "Continuar a coleta.")
        : null,
    observedAt: presentTimestamp(input.collection.lastObservationAt, clock, {
      includeRelative: true,
    }),
  };

  const readinessBlock: PresentationBlock = {
    explanation: readinessVm.presentation,
    evidence: readinessVm.evidence,
    actionHint: readinessVm.nextSafeAction,
    observedAt: null,
  };

  const hostSchedulerBlock: PresentationBlock = {
    explanation: {
      status: mapDomainStateToPresentation(
        worstLifecycle([input.host.state, input.scheduler.state]),
      ).status,
      severity: mapDomainStateToPresentation(
        worstLifecycle([input.host.state, input.scheduler.state]),
      ).severity,
      primaryMessage: {
        plainLanguage: `${hostSchedVm.hostPresentation.primaryMessage.plainLanguage} ${hostSchedVm.schedulerPresentation.primaryMessage.plainLanguage}`,
        technicalCode: "HOST_SCHEDULER_SUMMARY",
      },
      technicalDetail: hostSchedVm.schedulerPresentation.technicalDetail,
      reasonCodes: [
        ...hostSchedVm.hostPresentation.reasonCodes,
        ...hostSchedVm.schedulerPresentation.reasonCodes,
      ],
    },
    evidence: hostSchedVm.evidence,
    actionHint: hostSchedVm.nextSafeAction,
    observedAt: hostSchedVm.lastCycleAt,
  };

  const nextSafeAction =
    overallState === "fault"
      ? actionHint(
          "investigate_failed_run",
          "Investigar falha confirmada antes de qualquer avanço.",
        )
      : input.readiness.state === "not_ready"
        ? readinessVm.nextSafeAction
        : input.host.state === "deferred"
          ? hostSchedVm.nextSafeAction
          : input.scheduler.state === "blocked"
            ? hostSchedVm.nextSafeAction
            : input.collection.state === "in_progress"
              ? actionHint("continue_collecting", "Continuar a coleta.")
              : actionHint("monitor_collection", "Monitorar o estado operacional.");

  const overallPlain =
    overallState === "fault"
      ? "Há falha operacional confirmada."
      : overallState === "blocked" || overallState === "deferred"
        ? "Há bloqueio ou adiamento operacional."
        : overallState === "not_ready"
          ? "O sistema ainda não está pronto — isso não é uma falha."
          : overallState === "in_progress"
            ? "Operação em andamento com restrições conhecidas."
            : "Estado operacional consolidado.";

  return deepFreeze({
    overallState,
    overallPresentation: {
      status: overallMap.status,
      severity: overallMap.severity,
      primaryMessage: {
        plainLanguage: overallPlain,
        technicalCode: overallState.toUpperCase(),
      },
      technicalDetail: {
        plainLanguage: overallPlain,
        technicalCode: overallState.toUpperCase(),
        reasonCode: input.blockers[0]?.reasonCode ?? null,
      },
      reasonCodes: input.blockers.map((b) => b.reasonCode),
    },
    collectionSummary: collectionBlock,
    readinessSummary: readinessBlock,
    hostSchedulerSummary: hostSchedulerBlock,
    activeBlockers: input.blockers.map((b) => ({
      reasonCode: b.reasonCode,
      plainLanguage: b.plainLanguage,
      evidence: toEvidenceLinks(b.evidence),
    })),
    lastCompletedRun: input.lastCompletedRun
      ? buildRunViewModel(input.lastCompletedRun, clock)
      : null,
    lastFailedRun: input.lastFailedRun
      ? buildRunViewModel(input.lastFailedRun, clock)
      : null,
    lastKnownEvidence: toEvidenceLinks(input.evidence),
    nextSafeAction,
    scientificGate: input.scientificGate,
    r4Status: input.r4Status,
    r5Status: input.r5Status,
    generatedWithNow: clock?.nowIso ?? null,
  });
}
