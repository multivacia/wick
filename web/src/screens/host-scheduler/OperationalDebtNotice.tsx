import { Alert, Card } from "../../components/primitives";
import type { HostSchedulerViewModel } from "../../viewmodels";
import {
  OPERATIONAL_DEBT_DETAIL_WORDING,
  OPERATIONAL_DEBT_OFFICIAL_WORDING,
} from "./loadHostSchedulerScreenData";

export type OperationalDebtNoticeProps = {
  hostScheduler: HostSchedulerViewModel;
};

/**
 * Official operational debt notice — OPEN ≠ activation complete.
 */
export function OperationalDebtNotice({
  hostScheduler,
}: OperationalDebtNoticeProps) {
  const debt = hostScheduler.operationalDebt;

  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-operational-debt"
    >
      <h2 className="wick-host-scheduler-card-title">
        Débito técnico-operacional
      </h2>
      <p className="wick-host-scheduler-technical">
        Estado: <code data-testid="host-scheduler-debt-state">{debt}</code>
        {" · "}
        técnico: <code>OPERATIONAL_DEBT={debt.toUpperCase()}</code>
      </p>
      {debt === "open" ? (
        <Alert
          tone="informational"
          title="Débito aberto"
          data-testid="host-scheduler-debt-notice"
        >
          <p
            className="wick-host-scheduler-primary"
            data-testid="host-scheduler-debt-official"
          >
            {OPERATIONAL_DEBT_OFFICIAL_WORDING}
          </p>
          <p
            className="wick-host-scheduler-primary"
            data-testid="host-scheduler-debt-detail"
          >
            {OPERATIONAL_DEBT_DETAIL_WORDING}
          </p>
          <p className="wick-host-scheduler-muted">
            Débito aberto ≠ concluído. Scheduler não está ativo.
          </p>
        </Alert>
      ) : null}
      {debt === "unknown" ? (
        <p
          className="wick-host-scheduler-primary"
          data-testid="host-scheduler-debt-unknown"
        >
          Débito operacional desconhecido neste ViewModel — não equivale a
          débito fechado nem a ativação concluída.
        </p>
      ) : null}
      {debt === "none" ? (
        <p
          className="wick-host-scheduler-primary"
          data-testid="host-scheduler-debt-none"
        >
          Nenhum débito operacional aberto neste ViewModel sintético. Isto não
          prova ativação operacional real.
        </p>
      ) : null}
    </Card>
  );
}
