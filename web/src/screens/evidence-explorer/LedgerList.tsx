import { Alert, Button, StatusBadge } from "../../components/primitives";
import type { StatusBadgeStatus } from "../../components/primitives";
import type { GovernedDecisionRecordViewModel } from "../../viewmodels";
import { RelatedEvidenceLinks } from "../shared/RelatedEvidenceLinks";

export type LedgerListProps = {
  records: readonly GovernedDecisionRecordViewModel[];
  selectedDecisionId: string | null;
  resultCount: number;
  totalCount: number;
  emptyState: boolean;
  noResultsState: boolean;
  onSelect: (decisionId: string) => void;
  onClearFilters: () => void;
};

function RecordRow({
  record,
  selected,
  onSelect,
}: {
  record: GovernedDecisionRecordViewModel;
  selected: boolean;
  onSelect: (decisionId: string) => void;
}) {
  return (
    <li>
      <button
        type="button"
        className={[
          "wick-ledger-row",
          selected ? "wick-ledger-row--selected" : "",
        ]
          .filter(Boolean)
          .join(" ")}
        onClick={() => onSelect(record.decisionId)}
        aria-current={selected ? "true" : undefined}
        data-testid={`ledger-row-${record.decisionId}`}
        data-disposition={record.disposition.disposition}
      >
        <span className="wick-ledger-row__title">{record.title}</span>
        <StatusBadge
          status={record.disposition.status as StatusBadgeStatus}
          label={record.disposition.dispositionLabel}
        />
        <span className="wick-evidence-muted">
          {record.domainLabel}
          {record.relatedRelease ? ` · ${record.relatedRelease}` : ""}
          {" · "}
          {record.decisionDateDisplay}
        </span>
        <span className="wick-evidence-muted">
          Próxima ação: {record.nextGovernedAction}
        </span>
      </button>
    </li>
  );
}

export function LedgerList({
  records,
  selectedDecisionId,
  resultCount,
  totalCount,
  emptyState,
  noResultsState,
  onSelect,
  onClearFilters,
}: LedgerListProps) {
  if (emptyState) {
    return (
      <Alert
        tone="informational"
        title="Livro vazio"
        data-testid="ledger-empty-state"
      >
        <p className="wick-evidence-primary">
          Não há decisões curadas neste fixture ilustrativo.
        </p>
      </Alert>
    );
  }

  if (noResultsState) {
    return (
      <Alert
        tone="informational"
        title="Nenhum resultado"
        data-testid="ledger-no-results-state"
      >
        <p className="wick-evidence-primary">
          Nenhuma decisão corresponde aos filtros atuais.
        </p>
        <Button
          type="button"
          variant="secondary"
          onClick={onClearFilters}
          data-testid="ledger-no-results-clear"
        >
          Limpar filtros do livro
        </Button>
      </Alert>
    );
  }

  return (
    <div className="wick-ledger-list" data-testid="ledger-list">
      <p className="wick-evidence-muted" data-testid="ledger-result-count">
        Exibindo {resultCount} de {totalCount} decisões curadas
      </p>
      <ul className="wick-ledger-list__items">
        {records.map((record) => (
          <RecordRow
            key={record.decisionId}
            record={record}
            selected={record.decisionId === selectedDecisionId}
            onSelect={onSelect}
          />
        ))}
      </ul>
    </div>
  );
}

export type LedgerDetailProps = {
  record: GovernedDecisionRecordViewModel | null;
  onClearSelection: () => void;
};

