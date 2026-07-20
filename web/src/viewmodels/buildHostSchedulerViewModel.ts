import type { HostSchedulerDomainInput, ViewModelClock } from "./inputs.js";
import type { HostSchedulerViewModel } from "./outputs.js";
import { mapDomainStateToPresentation } from "./status.js";
import { explainReasonCode } from "./reasons.js";
import { presentTimestamp } from "./time.js";
import { actionHint, deepFreeze, toEvidenceLinks } from "./helpers.js";

export function buildHostSchedulerViewModel(
  input: HostSchedulerDomainInput,
  clock: ViewModelClock | null = null,
): HostSchedulerViewModel {
  const { host, scheduler, blockers } = input;
  const hostMap = mapDomainStateToPresentation(host.state);
  const schedMap = mapDomainStateToPresentation(scheduler.state);

  const hostPlain =
    host.discoveryNote ??
    (host.state === "deferred"
      ? explainReasonCode("HOST_DISCOVERY_DEFERRED")
      : "Estado do host indeterminado.");

  const schedPlain =
    scheduler.state === "blocked"
      ? explainReasonCode("SCHEDULER_BLOCKED")
      : scheduler.active === true
        ? "Agendador ativo (somente se evidenciado)."
        : scheduler.registered === false
          ? explainReasonCode("SCHEDULER_NOT_REGISTERED")
          : "Estado do agendador indeterminado.";

  const nextSafeAction =
    host.state === "deferred"
      ? actionHint(
          "complete_host_discovery",
          "Concluir descoberta de host em tarefa operacional separada.",
        )
      : !scheduler.activationAuthorized
        ? actionHint(
            "request_separate_activation_authorization",
            "Solicitar autorização humana separada antes de qualquer ativação.",
          )
        : actionHint(
            "review_blocker_evidence",
            "Revisar bloqueios de host/agendador.",
          );

  // Never imply activation: active stays false/null unless explicitly supplied true.
  const schedulerActive =
    scheduler.active === true && scheduler.activationAuthorized
      ? true
      : scheduler.active === true
        ? true
        : scheduler.active;

  return deepFreeze({
    hostDiscoveryState: host.state,
    hostPresentation: {
      status: hostMap.status,
      severity: hostMap.severity,
      primaryMessage: {
        plainLanguage: hostPlain,
        technicalCode: host.state.toUpperCase(),
      },
      technicalDetail: {
        plainLanguage: hostPlain,
        technicalCode: "HOST_DISCOVERY",
        reasonCode:
          host.state === "deferred" ? "HOST_DISCOVERY_DEFERRED" : null,
      },
      reasonCodes:
        host.state === "deferred" ? ["HOST_DISCOVERY_DEFERRED"] : [],
    },
    persistentHostPresent: host.persistentHostPresent,
    schedulerRegistered: scheduler.registered,
    schedulerActive,
    schedulerState: scheduler.state,
    schedulerPresentation: {
      status: schedMap.status,
      severity: schedMap.severity,
      primaryMessage: {
        plainLanguage: schedPlain,
        technicalCode: scheduler.state.toUpperCase(),
      },
      technicalDetail: {
        plainLanguage: schedPlain,
        technicalCode:
          scheduler.activationAuthorized === false
            ? "ACTIVATION_NOT_AUTHORIZED"
            : scheduler.state.toUpperCase(),
        reasonCode:
          scheduler.state === "blocked"
            ? "SCHEDULER_BLOCKED"
            : scheduler.activationAuthorized === false
              ? "ACTIVATION_NOT_AUTHORIZED"
              : null,
      },
      reasonCodes: [
        ...(scheduler.state === "blocked" ? (["SCHEDULER_BLOCKED"] as const) : []),
        ...(!scheduler.activationAuthorized
          ? (["ACTIVATION_NOT_AUTHORIZED"] as const)
          : []),
      ],
    },
    lastCycleState: scheduler.lastCycleState,
    lastCycleAt: presentTimestamp(scheduler.lastCycleAt, clock, {
      includeRelative: true,
    }),
    operationalDebt: scheduler.operationalDebt,
    activationAuthorized: scheduler.activationAuthorized,
    blockers: blockers.map((b) => ({
      reasonCode: b.reasonCode,
      plainLanguage: b.plainLanguage,
      evidence: toEvidenceLinks(b.evidence),
    })),
    nextSafeAction,
    evidence: toEvidenceLinks([...host.evidence, ...scheduler.evidence]),
  });
}
