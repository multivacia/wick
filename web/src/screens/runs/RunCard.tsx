import {
  Inline,
  StatusBadge,
  type StatusBadgeStatus,
} from "../../components/primitives";
import type { RunViewModel } from "../../viewmodels";
import { formatMetric, formatTimestamp } from "./formatters";

const STATUS_LABEL_PT: Partial<Record<StatusBadgeStatus, string>> = {
  healthy: "Saudável",
  completed: "Concluído",
  attention: "Atenção",
  not_ready: "Não pronto",
  blocked: "Bloqueado",
  deferred: "Adiado",
  unknown: "Desconhecido",
  fault: "Falha",
  informational: "Em andamento",
};

export type RunCardProps = {
  run: RunViewModel;
};

export function RunCard({ run }: RunCardProps) {
  const status = run.presentation.status as StatusBadgeStatus;
  const runKey = run.runId ?? "sem-id";

  return (
    <article
      className="wick-runs-card"
      data-testid={`runs-card-${runKey}`}
      data-run-state={run.state}
      data-run-status={status}
    >
      <Inline className="wick-runs-card__header">
        <h3 className="wick-runs-card-title">
          {run.runId ? (
            <>
              Execução <code>{run.runId}</code>
            </>
          ) : (
            "Execução sem identificador"
          )}
        </h3>
        <StatusBadge
          status={status}
          label={STATUS_LABEL_PT[status] ?? status}
          data-testid={`runs-status-${runKey}`}
          data-status={status}
        />
      </Inline>

      <p className="wick-runs-primary" data-testid={`runs-status-message-${runKey}`}>
        {run.presentation.primaryMessage.plainLanguage}
      </p>
      {run.presentation.primaryMessage.technicalCode ? (
        <p className="wick-runs-technical">
          Estado técnico:{" "}
          <code>{run.presentation.primaryMessage.technicalCode}</code>
        </p>
      ) : null}

      <dl className="wick-runs-field-list">
        <div className="wick-runs-field" data-testid={`runs-timing-${runKey}`}>
          <dt>Início</dt>
          <dd>{formatTimestamp(run.startedAt)}</dd>
          <dt>Fim</dt>
          <dd>{formatTimestamp(run.finishedAt)}</dd>
        </div>

        <div className="wick-runs-field" data-testid={`runs-counts-${runKey}`}>
          <dt>Aceitos</dt>
          <dd>{formatMetric(run.acceptedCount)}</dd>
          <dt>Rejeitados</dt>
          <dd>{formatMetric(run.rejectedCount)}</dd>
        </div>

        <div className="wick-runs-field" data-testid={`runs-store-${runKey}`}>
          <dt>Store antes</dt>
          <dd>{formatMetric(run.storeBeforeCount)}</dd>
          <dt>Store depois</dt>
          <dd>{formatMetric(run.storeAfterCount)}</dd>
        </div>

        <div
          className="wick-runs-field"
          data-testid={`runs-idempotency-${runKey}`}
        >
          <dt>Idempotência</dt>
          <dd>
            {run.idempotencyResult ? (
              <code>{run.idempotencyResult}</code>
            ) : (
              "indisponível"
            )}
          </dd>
        </div>

        <div className="wick-runs-field" data-testid={`runs-result-${runKey}`}>
          <dt>Resultado</dt>
          <dd>
            {run.resultLabel ? <code>{run.resultLabel}</code> : "indisponível"}
          </dd>
        </div>

        <div className="wick-runs-field" data-testid={`runs-failure-${runKey}`}>
          <dt>Motivo de falha</dt>
          <dd>
            {run.failureReason ? (
              <code>{run.failureReason}</code>
            ) : (
              "indisponível"
            )}
          </dd>
        </div>
      </dl>

      <div data-testid={`runs-evidence-${runKey}`}>
        <h4 className="wick-runs-subheading">Evidência técnica</h4>
        {run.evidence.length === 0 ? (
          <p className="wick-runs-muted">Nenhuma evidência fornecida.</p>
        ) : (
          <ul className="wick-runs-evidence-list">
            {run.evidence.map((item) => (
              <li key={`${item.kind}:${item.reference}`}>
                <span className="wick-runs-primary">{item.label}</span>
                <span className="wick-runs-technical">
                  {" "}
                  <code>{item.reference}</code> ({item.kind})
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </article>
  );
}
