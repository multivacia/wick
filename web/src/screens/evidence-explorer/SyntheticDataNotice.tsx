import type { FixtureMetadata } from "../../fixtures";
import { Alert } from "../../components/primitives";
import { SYNTHETIC_EVIDENCE_DISCLAIMER } from "./loadEvidenceExplorerScreenData";

export type SyntheticDataNoticeProps = {
  metadata: FixtureMetadata;
};

/**
 * Mandatory synthetic/illustrative notice for fixture-backed Evidence Explorer.
 */
export function SyntheticDataNotice({ metadata }: SyntheticDataNoticeProps) {
  return (
    <Alert
      tone="informational"
      title={metadata.exampleLabel}
      data-testid="evidence-explorer-synthetic-notice"
    >
      <p>
        <strong>{metadata.technicalLabel}</strong>
        {" — "}
        {SYNTHETIC_EVIDENCE_DISCLAIMER}.
      </p>
      <p className="wick-evidence-muted">
        Cenário: {metadata.fixtureLabel} ({metadata.fixtureId}).
      </p>
    </Alert>
  );
}
