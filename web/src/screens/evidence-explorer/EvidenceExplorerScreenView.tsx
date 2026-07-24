import { PageHeader, Section, Stack } from "../../components/primitives";
import {
  buildEvidenceExplorerViewModel,
  type EvidenceExplorerCriteria,
  type EvidenceExplorerFilters,
  type EvidenceExplorerViewModel,
  type GovernedDecisionLedgerCriteria,
  type GovernedDecisionLedgerFilters,
} from "../../viewmodels";
import type { EvidenceExplorerScreenData } from "./loadEvidenceExplorerScreenData";
import { CatalogDisclosure } from "./CatalogDisclosure";
import { EvidenceDetail } from "./EvidenceDetail";
import { EvidenceFilters } from "./EvidenceFilters";
import { EvidenceList } from "./EvidenceList";
import { EvidenceSearch } from "./EvidenceSearch";
import { GovernedDecisionLedgerSection } from "./GovernedDecisionLedgerSection";
import { SafetyNotices } from "./SafetyNotices";
import { SyntheticDataNotice } from "./SyntheticDataNotice";
import "./evidence-explorer.css";

export type EvidenceExplorerScreenViewProps = {
  data: EvidenceExplorerScreenData;
  criteria: EvidenceExplorerCriteria;
  ledgerCriteria: GovernedDecisionLedgerCriteria;
  onSearchQueryChange: (searchQuery: string) => void;
  onFiltersChange: (filters: EvidenceExplorerFilters) => void;
  onClearFilters: () => void;
  onSelectEvidence: (evidenceId: string) => void;
  onClearSelection: () => void;
  onLedgerFiltersChange: (filters: GovernedDecisionLedgerFilters) => void;
  onClearLedgerFilters: () => void;
  onSelectDecision: (decisionId: string) => void;
  onClearDecisionSelection: () => void;
};

/**
 * Presentational Evidence Explorer — search/filter/selection driven by parent.
 * Governed decision ledger section renders above catalog search/filters.
 */
export function EvidenceExplorerScreenView({
  data,
  criteria,
  ledgerCriteria,
  onSearchQueryChange,
  onFiltersChange,
  onClearFilters,
  onSelectEvidence,
  onClearSelection,
  onLedgerFiltersChange,
  onClearLedgerFilters,
  onSelectDecision,
  onClearDecisionSelection,
}: EvidenceExplorerScreenViewProps) {
  const vm: EvidenceExplorerViewModel = buildEvidenceExplorerViewModel(
    data.catalog,
    criteria,
  );
  const hasDetail =
    vm.selectedDetail !== null || vm.invalidSelectionFallback;
  const showListPane = !hasDetail;

  return (
    <Stack
      className="wick-evidence-explorer-screen"
      data-testid="evidence-explorer-screen"
    >
      <PageHeader
        eyebrow="Governança Wick"
        title={vm.pageTitle}
        description={vm.pageDescription}
      />

      <SyntheticDataNotice metadata={data.metadata} />
      <CatalogDisclosure disclosure={vm.catalogDisclosure} />
      <SafetyNotices notices={vm.safetyNotices} />

      <GovernedDecisionLedgerSection
        domain={data.ledger}
        criteria={ledgerCriteria}
        onFiltersChange={onLedgerFiltersChange}
        onClearFilters={onClearLedgerFilters}
        onSelectDecision={onSelectDecision}
        onClearSelection={onClearDecisionSelection}
      />

      <Section title="Busca e filtros" className="wick-evidence-section">
        <EvidenceSearch
          value={criteria.searchQuery}
          onChange={onSearchQueryChange}
        />
        <EvidenceFilters
          options={vm.filterOptions}
          filters={criteria.filters}
          onChange={onFiltersChange}
          onClear={onClearFilters}
        />
      </Section>

      <Section title="Catálogo" className="wick-evidence-section">
        <div
          className={[
            "wick-evidence-split",
            hasDetail ? "wick-evidence-split--detail-open" : "",
          ]
            .filter(Boolean)
            .join(" ")}
          data-testid="evidence-split"
        >
          <div
            className={[
              "wick-evidence-split__list",
              showListPane ? "" : "wick-evidence-split__list--collapsed",
            ]
              .filter(Boolean)
              .join(" ")}
            data-testid="evidence-split-list"
          >
            <EvidenceList
              items={vm.summaries}
              selectedEvidenceId={criteria.selectedEvidenceId ?? null}
              onSelect={onSelectEvidence}
              resultCount={vm.resultCount}
              emptyState={vm.emptyState}
              noResultsState={vm.noResultsState}
            />
          </div>
          <div
            className="wick-evidence-split__detail"
            data-testid="evidence-split-detail"
          >
            <EvidenceDetail
              detail={vm.selectedDetail}
              sourcePathDisclaimer={vm.sourcePathDisclaimer}
              invalidSelectionFallback={vm.invalidSelectionFallback}
              onClearSelection={onClearSelection}
            />
          </div>
        </div>
      </Section>
    </Stack>
  );
}
