import { Button, Inline } from "../../components/primitives";
import type {
  CollectionDataQualityFilterOptions,
  CollectionDataQualityFilters,
  CollectionQualitySeverity,
  CollectionQualityStatus,
} from "../../viewmodels";

export type SeriesFiltersProps = {
  options: CollectionDataQualityFilterOptions;
  filters: CollectionDataQualityFilters;
  onChange: (filters: CollectionDataQualityFilters) => void;
  onClear: () => void;
};

function FilterSelect<T extends string>({
  id,
  label,
  value,
  options,
  onValueChange,
  testId,
}: {
  id: string;
  label: string;
  value: T | undefined;
  options: Array<{ value: T; label: string }>;
  onValueChange: (next: T | undefined) => void;
  testId: string;
}) {
  return (
    <div className="wick-collected-data-filter">
      <label className="wick-collected-data-field-label" htmlFor={id}>
        {label}
      </label>
      <select
        id={id}
        className="wick-collected-data-select"
        value={value ?? ""}
        onChange={(event) => {
          const next = event.target.value;
          onValueChange(next === "" ? undefined : (next as T));
        }}
        data-testid={testId}
      >
        <option value="">Todos</option>
        {options.map((opt) => (
          <option key={opt.value} value={opt.value}>
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
}

export function SeriesFilters({
  options,
  filters,
  onChange,
  onClear,
}: SeriesFiltersProps) {
  const hasActive =
    Boolean(filters.seriesId) ||
    Boolean(filters.market) ||
    Boolean(filters.interval) ||
    Boolean(filters.qualityStatus) ||
    Boolean(filters.severity);

  return (
    <div className="wick-collected-data-filters" data-testid="collected-data-filters">
      <Inline className="wick-collected-data-filters__row">
        <FilterSelect
          id="cdq-filter-series"
          label="Série"
          value={filters.seriesId}
          options={options.seriesIds}
          onValueChange={(seriesId) => onChange({ ...filters, seriesId })}
          testId="collected-data-filter-series"
        />
        <FilterSelect
          id="cdq-filter-market"
          label="Mercado"
          value={filters.market}
          options={options.markets}
          onValueChange={(market) => onChange({ ...filters, market })}
          testId="collected-data-filter-market"
        />
        <FilterSelect
          id="cdq-filter-interval"
          label="Intervalo"
          value={filters.interval}
          options={options.intervals}
          onValueChange={(interval) => onChange({ ...filters, interval })}
          testId="collected-data-filter-interval"
        />
        <FilterSelect
          id="cdq-filter-status"
          label="Status de qualidade"
          value={filters.qualityStatus}
          options={options.qualityStatuses}
          onValueChange={(qualityStatus: CollectionQualityStatus | undefined) =>
            onChange({ ...filters, qualityStatus })
          }
          testId="collected-data-filter-status"
        />
        <FilterSelect
          id="cdq-filter-severity"
          label="Severidade"
          value={filters.severity}
          options={options.severities}
          onValueChange={(severity: CollectionQualitySeverity | undefined) =>
            onChange({ ...filters, severity })
          }
          testId="collected-data-filter-severity"
        />
      </Inline>
      <div className="wick-collected-data-filters__actions">
        <Button
          variant="secondary"
          size="sm"
          type="button"
          onClick={onClear}
          disabled={!hasActive}
          data-testid="collected-data-filters-clear"
        >
          Limpar filtros
        </Button>
      </div>
    </div>
  );
}
