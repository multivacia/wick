import { Alert, Section } from "../../components/primitives";
import type { ActionHint } from "../../viewmodels";

export type NextSafeActionPanelProps = {
  action: ActionHint;
};

/**
 * Advisory-only next action. Must not render executable controls.
 */
export function NextSafeActionPanel({ action }: NextSafeActionPanelProps) {
  return (
    <Section title="Próxima ação segura" data-testid="overview-next-safe-action">
      <Alert tone="attention" title="Orientação consultiva">
        <p className="wick-overview-primary">{action.plainLanguage}</p>
        <p className="wick-overview-technical">
          Código: <code>{action.code}</code>
          {" — "}
          somente orientação; nenhuma ação é executada por esta tela.
        </p>
        {action.advisoryOnly ? (
          <p className="wick-overview-muted">advisoryOnly = true</p>
        ) : null}
      </Alert>
    </Section>
  );
}
