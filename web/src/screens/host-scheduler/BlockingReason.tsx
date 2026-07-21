import { Card } from "../../components/primitives";
import type { HostSchedulerViewModel } from "../../viewmodels";

export type BlockingReasonProps = {
  hostScheduler: HostSchedulerViewModel;
};

export function BlockingReason({ hostScheduler }: BlockingReasonProps) {
  const blockers = hostScheduler.blockers;
  const hostCodes = hostScheduler.hostPresentation.reasonCodes;
  const schedCodes = hostScheduler.schedulerPresentation.reasonCodes;

  return (
    <Card
      className="wick-host-scheduler-card"
      data-testid="host-scheduler-blocking-reason"
    >
      <h2 className="wick-host-scheduler-card-title">Motivos de bloqueio</h2>
      {blockers.length === 0 &&
      hostCodes.length === 0 &&
      schedCodes.length === 0 ? (
        <p
          className="wick-host-scheduler-primary"
          data-testid="host-scheduler-blocking-none"
        >
          Nenhum bloqueio fornecido neste ViewModel.
        </p>
      ) : (
        <ul
          className="wick-host-scheduler-list"
          data-testid="host-scheduler-blocking-list"
        >
          {blockers.map((b) => (
            <li
              key={`blocker:${b.reasonCode}:${b.plainLanguage}`}
              data-testid={`host-scheduler-blocking-${b.reasonCode}`}
            >
              <p className="wick-host-scheduler-primary">{b.plainLanguage}</p>
              <p className="wick-host-scheduler-technical">
                Código: <code>{b.reasonCode}</code>
              </p>
            </li>
          ))}
          {hostCodes.map((code) => (
            <li key={`host:${code}`} data-testid={`host-scheduler-blocking-${code}`}>
              <p className="wick-host-scheduler-primary">
                {hostScheduler.hostPresentation.primaryMessage.plainLanguage}
              </p>
              <p className="wick-host-scheduler-technical">
                Código: <code>{code}</code>
              </p>
            </li>
          ))}
          {schedCodes.map((code) => (
            <li
              key={`sched:${code}`}
              data-testid={`host-scheduler-blocking-${code}`}
            >
              <p className="wick-host-scheduler-primary">
                {hostScheduler.schedulerPresentation.primaryMessage.plainLanguage}
              </p>
              <p className="wick-host-scheduler-technical">
                Código: <code>{code}</code>
              </p>
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
}
