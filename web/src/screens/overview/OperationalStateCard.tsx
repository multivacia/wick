import {
  Card,
  Inline,
  StatusBadge,
  type StatusBadgeStatus,
} from "../../components/primitives";
import type { StateExplanation } from "../../viewmodels";

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

export type OperationalStateCardProps = {
  explanation: StateExplanation;
  scientificGate: string;
  r4Status: string;
  r5Status: string;
};

export function OperationalStateCard({
  explanation,
  scientificGate,
  r4Status,
  r5Status,
}: OperationalStateCardProps) {
  const status = explanation.status as StatusBadgeStatus;
  return (
    <Card
      className="wick-overview-state-card"
      data-testid="overview-overall-state"
    >
      <Inline className="wick-overview-state-card__header">
        <StatusBadge
          status={status}
          label={STATUS_LABEL_PT[status] ?? status}
          data-testid="overview-overall-status-badge"
        />
      </Inline>
      <p className="wick-overview-primary">
        {explanation.primaryMessage.plainLanguage}
      </p>
      {explanation.primaryMessage.technicalCode ? (
        <p className="wick-overview-technical">
          Código técnico:{" "}
          <code>{explanation.primaryMessage.technicalCode}</code>
        </p>
      ) : null}
      <p className="wick-overview-technical">
        Detalhe: {explanation.technicalDetail.plainLanguage}
        {explanation.technicalDetail.technicalCode ? (
          <>
            {" "}
            (<code>{explanation.technicalDetail.technicalCode}</code>)
          </>
        ) : null}
      </p>
      <dl className="wick-overview-gate-list">
        <div>
          <dt>Gate científico</dt>
          <dd>
            <code>{scientificGate}</code>
          </dd>
        </div>
        <div>
          <dt>R4</dt>
          <dd>
            <code>{r4Status}</code>
          </dd>
        </div>
        <div>
          <dt>R5</dt>
          <dd>
            <code>{r5Status}</code>
          </dd>
        </div>
      </dl>
    </Card>
  );
}
