import { Section } from "../../components/primitives";
import type { RunViewModel } from "../../viewmodels";

export type PartialUnknownStateProps = {
  runs: RunViewModel[];
  summaryTechnicalCode: string | null;
};

/**
 * Surfaces partial / unknown supplied fields without inventing values.
 */
export function PartialUnknownState({
  runs,
  summaryTechnicalCode,
}: PartialUnknownStateProps) {
  const partialRuns = runs.filter((run) => {
    const missingMetric =
      run.acceptedCount.availability !== "available" ||
      run.rejectedCount.availability !== "available" ||
      run.storeAfterCount.availability !== "available";
    const missingTime =
      run.startedAt.availability !== "available" ||
      run.finishedAt.availability !== "available";
    return missingMetric || missingTime || run.state === "unknown";
  });

  if (partialRuns.length === 0 && summaryTechnicalCode !== "NO_RUNS") {
    return null;
  }

  return (
    <Section
      title="Dados parciais ou desconhecidos"
      data-testid="runs-partial-unknown"
    >
      <p className="wick-runs-primary">
        Alguns campos não foram fornecidos neste cenário. Valores ausentes
        permanecem indisponíveis — sem preenchimento artificial.
      </p>
      {summaryTechnicalCode ? (
        <p className="wick-runs-technical">
          Resumo técnico: <code>{summaryTechnicalCode}</code>
        </p>
      ) : null}
      {partialRuns.length > 0 ? (
        <ul className="wick-runs-evidence-list">
          {partialRuns.map((run) => (
            <li key={run.runId ?? "sem-id"}>
              <code>{run.runId ?? "sem-id"}</code>
              {" — "}
              estado <code>{run.state}</code>, apresentação{" "}
              <code>{run.presentation.status}</code>
            </li>
          ))}
        </ul>
      ) : (
        <p className="wick-runs-muted">
          Nenhuma linha parcial além do resumo agregado.
        </p>
      )}
    </Section>
  );
}
