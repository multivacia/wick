import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type BootstrapAndFDRExplanationProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function BootstrapAndFDRExplanation({
  r3eExperiment,
}: BootstrapAndFDRExplanationProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-bootstrap-fdr">
      <h2 className="wick-r3e-card-title">Bootstrap e FDR</h2>
      <p className="wick-r3e-primary" data-testid="r3e-bootstrap-summary">
        {r3eExperiment.bootstrapSummary}
      </p>
      <p className="wick-r3e-primary" data-testid="r3e-fdr-summary">
        {r3eExperiment.fdrSummary}
      </p>
      <p className="wick-r3e-muted" data-testid="r3e-no-fabricated-stats">
        Sem p-valores, intervalos de confiança ou tamanhos de efeito fabricados
        nesta tela.
      </p>
    </Card>
  );
}
