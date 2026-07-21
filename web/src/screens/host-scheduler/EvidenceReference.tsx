import { Card } from "../../components/primitives";
import type { HostSchedulerViewModel } from "../../viewmodels";
import { RelatedEvidenceLinks } from "../shared/RelatedEvidenceLinks";

export type EvidenceReferenceProps = {
  hostScheduler: HostSchedulerViewModel;
};

/**
 * Evidence as text only — never fabricate navigable links.
 * Catalog navigation links are placed outside the evidence card.
 */
export function EvidenceReference({ hostScheduler }: EvidenceReferenceProps) {
  const items = hostScheduler.evidence;

  return (
    <>
      <Card
        className="wick-host-scheduler-card"
        data-testid="host-scheduler-evidence-reference"
      >
        <h2 className="wick-host-scheduler-card-title">
          Referências de evidência
        </h2>
        {items.length === 0 ? (
          <p
            className="wick-host-scheduler-primary"
            data-testid="host-scheduler-evidence-empty"
          >
            Nenhuma evidência fornecida neste ViewModel.
          </p>
        ) : (
          <ul
            className="wick-host-scheduler-list"
            data-testid="host-scheduler-evidence-list"
          >
            {items.map((item) => (
              <li key={`${item.kind}:${item.reference}:${item.label}`}>
                <p className="wick-host-scheduler-primary">{item.label}</p>
                <p className="wick-host-scheduler-technical">
                  <code>{item.reference}</code>
                  {" · "}
                  kind=<code>{item.kind}</code>
                </p>
              </li>
            ))}
          </ul>
        )}
        <p className="wick-host-scheduler-muted">
          Referências exibidas como texto. Nenhum link operacional é fabricado.
        </p>
      </Card>
      <RelatedEvidenceLinks
        items={[
          {
            evidenceId: "ev-host-scheduler-operational-debt",
            label: "Dívida operacional — host e agendador",
          },
          {
            evidenceId: "ev-host-scheduler-activation-handoff",
            label: "Handoff de ativação do agendador (bloqueada)",
          },
        ]}
        title="Catálogo de evidências"
      />
    </>
  );
}
