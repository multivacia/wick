import {
  Alert,
  Card,
  Inline,
  StatusBadge,
  type StatusBadgeStatus,
} from "../../components/primitives";
import type { RunsViewModel } from "../../viewmodels";

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

export type RunsSummaryProps = {
  runs: RunsViewModel;
};

export function RunsSummary({ runs }: RunsSummaryProps) {
  const status = runs.summaryStatus as StatusBadgeStatus;
  return (
    <Card className="wick-runs-summary" data-testid="runs-summary">
      <Inline className="wick-runs-summary__header">
        <h2 className="wick-runs-card-title">Resumo das execuções</h2>
        <StatusBadge
          status={status}
          label={STATUS_LABEL_PT[status] ?? status}
          data-testid="runs-summary-status-badge"
          data-status={status}
        />
      </Inline>
      <p className="wick-runs-primary" data-testid="runs-summary-message">
        {runs.primaryMessage.plainLanguage}
      </p>
      {runs.primaryMessage.technicalCode ? (
        <p className="wick-runs-technical">
          Técnico: <code>{runs.primaryMessage.technicalCode}</code>
        </p>
      ) : null}
      {runs.actionHint ? (
        <Alert
          tone="informational"
          title="Sugestão (somente leitura)"
          data-testid="runs-action-hint"
          className="wick-runs-action-hint"
        >
          <p className="wick-runs-primary">{runs.actionHint.plainLanguage}</p>
          <p className="wick-runs-technical">
            Código: <code>{runs.actionHint.code}</code>
            {" · "}
            advisoryOnly = {String(runs.actionHint.advisoryOnly)}
          </p>
        </Alert>
      ) : null}
    </Card>
  );
}
