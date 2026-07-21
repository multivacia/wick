/**
 * UX-R2 I1 — Evidence Explorer screen data assembly.
 * Fixture-backed only. No network / filesystem / file export.
 */

import {
  EVIDENCE_CATALOG_FIXTURE_ID,
  getEvidenceCatalogFixture,
  type EvidenceCatalogFixture,
  type FixtureMetadata,
} from "../../fixtures";
import type { EvidenceCatalogInput } from "../../viewmodels";

export { EVIDENCE_CATALOG_FIXTURE_ID };

export const SYNTHETIC_EVIDENCE_DISCLAIMER =
  "Não representa evidência operacional ou científica real";

export type EvidenceExplorerScreenData = {
  fixtureId: typeof EVIDENCE_CATALOG_FIXTURE_ID;
  metadata: FixtureMetadata;
  catalog: EvidenceCatalogInput;
  nowIso: string;
};

export function loadEvidenceExplorerScreenData(): EvidenceExplorerScreenData {
  const packed: EvidenceCatalogFixture = getEvidenceCatalogFixture();
  return {
    fixtureId: EVIDENCE_CATALOG_FIXTURE_ID,
    metadata: packed.metadata,
    catalog: packed.catalog,
    nowIso: packed.nowIso,
  };
}
