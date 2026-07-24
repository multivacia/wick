import { Alert, Section } from "../../components/primitives";
import {
  buildGovernedDecisionLedgerViewModel,
  type GovernedDecisionLedgerCriteria,
  type GovernedDecisionLedgerFilters,
} from "../../viewmodels";
import type { GovernedDecisionLedgerDomainInput } from "../../viewmodels";
import { LedgerFilters } from "./LedgerFilters";
import { LedgerDetail, LedgerList } from "./LedgerList";

export type GovernedDecisionLedgerSectionProps = {
  domain: GovernedDecisionLedgerDomainInput;
  criteria: GovernedDecisionLedgerCriteria;
  onFiltersChange: (filters: GovernedDecisionLedgerFilters) => void;
  onClearFilters: () => void;
  onSelectDecision: (decisionId: string) => void;
  onClearSelection: () => void;
};

/**
 * Governed decision ledger — section above the Evidence catalog.
 * Fixture-backed, read-only, no new route.
 */
export function GovernedDecisionLedgerSection({
  domain,
  criteria,
  onFiltersChange,
  onClearFilters,
  onSelectDecision,
  onClearSelection,
}: GovernedDecisionLedgerSectionProps) {
  const vm = buildGovernedDecisionLedgerViewModel(domain, criteria);
  const selectedId = criteria.selectedDecisionId ?? null;

  return (
    <Section
      title={vm.sectionTitle}
      className="wick-evidence-section wick-ledger-section"
      data-testid="governed-decision-ledger-section"
    >
      <p className="wick-evidence-primary">{vm.sectionDescription}</p>
      <Alert
        tone="informational"
        title="Divulgação ilustrativa"
        data-testid="ledger-illustrative-disclosure"
      >
        <p className="wick-evidence-primary">{vm.illustrativeDisclosure}</p>
        <p className="wick-evidence-muted">{vm.freshnessDisclosure}</p>
        <p className="wick-evidence-muted">
          Curadoria: catalog_curated_at {vm.catalogCuratedAtDisplay};{" "}
          fixture_authored_at {vm.fixtureAuthoredAtDisplay}; versão do fixture{" "}
          {vm.fixtureVersion}.
        </p>
      </Alert>

      {vm.staleFixtureState && vm.staleDisclosure ? (
        <Alert
          tone="attention"
          title="Fixture/catálogo desatualizado"
          data-testid="ledger-stale-state"
        >
          <p className="wick-evidence-primary">{vm.staleDisclosure}</p>
        </Alert>
      ) : null}

      {vm.unknownStateNotice ? (
        <Alert
          tone="informational"
          title="Estados desconhecidos"
          data-testid="ledger-unknown-state"
        >
          <p className="wick-evidence-primary">{vm.unknownStateNotice}</p>
        </Alert>
      ) : null}

      <div
        className="wick-ledger-summary"
        data-testid="ledger-summary-counts"
        aria-label="Contagens do livro de decisões"
      >
        <p className="wick-evidence-muted">
          Aceitas (governança/UX, ≠ estratégia aprovada):{" "}
          <strong data-testid="ledger-count-accepted">
            {vm.counts.acceptedCount}
          </strong>
        </p>
        <p className="wick-evidence-muted">
          Bloqueadas (≠ falhas de sistema):{" "}
          <strong data-testid="ledger-count-blocked">
            {vm.counts.blockedCount}
          </strong>
        </p>
        <p className="wick-evidence-muted">
          Com gatilho de reavaliação (≠ ação automática):{" "}
          <strong data-testid="ledger-count-triggers">
            {vm.counts.triggerCount}
          </strong>
        </p>
        <p className="wick-evidence-muted">
          Disposição desconhecida (≠ zero inventado):{" "}
          <strong data-testid="ledger-count-unknown">
            {vm.counts.unknownDispositionCount === 0
              ? "nenhuma"
              : String(vm.counts.unknownDispositionCount)}
          </strong>
        </p>
      </div>

      <LedgerFilters
        options={vm.filterOptions}
        filters={criteria.filters}
        onChange={onFiltersChange}
        onClear={onClearFilters}
      />

      <div className="wick-ledger-split" data-testid="ledger-split">
        <LedgerList
          records={vm.records}
          selectedDecisionId={selectedId}
          resultCount={vm.counts.resultCount}
          totalCount={vm.counts.totalCount}
          emptyState={vm.emptyState}
          noResultsState={vm.noResultsState}
          onSelect={onSelectDecision}
          onClearFilters={onClearFilters}
        />
        <LedgerDetail
          record={vm.selectedRecord}
          onClearSelection={onClearSelection}
        />
      </div>

      <details className="wick-ledger-safeguards">
        <summary>Salvaguardas semânticas</summary>
        <ul>
          {vm.semanticSafeguards.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </details>
    </Section>
  );
}
