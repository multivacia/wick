/**
 * UX-R4 I2 — curated Governed Decision Ledger fixture.
 * Synthetic/illustrative metadata only. No runtime FS / network / FU payloads.
 */

import { fixtureMetadata, type FixtureMetadata } from "./metadata.js";
import type { GovernedDecisionLedgerDomainInput } from "../viewmodels/governedDecisionLedgerTypes.js";
import {
  isLedgerDecisionType,
  isLedgerDisposition,
  isLedgerDomain,
} from "../viewmodels/governedDecisionLedgerEnums.js";

export const GOVERNED_DECISION_LEDGER_FIXTURE_ID =
  "governed_decision_ledger_current_state_illustrative" as const;

export const GOVERNED_DECISION_LEDGER_FIXTURE_VERSION = 1 as const;

/** Curated illustrative clock — not live freshness. */
export const GOVERNED_DECISION_LEDGER_NOW_ISO = "2026-07-24T12:00:00.000Z";

const CATALOG_CURATED_AT = "2026-07-24T12:00:00.000Z";
const FIXTURE_AUTHORED_AT = "2026-07-24T11:30:00.000Z";

const ILLUSTRATIVE_DISCLOSURE =
  "Livro de decisões ilustrativo, curado e somente leitura (fixture-backed). Não é backlog, fluxo de aprovação, rastreador de tarefas nem painel de resultados científicos.";

const STALE_DISCLOSURE =
  "O catálogo curado deste livro está marcado como desatualizado em relação ao relógio ilustrativo. Desatualizado ≠ validação científica nem ativação operacional.";

