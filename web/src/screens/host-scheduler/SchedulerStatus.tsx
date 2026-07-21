import {
  Card,
  Inline,
  StatusBadge,
  type StatusBadgeStatus,
} from "../../components/primitives";
import type { HostSchedulerViewModel } from "../../viewmodels";

const STATUS_LABEL_PT: Partial<Record<StatusBadgeStatus, string>> = {
  healthy: "Saudável",
  completed: "Concluído",
  attention: "Atenção",
  not_ready: "Não pronto",
  blocked: "Bloqueado",
  deferred: "Adiado",
  unknown: "Desconhecido",
  fault: "Falha",
  informational: "Informativo",
};

function formatTriState(
  value: boolean | null,
  labels: { true: string; false: string; null: string },
): string {
  if (value === null) return labels.null;
  return value ? labels.true : labels.false;
}

export type SchedulerStatusProps = {
  hostScheduler: HostSchedulerViewModel;
};

/**
 * Scheduler status — BLOCKED ≠ FAULT; INACTIVE ≠ FAILED; NOT_CONFIGURED ≠ FAILED.
 */
export function SchedulerStatus({ hostScheduler }: SchedulerStatusProps) {
  const status = hostScheduler.schedulerPresentation.status as StatusBadgeStatus;
  const isBlocked = hostScheduler.schedulerState === "blocked";
  const isInactive = hostScheduler.schedulerActive === false;
  const isNotRegistered = hostScheduler.schedulerRegistered === false;

  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-scheduler-status"
    >
      <Inline className="wick-host-scheduler-card__header">
        <h2 className="wick-host-scheduler-card-title">Agendador</h2>
        <StatusBadge
          status={status}
          label={STATUS_LABEL_PT[status] ?? status}
          data-testid="host-scheduler-scheduler-badge"
          data-status={status}
        />
      </Inline>
      <p
        className="wick-host-scheduler-primary"
        data-testid="host-scheduler-scheduler-message"
      >
        {hostScheduler.schedulerPresentation.primaryMessage.plainLanguage}
      </p>
      <p className="wick-host-scheduler-technical">
        Técnico:{" "}
        <code>
          {hostScheduler.schedulerPresentation.primaryMessage.technicalCode ??
            hostScheduler.schedulerState.toUpperCase()}
        </code>
        {" · "}
        domínio: <code>{hostScheduler.schedulerState}</code>
      </p>
      <dl className="wick-host-scheduler-field-list">
        <div className="wick-host-scheduler-field">
          <dt>Registrado</dt>
          <dd data-testid="host-scheduler-registered">
            {formatTriState(hostScheduler.schedulerRegistered, {
              true: "sim",
              false: "não configurado",
              null: "indisponível",
            })}
          </dd>
        </div>
        <div className="wick-host-scheduler-field">
          <dt>Ativo</dt>
          <dd data-testid="host-scheduler-active">
            {formatTriState(hostScheduler.schedulerActive, {
              true: "sim",
              false: "inativo",
              null: "indisponível",
            })}
          </dd>
        </div>
        <div className="wick-host-scheduler-field">
          <dt>Ativação autorizada</dt>
          <dd data-testid="host-scheduler-activation-authorized">
            {hostScheduler.activationAuthorized ? "sim" : "não"}
          </dd>
        </div>
      </dl>
      {isBlocked ? (
        <p
          className="wick-host-scheduler-muted"
          data-testid="host-scheduler-blocked-note"
        >
          BLOCKED ≠ FAULT. Bloqueado não é falha confirmada (vermelho reservado
          a fault).
        </p>
      ) : null}
      {isInactive ? (
        <p
          className="wick-host-scheduler-muted"
          data-testid="host-scheduler-inactive-note"
        >
          SCHEDULER_INACTIVE ≠ SCHEDULER_FAILED. Inativo não é falha.
        </p>
      ) : null}
      {isNotRegistered ? (
        <p
          className="wick-host-scheduler-muted"
          data-testid="host-scheduler-not-configured-note"
        >
          NOT_CONFIGURED ≠ FAILED. Não registrado não é falha confirmada.
        </p>
      ) : null}
    </Card>
  );
}
