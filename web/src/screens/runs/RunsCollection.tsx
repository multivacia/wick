import { Section } from "../../components/primitives";
import type { RunViewModel } from "../../viewmodels";
import { RunCard } from "./RunCard";
import { RunsTable } from "./RunsTable";

export type RunsCollectionProps = {
  runs: RunViewModel[];
};

export function RunsCollection({ runs }: RunsCollectionProps) {
  if (runs.length === 0) {
    return null;
  }

  return (
    <Section title="Coleção de execuções" data-testid="runs-collection">
      <div className="wick-runs-collection-desktop">
        <RunsTable runs={runs} />
      </div>
      <div className="wick-runs-collection-mobile" data-testid="runs-cards">
        {runs.map((run) => (
          <RunCard key={run.runId ?? "sem-id"} run={run} />
        ))}
      </div>
    </Section>
  );
}
