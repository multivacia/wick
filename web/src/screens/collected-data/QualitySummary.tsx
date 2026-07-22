import { Alert, Card, StatusBadge } from "../../components/primitives";
import type { CollectionDataQualityViewModel } from "../../viewmodels";
import type { StatusBadgeStatus } from "../../components/primitives";

export type QualitySummaryProps = {
  vm: CollectionDataQualityViewModel;
};

export function QualitySummary({ vm }: QualitySummaryProps) {
  const agg = vm.aggregateQuality;
  return (
    <Card className="wick-collected-data-card" data-testid="collected-data-summary">
      <h2 className="wick-collected-data-card-title">Resumo de qualidade</h2>
      <div className="wick-collected-data-summary-row">
        <StatusBadge
          status={agg.status as StatusBadgeStatus}
          label={agg.qualityStatusLabel}
          data-testid="collected-data-aggregate-badge"
        />
        <p className="wick-collected-data-muted" data-testid="collected-data-as-of">
          Referência ilustrativa: <time dateTime={vm.asOfIso}>{vm.asOfIso}</time>
        </p>
      </div>
      <p className="wick-collected-data-primary" data-testid="collected-data-illustrative-disclosure">
        {vm.illustrativeDisclosure}
      </p>
      <Alert
        tone="informational"
        title="Atualidade ilustrativa"
        data-testid="collected-data-freshness-disclosure"
      >
        <p>{vm.freshnessDisclosure}</p>
        {vm.hasStaleSeries ? (
          <p className="wick-collected-data-muted">
            Há séries ilustrativas desatualizadas (STALE ≠ FAULT; STALE ≠ VALIDATION_READY).
          </p>
        ) : null}
      </Alert>
      <ul
        className="wick-collected-data-safeguards"
        data-testid="collected-data-semantic-safeguards"
      >
        {vm.semanticSafeguards.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
      <div className="wick-collected-data-known-unknown">
        <div>
          <h3 className="wick-collected-data-subtitle">Conhecido (ilustrativo)</h3>
          <ul>
            {vm.knownState.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div>
          <h3 className="wick-collected-data-subtitle">Desconhecido</h3>
          <ul data-testid="collected-data-unknown-state">
            {vm.unknownState.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
          {vm.hasUnknownCounts ? (
            <p className="wick-collected-data-muted">
              Contagens desconhecidas aparecem como &quot;Desconhecido&quot; — UNKNOWN ≠ ZERO.
            </p>
          ) : null}
        </div>
      </div>
      {vm.aggregateLimitations.length > 0 ? (
        <div>
          <h3 className="wick-collected-data-subtitle">Limitações</h3>
          <ul>
            {vm.aggregateLimitations.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      ) : null}
    </Card>
  );
}
