import { PageHeader, Section, StatusBadge, Stack } from "../components/primitives";
import type { RoutePlaceholderModel } from "./navigation";
import "./shell.css";

export type RoutePlaceholderProps = {
  model: RoutePlaceholderModel;
};

export function RoutePlaceholder({ model }: RoutePlaceholderProps) {
  return (
    <Stack className="wick-route-placeholder">
      <PageHeader
        eyebrow="Shell operacional"
        title={model.title}
        description={model.description}
      />
      <Section title="Identificador técnico">
        <p className="wick-route-placeholder__route">
          <code>{model.routeId}</code>
        </p>
        <StatusBadge status="deferred" label={model.statusLabel} />
      </Section>
    </Stack>
  );
}
