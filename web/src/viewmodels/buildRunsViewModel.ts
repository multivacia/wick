import type { RunsDomainInput, ViewModelClock } from "./inputs.js";
import type { RunsViewModel } from "./outputs.js";
import { buildRunViewModel, worstLifecycle } from "./buildRunViewModel.js";
import { mapDomainStateToPresentation } from "./status.js";
import { actionHint, deepFreeze } from "./helpers.js";

export function buildRunsViewModel(
  input: RunsDomainInput,
  clock: ViewModelClock | null = null,
): RunsViewModel {
  const runs = input.runs.map((run) => buildRunViewModel(run, clock));
  const aggregate = worstLifecycle(runs.map((r) => r.state));
  const mapping = mapDomainStateToPresentation(aggregate);

  let plainLanguage = "Nenhuma execução fornecida.";
  let technicalCode: string | null = "NO_RUNS";
  let hint = actionHint("no_action_available", "Nenhuma ação segura sugerida.");

  if (runs.length > 0) {
    technicalCode = aggregate.toUpperCase();
    if (aggregate === "fault") {
      plainLanguage = "Há execução com falha confirmada.";
      hint = actionHint(
        "investigate_failed_run",
        "Revisar evidência da execução com falha.",
      );
    } else if (aggregate === "in_progress") {
      plainLanguage = "Há execução em andamento.";
      hint = actionHint("monitor_collection", "Monitorar a coleta em andamento.");
    } else if (aggregate === "complete") {
      plainLanguage = "Execuções concluídas disponíveis.";
      hint = actionHint("continue_collecting", "Continuar a coleta conforme plano.");
    } else {
      plainLanguage = "Estado das execuções requer atenção operacional.";
      hint = actionHint(
        "review_blocker_evidence",
        "Revisar evidência dos bloqueios ou estados indeterminados.",
      );
    }
  }

  return deepFreeze({
    runs,
    summaryStatus: mapping.status,
    primaryMessage: { plainLanguage, technicalCode },
    actionHint: hint,
  });
}
