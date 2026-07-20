import { Section } from "../../components/primitives";
import type { OverviewViewModel } from "../../viewmodels";

export type BlockerListProps = {
  blockers: OverviewViewModel["activeBlockers"];
};

export function BlockerList({ blockers }: BlockerListProps) {
  return (
    <Section title="Bloqueios ativos" data-testid="overview-active-blockers">
      {blockers.length === 0 ? (
        <p className="wick-overview-muted">Nenhum bloqueio ativo neste cenário.</p>
      ) : (
        <ul className="wick-overview-blocker-list">
          {blockers.map((blocker) => (
            <li key={blocker.reasonCode}>
              <p className="wick-overview-primary">{blocker.plainLanguage}</p>
              <p className="wick-overview-technical">
                Código: <code>{blocker.reasonCode}</code>
              </p>
            </li>
          ))}
        </ul>
      )}
    </Section>
  );
}
