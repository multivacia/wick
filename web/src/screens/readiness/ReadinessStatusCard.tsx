import {
  Card,
  Inline,
  StatusBadge,
  type StatusBadgeStatus,
} from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";

const STATUS_LABEL_PT: Partial<Record<StatusBadgeStatus, string>> = {
  healthy: "Pronto",
  completed: "Concluído",
  attention: "Atenção",
  not_ready: "Não pronto",
  blocked: "Bloqueado",
  deferred: "Adiado",
  unknown: "Desconhecido",
  fault: "Falha",
  informational: "Em andamento",
};

export type ReadinessStatusCardProps = {
  readiness: ReadinessViewModel;
};

/**
 * Primary readiness status — plain language first; READY ≠ strategy approval.
 */
export function ReadinessStatusCard({ readiness }: ReadinessStatusCardProps) {
  const status = readiness.presentation.status as StatusBadgeStatus;
  const isReady = readiness.state === "ready";

  return (
    <Card className="wick-readiness-card" data-testid="readiness-status-card">
      <Inline className="wick-readiness-card__header">
        <h2 className="wick-readiness-card-title">Estado de prontidão</h2>
        <StatusBadge
          status={status}
          label={STATUS_LABEL_PT[status] ?? status}
          data-testid="readiness-status-badge"
          data-status={status}
        />
      </Inline>
      <p className="wick-readiness-primary" data-testid="readiness-status-message">
        {readiness.presentation.primaryMessage.plainLanguage}
      </p>
      <p className="wick-readiness-technical">
        Técnico:{" "}
        <code>
          {readiness.presentation.primaryMessage.technicalCode ??
            readiness.state.toUpperCase()}
        </code>
        {" · "}
        domínio: <code>{readiness.state}</code>
      </p>
      {isReady ? (
        <p
          className="wick-readiness-primary"
          data-testid="readiness-ready-disclaimer"
        >
          Prontidão para considerar a execução da validação futura{" "}
          <strong>não</strong> é aprovação de estratégia, de edge preditivo nem
          de rentabilidade.
        </p>
      ) : null}
      {status === "not_ready" || readiness.state === "not_ready" ? (
        <p className="wick-readiness-muted" data-testid="readiness-not-ready-note">
          Não pronto ≠ falha. Este estado usa atenção (âmbar), não fault/vermelho.
        </p>
      ) : null}
    </Card>
  );
}
