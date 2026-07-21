import { useState } from "react";
import { useSearchParams } from "react-router-dom";
import {
  clearEvidenceFilters,
  parseEvidenceIdParam,
  type EvidenceExplorerCriteria,
  type EvidenceExplorerFilters,
} from "../../viewmodels";
import { EvidenceExplorerScreenView } from "./EvidenceExplorerScreenView";
import { loadEvidenceExplorerScreenData } from "./loadEvidenceExplorerScreenData";

/**
 * Evidências — Evidence Explorer product screen (UX-R2).
 * Read-only, fixture-backed curated catalog. No filesystem / downloads.
 * Deep-link via ?evidenceId= query param.
 */
export function EvidenceExplorerScreen() {
  const data = loadEvidenceExplorerScreenData();
  const [searchParams, setSearchParams] = useSearchParams();
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<EvidenceExplorerFilters>(
    clearEvidenceFilters(),
  );

  const selectedEvidenceId = parseEvidenceIdParam(searchParams);

  const criteria: EvidenceExplorerCriteria = {
    searchQuery,
    filters,
    selectedEvidenceId,
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
      onSearchQueryChange={setSearchQuery}
      onFiltersChange={setFilters}
      onClearFilters={() => setFilters(clearEvidenceFilters())}
      onSelectEvidence={handleSelectEvidence}
      onClearSelection={handleClearSelection}
    />
  );
}
