import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type M0M5ExplanationProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function M0M5Explanation({ r3eExperiment }: M0M5ExplanationProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-m0-m5-explanation">
      <h2 className="wick-r3e-card-title">Estágios M0–M5</h2>
      <p className="wick-r3e-primary">
        Em linguagem simples: cada estágio M acrescenta uma camada de informação.
        M0 é o baseline; M5 é o contexto completo mais o padrão de candle.
      </p>
      <div className="wick-r3e-stage-list" data-testid="r3e-model-stages">
        {r3eExperiment.modelStages.map((stage) => (
          <article
            key={stage.id}
            className="wick-r3e-stage"
            data-testid={`r3e-stage-${stage.id}`}
          >
            <h3 className="wick-r3e-stage-title">{stage.id}</h3>
            <p className="wick-r3e-primary">{stage.plainLanguage}</p>
            <p className="wick-r3e-technical">{stage.technicalDefinition}</p>
          </article>
        ))}
      </div>
    </Card>
  );
}
