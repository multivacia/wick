import type { ReactNode } from "react";
import { Button, Card, Inline, StatusBadge } from "../../components/primitives";
import type { EvidenceDetailViewModel } from "../../viewmodels";

export type EvidenceDetailProps = {
  detail: EvidenceDetailViewModel | null;
  sourcePathDisclaimer: string;
  invalidSelectionFallback: boolean;
  onClearSelection: () => void;
};

function Field({
  label,
  children,
  testId,
}: {
  label: string;
  children: ReactNode;
  testId?: string;
}) {
  return (
    <div className="wick-evidence-field" data-testid={testId}>
      <dt>{label}</dt>
      <dd>{children}</dd>
    </div>
  );
}

function StringList({ items, empty }: { items: string[]; empty: string }) {
  if (items.length === 0) {
    return <span className="wick-evidence-muted">{empty}</span>;
  }
  return (
    <ul className="wick-evidence-detail-list">
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
  );
}

export function EvidenceDetail({
  detail,
  sourcePathDisclaimer,
  invalidSelectionFallback,
  onClearSelection,
}: EvidenceDetailProps) {
  if (invalidSelectionFallback && !detail) {
    return (
      <Card
        className="wick-evidence-detail"
        data-testid="evidence-detail-invalid-selection"
      >
        <h2 className="wick-evidence-detail-title">Seleção indisponível</h2>
        <p className="wick-evidence-primary">
          A evidência selecionada não está visível com os filtros atuais, ou o
          identificador é inválido.
        </p>
        <Button
          variant="secondary"
          size="sm"
          type="button"
          onClick={onClearSelection}
          data-testid="evidence-detail-clear-selection"
        >
          Voltar à lista
        </Button>
      </Card>
    );
  }

  if (!detail) {
    return (
      <Card
        className="wick-evidence-detail"
        data-testid="evidence-detail-empty"
      >
        <h2 className="wick-evidence-detail-title">Detalhe</h2>
        <p className="wick-evidence-muted">
          Selecione uma evidência na lista para inspecionar metadados e resumo.
        </p>
      </Card>
    );
  }

  return (
    <Card
      className="wick-evidence-detail"
      data-testid="evidence-detail"
    >
      <Inline className="wick-evidence-detail__header">
        <h2 className="wick-evidence-detail-title">{detail.title}</h2>
        <StatusBadge
          status={detail.statusPresentation.status}
          label={detail.status}
          data-testid="evidence-detail-status-badge"
        />
      </Inline>

      <Button
        variant="quiet"
        size="sm"
        type="button"
        className="wick-evidence-detail__back"
        onClick={onClearSelection}
        data-testid="evidence-detail-back"
      >
        Voltar à lista
      </Button>

      <p
        className="wick-evidence-primary"
        data-testid="evidence-detail-summary"
      >
        {detail.summary}
      </p>

      <dl className="wick-evidence-field-list">
        <Field label="Identificador" testId="evidence-detail-id">
          <code>{detail.evidenceId}</code>
        </Field>
        <Field label="Classe" testId="evidence-detail-class">
          {detail.evidenceClassLabel} (<code>{detail.evidenceClass}</code>)
        </Field>
        <Field label="Release" testId="evidence-detail-release">
          {detail.release}
        </Field>
        <Field label="Incremento" testId="evidence-detail-increment">
          {detail.increment ?? "—"}
        </Field>
        <Field label="Experimento" testId="evidence-detail-experiment">
          {detail.experimentId ?? "—"}
        </Field>
        <Field label="Origem dos dados" testId="evidence-detail-origin">
          {detail.dataOriginLabel} (<code>{detail.dataOrigin}</code>)
        </Field>
        <Field label="Estágio científico" testId="evidence-detail-stage">
          {detail.scientificStageLabel} (<code>{detail.scientificStage}</code>)
        </Field>
        <Field label="Atualidade" testId="evidence-detail-staleness">
          {detail.stalenessLabel} (<code>{detail.staleness}</code>)
        </Field>
        <Field label="Criado em" testId="evidence-detail-created">
          {detail.createdAtOrUnknown}
        </Field>
        <Field label="Caminho de origem" testId="evidence-detail-source-path">
          <code data-testid="evidence-detail-source-path-code">
            {detail.sourcePath}
          </code>
        </Field>
      </dl>

      <p
        className="wick-evidence-muted"
        data-testid="evidence-source-path-disclaimer"
      >
        {sourcePathDisclaimer}
      </p>

      <section data-testid="evidence-detail-supports">
        <h3 className="wick-evidence-subtitle">Suporta</h3>
        <StringList items={detail.supports} empty="Nenhum item." />
      </section>

      <section data-testid="evidence-detail-limitations">
        <h3 className="wick-evidence-subtitle">Limitações</h3>
        <StringList items={detail.limitations} empty="Nenhuma limitação listada." />
      </section>

      <section data-testid="evidence-detail-known">
        <h3 className="wick-evidence-subtitle">Estado conhecido</h3>
        <StringList items={detail.knownState} empty="Nenhum item." />
      </section>

      <section data-testid="evidence-detail-unknown">
        <h3 className="wick-evidence-subtitle">Estado desconhecido</h3>
        <StringList items={detail.unknownState} empty="Nenhum item." />
      </section>

      <section data-testid="evidence-detail-flags">
        <h3 className="wick-evidence-subtitle">Flags de governança</h3>
        <StringList items={detail.governanceFlags} empty="Nenhuma flag." />
      </section>
    </Card>
  );
}
