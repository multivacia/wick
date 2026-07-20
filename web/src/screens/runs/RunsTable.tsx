import type { RunViewModel } from "../../viewmodels";
import {
  StatusBadge,
  type StatusBadgeStatus,
} from "../../components/primitives";
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

export type RunsTableProps = {
  runs: RunViewModel[];
};

export function RunsTable({ runs }: RunsTableProps) {
  return (
    <div className="wick-runs-table-wrap" data-testid="runs-table">
      <table className="wick-runs-table">
        <caption className="wick-runs-table-caption">
          Lista de execuções ilustrativas com status, tempos, contagens e
          evidência técnica.
        </caption>
        <thead>
          <tr>
            <th scope="col">Execução</th>
            <th scope="col">Status</th>
            <th scope="col">Início</th>
            <th scope="col">Fim</th>
            <th scope="col">Aceitos</th>
            <th scope="col">Rejeitados</th>
            <th scope="col">Store</th>
            <th scope="col">Idempotência</th>
            <th scope="col">Falha</th>
            <th scope="col">Evidência</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => {
            const status = run.presentation.status as StatusBadgeStatus;
            const runKey = run.runId ?? "sem-id";
            return (
              <tr
                key={runKey}
                data-testid={`runs-row-${runKey}`}
                data-run-state={run.state}
                data-run-status={status}
              >
                <th scope="row" data-label="Execução">
                  {run.runId ? (
                    <code className="wick-runs-id">{run.runId}</code>
                  ) : (
                    "indisponível"
                  )}
                  <span className="wick-runs-table-plain">
                    {run.presentation.primaryMessage.plainLanguage}
                  </span>
                </th>
                <td data-label="Status">
                  <StatusBadge
                    status={status}
                    label={STATUS_LABEL_PT[status] ?? status}
                    data-testid={`runs-table-status-${runKey}`}
                    data-status={status}
                  />
                </td>
                <td data-label="Início">{formatTimestamp(run.startedAt)}</td>
                <td data-label="Fim">{formatTimestamp(run.finishedAt)}</td>
                <td data-label="Aceitos">{formatMetric(run.acceptedCount)}</td>
                <td data-label="Rejeitados">
                  {formatMetric(run.rejectedCount)}
                </td>
                <td data-label="Store">
                  {formatMetric(run.storeBeforeCount)} →{" "}
                  {formatMetric(run.storeAfterCount)}
                </td>
                <td data-label="Idempotência">
                  {run.idempotencyResult ? (
                    <code>{run.idempotencyResult}</code>
                  ) : (
                    "indisponível"
                  )}
                </td>
                <td data-label="Falha">
                  {run.failureReason ? (
                    <code>{run.failureReason}</code>
                  ) : (
                    "indisponível"
                  )}
                </td>
                <td data-label="Evidência">
                  {run.evidence.length === 0 ? (
                    "indisponível"
                  ) : (
                    <ul className="wick-runs-evidence-inline">
                      {run.evidence.map((item) => (
                        <li key={`${item.kind}:${item.reference}`}>
                          <code>{item.reference}</code>
                        </li>
                      ))}
                    </ul>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
