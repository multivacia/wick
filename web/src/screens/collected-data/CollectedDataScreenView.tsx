import { PageHeader, Section, Stack } from "../../components/primitives";
import {
  buildCollectionDataQualityViewModel,
  type CollectionDataQualityCriteria,
  type CollectionDataQualityFilters,
  type CollectionDataQualityViewModel,
} from "../../viewmodels";
import type { CollectedDataScreenData } from "./loadCollectedDataScreenData";
import { CrossNavLinks } from "./CrossNavLinks";
import { NextSafeAction } from "./NextSafeAction";
import { QualitySummary } from "./QualitySummary";
import { SeriesFilters } from "./SeriesFilters";
import { SeriesList } from "./SeriesList";
import { SyntheticDataNotice } from "./SyntheticDataNotice";
import "./collected-data.css";

export type CollectedDataScreenViewProps = {
  data: CollectedDataScreenData;
  criteria: CollectionDataQualityCriteria;
  onFiltersChange: (filters: CollectionDataQualityFilters) => void;
  onClearFilters: () => void;
};

/**
 * Presentational Dados Coletados — filters driven by parent.
 */
export function CollectedDataScreenView({
  data,
  criteria,
  onFiltersChange,
  onClearFilters,
}: CollectedDataScreenViewProps) {
  const vm: CollectionDataQualityViewModel = buildCollectionDataQualityViewModel(
    data.domain,
    criteria,
    { nowIso: data.nowIso },
  );

  return (
    <Stack
      className="wick-collected-data-screen"
      data-testid="collected-data-screen"
    >
      <PageHeader
        eyebrow="Operação Wick"
        title={vm.pageTitle}
        description={vm.pageDescription}
      />

      <SyntheticDataNotice metadata={data.metadata} />
      <QualitySummary vm={vm} />

      <Section title="Filtros" className="wick-collected-data-section">
        <SeriesFilters
          options={vm.filterOptions}
          filters={criteria.filters}
          onChange={onFiltersChange}
          onClear={onClearFilters}
        />
      </Section>

      <Section title="Séries coletadas" className="wick-collected-data-section">
        <SeriesList
          series={vm.series}
          resultCount={vm.resultCount}
          totalSeriesCount={vm.totalSeriesCount}
          emptyState={vm.emptyState}
          noResultsState={vm.noResultsState}
          onClearFilters={onClearFilters}
        />
      </Section>

      <NextSafeAction hint={vm.nextSafeAction} />
      <CrossNavLinks relatedEvidence={vm.relatedEvidence} />
    </Stack>
  );
}
