import { Card } from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";

export type ValidationExecutionStateProps = {
  readiness: ReadinessViewModel;
};

/**
 * VALIDATION_NOT_EXECUTED ≠ VALIDATION_FAILED.
 * Boolean false means not executed — never invent a failure.
 */
export function ValidationExecutionState({
  readiness,
}: ValidationExecutionStateProps) {
  const executed = readiness.validationCommandExecuted;
  const authorized = readiness.validationAuthorized;

  return (
    <Card
      className="wick-readiness-card"
      data-testid="readiness-validation-execution"
    >
      <h2 className="wick-readiness-card-title">Validação executada?</h2>
      <p
        className="wick-readiness-primary"
        data-testid="readiness-validation-executed-message"
      >
        {executed
          ? "O ViewModel indica que um comando de validação já foi executado (campo fornecido)."
          : "Validação ainda não executada. Isso não significa falha de validação."}
      </p>
      <dl className="wick-readiness-field-list">
        <div className="wick-readiness-field">
          <dt>validationCommandExecuted</dt>
          <dd data-testid="readiness-validation-executed">
            <code>{String(executed)}</code>
          </dd>
        </div>
        <div className="wick-readiness-field">
          <dt>validationAuthorized</dt>
          <dd data-testid="readiness-validation-authorized">
            <code>{String(authorized)}</code>
          </dd>
        </div>
      </dl>
      <p className="wick-readiness-muted">
        VALIDATION_NOT_EXECUTED ≠ VALIDATION_FAILED. Esta tela não executa
        validação.
      </p>
    </Card>
  );
}
