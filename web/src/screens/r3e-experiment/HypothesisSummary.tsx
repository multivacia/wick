import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type HypothesisSummaryProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function HypothesisSummary({ r3eExperiment }: HypothesisSummaryProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-hypothesis-summary">
      <h2 className="wick-r3e-card-title">Hipótese</h2>
      <p className="wick-r3e-primary">{r3eExperiment.hypothesis}</p>
      <p className="wick-r3e-muted">
        Hipótese ≠ resultado comprovado. Esta tela não afirma que H2 foi
        confirmada.
      </p>
    </Card>
  );
}
