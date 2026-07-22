import type { FixtureMetadata } from "../../fixtures";
import {
  COLLECTION_DATA_QUALITY_FIXTURE_ID,
  getCollectionDataQualityFixture,
  type CollectionDataQualityFixture,
} from "../../fixtures/collectionDataQuality";
import type { CollectionDataQualityDomainInput } from "../../viewmodels";

export { COLLECTION_DATA_QUALITY_FIXTURE_ID };

export const SYNTHETIC_COLLECTION_DISCLAIMER =
  "Conjunto ilustrativo (fixture-backed). Não é evidência operacional ao vivo, não aprova cientificamente e não autoriza validação nem ativação";

export type CollectedDataScreenData = {
  fixtureId: typeof COLLECTION_DATA_QUALITY_FIXTURE_ID;
  metadata: FixtureMetadata;
  domain: CollectionDataQualityDomainInput;
  nowIso: string;
};

export function loadCollectedDataScreenData(): CollectedDataScreenData {
  const packed: CollectionDataQualityFixture = getCollectionDataQualityFixture();
  return {
    fixtureId: COLLECTION_DATA_QUALITY_FIXTURE_ID,
    metadata: packed.metadata,
    domain: packed.domain,
    nowIso: packed.nowIso,
  };
}
