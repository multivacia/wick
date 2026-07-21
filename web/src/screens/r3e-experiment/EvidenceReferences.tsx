import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type EvidenceReferencesProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function EvidenceReferences({ r3eExperiment }: EvidenceReferencesProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-evidence-references">
      <h2 className="wick-r3e-card-title">Referências de evidência</h2>
      <p className="wick-r3e-muted">
        Caminhos textuais para documentos governados — não são resultados de
        validação futura.
      </p>
      <ul className="wick-r3e-list">
        {r3eExperiment.evidence.map((item) => (
          <li key={`${item.kind}:${item.reference}`}>
            <p className="wick-r3e-primary">{item.label}</p>
            <p className="wick-r3e-technical">
              {item.kind}: {item.reference}
            </p>
          </li>
        ))}
      </ul>
    </Card>
  );
}
