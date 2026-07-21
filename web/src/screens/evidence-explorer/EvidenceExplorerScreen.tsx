import { useState } from "react";
import {
  clearEvidenceFilters,
  type EvidenceExplorerCriteria,
  type EvidenceExplorerFilters,
} from "../../viewmodels";
import { EvidenceExplorerScreenView } from "./EvidenceExplorerScreenView";
import { loadEvidenceExplorerScreenData } from "./loadEvidenceExplorerScreenData";

/**
 * Evidências — Evidence Explorer product screen (UX-R2 I1).
 * Read-only, fixture-backed curated catalog. No filesystem / downloads.
 */
export function EvidenceExplorerScreen() {
  const data = loadEvidenceExplorerScreenData();
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState<EvidenceExplorerFilters>(
    clearEvidenceFilters(),
  );
  const [selectedEvidenceId, setSelectedEvidenceId] = useState<string | null>(
    null,
  );

  const criteria: EvidenceExplorerCriteria = {
    searchQuery,
    filters,
    selectedEvidenceId,
  };

  return (
    <EvidenceExplorerScreenView
      data={data}
      criteria={criteria}
      onSearchQueryChange={setSearchQuery}
      onFiltersChange={setFilters}
      onClearFilters={() => setFilters(clearEvidenceFilters())}
      onSelectEvidence={setSelectedEvidenceId}
      onClearSelection={() => setSelectedEvidenceId(null)}
    />
  );
}
