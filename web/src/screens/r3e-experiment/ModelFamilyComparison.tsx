import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type ModelFamilyComparisonProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function ModelFamilyComparison({
  r3eExperiment,
}: ModelFamilyComparisonProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-model-family-comparison">
      <h2 className="wick-r3e-card-title">Comparação de famílias de modelo</h2>
      <p className="wick-r3e-primary">
        As famílias abaixo organizam a escada M0–M5. A comparação é científica e
        explicativa — não é uma recomendação de compra ou venda.
      </p>
      <ul className="wick-r3e-list">
        {r3eExperiment.modelFamilies.map((family) => (
          <li key={family}>{family}</li>
        ))}
      </ul>
      <p className="wick-r3e-muted" data-testid="r3e-model-comparison-guard">
        MODEL_COMPARISON ≠ TRADING_RECOMMENDATION · STATISTICAL_SIGNIFICANCE ≠
        ECONOMIC_USEFULNESS
      </p>
    </Card>
  );
}
