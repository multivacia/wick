import type { FixtureMetadata } from "../../fixtures";
import { Alert } from "../../components/primitives";
import { SYNTHETIC_COLLECTION_DISCLAIMER } from "./loadCollectedDataScreenData";

export type SyntheticDataNoticeProps = {
  metadata: FixtureMetadata;
};

/**
 * Mandatory synthetic/illustrative notice for fixture-backed Dados Coletados.
 */
export function SyntheticDataNotice({ metadata }: SyntheticDataNoticeProps) {
  return (
    <Alert
      tone="informational"
      title={metadata.exampleLabel}
      data-testid="collected-data-synthetic-notice"
    >
      <p>
        <strong>{metadata.technicalLabel}</strong>
        {" — "}
        {SYNTHETIC_COLLECTION_DISCLAIMER}.
      </p>
      <p className="wick-collected-data-muted">
        Cenário: {metadata.fixtureLabel} ({metadata.fixtureId}).
      </p>
    </Alert>
  );
}
