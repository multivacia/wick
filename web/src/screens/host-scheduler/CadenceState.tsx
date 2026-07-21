import { Card } from "../../components/primitives";
import { VM_FIELD_ABSENT_DISCLOSURE } from "./loadHostSchedulerScreenData";

/**
 * Cadence is not on HostSchedulerViewModel — remain unavailable.
 */
export function CadenceState() {
  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-cadence-state"
    >
      <h2 className="wick-host-scheduler-card-title">Cadência</h2>
      <p
        className="wick-host-scheduler-primary"
        data-testid="host-scheduler-cadence-value"
      >
        indisponível
      </p>
      <p className="wick-host-scheduler-muted" data-testid="host-scheduler-cadence-absent">
        {VM_FIELD_ABSENT_DISCLOSURE} Nenhuma cadência cron/systemd é inventada
        nesta tela.
      </p>
    </Card>
  );
}
