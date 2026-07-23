import { Card, PageHeader, Section, Stack } from "../../components/primitives";
import { RelatedProductLinks } from "../shared/RelatedProductLinks";
import { COLLECTED_DATA_RELATED_LINK } from "../shared/collectedDataRelatedLink";
import { BlockerList } from "./BlockerList";
import { EvidenceSummary } from "./EvidenceSummary";
import { loadOverviewScreenData } from "./loadOverviewScreenData";
import { NextSafeActionPanel } from "./NextSafeActionPanel";
import { OperationalStateCard } from "./OperationalStateCard";
import { SummaryCard } from "./SummaryCard";
import { SyntheticDataNotice } from "./SyntheticDataNotice";
import "./overview.css";

/**
 * Visão Geral — first product screen (I6E).
 * Read-only, fixture-backed, advisory next action only.
 */
export function OverviewScreen() {
  const { overview, metadata } = loadOverviewScreenData();

  return (
    <Stack className="wick-overview-screen" data-testid="overview-screen">
      <PageHeader
        eyebrow="Operação Wick"
        title="Visão Geral"
        description="Resumo do estado operacional em linguagem clara, com evidência técnica em segundo plano."
      />

      <SyntheticDataNotice metadata={metadata} />

      <Section title="Estado operacional geral" className="wick-overview-section">
        <OperationalStateCard
          explanation={overview.overallPresentation}
          scientificGate={overview.scientificGate}
          r4Status={overview.r4Status}
          r5Status={overview.r5Status}
        />
      </Section>

      <Section title="Resumos" className="wick-overview-section">
        <div className="wick-overview-summary-grid">
          <SummaryCard
            title="Coleta"
            block={overview.collectionSummary}
            testId="overview-collection-summary"
          />
          <SummaryCard
            title="Prontidão"
            block={overview.readinessSummary}
            testId="overview-readiness-summary"
          />
          <SummaryCard
            title="Host e agendador"
            block={overview.hostSchedulerSummary}
            testId="overview-host-scheduler-summary"
          />
        </div>
      </Section>

      <BlockerList blockers={overview.activeBlockers} />

      <Section title="Navegação relacionada" className="wick-overview-section">
        <Card
          className="wick-overview-related-card"
          data-testid="overview-related-nav"
        >
          <p className="wick-overview-muted">
            Completeness, gaps, duplicates e contagens de série ilustrativas
            estão em Dados Coletados — não neste resumo operacional.
            DATA_QUALITY ≠ SCIENTIFIC_APPROVAL.
          </p>
          <RelatedProductLinks
            items={[COLLECTED_DATA_RELATED_LINK]}
            testId="overview-related-product-links"
          />
        </Card>
      </Section>

      <EvidenceSummary
        evidence={overview.lastKnownEvidence}
        lastCompletedRun={overview.lastCompletedRun}
        lastFailedRun={overview.lastFailedRun}
      />

      <NextSafeActionPanel action={overview.nextSafeAction} />
    </Stack>
  );
}
