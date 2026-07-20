import { Card } from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";

export type EvidenceReferenceProps = {
  readiness: ReadinessViewModel;
};

/**
 * Evidence as text only — never fabricate navigable links.
 */
export function EvidenceReference({ readiness }: EvidenceReferenceProps) {
  const items = readiness.evidence;

  return (
    <Card
      className="wick-readiness-card"
      data-testid="readiness-evidence-reference"
    >
      <h2 className="wick-readiness-card-title">Referências de evidência</h2>
      {items.length === 0 ? (
        <p className="wick-readiness-primary" data-testid="readiness-evidence-empty">
          Nenhuma evidência fornecida neste ViewModel.
        </p>
      ) : (
        <ul className="wick-readiness-list" data-testid="readiness-evidence-list">
          {items.map((item) => (
            <li key={`${item.kind}:${item.reference}:${item.label}`}>
              <p className="wick-readiness-primary">{item.label}</p>
              <p className="wick-readiness-technical">
                <code>{item.reference}</code>
                {" · "}
                kind=<code>{item.kind}</code>
              </p>
            </li>
          ))}
        </ul>
      )}
      <p className="wick-readiness-muted">
        Referências exibidas como texto. Nenhum link operacional é fabricado.
      </p>
    </Card>
  );
}
