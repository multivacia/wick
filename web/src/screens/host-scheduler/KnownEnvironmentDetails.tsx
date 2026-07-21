import { Card } from "../../components/primitives";
import { VM_FIELD_ABSENT_DISCLOSURE } from "./loadHostSchedulerScreenData";

/**
 * Environment identity fields are not on HostSchedulerViewModel.
 * Disclose unavailability — never invent hostname, IP or paths.
 */
export function KnownEnvironmentDetails() {
  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-environment-details"
    >
      <h2 className="wick-host-scheduler-card-title">
        Detalhes conhecidos do ambiente
      </h2>
      <dl className="wick-host-scheduler-field-list">
        <div className="wick-host-scheduler-field">
          <dt>Hostname</dt>
          <dd data-testid="host-scheduler-hostname">indisponível</dd>
        </div>
        <div className="wick-host-scheduler-field">
          <dt>Endereço / IP</dt>
          <dd data-testid="host-scheduler-address">indisponível</dd>
        </div>
        <div className="wick-host-scheduler-field">
          <dt>Caminhos sensíveis</dt>
          <dd data-testid="host-scheduler-paths">indisponível</dd>
        </div>
      </dl>
      <p className="wick-host-scheduler-muted" data-testid="host-scheduler-env-absent">
        {VM_FIELD_ABSENT_DISCLOSURE} Identidade de host, IPs e caminhos não
        fazem parte deste ViewModel e não são fabricados.
      </p>
    </Card>
  );
}
