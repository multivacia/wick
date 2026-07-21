import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type DeltaCandleExplanationProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function DeltaCandleExplanation({
  r3eExperiment,
}: DeltaCandleExplanationProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-delta-candle-explanation">
      <h2 className="wick-r3e-card-title">DELTA_CANDLE</h2>
      <p className="wick-r3e-primary" data-testid="r3e-delta-candle-definition">
        {r3eExperiment.deltaCandleDefinition}
      </p>
      <p className="wick-r3e-muted">
        A definição de DELTA_CANDLE não inclui p-valor, intervalo de confiança,
        retorno, Sharpe nem lucro garantido.
      </p>
    </Card>
  );
}
