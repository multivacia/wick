import { Button, Inline } from "../../components/primitives";
import type {
  EvidenceExplorerFilterOptions,
  EvidenceExplorerFilters,
} from "../../viewmodels";

export type EvidenceFiltersProps = {
  options: EvidenceExplorerFilterOptions;
  filters: EvidenceExplorerFilters;
  onChange: (filters: EvidenceExplorerFilters) => void;
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
    <div className="wick-evidence-filter">
      <label className="wick-evidence-field-label" htmlFor={id}>
        {label}
      </label>
      <select
        id={id}
        className="wick-evidence-select"
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

export function EvidenceFilters({
  options,
  filters,
  onChange,
  onClear,
}: EvidenceFiltersProps) {
  const hasActive =
    Boolean(filters.evidenceClass) ||
    Boolean(filters.release) ||
    Boolean(filters.status) ||
    Boolean(filters.dataOrigin) ||
    Boolean(filters.scientificStage) ||
    Boolean(filters.staleness);

  return (
    <div className="wick-evidence-filters" data-testid="evidence-filters">
      <Inline className="wick-evidence-filters__row">
        <FilterSelect
          id="evidence-filter-class"
          label="Classe"
          value={filters.evidenceClass}
          options={options.evidenceClasses}
          onValueChange={(evidenceClass) =>
            onChange({ ...filters, evidenceClass })
          }
          testId="evidence-filter-class"
        />
        <FilterSelect
          id="evidence-filter-release"
          label="Release"
          value={filters.release}
          options={options.releases}
          onValueChange={(release) => onChange({ ...filters, release })}
          testId="evidence-filter-release"
        />
        <FilterSelect
          id="evidence-filter-status"
          label="Status"
          value={filters.status}
          options={options.statuses}
          onValueChange={(status) => onChange({ ...filters, status })}
          testId="evidence-filter-status"
        />
        <FilterSelect
          id="evidence-filter-origin"
          label="Origem"
          value={filters.dataOrigin}
          options={options.dataOrigins}
          onValueChange={(dataOrigin) => onChange({ ...filters, dataOrigin })}
          testId="evidence-filter-origin"
        />
        <FilterSelect
          id="evidence-filter-stage"
          label="Estágio científico"
          value={filters.scientificStage}
          options={options.scientificStages}
          onValueChange={(scientificStage) =>
            onChange({ ...filters, scientificStage })
          }
          testId="evidence-filter-stage"
        />
        <FilterSelect
          id="evidence-filter-staleness"
          label="Atualidade"
          value={filters.staleness}
          options={options.stalenessValues}
          onValueChange={(staleness) => onChange({ ...filters, staleness })}
          testId="evidence-filter-staleness"
        />
      </Inline>
      <div className="wick-evidence-filters__actions">
        <Button
          variant="secondary"
          size="sm"
          type="button"
          onClick={onClear}
          disabled={!hasActive}
          data-testid="evidence-filters-clear"
        >
          Limpar filtros
        </Button>
      </div>
    </div>
  );
}
