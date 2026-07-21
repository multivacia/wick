import type { R3eExperimentDomainInput, ViewModelClock } from "./inputs.js";
import type { R3eExperimentViewModel } from "./outputs.js";
import { actionHint, deepFreeze, toEvidenceLinks } from "./helpers.js";

/**
 * Build explanatory R3E Experiment ViewModel.
 * Definitions and governed status codes only — never invent metrics or outcomes.
 */
export function buildR3eExperimentViewModel(
  input: R3eExperimentDomainInput,
  clock: ViewModelClock | null = null,
): R3eExperimentViewModel {
  void clock;
  const validationExecuted = input.validationCommandExecuted === true;
  const effectPeeking = input.effectPeekingPerformed === true;

  return deepFreeze({
    experimentId: input.experimentId,
    parentExperimentId: input.parentExperimentId,
    title: input.title,
    purpose: input.purpose,
    hypothesis: input.hypothesis,
    protocolVersion: input.protocolVersion,
    modelFamilies: [...input.modelFamilies],
    modelStages: input.modelStages.map((stage) => ({ ...stage })),
    deltaCandleDefinition: input.deltaCandleDefinition,
    temporalValidationSummary: input.temporalValidationSummary,
    holdoutSummary: input.holdoutSummary,
    leakageProtectionSummary: input.leakageProtectionSummary,
    bootstrapSummary: input.bootstrapSummary,
    fdrSummary: input.fdrSummary,
    currentScientificState: input.currentScientificState,
    r3dResult: input.r3dResult,
    r3eGate: input.r3eGate,
    collectionState: input.collectionState,
    readinessState: input.readinessState,
    validationExecutionState: {
      executed: validationExecuted,
      label: validationExecuted
        ? "Validação futura executada"
        : "Validação futura não executada",
      distinctFromFailed:
        "VALIDATION_NOT_EXECUTED ≠ VALIDATION_FAILED — ausência de execução não é falha de validação.",
    },
    effectPeekingState: {
      performed: effectPeeking,
      label: effectPeeking
        ? "Effect peeking realizado"
        : "Effect peeking não realizado",
      distinctFromNotReported:
        "EFFECT_PEEKING_FALSE ≠ EFFECT_NOT_REPORTED — o estado é conhecido e falso; não é omissão.",
    },
    futureUnseenResultsPresent: false,
    r4Status: input.r4Status,
    r5Status: input.r5Status,
    knownStatements: input.knownStatements.map((s) => ({ ...s })),
    unknownStatements: input.unknownStatements.map((s) => ({ ...s })),
    nextSafeScientificAction: actionHint(
      "await_future_unseen_data",
      input.nextSafeScientificActionPlain,
    ),
    evidence: toEvidenceLinks(input.evidence),
  });
}
