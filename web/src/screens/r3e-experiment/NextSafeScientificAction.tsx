import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type NextSafeScientificActionProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function NextSafeScientificAction({
  r3eExperiment,
}: NextSafeScientificActionProps) {
  const action = r3eExperiment.nextSafeScientificAction;
  return (
    <Card className="wick-r3e-card" data-testid="r3e-next-safe-action">
      <h2 className="wick-r3e-card-title">Próxima ação científica segura</h2>
      <p className="wick-r3e-primary">{action.plainLanguage}</p>
      <p className="wick-r3e-technical">Código: {action.code}</p>
      <p className="wick-r3e-muted">
        Ação apenas consultiva (advisoryOnly=
        {String(action.advisoryOnly)}). Não executa validação nem altera R4/R5.
      </p>
    </Card>
  );
}
