import type { FixtureMetadata } from "../../fixtures";
import { Alert } from "../../components/primitives";
import { SYNTHETIC_EVIDENCE_DISCLAIMER } from "./loadRunsScreenData";

export type SyntheticDataNoticeProps = {
  metadata: FixtureMetadata;
};

/**
 * Mandatory synthetic/illustrative notice for fixture-backed Runs screen.
 */
export function SyntheticDataNotice({ metadata }: SyntheticDataNoticeProps) {
  return (
    <Alert
      tone="informational"
      title={metadata.exampleLabel}
      data-testid="runs-synthetic-notice"
    >
      <p>
        <strong>{metadata.technicalLabel}</strong>
        {" — "}
        {SYNTHETIC_EVIDENCE_DISCLAIMER}.
      </p>
      <p className="wick-runs-muted">
        Cenário: {metadata.fixtureLabel} ({metadata.fixtureId}).
      </p>
    </Alert>
  );
}
