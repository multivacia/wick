import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type TemporalValidationSummaryProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function TemporalValidationSummary({
  r3eExperiment,
}: TemporalValidationSummaryProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-temporal-validation">
      <h2 className="wick-r3e-card-title">Validação temporal e holdout</h2>
      <p className="wick-r3e-primary" data-testid="r3e-nested-walk-forward">
        {r3eExperiment.temporalValidationSummary}
      </p>
      <p className="wick-r3e-primary" data-testid="r3e-holdout-summary">
        {r3eExperiment.holdoutSummary}
      </p>
      <p className="wick-r3e-muted">
        Nested walk-forward e holdout são proteções de tempo — não são resultados
        de validação futura já executada.
      </p>
    </Card>
  );
}
