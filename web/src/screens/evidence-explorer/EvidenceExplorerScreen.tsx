import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  clearEvidenceFilters,
  clearLedgerFilters,
  parseEvidenceIdParam,
  type EvidenceExplorerCriteria,
  type EvidenceExplorerFilters,
  type GovernedDecisionLedgerCriteria,
  type GovernedDecisionLedgerFilters,
} from "../../viewmodels";
import { EvidenceExplorerScreenView } from "./EvidenceExplorerScreenView";
import { loadEvidenceExplorerScreenData } from "./loadEvidenceExplorerScreenData";

/**
 * Evidências — Evidence Explorer product screen (UX-R2 + UX-R4 I2 ledger).
 * Read-only, fixture-backed curated catalog + governed decision ledger.
 * Deep-link via ?evidenceId= query param.
 */
export function EvidenceExplorerScreen() {
  const data = loadEvidenceExplorerScreenData();
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<EvidenceExplorerFilters>(
    clearEvidenceFilters(),
  );
  const [ledgerFilters, setLedgerFilters] =
    useState<GovernedDecisionLedgerFilters>(clearLedgerFilters());
  const [selectedDecisionId, setSelectedDecisionId] = useState<string | null>(
    null,
  );

  const selectedEvidenceId = parseEvidenceIdParam(searchParams);

  const criteria: EvidenceExplorerCriteria = {
    searchQuery,
    filters,
    selectedEvidenceId,
  };

  const ledgerCriteria: GovernedDecisionLedgerCriteria = {
    filters: ledgerFilters,
    selectedDecisionId,
  };

  function handleSelectEvidence(id: string) {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      next.set("evidenceId", id);
      return next;
    });
  }

  function handleClearSelection() {
    setSearchParams((prev) => {
      const next = new URLSearchParams(prev);
      next.delete("evidenceId");
      return next;
    });
  }

  return (
    <EvidenceExplorerScreenView
      data={data}
      criteria={criteria}
      ledgerCriteria={ledgerCriteria}
      onSearchQueryChange={setSearchQuery}
      onFiltersChange={setFilters}
      onClearFilters={() => setFilters(clearEvidenceFilters())}
      onSelectEvidence={handleSelectEvidence}
      onClearSelection={handleClearSelection}
      onLedgerFiltersChange={setLedgerFilters}
      onClearLedgerFilters={() => setLedgerFilters(clearLedgerFilters())}
      onSelectDecision={setSelectedDecisionId}
      onClearDecisionSelection={() => setSelectedDecisionId(null)}
    />
  );
}
