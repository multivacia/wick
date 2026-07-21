import type { FixtureMetadata } from "../../fixtures";
import { Alert } from "../../components/primitives";
import {
  R3E_SYNTHETIC_SCIENCE_DISCLAIMER,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "./loadR3eExperimentScreenData";

export type SyntheticDataNoticeProps = {
  metadata: FixtureMetadata;
};

/**
 * Mandatory synthetic/illustrative notice for fixture-backed R3E screen.
 */
export function SyntheticDataNotice({ metadata }: SyntheticDataNoticeProps) {
  return (
    <Alert
      tone="informational"
      title={metadata.exampleLabel}
      data-testid="r3e-experiment-synthetic-notice"
    >
      <p>
        <strong>{metadata.technicalLabel}</strong>
        {" — "}
        {SYNTHETIC_EVIDENCE_DISCLAIMER}.
      </p>
      <p className="wick-r3e-primary">{R3E_SYNTHETIC_SCIENCE_DISCLAIMER}</p>
      <p className="wick-r3e-muted">
        Cenário: {metadata.fixtureLabel} ({metadata.fixtureId}).
      </p>
    </Alert>
  );
}
