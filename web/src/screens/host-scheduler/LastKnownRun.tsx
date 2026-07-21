import { Card } from "../../components/primitives";
import type { HostSchedulerViewModel } from "../../viewmodels";

export type LastKnownRunProps = {
  hostScheduler: HostSchedulerViewModel;
};

/**
 * Last known scheduler cycle from ViewModel timestamps only.
 */
export function LastKnownRun({ hostScheduler }: LastKnownRunProps) {
  const ts = hostScheduler.lastCycleAt;
  const available = ts.availability === "available";

  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-last-known-run"
    >
      <h2 className="wick-host-scheduler-card-title">Último ciclo conhecido</h2>
      <dl className="wick-host-scheduler-field-list">
        <div className="wick-host-scheduler-field">
          <dt>Estado do ciclo</dt>
          <dd data-testid="host-scheduler-last-cycle-state">
            <code>{hostScheduler.lastCycleState}</code>
          </dd>
        </div>
        <div className="wick-host-scheduler-field">
          <dt>Horário</dt>
          <dd data-testid="host-scheduler-last-cycle-at">
            {available
              ? (ts.displayText ?? ts.rawIso ?? "disponível sem texto")
              : "indisponível"}
          </dd>
        </div>
        <div className="wick-host-scheduler-field">
          <dt>Disponibilidade</dt>
          <dd data-testid="host-scheduler-last-cycle-availability">
            <code>{ts.availability}</code>
          </dd>
        </div>
      </dl>
      {!available ? (
        <p className="wick-host-scheduler-muted">
          MISSING ≠ FALSE · MISSING ≠ ZERO. Timestamp ausente permanece
          indisponível — não é fabricado.
        </p>
      ) : null}
      {hostScheduler.lastCycleState === "not_started" ? (
        <p
          className="wick-host-scheduler-muted"
          data-testid="host-scheduler-last-cycle-not-started"
        >
          not_started ≠ fault. Ciclo não iniciado não é falha confirmada.
        </p>
      ) : null}
    </Card>
  );
}
