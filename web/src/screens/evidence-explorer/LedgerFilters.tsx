import { Button, Inline } from "../../components/primitives";
import type {
  GovernedDecisionLedgerFilterOptions,
  GovernedDecisionLedgerFilters,
} from "../../viewmodels";

export type LedgerFiltersProps = {
  options: GovernedDecisionLedgerFilterOptions;
  filters: GovernedDecisionLedgerFilters;
  onChange: (filters: GovernedDecisionLedgerFilters) => void;
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

export function LedgerFilters({
  options,
  filters,
  onChange,
  onClear,
}: LedgerFiltersProps) {
  const hasActive =
    Boolean(filters.disposition) ||
    Boolean(filters.domain) ||
    Boolean(filters.release) ||
    Boolean(filters.decisionType) ||
    Boolean(filters.reassessmentAvailability);

  return (
    <div className="wick-ledger-filters" data-testid="ledger-filters">
      <Inline className="wick-evidence-filters__row">
        <FilterSelect
          id="ledger-filter-disposition"
          label="Disposição"
          value={filters.disposition}
          options={options.dispositions}
          onValueChange={(disposition) => onChange({ ...filters, disposition })}
          testId="ledger-filter-disposition"
        />
        <FilterSelect
          id="ledger-filter-domain"
          label="Domínio"
          value={filters.domain}
          options={options.domains}
          onValueChange={(domain) => onChange({ ...filters, domain })}
          testId="ledger-filter-domain"
        />
        <FilterSelect
          id="ledger-filter-release"
          label="Release"
          value={filters.release}
          options={options.releases}
          onValueChange={(release) => onChange({ ...filters, release })}
          testId="ledger-filter-release"
        />
        <FilterSelect
          id="ledger-filter-decision-type"
          label="Tipo de decisão"
          value={filters.decisionType}
          options={options.decisionTypes}
          onValueChange={(decisionType) =>
            onChange({ ...filters, decisionType })
          }
          testId="ledger-filter-decision-type"
        />
        <FilterSelect
          id="ledger-filter-reassessment"
          label="Reavaliação"
          value={filters.reassessmentAvailability}
          options={options.reassessmentAvailability}
          onValueChange={(reassessmentAvailability) =>
            onChange({ ...filters, reassessmentAvailability })
          }
          testId="ledger-filter-reassessment"
        />
      </Inline>
      {hasActive ? (
        <div className="wick-ledger-filters__clear">
          <Button
            type="button"
            variant="secondary"
            onClick={onClear}
            data-testid="ledger-filters-clear"
          >
            Limpar filtros do livro
          </Button>
        </div>
      ) : null}
    </div>
  );
}
