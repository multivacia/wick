import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type ExperimentPurposeProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function ExperimentPurpose({ r3eExperiment }: ExperimentPurposeProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-experiment-purpose">
      <h2 className="wick-r3e-card-title">Propósito do experimento</h2>
      <p className="wick-r3e-primary">{r3eExperiment.purpose}</p>
      <dl className="wick-r3e-field-list">
        <div className="wick-r3e-field">
          <dt>Identificador</dt>
          <dd data-testid="r3e-experiment-id">{r3eExperiment.experimentId}</dd>
        </div>
        <div className="wick-r3e-field">
          <dt>Experimento relacionado</dt>
          <dd data-testid="r3e-parent-experiment-id">
            {r3eExperiment.parentExperimentId}
          </dd>
        </div>
        <div className="wick-r3e-field">
          <dt>Protocolo</dt>
          <dd>{r3eExperiment.protocolVersion}</dd>
        </div>
      </dl>
    </Card>
  );
}
