/**
 * UX-R2 I1 — Evidence Explorer screen data assembly.
 * Fixture-backed only. No network / filesystem / file export.
 * UX-R4 I2 adds curated governed decision ledger domain alongside catalog.
 */

import {
  EVIDENCE_CATALOG_FIXTURE_ID,
  getEvidenceCatalogFixture,
  getGovernedDecisionLedgerFixture,
  GOVERNED_DECISION_LEDGER_FIXTURE_ID,
  type EvidenceCatalogFixture,
  type FixtureMetadata,
  type GovernedDecisionLedgerFixture,
} from "../../fixtures";
import type {
  EvidenceCatalogInput,
  GovernedDecisionLedgerDomainInput,
} from "../../viewmodels";

export { EVIDENCE_CATALOG_FIXTURE_ID, GOVERNED_DECISION_LEDGER_FIXTURE_ID };

export const SYNTHETIC_EVIDENCE_DISCLAIMER =
  "Não representa evidência operacional ou científica real";

export type EvidenceExplorerScreenData = {
  fixtureId: typeof EVIDENCE_CATALOG_FIXTURE_ID;
  metadata: FixtureMetadata;
  catalog: EvidenceCatalogInput;
  nowIso: string;
  ledgerFixtureId: typeof GOVERNED_DECISION_LEDGER_FIXTURE_ID;
  ledger: GovernedDecisionLedgerDomainInput;
  ledgerMetadata: FixtureMetadata;
  ledgerNowIso: string;
};

export function loadEvidenceExplorerScreenData(): EvidenceExplorerScreenData {
  const packed: EvidenceCatalogFixture = getEvidenceCatalogFixture();
  const ledgerPacked: GovernedDecisionLedgerFixture =
    getGovernedDecisionLedgerFixture();
  return {
    fixtureId: EVIDENCE_CATALOG_FIXTURE_ID,
    metadata: packed.metadata,
    catalog: packed.catalog,
    nowIso: packed.nowIso,
    ledgerFixtureId: GOVERNED_DECISION_LEDGER_FIXTURE_ID,
    ledger: ledgerPacked.domain,
    ledgerMetadata: ledgerPacked.metadata,
    ledgerNowIso: ledgerPacked.nowIso,
  };
}
