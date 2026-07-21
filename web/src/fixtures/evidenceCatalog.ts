/**
 * UX-R2 I1 — standalone curated Evidence Catalog fixture.
 * Synthetic/illustrative metadata only. No runtime FS / network / FU payloads.
 */

import { fixtureMetadata, type FixtureMetadata } from "./metadata.js";
import type {
  EvidenceCatalogEntryInput,
  EvidenceCatalogInput,
} from "../viewmodels/evidenceExplorerTypes.js";
import { assertValidEvidenceSourcePath } from "../viewmodels/evidenceSourcePath.js";
import {
  isEvidenceClass,
  isEvidenceDataOrigin,
  isEvidenceScientificStage,
  isEvidenceStaleness,
} from "../viewmodels/evidenceEnums.js";

export const EVIDENCE_CATALOG_FIXTURE_ID =
  "evidence_catalog_current_state_illustrative" as const;

export const EVIDENCE_CATALOG_NOW_ISO = "2026-07-21T12:00:00.000Z";

const ENTRIES: EvidenceCatalogEntryInput[] = [
  {
    evidenceId: "ev-ux-r1-formal-closure",
    title: "Encerramento formal e aceitação da release UX-R1",
    evidenceClass: "release_record",
    release: "UX-R1",
    increment: null,
    experimentId: null,
    status: "CLOSED_ACCEPTED",
    dataOrigin: "GOVERNANCE_RECORD",
    scientificStage: "NOT_APPLICABLE",
    createdAtOrUnknown: "2026-07-15T00:00:00.000Z",
    sourcePath:
      "docs/releases/UX-R1-FORMAL-RELEASE-CLOSURE-AND-ACCEPTANCE.md",
    summary:
      "Registro de governança do fechamento formal de UX-R1 no escopo fixture-backed read-only. Não altera estado científico de R3E nem autoriza dinheiro real.",
    supports: [
      "Confirma UX-R1 CLOSED_ACCEPTED_FIXTURE_BACKED_READ_ONLY",
      "Documenta aceite do escopo fixture-backed",
    ],
    limitations: [
      "Não prova vantagem preditiva",
      "Não desbloqueia R4/R5",
      "Não autoriza ordens reais",
    ],
    knownState: [
      "UX-R1 release fechada e aceita no escopo autorizado",
      "Telas operacionais UX-R1 são fixture-backed e somente leitura",
    ],
    unknownState: [
      "Nenhuma implicação científica futura é estabelecida por este registro",
    ],
    governanceFlags: [
      "UX_R1_RELEASE_STATUS=CLOSED",
      "UX_R1_RELEASE_ACCEPTANCE_STATUS=ACCEPTED",
    ],
    staleness: "HISTORICAL",
  },
  {
    evidenceId: "ev-ux-r2-discovery-assessment",
    title: "Avaliação de descoberta e escopo UX-R2",
    evidenceClass: "impact_assessment",
    release: "UX-R2",
    increment: null,
    experimentId: null,
    status: "SCOPE_RECOMMENDED",
    dataOrigin: "GOVERNANCE_RECORD",
    scientificStage: "NOT_APPLICABLE",
    createdAtOrUnknown: "2026-07-18T00:00:00.000Z",
    sourcePath:
      "docs/ai-impact/UX-R2-DISCOVERY-AND-SCOPE_IMPACT_ASSESSMENT.md",
    summary:
      "Avaliação de impacto da descoberta UX-R2 com direção recomendada D_EVIDENCE_AND_AUDIT_EXPLORER e primeiro incremento I1 Evidence Explorer.",
    supports: [
      "UX_R2_DISCOVERY_DECISION=SCOPE_RECOMMENDED",
      "Direção recomendada: Evidence and Audit Explorer",
    ],
    limitations: [
      "Assessment de escopo — não é implementação de produto",
      "Não autoriza integração com dados reais",
    ],
    knownState: [
      "Direção recomendada registrada",
      "Primeiro incremento recomendado: UX-R2 I1 Evidence Explorer",
    ],
    unknownState: [
      "Detalhes de implementação posteriores a I1 permanecem fora deste registro",
    ],
    governanceFlags: [
      "UX_R2_DISCOVERY_AND_SCOPE_STATUS=MERGED",
      "UX_R2_RECOMMENDED_DIRECTION=D_EVIDENCE_AND_AUDIT_EXPLORER",
    ],
    staleness: "CURRENT_AS_OF_FIXTURE",
  },
  {
    evidenceId: "ev-ux-r2-i1-authorization",
    title: "Avaliação de autorização UX-R2 I1 Evidence Explorer",
    evidenceClass: "impact_assessment",
    release: "UX-R2",
    increment: "I1",
    experimentId: null,
    status: "AUTHORIZED_WITH_CONDITIONS",
    dataOrigin: "GOVERNANCE_RECORD",
    scientificStage: "NOT_APPLICABLE",
    createdAtOrUnknown: "2026-07-20T00:00:00.000Z",
    sourcePath:
      "docs/ai-impact/UX-R2-I1-EVIDENCE-EXPLORER-AUTHORIZATION-ASSESSMENT_IMPACT_ASSESSMENT.md",
    summary:
      "Autorização com condições para o Evidence Explorer fixture-backed, somente leitura, catálogo curado, list+detail, sem acesso a repositório em runtime.",
    supports: [
      "UX_R2_I1_DECISION=AUTHORIZED_WITH_CONDITIONS",
      "Rota recomendada /governance/evidence",
      "Postura A_STATIC_FIXTURE_BACKED_EVIDENCE_CATALOG",
    ],
    limitations: [
      "Sem downloads, Markdown render ou links externos",
      "Sem payloads de future-unseen",
      "Sem mudança de estado científico",
    ],
    knownState: [
      "Boundary de implementação I1 documentado",
      "NAV_LABEL=Evidências autorizado como item de governança",
    ],
    unknownState: [
      "Integrações futuras (API, FS, build-time ingest) não autorizadas",
    ],
    governanceFlags: [
      "UX_R2_I1_STATUS=AUTHORIZATION_ASSESSMENT_MERGED",
      "RECOMMENDED_ROUTE=/governance/evidence",
    ],
    staleness: "CURRENT_AS_OF_FIXTURE",
  },
  {
    evidenceId: "ev-r3d-validation-conclusion",
    title: "Conclusão de validação R3D — sem edge mensurável",
    evidenceClass: "validation_report",
    release: "R3D",
    increment: null,
    experimentId: "R3D",
    status: "NO_MEASURABLE_EDGE",
    dataOrigin: "HISTORICAL_AUDITED",
    scientificStage: "AUDITED_COMPLETE",
    createdAtOrUnknown: "2026-06-01T00:00:00.000Z",
    sourcePath: "docs/audits/R3D_AUDIT_RESULTS.md",
    summary:
      "Conclusão auditada de R3D: R3D_RESULT=NO_MEASURABLE_EDGE. Esta conclusão é distinta do gate R3E e não implica rejeição do experimento R3E.",
    supports: [
      "R3D_RESULT=NO_MEASURABLE_EDGE",
      "Validação histórica auditada registrada",
    ],
    limitations: [
      "Não equivale a rejeição do gate R3E",
      "Não inclui resultados de future-unseen",
      "Não autoriza trading",
    ],
    knownState: [
      "R3D concluído com NO_MEASURABLE_EDGE",
      "R3D ≠ R3E (conclusões e gates separados)",
    ],
    unknownState: [
      "Estado final de R3E permanece governado pelo gate PENDING_FUTURE_UNSEEN_DATA",
    ],
    governanceFlags: [
      "R3D_RESULT=NO_MEASURABLE_EDGE",
      "R3D_NEQ_R3E_REJECTED=true",
    ],
    staleness: "HISTORICAL",
  },
  {
    evidenceId: "ev-r3e-pending-future-unseen",
    title: "Estado R3E — gate pendente de dados futuros não vistos",
    evidenceClass: "experiment_specification",
    release: "R3E",
    increment: null,
    experimentId: "R3E",
    status: "PENDING_FUTURE_UNSEEN_DATA",
    dataOrigin: "SYNTHETIC_ILLUSTRATIVE",
    scientificStage: "PENDING_FUTURE_UNSEEN",
    createdAtOrUnknown: "2026-07-10T00:00:00.000Z",
    sourcePath: "docs/audits/R3E_AUDIT_RESULTS.md",
    summary:
      "Estado governado do experimento R3E: R3E_GATE=PENDING_FUTURE_UNSEEN_DATA. Distinto da conclusão R3D; não implica rejeição do experimento R3E.",
    supports: [
      "R3E_GATE=PENDING_FUTURE_UNSEEN_DATA",
      "PENDING_FUTURE_UNSEEN_DATA ≠ FAILED",
    ],
    limitations: [
      "Sem payloads de resultados future-unseen neste catálogo",
      "Não executa validate nem effect peeking",
      "Não desbloqueia R4",
    ],
    knownState: [
      "Gate R3E permanece pendente de dados futuros não vistos",
      "R3D e R3E mantêm conclusões separadas",
    ],
    unknownState: [
      "Resultados em dados futuros não vistos ainda não existem neste explorador",
    ],
    governanceFlags: [
      "R3E_GATE=PENDING_FUTURE_UNSEEN_DATA",
      "FUTURE_UNSEEN_RESULTS_PRESENT=false",
    ],
    staleness: "CURRENT_AS_OF_FIXTURE",
  },
  {
    evidenceId: "ev-fu-collection-readiness",
    title: "Prontidão de coleta future-unseen — janela insuficiente",
    evidenceClass: "collection_readiness_evidence",
    release: "R3E-FU",
    increment: null,
    experimentId: "R3E-FU",
    status: "NOT_READY",
    dataOrigin: "SYNTHETIC_ILLUSTRATIVE",
    scientificStage: "PENDING_FUTURE_UNSEEN",
    createdAtOrUnknown: "2026-07-12T00:00:00.000Z",
    sourcePath:
      "reports/ai-implementation/R3E-READINESS-001_IMPLEMENTATION_REPORT.md",
    summary:
      "Estado ilustrativo de prontidão: WINDOW_DAYS_INSUFFICIENT e NOT_READY. Sem payloads de resultados future-unseen; sem execução de validação.",
    supports: [
      "WINDOW_DAYS_INSUFFICIENT",
      "STATUS=NOT_READY",
      "Coleta/prontidão como metadado de estado apenas",
    ],
    limitations: [
      "Sem tabelas de resultados futuros",
      "Sem métricas fabricadas de edge ou PnL",
      "NOT_READY ≠ FAULT",
    ],
    knownState: [
      "Janela de coleta insuficiente para readiness",
      "Validação future-unseen não executada neste catálogo",
    ],
    unknownState: [
      "Quando a janela será suficiente permanece operacionalmente aberto",
    ],
    governanceFlags: [
      "WINDOW_DAYS_INSUFFICIENT=true",
      "READINESS_STATUS=NOT_READY",
      "FU_RESULT_PAYLOADS=absent",
    ],
    staleness: "PENDING_REFRESH",
  },
  {
    evidenceId: "ev-host-scheduler-operational-debt",
    title: "Dívida operacional — host e ativação do agendador",
    evidenceClass: "operational_debt_record",
    release: "R3E-B5",
    increment: null,
    experimentId: null,
    status: "BLOCKED",
    dataOrigin: "SYNTHETIC_ILLUSTRATIVE",
    scientificStage: "BLOCKED",
    createdAtOrUnknown: "2026-07-08T00:00:00.000Z",
    sourcePath:
      "reports/ai-implementation/R3E-B5-SCHEDULER-ACTIVATION-001_BLOCKED_DECISION_HANDOFF.md",
    summary:
      "Registro ilustrativo de dívida operacional: HOST_DISCOVERY=DEFERRED e SCHEDULER_ACTIVATION=BLOCKED. Sem ativação de scheduler nesta UI.",
    supports: [
      "HOST_DISCOVERY=DEFERRED",
      "SCHEDULER_ACTIVATION=BLOCKED",
      "Dívida operacional explícita",
    ],
    limitations: [
      "Não realiza discovery de host real",
      "Não ativa scheduler",
      "BLOCKED/DEFERRED ≠ FAULT",
    ],
    knownState: [
      "Descoberta de host adiada",
      "Ativação do agendador bloqueada por decisão registrada",
    ],
    unknownState: [
      "Presença efetiva de host persistente no ambiente do operador",
    ],
    governanceFlags: [
      "HOST_DISCOVERY=DEFERRED",
      "SCHEDULER_ACTIVATION=BLOCKED",
    ],
    staleness: "CURRENT_AS_OF_FIXTURE",
  },
];

