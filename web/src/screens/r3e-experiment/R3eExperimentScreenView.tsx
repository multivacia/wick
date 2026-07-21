import { PageHeader, Section, Stack } from "../../components/primitives";
import type { R3eExperimentScreenData } from "./loadR3eExperimentScreenData";
import { BootstrapAndFDRExplanation } from "./BootstrapAndFDRExplanation";
import { CurrentScientificState } from "./CurrentScientificState";
import { DeltaCandleExplanation } from "./DeltaCandleExplanation";
import { EvidenceReferences } from "./EvidenceReferences";
import { ExperimentPurpose } from "./ExperimentPurpose";
import { FutureUnseenGate } from "./FutureUnseenGate";
import { HypothesisSummary } from "./HypothesisSummary";
import { LeakageProtection } from "./LeakageProtection";
import { M0M5Explanation } from "./M0M5Explanation";
import { ModelFamilyComparison } from "./ModelFamilyComparison";
import { NextSafeScientificAction } from "./NextSafeScientificAction";
import { PartialUnknownState } from "./PartialUnknownState";
import { ProtocolSummary } from "./ProtocolSummary";
import { R3DAndR3EDistinction } from "./R3DAndR3EDistinction";
import { SyntheticDataNotice } from "./SyntheticDataNotice";
import { TemporalValidationSummary } from "./TemporalValidationSummary";
import { WhatIsKnown } from "./WhatIsKnown";
import { WhatIsNotKnown } from "./WhatIsNotKnown";
import "./r3e-experiment.css";

export type R3eExperimentScreenViewProps = {
  data: R3eExperimentScreenData;
};

/**
 * Presentational Experimento R3E screen — accepts assembled fixture data.
 */
export function R3eExperimentScreenView({
  data,
}: R3eExperimentScreenViewProps) {
  const { r3eExperiment, metadata } = data;

  return (
    <Stack
      className="wick-r3e-experiment-screen"
      data-testid="r3e-experiment-screen"
    >
      <PageHeader
        eyebrow="Experimentos Wick"
        title="Experimento R3E"
        description="Explicação governada do experimento contextual R3E — somente leitura, fixture sintético, sem validação futura nem recomendações de trading."
      />

      <SyntheticDataNotice metadata={metadata} />

      <Section title="Contexto" className="wick-r3e-section">
        <div className="wick-r3e-grid">
          <ExperimentPurpose r3eExperiment={r3eExperiment} />
          <HypothesisSummary r3eExperiment={r3eExperiment} />
          <R3DAndR3EDistinction r3eExperiment={r3eExperiment} />
          <ProtocolSummary r3eExperiment={r3eExperiment} />
        </div>
      </Section>

      <Section title="Modelos e protocolo" className="wick-r3e-section">
        <div className="wick-r3e-grid">
          <ModelFamilyComparison r3eExperiment={r3eExperiment} />
          <DeltaCandleExplanation r3eExperiment={r3eExperiment} />
        </div>
        <M0M5Explanation r3eExperiment={r3eExperiment} />
      </Section>

      <Section title="Proteções metodológicas" className="wick-r3e-section">
        <div className="wick-r3e-grid">
          <TemporalValidationSummary r3eExperiment={r3eExperiment} />
          <LeakageProtection r3eExperiment={r3eExperiment} />
          <BootstrapAndFDRExplanation r3eExperiment={r3eExperiment} />
        </div>
      </Section>

      <Section title="Estado e gate" className="wick-r3e-section">
        <div className="wick-r3e-grid">
          <CurrentScientificState r3eExperiment={r3eExperiment} />
          <FutureUnseenGate r3eExperiment={r3eExperiment} />
          <WhatIsKnown r3eExperiment={r3eExperiment} />
          <WhatIsNotKnown r3eExperiment={r3eExperiment} />
          <NextSafeScientificAction r3eExperiment={r3eExperiment} />
          <EvidenceReferences r3eExperiment={r3eExperiment} />
        </div>
      </Section>

      <PartialUnknownState r3eExperiment={r3eExperiment} />
    </Stack>
  );
}
