import { Alert } from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";

export type PartialUnknownStateProps = {
  readiness: ReadinessViewModel;
};

/**
 * Surface unknown / partial / missing without equating to fault or zero.
 */
export function PartialUnknownState({ readiness }: PartialUnknownStateProps) {
  const unknownState =
    readiness.state === "unknown" || readiness.state === "not_available";
  const metricsMissing =
    readiness.windowDays.availability !== "available" ||
    readiness.requiredWindowDays.availability !== "available" ||
    readiness.windowDays.value === null ||
    readiness.requiredWindowDays.value === null;

  if (!unknownState && !metricsMissing) {
    return null;
  }

  return (
    <Alert
      tone="informational"
      title="Estado parcial ou desconhecido"
      data-testid="readiness-partial-unknown"
    >
      <p className="wick-readiness-primary">
        {unknownState
          ? "O estado de prontidão é desconhecido ou indisponível — isso não é falha confirmada."
          : "Parte das métricas de janela está ausente ou indisponível."}
      </p>
      <p className="wick-readiness-muted">
        UNKNOWN ≠ ZERO · MISSING ≠ ZERO · UNKNOWN ≠ FAULT. Valores ausentes
        permanecem indisponíveis.
      </p>
    </Alert>
  );
}
