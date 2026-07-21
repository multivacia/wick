import { Alert, Card } from "../../components/primitives";
import type { HostSchedulerViewModel } from "../../viewmodels";

export type NextSafeHumanActionProps = {
  hostScheduler: HostSchedulerViewModel;
};

/**
 * Advisory text only — no operational controls.
 */
export function NextSafeHumanAction({
  hostScheduler,
}: NextSafeHumanActionProps) {
  const hint = hostScheduler.nextSafeAction;

  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-next-safe-action"
    >
      <h2 className="wick-host-scheduler-card-title">
        Próxima ação humana segura
      </h2>
      <Alert
        tone="informational"
        title="Sugestão (somente leitura)"
        data-testid="host-scheduler-action-hint"
      >
        <p className="wick-host-scheduler-primary">{hint.plainLanguage}</p>
        <p className="wick-host-scheduler-technical">
          Código: <code>{hint.code}</code>
          {" · "}
          advisoryOnly = <code>{String(hint.advisoryOnly)}</code>
        </p>
      </Alert>
      <p className="wick-host-scheduler-muted">
        Texto consultivo apenas — esta tela não descobre host, não solicita
        credenciais e não ativa, instala nem configura o agendador.
      </p>
    </Card>
  );
}
