import { Card } from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";
import { ILLUSTRATIVE_WINDOW_DISCLOSURE } from "./loadReadinessScreenData";

export type WindowProgressProps = {
  readiness: ReadinessViewModel;
};

function formatDays(
  value: number | null,
  availability: string,
  displayText: string | null,
): string {
  if (availability !== "available" || value === null) {
    return displayText ?? "indisponível";
  }
  return displayText ?? `${value} dias`;
}

/**
 * Calm linear / textual window comparison — never a gauge or casino viz.
 */
export function WindowProgress({ readiness }: WindowProgressProps) {
  const observed = readiness.windowDays;
  const required = readiness.requiredWindowDays;
  const bothAvailable =
    observed.availability === "available" &&
    required.availability === "available" &&
    observed.value !== null &&
    required.value !== null;

  const remaining =
    bothAvailable && required.value !== null && observed.value !== null
      ? Math.max(required.value - observed.value, 0)
      : null;

  const ratio =
    bothAvailable && required.value !== null && required.value > 0
      ? Math.min(observed.value! / required.value, 1)
      : null;

  const statusLabel = bothAvailable
    ? remaining === 0
      ? "Janela ilustrativa atingida"
      : "Janela ilustrativa insuficiente"
    : "Progresso de janela indisponível";

  return (
    <Card className="wick-readiness-card" data-testid="readiness-window-progress">
      <h2 className="wick-readiness-card-title">Progresso da janela</h2>
      <p className="wick-readiness-primary" data-testid="readiness-window-status">
        {statusLabel}
      </p>
      <dl className="wick-readiness-field-list">
        <div className="wick-readiness-field">
          <dt>Dias observados</dt>
          <dd data-testid="readiness-window-observed">
            {formatDays(observed.value, observed.availability, observed.displayText)}
          </dd>
        </div>
        <div className="wick-readiness-field">
          <dt>Dias exigidos</dt>
          <dd data-testid="readiness-window-required">
            {formatDays(required.value, required.availability, required.displayText)}
          </dd>
        </div>
        <div className="wick-readiness-field">
          <dt>Dias restantes</dt>
          <dd data-testid="readiness-window-remaining">
            {remaining === null ? "indisponível" : `${remaining} dias`}
          </dd>
        </div>
      </dl>

      {ratio !== null ? (
        <div
          className="wick-readiness-progress"
          role="progressbar"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(ratio * 100)}
          aria-label="Progresso ilustrativo da janela futura observada"
          data-testid="readiness-window-bar"
        >
          <div
            className="wick-readiness-progress__fill"
            style={{ width: `${Math.round(ratio * 100)}%` }}
          />
        </div>
      ) : (
        <p
          className="wick-readiness-muted"
          data-testid="readiness-window-bar-absent"
        >
          Barra de progresso omitida — métricas de janela indisponíveis (não
          preenchidas com zero).
        </p>
      )}

      <p
        className="wick-readiness-muted"
        data-testid="readiness-window-disclosure"
      >
        {ILLUSTRATIVE_WINDOW_DISCLOSURE} Atingir a contagem ilustrativa de dias{" "}
        <strong>não</strong> prova edge preditivo.
      </p>
    </Card>
  );
}
