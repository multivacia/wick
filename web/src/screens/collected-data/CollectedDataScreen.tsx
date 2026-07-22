import { useState } from "react";
import {
  clearCollectionFilters,
  type CollectionDataQualityCriteria,
  type CollectionDataQualityFilters,
} from "../../viewmodels";
import { CollectedDataScreenView } from "./CollectedDataScreenView";
import { loadCollectedDataScreenData } from "./loadCollectedDataScreenData";

/**
 * Dados Coletados — Collection Data Quality product screen (UX-R3 I1).
 * Read-only, fixture-backed. No filesystem / network / validation / activation.
 */
export function CollectedDataScreen() {
  const data = loadCollectedDataScreenData();
  const [filters, setFilters] = useState<CollectionDataQualityFilters>(
    clearCollectionFilters(),
  );

  const criteria: CollectionDataQualityCriteria = { filters };

  return (
    <CollectedDataScreenView
      data={data}
      criteria={criteria}
      onFiltersChange={setFilters}
      onClearFilters={() => setFilters(clearCollectionFilters())}
    />
  );
}
