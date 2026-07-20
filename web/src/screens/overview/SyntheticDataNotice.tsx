import type { FixtureMetadata } from "../../fixtures";
import { Alert } from "../../components/primitives";
import { SYNTHETIC_EVIDENCE_DISCLAIMER } from "./loadOverviewScreenData";

export type SyntheticDataNoticeProps = {
  metadata: FixtureMetadata;
};

/**
 * Mandatory synthetic/illustrative notice for fixture-backed screens.
 */
export function SyntheticDataNotice({ metadata }: SyntheticDataNoticeProps) {
  return (
    <Alert
      tone="informational"
      title={metadata.exampleLabel}
      data-testid="overview-synthetic-notice"
    >
      <p>
        <strong>{metadata.technicalLabel}</strong>
        {" — "}
        {SYNTHETIC_EVIDENCE_DISCLAIMER}.
      </p>
      <p className="wick-overview-muted">
        Cenário: {metadata.fixtureLabel} ({metadata.fixtureId}).
      </p>
    </Alert>
  );
}
