import { Card, StatusBadge } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type FutureUnseenGateProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function FutureUnseenGate({ r3eExperiment }: FutureUnseenGateProps) {
  const validation = r3eExperiment.validationExecutionState;
  const peeking = r3eExperiment.effectPeekingState;

  return (
    <Card className="wick-r3e-card" data-testid="r3e-future-unseen-gate">
      <div className="wick-r3e-card__header">
        <h2 className="wick-r3e-card-title">Gate de dados futuros não vistos</h2>
        <StatusBadge
          status="attention"
          label={r3eExperiment.r3eGate}
          data-testid="r3e-future-gate-badge"
        />
      </div>
      <p className="wick-r3e-primary" data-testid="r3e-pending-neq-failed">
        PENDING_FUTURE_UNSEEN_DATA ≠ FAILED. O gate está pendente — não falhou.
      </p>
      <dl className="wick-r3e-field-list">
        <div className="wick-r3e-field">
          <dt>Validação futura</dt>
          <dd data-testid="r3e-validation-execution-state">
            {validation.label}
          </dd>
        </div>
        <div className="wick-r3e-field">
          <dt>Effect peeking</dt>
          <dd data-testid="r3e-effect-peeking-state">{peeking.label}</dd>
        </div>
        <div className="wick-r3e-field">
          <dt>Resultados futuros</dt>
          <dd data-testid="r3e-future-unseen-absent">
            Ausentes nesta tela (futureUnseenResultsPresent=false)
          </dd>
        </div>
      </dl>
      <p className="wick-r3e-muted" data-testid="r3e-validation-neq-failed">
        {validation.distinctFromFailed}
      </p>
      <p className="wick-r3e-muted" data-testid="r3e-peeking-neq-unreported">
        {peeking.distinctFromNotReported}
      </p>
    </Card>
  );
}
