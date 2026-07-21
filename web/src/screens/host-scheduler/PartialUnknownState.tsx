import { Alert } from "../../components/primitives";
import type { HostSchedulerViewModel } from "../../viewmodels";

export type PartialUnknownStateProps = {
  hostScheduler: HostSchedulerViewModel;
};

/**
 * Surface unknown / partial / missing without equating to fault or offline.
 */
export function PartialUnknownState({
  hostScheduler,
}: PartialUnknownStateProps) {
  const unknownHost =
    hostScheduler.hostDiscoveryState === "unknown" ||
    hostScheduler.hostDiscoveryState === "not_available";
  const unknownScheduler =
    hostScheduler.schedulerState === "unknown" ||
    hostScheduler.schedulerState === "not_available";
  const nullPresence = hostScheduler.persistentHostPresent === null;
  const nullRegistered = hostScheduler.schedulerRegistered === null;
  const nullActive = hostScheduler.schedulerActive === null;
  const debtUnknown = hostScheduler.operationalDebt === "unknown";
  const tsMissing = hostScheduler.lastCycleAt.availability !== "available";

  const show =
    unknownHost ||
    unknownScheduler ||
    nullPresence ||
    nullRegistered ||
    nullActive ||
    debtUnknown ||
    tsMissing;

  if (!show) {
    return null;
  }

  return (
    <Alert
      tone="informational"
      title="Estado parcial ou desconhecido"
      data-testid="host-scheduler-partial-unknown"
    >
      <p className="wick-host-scheduler-primary">
        Parte do estado de host/agendador está ausente, desconhecida ou
        indisponível neste ViewModel.
      </p>
      <p className="wick-host-scheduler-muted">
        UNKNOWN ≠ OFFLINE · UNKNOWN ≠ FAULT · MISSING ≠ FALSE · MISSING ≠ ZERO.
        Valores ausentes permanecem indisponíveis.
      </p>
    </Alert>
  );
}
