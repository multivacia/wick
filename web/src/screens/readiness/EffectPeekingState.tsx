import { Card } from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";

export type EffectPeekingStateProps = {
  readiness: ReadinessViewModel;
};

/**
 * EFFECT_PEEKING_FALSE ≠ EFFECT_NOT_REPORTED — boolean is explicitly reported.
 */
export function EffectPeekingState({ readiness }: EffectPeekingStateProps) {
  const peeked = readiness.effectPeekingPerformed;

  return (
    <Card className="wick-readiness-card" data-testid="readiness-effect-peeking">
      <h2 className="wick-readiness-card-title">Effect peeking</h2>
      <p
        className="wick-readiness-primary"
        data-testid="readiness-effect-peeking-message"
      >
        {peeked
          ? "O ViewModel indica que effect peeking foi realizado (campo fornecido)."
          : "Effect peeking não realizado (valor explícito false no ViewModel)."}
      </p>
      <p className="wick-readiness-technical">
        effectPeekingPerformed = <code>{String(peeked)}</code>
      </p>
      <p className="wick-readiness-muted">
        EFFECT_PEEKING_FALSE ≠ EFFECT_NOT_REPORTED. O campo está presente e
        explícito; não há “não informado”.
      </p>
    </Card>
  );
}
