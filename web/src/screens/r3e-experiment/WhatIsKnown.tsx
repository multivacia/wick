import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type WhatIsKnownProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function WhatIsKnown({ r3eExperiment }: WhatIsKnownProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-what-is-known">
      <h2 className="wick-r3e-card-title">O que é conhecido</h2>
      <ul className="wick-r3e-list">
        {r3eExperiment.knownStatements.map((statement) => (
          <li key={statement.id}>
            <p className="wick-r3e-primary">{statement.plainLanguage}</p>
            {statement.technicalCode ? (
              <p className="wick-r3e-technical">{statement.technicalCode}</p>
            ) : null}
          </li>
        ))}
      </ul>
    </Card>
  );
}
