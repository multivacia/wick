import { Alert, Card } from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";

export type NextSafeActionProps = {
  readiness: ReadinessViewModel;
};

export function NextSafeAction({ readiness }: NextSafeActionProps) {
  const hint = readiness.nextSafeAction;

  return (
    <Card className="wick-readiness-card" data-testid="readiness-next-safe-action">
      <h2 className="wick-readiness-card-title">Próxima ação segura</h2>
      <Alert
        tone="informational"
        title="Sugestão (somente leitura)"
        data-testid="readiness-action-hint"
      >
        <p className="wick-readiness-primary">{hint.plainLanguage}</p>
        <p className="wick-readiness-technical">
          Código: <code>{hint.code}</code>
          {" · "}
          advisoryOnly = <code>{String(hint.advisoryOnly)}</code>
        </p>
      </Alert>
      <p className="wick-readiness-muted">
        Texto consultivo apenas — esta tela não executa validação, coleta nem
        scheduler.
      </p>
    </Card>
  );
}
