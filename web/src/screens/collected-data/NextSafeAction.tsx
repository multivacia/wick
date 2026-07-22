import { Alert, Card } from "../../components/primitives";
import type { ActionHint } from "../../viewmodels";

export type NextSafeActionProps = {
  hint: ActionHint;
};

export function NextSafeAction({ hint }: NextSafeActionProps) {
  return (
    <Card className="wick-collected-data-card" data-testid="collected-data-next-safe-action">
      <h2 className="wick-collected-data-card-title">Próxima ação segura</h2>
      <Alert
        tone="informational"
        title="Sugestão (somente leitura)"
        data-testid="collected-data-action-hint"
      >
        <p className="wick-collected-data-primary">{hint.plainLanguage}</p>
        <p className="wick-collected-data-muted">
          Código: <code>{hint.code}</code>
          {" · "}
          advisoryOnly = <code>{String(hint.advisoryOnly)}</code>
        </p>
      </Alert>
      <p className="wick-collected-data-muted">
        Texto consultivo apenas — esta tela não executa validação, coleta nem
        scheduler.
      </p>
    </Card>
  );
}
