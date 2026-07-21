import { Card } from "../../components/primitives";
import { VM_FIELD_ABSENT_DISCLOSURE } from "./loadHostSchedulerScreenData";

/**
 * Next expected run is not on HostSchedulerViewModel — remain unavailable.
 */
export function NextExpectedRun() {
  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-next-expected-run"
    >
      <h2 className="wick-host-scheduler-card-title">
        Próxima execução esperada
      </h2>
      <p
        className="wick-host-scheduler-primary"
        data-testid="host-scheduler-next-run-value"
      >
        indisponível
      </p>
      <p className="wick-host-scheduler-muted" data-testid="host-scheduler-next-run-absent">
        {VM_FIELD_ABSENT_DISCLOSURE} Nenhum next-run é inventado; ativação
        permanece bloqueada.
      </p>
    </Card>
  );
}