export function LedgerDetail({ record, onClearSelection }: LedgerDetailProps) {
  if (!record) {
    return (
      <div
        className="wick-ledger-detail wick-ledger-detail--empty"
        data-testid="ledger-detail-empty"
      >
        <p className="wick-evidence-muted">
          Selecione uma decisão para inspecionar racional, limites, evidências,
          gatilho e próxima ação governada.
        </p>
      </div>
    );
  }

  return (
    <article
      className="wick-ledger-detail"
      data-testid={`ledger-detail-${record.decisionId}`}
      aria-labelledby={`ledger-detail-title-${record.decisionId}`}
    >
      <header className="wick-ledger-detail__header">
        <div>
          <h3
            id={`ledger-detail-title-${record.decisionId}`}
            className="wick-ledger-detail__title"
          >
            {record.title}
          </h3>
          <StatusBadge
            status={record.disposition.status as StatusBadgeStatus}
            label={record.disposition.dispositionLabel}
          />
        </div>
        <Button
          type="button"
          variant="secondary"
          onClick={onClearSelection}
          data-testid="ledger-detail-clear"
        >
          Fechar detalhe
        </Button>
      </header>

      <p className="wick-evidence-primary">{record.summary}</p>
      <p className="wick-evidence-muted">{record.disposition.dispositionMeaning}</p>

      <dl className="wick-ledger-detail__fields">
        <div>
          <dt>Disposição</dt>
          <dd>
            {record.disposition.dispositionLabel}{" "}
            <span className="wick-evidence-muted">
              ({record.disposition.disposition})
            </span>
          </dd>
        </div>
        <div>
          <dt>Domínio</dt>
          <dd>
            {record.domainLabel}{" "}
            <span className="wick-evidence-muted">({record.domain})</span>
          </dd>
        </div>
        <div>
          <dt>Tipo</dt>
          <dd>
            {record.decisionTypeLabel}{" "}
            <span className="wick-evidence-muted">({record.decisionType})</span>
          </dd>
        </div>
        <div>
          <dt>Data da decisão</dt>
          <dd data-unknown={record.decisionDateIsUnknown ? "true" : "false"}>
            {record.decisionDateDisplay}
          </dd>
        </div>
        <div>
          <dt>Escopo</dt>
          <dd>{record.scope}</dd>
        </div>
        <div>
          <dt>Racional</dt>
          <dd>{record.rationale}</dd>
        </div>
        {record.hasConditions ? (
          <div data-testid="ledger-detail-conditions">
            <dt>Condições</dt>
            <dd>
              <ul>
                {record.conditions.map((item) => (
                  <li key={item}>{item}</li>
                ))}
              </ul>
            </dd>
          </div>
        ) : (
          <div data-testid="ledger-detail-no-conditions">
            <dt>Condições</dt>
            <dd>Nenhuma condição adicional registrada.</dd>
          </div>
        )}
        <div>
          <dt>Não inferir</dt>
          <dd>
            <ul data-testid="ledger-must-not-infer">
              {record.mustNotInfer.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </dd>
        </div>
        <div data-testid="ledger-detail-reassessment">
          <dt>Gatilho de reavaliação</dt>
          <dd>
            {record.hasReassessmentTrigger
              ? record.reassessmentTrigger
              : "Nenhum gatilho descritivo registrado. Ausência de gatilho ≠ permissão."}
          </dd>
        </div>
        <div>
          <dt>Próxima ação governada</dt>
          <dd>{record.nextGovernedAction}</dd>
        </div>
        {record.scientificBoundary ? (
          <div>
            <dt>Limite científico</dt>
            <dd>{record.scientificBoundary}</dd>
          </div>
        ) : null}
        {record.operationalBoundary ? (
          <div>
            <dt>Limite operacional</dt>
            <dd>{record.operationalBoundary}</dd>
          </div>
        ) : null}
        {record.isSuperseded ? (
          <div data-testid="ledger-detail-superseded">
            <dt>Substituição</dt>
            <dd>
              {record.supersededBy
                ? `Substituída por ${record.supersededBy}`
                : "Registro marcado como substituído (histórico retido)."}
              {record.supersedes
                ? ` Substitui ${record.supersedes}.`
                : ""}
            </dd>
          </div>
        ) : null}
        <div>
          <dt>Curadoria ilustrativa</dt>
          <dd>
            fixture_authored_at: {record.fixtureAuthoredAtDisplay};{" "}
            catalog_curated_at: {record.catalogCuratedAtDisplay}
          </dd>
        </div>
      </dl>

      <RelatedEvidenceLinks
        items={record.evidenceRefs}
        title="Evidências de suporte"
      />
    </article>
  );
}
