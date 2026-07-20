import type { ReadinessDomainInput, ViewModelClock } from "./inputs.js";
import type { ReadinessViewModel } from "./outputs.js";
import { mapDomainStateToPresentation } from "./status.js";
import { explainReasonCode } from "./reasons.js";
import { metricPresentation } from "./time.js";
import { actionHint, deepFreeze, toEvidenceLinks } from "./helpers.js";

export function buildReadinessViewModel(
  input: ReadinessDomainInput,
  _clock: ViewModelClock | null = null,
): ReadinessViewModel {
  void _clock;
  const readiness = input.readiness;
  const mapping = mapDomainStateToPresentation(readiness.state);
  const codes = [...readiness.blockingReasonCodes];

  const plain =
    readiness.explanationPlainLanguage ??
    (codes[0]
      ? explainReasonCode(codes[0])
      : readiness.state === "ready"
        ? "Critérios de prontidão satisfeitos. Isso não autoriza validação."
        : readiness.state === "not_ready"
          ? "A prontidão ainda não foi atingida."
          : readiness.state === "not_available" || readiness.state === "unknown"
            ? "Relatório de prontidão indisponível."
            : "Estado de prontidão indeterminado.");

  const nextSafeAction =
    readiness.state === "not_ready" && codes.includes("WINDOW_DAYS_INSUFFICIENT")
      ? actionHint(
          "wait_for_sufficient_future_window",
          "Aguardar janela futura suficiente antes de qualquer validação.",
        )
      : readiness.state === "ready"
        ? actionHint(
            "do_not_validate",
            "Prontidão operacional não autoriza validação científica.",
          )
        : actionHint(
            "review_blocker_evidence",
            "Revisar razões de bloqueio da prontidão.",
          );

  return deepFreeze({
    state: readiness.state,
    presentation: {
      status: mapping.status,
      severity: mapping.severity,
      primaryMessage: {
        plainLanguage: plain,
        technicalCode: readiness.state.toUpperCase(),
      },
      technicalDetail: {
        plainLanguage: plain,
        technicalCode: codes[0] ?? readiness.state.toUpperCase(),
        reasonCode: codes[0] ?? null,
      },
      reasonCodes: codes,
    },
    windowDays: metricPresentation(
      "window_days",
      readiness.windowDays.value,
      readiness.windowDays.availability,
      "days",
    ),
    requiredWindowDays: metricPresentation(
      "required_window_days",
      readiness.requiredWindowDays.value,
      readiness.requiredWindowDays.availability,
      "days",
    ),
    blockingReasonCodes: codes,
    validationAuthorized: readiness.validationAuthorized,
    validationCommandExecuted: readiness.validationCommandExecuted,
    effectPeekingPerformed: readiness.effectPeekingPerformed,
    nextSafeAction,
    evidence: toEvidenceLinks(readiness.evidence),
  });
}
