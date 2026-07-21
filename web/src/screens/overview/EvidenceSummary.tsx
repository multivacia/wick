import { Section } from "../../components/primitives";
import type { EvidenceLink, RunViewModel } from "../../viewmodels";
import { RelatedEvidenceLinks } from "../shared/RelatedEvidenceLinks";

export type EvidenceSummaryProps = {
  evidence: EvidenceLink[];
  lastCompletedRun: RunViewModel | null;
  lastFailedRun: RunViewModel | null;
};

function formatMetric(
  label: string,
  metric: { value: number | null; displayText: string | null; availability: string },
): string {
  if (metric.value === null || metric.availability !== "available") {
    return `${label}: indisponível`;
  }
  return `${label}: ${metric.displayText ?? String(metric.value)}`;
}

export function EvidenceSummary({
  evidence,
  lastCompletedRun,
  lastFailedRun,
}: EvidenceSummaryProps) {
  return (
    <Section title="Evidência mais recente" data-testid="overview-latest-evidence">
      {evidence.length === 0 && !lastCompletedRun && !lastFailedRun ? (
        <p className="wick-overview-muted">
          Nenhuma evidência fornecida neste cenário (sem preenchimento artificial).
        </p>
      ) : null}

      {lastCompletedRun ? (
        <div className="wick-overview-evidence-block">
          <h3 className="wick-overview-subheading">Última execução concluída</h3>
          <p className="wick-overview-primary">
            {lastCompletedRun.presentation.primaryMessage.plainLanguage}
          </p>
          <p className="wick-overview-technical">
            Run: <code>{lastCompletedRun.runId ?? "indisponível"}</code>
          </p>
          <ul className="wick-overview-metric-list">
            <li>
              {formatMetric("Aceitos", lastCompletedRun.acceptedCount)}
            </li>
            <li>
              {formatMetric("Rejeitados", lastCompletedRun.rejectedCount)}
            </li>
            <li>
              {formatMetric("Store antes", lastCompletedRun.storeBeforeCount)}
            </li>
            <li>
              {formatMetric("Store depois", lastCompletedRun.storeAfterCount)}
            </li>
          </ul>
        </div>
      ) : null}

      {lastFailedRun ? (
        <div className="wick-overview-evidence-block">
          <h3 className="wick-overview-subheading">Última execução com falha</h3>
          <p className="wick-overview-primary">
            {lastFailedRun.presentation.primaryMessage.plainLanguage}
          </p>
          <p className="wick-overview-technical">
            Run: <code>{lastFailedRun.runId ?? "indisponível"}</code>
            {lastFailedRun.failureReason ? (
              <>
                {" "}
                — motivo: <code>{lastFailedRun.failureReason}</code>
              </>
            ) : null}
          </p>
        </div>
      ) : null}

      {evidence.length > 0 ? (
        <ul className="wick-overview-evidence-list">
          {evidence.map((item) => (
            <li key={`${item.kind}:${item.reference}`}>
              <span className="wick-overview-primary">{item.label}</span>
              <span className="wick-overview-technical">
                {" "}
                (<code>{item.reference}</code> ({item.kind})
              </span>
            </li>
          ))}
        </ul>
      ) : null}

      <RelatedEvidenceLinks
        items={[
          {
            evidenceId: "ev-r3e-pending-future-unseen",
            label: "Estado R3E — gate pendente de dados futuros",
          },
          {
            evidenceId: "ev-fu-collection-readiness",
            label: "Prontidão de coleta future-unseen",
          },
          {
            evidenceId: "ev-host-scheduler-operational-debt",
            label: "Dívida operacional — host e agendador",
          },
          {
            evidenceId: "ev-ux-r1-formal-closure",
            label: "Encerramento formal UX-R1",
          },
        ]}
      />
    </Section>
  );
}
