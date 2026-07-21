import { Card, StatusBadge } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type R3DAndR3EDistinctionProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function R3DAndR3EDistinction({
  r3eExperiment,
}: R3DAndR3EDistinctionProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-r3d-distinction">
      <div className="wick-r3e-card__header">
        <h2 className="wick-r3e-card-title">Distinção R3D e R3E</h2>
      </div>
      <dl className="wick-r3e-field-list">
        <div className="wick-r3e-field">
          <dt>Resultado R3D</dt>
          <dd>
            <StatusBadge
              status="blocked"
              label={r3eExperiment.r3dResult}
              data-testid="r3e-r3d-result-badge"
              data-status="blocked"
            />
          </dd>
        </div>
        <div className="wick-r3e-field">
          <dt>Gate R3E</dt>
          <dd>
            <StatusBadge
              status="attention"
              label={r3eExperiment.r3eGate}
              data-testid="r3e-gate-badge"
              data-status="attention"
            />
          </dd>
        </div>
      </dl>
      <p className="wick-r3e-primary" data-testid="r3e-r3d-neq-r3e">
        NO_MEASURABLE_EDGE (R3D) ≠ R3E_REJECTED. A R3D encerrou sem edge
        mensurável; a R3E permanece pendente de dados futuros não vistos.
      </p>
      <p className="wick-r3e-muted">
        EXPLORATORY_COMPLETE ≠ EDGE_PROVEN · R3E_PENDING ≠ STRATEGY_APPROVED
      </p>
    </Card>
  );
}