const RECORDS: GovernedDecisionLedgerDomainInput["records"] = [
  {
    decisionId: "dec-ux-r1-fixture-backed-read-only-acceptance",
    title: "UX-R1 — escopo fixture-backed somente leitura aceito",
    summary:
      "Release UX-R1 encerrada e aceita no limite fixture-backed read-only.",
    domain: "RELEASE_GOVERNANCE",
    decisionType: "RELEASE_ACCEPTANCE_DECISION",
    disposition: "ACCEPTED",
    decisionDate: "2026-07-21",
    scope: "FIXTURE_BACKED_READ_ONLY",
    rationale:
      "Escopo fixture-backed somente leitura foi formalmente aceito e governado.",
    evidenceRefs: [
      {
        evidenceId: "ev-ux-r1-formal-closure",
        label: "Encerramento formal UX-R1",
      },
    ],
    mustNotInfer: [
      "Aceitar UX-R1 ≠ aprovar estratégia de trading",
      "Aceitar UX-R1 ≠ desbloquear R4 científico",
    ],
    reassessmentTrigger: null,
    nextGovernedAction:
      "Manter o limite fixture-backed; não reinterpretar como aprovação científica.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "UX-R1",
    scientificBoundary: "Sem alteração de conclusão científica.",
    operationalBoundary: "Sem ativação operacional.",
  },
  {
    decisionId: "dec-ux-r2-evidence-audit-exploration-acceptance",
    title: "UX-R2 — exploração de evidências e auditoria aceita",
    summary:
      "Release UX-R2 encerrada no escopo fixture-backed de exploração de evidências e auditoria.",
    domain: "RELEASE_GOVERNANCE",
    decisionType: "RELEASE_ACCEPTANCE_DECISION",
    disposition: "ACCEPTED",
    decisionDate: "2026-07-21",
    scope: "FIXTURE_BACKED_EVIDENCE_AND_AUDIT_EXPLORATION",
    rationale:
      "Evidence Explorer e exploração de auditoria fixture-backed foram aceitos e governados.",
    evidenceRefs: [
      {
        evidenceId: "ev-ux-r2-discovery-assessment",
        label: "Discovery UX-R2",
      },
      {
        evidenceId: "ev-ux-r2-i1-impl-handoff",
        label: "Implementação Evidence Explorer",
      },
    ],
    mustNotInfer: [
      "Presença de evidência ≠ aprovação científica",
      "Catálogo ilustrativo ≠ evidência operacional ao vivo",
    ],
    reassessmentTrigger: null,
    nextGovernedAction:
      "Usar Evidências como superfície de leitura; não tratar o catálogo como prova científica.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "UX-R2",
    scientificBoundary: "Sem reinterpretar R3D/R3E.",
  },
  {
    decisionId: "dec-ux-r3-collection-quality-coherence-acceptance",
    title: "UX-R3 — monitoramento de coleta e coerência aceitos",
    summary:
      "Release UX-R3 aceita no escopo fixture-backed de monitoramento, qualidade e coerência.",
    domain: "RELEASE_GOVERNANCE",
    decisionType: "RELEASE_ACCEPTANCE_DECISION",
    disposition: "ACCEPTED",
    decisionDate: "2026-07-23",
    scope: "FIXTURE_BACKED_COLLECTION_MONITORING_DATA_QUALITY_AND_COHERENCE",
    rationale:
      "Dados Coletados e coerência de fluxo fixture-backed foram aceitos e governados.",
    evidenceRefs: [
      {
        evidenceId: "ev-fu-collection-readiness",
        label: "Prontidão da coleta (ilustrativa)",
      },
    ],
    mustNotInfer: [
      "Qualidade de dados ≠ aprovação científica",
      "Cobertura ilustrativa ≠ janela futura completa",
    ],
    reassessmentTrigger: null,
    nextGovernedAction:
      "Manter Dados Coletados como monitoramento ilustrativo; não validar nem ativar.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "UX-R3",
    relatedIncrement: "I2+I3",
  },
  {
    decisionId: "dec-r3d-no-measurable-edge",
    title: "R3D — sem vantagem mensurável registrada",
    summary:
      "Conclusão científica registrada: NO_MEASURABLE_EDGE no contexto R3D.",
    domain: "SCIENTIFIC_GOVERNANCE",
    decisionType: "REVIEW_DECISION",
    disposition: "REJECTED",
    decisionDate: "2026-07-18",
    scope: "R3D measurable-edge evaluation v1",
    rationale:
      "Gate R3 registrou rejeição por ausência de vantagem mensurável (NO_MEASURABLE_EDGE).",
    evidenceRefs: [
      {
        evidenceId: "ev-r3d-validation-conclusion",
        label: "Conclusão R3D",
      },
    ],
    mustNotInfer: [
      "REJECTED ≠ INVALID_FOREVER",
      "NO_MEASURABLE_EDGE ≠ falha operacional de coleta",
      "Resultado R3D ≠ rejeição de toda estratégia futura",
    ],
    reassessmentTrigger:
      "Nova evidência independente materialmente distinta do escopo R3D v1.",
    nextGovernedAction:
      "Preservar SCIENTIFIC_CONCLUSION=UNCHANGED; não reinterpretar R3D neste livro.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "R3D",
    scientificBoundary: "R3D_RESULT = NO_MEASURABLE_EDGE",
  },
  {
    decisionId: "dec-r3e-pending-future-unseen",
    title: "R3E — pendente de dados future-unseen",
    summary:
      "Experimento R3E permanece pendente da janela future-unseen exigida.",
    domain: "SCIENTIFIC_GOVERNANCE",
    decisionType: "BLOCKING_DECISION",
    disposition: "BLOCKED",
    decisionDate: "2026-07-18",
    scope: "R3E exploratory complete pending future-unseen data",
    rationale:
      "R3E_GATE = PENDING_FUTURE_UNSEEN_DATA. Coleta em andamento; prontidão ainda insuficiente.",
    evidenceRefs: [
      {
        evidenceId: "ev-r3e-pending-future-unseen",
        label: "R3E pendente future-unseen",
      },
      {
        evidenceId: "ev-fu-collection-readiness",
        label: "Prontidão da coleta",
      },
    ],
    mustNotInfer: [
      "BLOCKED ≠ SYSTEM_FAILURE",
      "Pendente future-unseen ≠ falha de UX",
      "Gatilho de reavaliação ≠ permissão automática de validação",
    ],
    reassessmentTrigger:
      "Janela future-unseen atinge a duração exigida e readiness deixa de ser NOT_READY.",
    nextGovernedAction:
      "Continuar coleta; não executar validate nem effect peeking.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "R3E",
    conditions: [
      "Não executar VALIDATION_EXECUTION",
      "Não realizar EFFECT_PEEKING",
      "Não acessar payloads future-unseen nesta superfície",
    ],
    scientificBoundary: "R3E_GATE = PENDING_FUTURE_UNSEEN_DATA",
  },
  {
    decisionId: "dec-host-discovery-deferred",
    title: "Descoberta de host — adiada",
    summary: "HOST_DISCOVERY permanece DEFERRED por decisão operacional.",
    domain: "OPERATIONAL_GOVERNANCE",
    decisionType: "DEFERRAL_DECISION",
    disposition: "DEFERRED",
    decisionDate: "2026-07-18",
    scope: "Operational host discovery",
    rationale:
      "Débito técnico-operacional aceito e registrado. Descoberta de host adiada conscientemente.",
    evidenceRefs: [
      {
        evidenceId: "ev-host-scheduler-operational-debt",
        label: "Débito operacional host/scheduler",
      },
    ],
    mustNotInfer: [
      "DEFERRED ≠ REJECTED",
      "Host adiado ≠ host indisponível para sempre",
    ],
    reassessmentTrigger: "Host operacional é formalmente identificado.",
    nextGovernedAction:
      "Seguir frentes não dependentes; não considerar descoberta concluída.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "R3E-B5",
    operationalBoundary: "HOST_DISCOVERY = DEFERRED; OPERATIONAL_DEBT = OPEN",
  },
  {
    decisionId: "dec-scheduler-activation-blocked",
    title: "Ativação do scheduler — bloqueada",
    summary: "SCHEDULER_ACTIVATION permanece BLOCKED.",
    domain: "OPERATIONAL_GOVERNANCE",
    decisionType: "BLOCKING_DECISION",
    disposition: "BLOCKED",
    decisionDate: "2026-07-18",
    scope: "Scheduler activation",
    rationale:
      "Ativação do scheduler bloqueada enquanto dívida operacional e host permanecem abertos.",
    evidenceRefs: [
      {
        evidenceId: "ev-host-scheduler-activation-handoff",
        label: "Handoff de ativação do scheduler",
      },
    ],
    mustNotInfer: [
      "BLOCKED ≠ SYSTEM_FAILURE",
      "Scheduler bloqueado ≠ coleta falhou",
    ],
    reassessmentTrigger:
      "Ativação do scheduler é formalmente autorizada após resolução do débito operacional.",
    nextGovernedAction:
      "Não ativar scheduler; preservar SCHEDULER_ACTIVATION=BLOCKED.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "R3E-B5",
    conditions: [
      "Sem SCHEDULER_ACTIVATION_AUTHORIZED",
      "Sem ações operacionais nesta superfície",
    ],
    operationalBoundary: "SCHEDULER_ACTIVATION = BLOCKED",
  },
  {
    decisionId: "dec-scientific-r4-blocked",
    title: "R4 científico — bloqueado",
    summary: "R4_STATUS permanece BLOCKED; sem mudança de estado autorizada.",
    domain: "SCIENTIFIC_GOVERNANCE",
    decisionType: "BLOCKING_DECISION",
    disposition: "BLOCKED",
    decisionDate: "2026-07-18",
    scope: "Scientific R4 stage",
    rationale:
      "R4 científico bloqueado até pré-condições de future-unseen e gates anteriores.",
    evidenceRefs: [
      {
        evidenceId: "ev-r3e-pending-future-unseen",
        label: "Dependência R3E / future-unseen",
      },
    ],
    mustNotInfer: [
      "Blocked scientific R4 ≠ UX failure",
      "R4 bloqueado ≠ falha do Evidence Explorer",
    ],
    reassessmentTrigger:
      "Pré-condições científicas de R4 são formalmente satisfeitas e autorizadas.",
    nextGovernedAction: "Não desbloquear R4; preservar R4_STATUS=BLOCKED.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "R4",
    scientificBoundary: "R4_STATUS = BLOCKED; R4_STATE_CHANGE_AUTHORIZED = false",
  },
  {
    decisionId: "dec-r5-not-started",
    title: "R5 — não iniciado",
    summary: "R5_STATUS permanece NOT_STARTED.",
    domain: "SCIENTIFIC_GOVERNANCE",
    decisionType: "DEFERRAL_DECISION",
    disposition: "DEFERRED",
    decisionDate: "UNKNOWN",
    scope: "Scientific R5 stage",
    rationale:
      "R5 não foi iniciado. Não há autorização para mudança de estado de R5.",
    evidenceRefs: [
      {
        evidenceId: "ev-r3e-readiness-safety-review",
        label: "Revisão de segurança / readiness",
      },
    ],
    mustNotInfer: [
      "NOT_STARTED ≠ FAULT",
      "UNKNOWN date ≠ zero",
      "R5 não iniciado ≠ rejeição científica permanente",
    ],
    reassessmentTrigger: null,
    nextGovernedAction: "Não iniciar R5; preservar R5_STATUS=NOT_STARTED.",
    isIllustrative: true,
    fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
    catalogCuratedAt: CATALOG_CURATED_AT,
    relatedRelease: "R5",
    scientificBoundary: "R5_STATUS = NOT_STARTED; R5_STATE_CHANGE_AUTHORIZED = false",
  },
];

