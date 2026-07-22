import { Alert, Button, Card, StatusBadge } from "../../components/primitives";
import type { StatusBadgeStatus } from "../../components/primitives";
import type { CollectionSeriesViewModel } from "../../viewmodels";

export type SeriesListProps = {
  series: readonly CollectionSeriesViewModel[];
  resultCount: number;
  totalSeriesCount: number;
  emptyState: boolean;
  noResultsState: boolean;
  onClearFilters: () => void;
};

function CountCell({
  label,
  displayText,
  isUnknown,
}: {
  label: string;
  displayText: string;
  isUnknown: boolean;
}) {
  return (
    <div className="wick-collected-data-metric">
      <dt>{label}</dt>
      <dd data-unknown={isUnknown ? "true" : "false"}>{displayText}</dd>
    </div>
  );
}

function SeriesCard({ entry }: { entry: CollectionSeriesViewModel }) {
  return (
    <article
      className="wick-collected-data-series"
      data-testid={`collected-data-series-${entry.seriesId}`}
      data-severity={entry.quality.qualitySeverity}
      data-quality-status={entry.quality.qualityStatus}
    >
      <header className="wick-collected-data-series__header">
        <h3 className="wick-collected-data-series__title">{entry.seriesId}</h3>
        <StatusBadge
          status={entry.quality.status as StatusBadgeStatus}
          label={`${entry.quality.qualityStatusLabel} · ${entry.quality.qualitySeverityLabel}`}
        />
      </header>
      <p className="wick-collected-data-muted">
        {entry.market} · {entry.asset} · {entry.interval} · fonte {entry.source} (
        {entry.sourceStateLabel})
      </p>
      <p className="wick-collected-data-muted">
        Janela representada: {entry.coverageWindowLabel}
      </p>
      <p className="wick-collected-data-muted">
        Última atualização ilustrativa:{" "}
        {entry.lastUpdate.displayText ?? "Desconhecida"}
        {entry.lastUpdate.freshness === "stale" ? " (desatualizada)" : ""}
      </p>
      <dl className="wick-collected-data-metrics" data-testid={`collected-data-metrics-${entry.seriesId}`}>
        <CountCell
          label="Esperados"
          displayText={entry.expectedRecords.displayText}
          isUnknown={entry.expectedRecords.isUnknown}
        />
        <CountCell
          label="Aceitos"
          displayText={entry.acceptedRecords.displayText}
          isUnknown={entry.acceptedRecords.isUnknown}
        />
        <CountCell
          label="Rejeitados"
          displayText={entry.rejectedRecords.displayText}
          isUnknown={entry.rejectedRecords.isUnknown}
        />
        <CountCell
          label="Lacunas"
          displayText={entry.gapCount.displayText}
          isUnknown={entry.gapCount.isUnknown}
        />
        <CountCell
          label="Duplicatas"
          displayText={entry.duplicateCount.displayText}
          isUnknown={entry.duplicateCount.isUnknown}
        />
        <CountCell
          label="Candle aberto excluído"
          displayText={entry.openCandleExclusionCount.displayText}
          isUnknown={entry.openCandleExclusionCount.isUnknown}
        />
      </dl>
      {entry.findings.length > 0 ? (
        <ul className="wick-collected-data-findings">
          {entry.findings.map((finding) => (
            <li key={finding.code}>
              <strong>{finding.severity}</strong>: {finding.message}
            </li>
          ))}
        </ul>
      ) : null}
      {entry.limitations.length > 0 ? (
        <ul className="wick-collected-data-muted-list">
          {entry.limitations.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : null}
    </article>
  );
}

export function SeriesList({
  series,
  resultCount,
  totalSeriesCount,
  emptyState,
  noResultsState,
  onClearFilters,
}: SeriesListProps) {
  if (emptyState) {
    return (
      <Card className="wick-collected-data-card" data-testid="collected-data-empty-state">
        <h2 className="wick-collected-data-card-title">Nenhuma série</h2>
        <p className="wick-collected-data-primary">
          Não há séries ilustrativas neste fixture.
        </p>
        <p className="wick-collected-data-muted">
          Lista vazia não é falha confirmada (EMPTY ≠ FAULT).
        </p>
      </Card>
    );
  }

  if (noResultsState) {
    return (
      <Card className="wick-collected-data-card" data-testid="collected-data-no-results">
        <h2 className="wick-collected-data-card-title">Sem resultados</h2>
        <Alert tone="attention" title="Filtros sem correspondência">
          <p>
            Nenhuma série corresponde aos filtros atuais ({totalSeriesCount} séries no
            catálogo ilustrativo).
          </p>
        </Alert>
        <Button
          variant="secondary"
          size="sm"
          type="button"
          onClick={onClearFilters}
          data-testid="collected-data-no-results-clear"
        >
          Limpar filtros
        </Button>
      </Card>
    );
  }

  return (
    <div className="wick-collected-data-series-list" data-testid="collected-data-series-list">
      <p className="wick-collected-data-muted" data-testid="collected-data-result-count">
        Exibindo {resultCount} de {totalSeriesCount} séries (ordenadas por severidade, depois
        atualização).
      </p>
      <div className="wick-collected-data-series-grid">
        {series.map((entry) => (
          <SeriesCard key={entry.seriesId} entry={entry} />
        ))}
      </div>
    </div>
  );
}