function assertFixtureIntegrity(entries: EvidenceCatalogEntryInput[]): void {
  for (const entry of entries) {
    if (!entry.evidenceId.trim()) {
      throw new Error("evidenceId required");
    }
    if (!isEvidenceClass(entry.evidenceClass)) {
      throw new Error(`Invalid evidenceClass: ${entry.evidenceClass}`);
    }
    if (!isEvidenceDataOrigin(entry.dataOrigin)) {
      throw new Error(`Invalid dataOrigin: ${entry.dataOrigin}`);
    }
    if (!isEvidenceScientificStage(entry.scientificStage)) {
      throw new Error(`Invalid scientificStage: ${entry.scientificStage}`);
    }
    if (!isEvidenceStaleness(entry.staleness)) {
      throw new Error(`Invalid staleness: ${entry.staleness}`);
    }
    assertValidEvidenceSourcePath(entry.sourcePath);
    const blob = JSON.stringify(entry).toLowerCase();
    if (
      blob.includes("futureunseenresultspresent=true") ||
      blob.includes('"pnl"') ||
      blob.includes("sharpe=") ||
      /p\s*=\s*0\./.test(blob)
    ) {
      throw new Error(
        `Forbidden scientific/FU payload content in ${entry.evidenceId}`,
      );
    }
  }
}

assertFixtureIntegrity(ENTRIES);

export type EvidenceCatalogFixture = {
  metadata: FixtureMetadata;
  catalog: EvidenceCatalogInput;
  nowIso: string;
};

export function getEvidenceCatalogFixture(): EvidenceCatalogFixture {
  return {
    metadata: fixtureMetadata(
      EVIDENCE_CATALOG_FIXTURE_ID,
      "Catálogo de evidências — estado atual ilustrativo",
      "Catálogo curado sintético para o Evidence Explorer (UX-R2 I1). Metadados e resumos apenas; sem acesso a arquivos nem resultados future-unseen.",
    ),
    catalog: { entries: ENTRIES.map((e) => ({ ...e })) },
    nowIso: EVIDENCE_CATALOG_NOW_ISO,
  };
}
