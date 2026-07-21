import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type ProtocolSummaryProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function ProtocolSummary({ r3eExperiment }: ProtocolSummaryProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-protocol-summary">
      <h2 className="wick-r3e-card-title">Resumo do protocolo</h2>
      <p className="wick-r3e-primary">
        Protocolo congelado: <strong>{r3eExperiment.protocolVersion}</strong>.
        Famílias de modelo sob comparação:
      </p>
      <ul className="wick-r3e-list" data-testid="r3e-model-families">
        {r3eExperiment.modelFamilies.map((family) => (
          <li key={family}>{family}</li>
        ))}
      </ul>
      <p className="wick-r3e-muted">
        Comparação de modelos ≠ recomendação de trading.
      </p>
    </Card>
  );
}
