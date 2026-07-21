import { Card } from "../../components/primitives";
import type { R3eExperimentViewModel } from "../../viewmodels";

export type LeakageProtectionProps = {
  r3eExperiment: R3eExperimentViewModel;
};

export function LeakageProtection({ r3eExperiment }: LeakageProtectionProps) {
  return (
    <Card className="wick-r3e-card" data-testid="r3e-leakage-protection">
      <h2 className="wick-r3e-card-title">Proteção contra leakage</h2>
      <p className="wick-r3e-primary">{r3eExperiment.leakageProtectionSummary}</p>
    </Card>
  );
}
