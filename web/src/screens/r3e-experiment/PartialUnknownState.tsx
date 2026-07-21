import { Alert } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type PartialUnknownStateProps = {
  r3eExperiment: R3eExperimentViewModel;
};

/**
 * Disclose absent future-unseen results and pending scientific unknowns.
 */
export function PartialUnknownState({
  r3eExperiment,
}: PartialUnknownStateProps) {
  return (
    <Alert
      tone="informational"
      title="Estado parcial / desconhecido"
      data-testid="r3e-partial-unknown"
    >
      <p className="wick-r3e-primary">
        Resultados de dados futuros não vistos estão ausentes (
        futureUnseenResultsPresent=
        {String(r3eExperiment.futureUnseenResultsPresent)}). Validação futura
        não executada; effect peeking não realizado.
      </p>
      <p className="wick-r3e-muted">
        PENDING ≠ FAILED · NOT_EXECUTED ≠ FAILED · FALSE ≠ NOT_REPORTED ·
        ILLUSTRATIVE ≠ SCIENTIFIC_PROOF
      </p>
    </Alert>
  );
}
