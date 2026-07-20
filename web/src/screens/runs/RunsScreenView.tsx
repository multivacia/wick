import { PageHeader, Section, Stack } from "../../components/primitives";
import type { RunsScreenData } from "./loadRunsScreenData";
import { EmptyRunsState } from "./EmptyRunsState";
import { PartialUnknownState } from "./PartialUnknownState";
import { RunsCollection } from "./RunsCollection";
import { RunsSummary } from "./RunsSummary";
import { SyntheticDataNotice } from "./SyntheticDataNotice";
import "./runs.css";

export type RunsScreenViewProps = {
  data: RunsScreenData;
};

/**
 * Presentational Runs screen — accepts assembled fixture data.
 */
export function RunsScreenView({ data }: RunsScreenViewProps) {
  const { runs, metadata } = data;
  const isEmpty = runs.runs.length === 0;

  return (
    <Stack className="wick-runs-screen" data-testid="runs-screen">
      <PageHeader
        eyebrow="Operação Wick"
        title="Execuções"
        description="Ciclos de coleta com run_id, status, tempos, contagens e evidências — somente leitura."
      />

      <SyntheticDataNotice metadata={metadata} />

      <Section title="Resumo" className="wick-runs-section">
        <RunsSummary runs={runs} />
      </Section>

      {isEmpty ? (
        <EmptyRunsState
          technicalCode={runs.primaryMessage.technicalCode}
          plainLanguage={runs.primaryMessage.plainLanguage}
        />
      ) : (
        <RunsCollection runs={runs.runs} />
      )}

      <PartialUnknownState
        runs={runs.runs}
        summaryTechnicalCode={runs.primaryMessage.technicalCode}
      />
    </Stack>
  );
}
