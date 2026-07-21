import { Card, StatusBadge } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type CurrentScientificStateProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function CurrentScientificState({
  r3eExperiment,
}: CurrentScientificStateProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-current-scientific-state">
      <div className="wick-r3e-card__header">
        <h2 className="wick-r3e-card-title">Estado científico atual</h2>
        <StatusBadge
          status="attention"
          label="Exploratório pendente"
          data-testid="r3e-scientific-state-badge"
        />
      </div>
      <p className="wick-r3e-primary">{r3eExperiment.currentScientificState}</p>
      <dl className="wick-r3e-field-list">
        <div className="wick-r3e-field">
          <dt>Coleta</dt>
          <dd data-testid="r3e-collection-state">
            {r3eExperiment.collectionState}
          </dd>
        </div>
        <div className="wick-r3e-field">
          <dt>Prontidão</dt>
          <dd data-testid="r3e-readiness-state">
            {r3eExperiment.readinessState}
          </dd>
        </div>
        <div className="wick-r3e-field">
          <dt>R4</dt>
          <dd data-testid="r3e-r4-status">{r3eExperiment.r4Status}</dd>
        </div>
        <div className="wick-r3e-field">
          <dt>R5</dt>
          <dd data-testid="r3e-r5-status">{r3eExperiment.r5Status}</dd>
        </div>
      </dl>
      <p className="wick-r3e-muted">
        AUDIT_COMPLETE ≠ FUTURE_VALIDATION_COMPLETE
      </p>
    </Card>
  );
}
