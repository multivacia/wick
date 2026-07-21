import { PageHeader, Section, Stack } from "../../components/primitives";
import type { HostSchedulerScreenData } from "./loadHostSchedulerScreenData";
import { BlockingReason } from "./BlockingReason";
import { CadenceState } from "./CadenceState";
import { EvidenceReference } from "./EvidenceReference";
import { HostDiscoveryStatus } from "./HostDiscoveryStatus";
import { KnownEnvironmentDetails } from "./KnownEnvironmentDetails";
import { LastKnownRun } from "./LastKnownRun";
import { NextExpectedRun } from "./NextExpectedRun";
import { NextSafeHumanAction } from "./NextSafeHumanAction";
import { OperationalDebtNotice } from "./OperationalDebtNotice";
import { PartialUnknownState } from "./PartialUnknownState";
import { SchedulerStatus } from "./SchedulerStatus";
import { SyntheticDataNotice } from "./SyntheticDataNotice";
import "./host-scheduler.css";

export type HostSchedulerScreenViewProps = {
  data: HostSchedulerScreenData;
};

/**
 * Presentational Host e Automação screen — accepts assembled fixture data.
 */
export function HostSchedulerScreenView({
  data,
}: HostSchedulerScreenViewProps) {
  const { hostScheduler, metadata } = data;

  return (
    <Stack
      className="wick-host-scheduler-screen"
      data-testid="host-scheduler-screen"
    >
      <PageHeader
        eyebrow="Operação Wick"
        title="Host e Automação"
        description="Estado conhecido de descoberta de host e agendamento — somente leitura, sem ativação e sem evidência operacional real."
      />

      <SyntheticDataNotice metadata={metadata} />

      <Section title="Host e débito" className="wick-host-scheduler-section">
        <div className="wick-host-scheduler-grid">
          <HostDiscoveryStatus hostScheduler={hostScheduler} />
          <OperationalDebtNotice hostScheduler={hostScheduler} />
        </div>
      </Section>

      <Section title="Agendador" className="wick-host-scheduler-section">
        <SchedulerStatus hostScheduler={hostScheduler} />
      </Section>

      <Section
        title="Ambiente e cadência"
        className="wick-host-scheduler-section"
      >
        <div className="wick-host-scheduler-grid">
          <KnownEnvironmentDetails />
          <CadenceState />
          <LastKnownRun hostScheduler={hostScheduler} />
          <NextExpectedRun />
        </div>
      </Section>

      <Section
        title="Bloqueios e próximos passos"
        className="wick-host-scheduler-section"
      >
        <div className="wick-host-scheduler-grid">
          <BlockingReason hostScheduler={hostScheduler} />
          <NextSafeHumanAction hostScheduler={hostScheduler} />
          <EvidenceReference hostScheduler={hostScheduler} />
        </div>
      </Section>

      <PartialUnknownState hostScheduler={hostScheduler} />
    </Stack>
  );
}