function assertFixtureIntegrity(
  domain: GovernedDecisionLedgerDomainInput,
): void {
  if (domain.fixtureVersion !== 1) {
    throw new Error("Governed decision ledger fixtureVersion must be 1");
  }
  if (domain.records.length !== 9) {
    throw new Error(
      `Expected exactly 9 grounded seed records, got ${domain.records.length}`,
    );
  }
  for (const record of domain.records) {
    if (!record.isIllustrative) {
      throw new Error(`Record ${record.decisionId} must be illustrative`);
    }
    if (!isLedgerDisposition(record.disposition)) {
      throw new Error(`Invalid disposition on ${record.decisionId}`);
    }
    if (!isLedgerDomain(record.domain)) {
      throw new Error(`Invalid domain on ${record.decisionId}`);
    }
    if (!isLedgerDecisionType(record.decisionType)) {
      throw new Error(`Invalid decisionType on ${record.decisionId}`);
    }
    if (!/^dec-/.test(record.decisionId)) {
      throw new Error(`decisionId must start with dec-: ${record.decisionId}`);
    }
    for (const ref of record.evidenceRefs) {
      if (/^https?:\/\//i.test(ref.evidenceId) || ref.evidenceId.includes("..")) {
        throw new Error(`Unsafe evidence ref on ${record.decisionId}`);
      }
    }
  }
}

const DOMAIN: GovernedDecisionLedgerDomainInput = {
  fixtureVersion: GOVERNED_DECISION_LEDGER_FIXTURE_VERSION,
  catalogCuratedAt: CATALOG_CURATED_AT,
  fixtureAuthoredAt: FIXTURE_AUTHORED_AT,
  freshness: "current",
  staleDisclosure: STALE_DISCLOSURE,
  illustrativeDisclosure: ILLUSTRATIVE_DISCLOSURE,
  records: RECORDS,
};

assertFixtureIntegrity(DOMAIN);

export type GovernedDecisionLedgerFixture = {
  metadata: FixtureMetadata;
  domain: GovernedDecisionLedgerDomainInput;
  nowIso: string;
};

export function getGovernedDecisionLedgerFixture(): GovernedDecisionLedgerFixture {
  return {
    metadata: fixtureMetadata(
      GOVERNED_DECISION_LEDGER_FIXTURE_ID,
      "Livro de decisões governadas (estado atual ilustrativo)",
      "Curated illustrative governed decision ledger for Evidence Explorer",
    ),
    domain: structuredClone(DOMAIN),
    nowIso: GOVERNED_DECISION_LEDGER_NOW_ISO,
  };
}
