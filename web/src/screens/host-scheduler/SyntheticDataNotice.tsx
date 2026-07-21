import type { FixtureMetadata } from "../../fixtures";
import { Alert } from "../../components/primitives";
import {
  HOST_SCHEDULER_SYNTHETIC_ACTIVATION_DISCLAIMER,
  SYNTHETIC_EVIDENCE_DISCLAIMER,
} from "./loadHostSchedulerScreenData";

export type SyntheticDataNoticeProps = {
  metadata: FixtureMetadata;
};

/**
 * Mandatory synthetic/illustrative notice for fixture-backed Host screen.
 */
export function SyntheticDataNotice({ metadata }: SyntheticDataNoticeProps) {
  return (
    <Alert
      tone="informational"
      title={metadata.exampleLabel}
      data-testid="host-scheduler-synthetic-notice"
    >
      <p>
        <strong>{metadata.technicalLabel}</strong>
        {" — "}
        {SYNTHETIC_EVIDENCE_DISCLAIMER}.
      </p>
      <p className="wick-host-scheduler-primary">
        {HOST_SCHEDULER_SYNTHETIC_ACTIVATION_DISCLAIMER}
      </p>
      <p className="wick-host-scheduler-muted">
        Cenário: {metadata.fixtureLabel} ({metadata.fixtureId}).
      </p>
    </Alert>
  );
}
