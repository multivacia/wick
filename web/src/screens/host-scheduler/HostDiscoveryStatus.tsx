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

export type HostDiscoveryStatusProps = {
  hostScheduler: HostSchedulerViewModel;
};

/**
 * Host discovery status — DEFERRED ≠ COMPLETE ≠ FAILED.
 */
export function HostDiscoveryStatus({
  hostScheduler,
}: HostDiscoveryStatusProps) {
  const status = hostScheduler.hostPresentation.status as StatusBadgeStatus;
  const isDeferred = hostScheduler.hostDiscoveryState === "deferred";
  const isUnknown =
    hostScheduler.hostDiscoveryState === "unknown" ||
    hostScheduler.hostDiscoveryState === "not_available";

  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-discovery-status"
    >
      <Inline className="wick-host-scheduler-card__header">
        <h2 className="wick-host-scheduler-card-title">
          Descoberta de host
        </h2>
        <StatusBadge
          status={status}
          label={STATUS_LABEL_PT[status] ?? status}
          data-testid="host-scheduler-discovery-badge"
          data-status={status}
        />
      </Inline>
      <p
        className="wick-host-scheduler-primary"
        data-testid="host-scheduler-discovery-message"
      >
        {hostScheduler.hostPresentation.primaryMessage.plainLanguage}
      </p>
      <p className="wick-host-scheduler-technical">
        Técnico:{" "}
        <code>
          {hostScheduler.hostPresentation.primaryMessage.technicalCode ??
            hostScheduler.hostDiscoveryState.toUpperCase()}
        </code>
        {" · "}
        domínio: <code>{hostScheduler.hostDiscoveryState}</code>
      </p>
      <dl className="wick-host-scheduler-field-list">
        <div className="wick-host-scheduler-field">
          <dt>Host persistente presente</dt>
          <dd data-testid="host-scheduler-persistent-host">
            {formatTriState(hostScheduler.persistentHostPresent, {
              true: "sim",
              false: "não",
              null: "indisponível",
            })}
          </dd>
        </div>
      </dl>
      {isDeferred ? (
        <p
          className="wick-host-scheduler-muted"
          data-testid="host-scheduler-deferred-note"
        >
          DEFERRED ≠ COMPLETE · DEFERRED ≠ FAILED. Adiado não é falha
          confirmada nem descoberta concluída.
        </p>
      ) : null}
      {isUnknown ? (
        <p
          className="wick-host-scheduler-muted"
          data-testid="host-scheduler-unknown-host-note"
        >
          UNKNOWN ≠ OFFLINE. Estado desconhecido não implica host offline.
        </p>
      ) : null}
    </Card>
  );
}
