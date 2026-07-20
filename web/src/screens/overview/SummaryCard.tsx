import {
  Card,
  Inline,
  StatusBadge,
  type StatusBadgeStatus,
} from "../../components/primitives";
import type { PresentationBlock } from "../../viewmodels";

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

export type SummaryCardProps = {
  title: string;
  block: PresentationBlock;
  testId: string;
};

export function SummaryCard({ title, block, testId }: SummaryCardProps) {
  const status = block.explanation.status as StatusBadgeStatus;
  const observed = block.observedAt;
  return (
    <Card className="wick-overview-summary-card" data-testid={testId}>
      <Inline className="wick-overview-summary-card__header">
        <h3 className="wick-overview-card-title">{title}</h3>
        <StatusBadge
          status={status}
          label={STATUS_LABEL_PT[status] ?? status}
          data-status={status}
        />
      </Inline>
      <p className="wick-overview-primary">
        {block.explanation.primaryMessage.plainLanguage}
      </p>
      {block.explanation.technicalDetail.technicalCode ||
      block.explanation.technicalDetail.reasonCode ? (
        <p className="wick-overview-technical">
          Técnico:{" "}
          <code>
            {block.explanation.technicalDetail.technicalCode ??
              block.explanation.technicalDetail.reasonCode}
          </code>
        </p>
      ) : (
        <p className="wick-overview-technical">
          {block.explanation.technicalDetail.plainLanguage}
        </p>
      )}
      {observed ? (
        <p className="wick-overview-muted">
          Observado:{" "}
          {observed.displayText ??
            observed.rawIso ??
            "indisponível (não inventado)"}
          {observed.availability !== "available" ? (
            <>
              {" "}
              <span>(disponibilidade: {observed.availability})</span>
            </>
          ) : null}
        </p>
      ) : null}
      {block.actionHint ? (
        <p className="wick-overview-muted">
          Sugestão: {block.actionHint.plainLanguage}
        </p>
      ) : null}
    </Card>
  );
}
