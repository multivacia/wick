import { Card } from "../../components/primitives";
import { explainReasonCode } from "../../viewmodels";
import type { ReadinessViewModel } from "../../viewmodels";

export type BlockingReasonProps = {
  readiness: ReadinessViewModel;
};

export function BlockingReason({ readiness }: BlockingReasonProps) {
  const codes = readiness.blockingReasonCodes;
  const detail = readiness.presentation.technicalDetail;

  return (
    <Card className="wick-readiness-card" data-testid="readiness-blocking-reason">
      <h2 className="wick-readiness-card-title">Motivo de bloqueio</h2>
      {codes.length === 0 ? (
        <p className="wick-readiness-primary" data-testid="readiness-blocking-none">
          Nenhum código de bloqueio fornecido neste ViewModel.
        </p>
      ) : (
        <ul className="wick-readiness-list" data-testid="readiness-blocking-list">
          {codes.map((code) => (
            <li key={code} data-testid={`readiness-blocking-${code}`}>
              <p className="wick-readiness-primary">{explainReasonCode(code)}</p>
              <p className="wick-readiness-technical">
                Código: <code>{code}</code>
              </p>
            </li>
          ))}
        </ul>
      )}
      {detail.reasonCode ? (
        <p className="wick-readiness-technical">
          Detalhe técnico: {detail.plainLanguage} (
          <code>{detail.technicalCode}</code>)
        </p>
      ) : null}
    </Card>
  );
}
