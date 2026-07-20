import { PageHeader, Section, Stack } from "../../components/primitives";
import type { ReadinessScreenData } from "./loadReadinessScreenData";
import { BlockingReason } from "./BlockingReason";
import { CollectionState } from "./CollectionState";
import { EffectPeekingState } from "./EffectPeekingState";
import { EvidenceReference } from "./EvidenceReference";
import { NextSafeAction } from "./NextSafeAction";
import { PartialUnknownState } from "./PartialUnknownState";
import { ReadinessStatusCard } from "./ReadinessStatusCard";
import { SyntheticDataNotice } from "./SyntheticDataNotice";
import { ValidationExecutionState } from "./ValidationExecutionState";
import { WindowProgress } from "./WindowProgress";
import "./readiness.css";

export type ReadinessScreenViewProps = {
  data: ReadinessScreenData;
};

/**
 * Presentational Readiness screen — accepts assembled fixture data.
 */
export function ReadinessScreenView({ data }: ReadinessScreenViewProps) {
  const { readiness, metadata } = data;

  return (
    <Stack className="wick-readiness-screen" data-testid="readiness-screen">
      <PageHeader
        eyebrow="Operação Wick"
        title="Prontidão"
        description="A validação futura já pode ser considerada? Janela observada, motivos de bloqueio e próximos passos seguros — somente leitura."
      />

      <SyntheticDataNotice metadata={metadata} />

      <Section title="Estado" className="wick-readiness-section">
        <ReadinessStatusCard readiness={readiness} />
      </Section>

      <Section title="Janela futura" className="wick-readiness-section">
        <WindowProgress readiness={readiness} />
      </Section>

      <Section title="Bloqueios e governança" className="wick-readiness-section">
        <div className="wick-readiness-grid">
          <BlockingReason readiness={readiness} />
          <ValidationExecutionState readiness={readiness} />
          <EffectPeekingState readiness={readiness} />
          <CollectionState readiness={readiness} />
        </div>
      </Section>

      <Section title="Próximos passos" className="wick-readiness-section">
        <NextSafeAction readiness={readiness} />
        <EvidenceReference readiness={readiness} />
      </Section>

      <PartialUnknownState readiness={readiness} />
    </Stack>
  );
}
