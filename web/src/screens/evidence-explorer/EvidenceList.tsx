import { StatusBadge } from "../../components/primitives";
import type { EvidenceSummaryItem } from "../../viewmodels";

export type EvidenceListProps = {
  items: EvidenceSummaryItem[];
  selectedEvidenceId: string | null;
  onSelect: (evidenceId: string) => void;
  resultCount: number;
  emptyState: boolean;
  noResultsState: boolean;
};

export function EvidenceList({
  items,
  selectedEvidenceId,
  onSelect,
  resultCount,
  emptyState,
  noResultsState,
}: EvidenceListProps) {
  if (emptyState) {
    return (
      <div
        className="wick-evidence-list-empty"
        data-testid="evidence-list-empty"
      >
        <p>O catálogo de evidências está vazio.</p>
      </div>
    );
  }

  if (noResultsState) {
    return (
      <div
        className="wick-evidence-list-empty"
        data-testid="evidence-list-no-results"
      >
        <p>Nenhuma evidência corresponde à busca ou aos filtros atuais.</p>
      </div>
    );
  }

  return (
    <div className="wick-evidence-list" data-testid="evidence-list">
      <p className="wick-evidence-muted" data-testid="evidence-result-count">
        {resultCount}{" "}
        {resultCount === 1 ? "evidência encontrada" : "evidências encontradas"}
      </p>
      <ul className="wick-evidence-list__items">
        {items.map((item) => {
          const selected = item.evidenceId === selectedEvidenceId;
          return (
            <li key={item.evidenceId}>
              <button
                type="button"
                className={[
                  "wick-evidence-list__item",
                  selected ? "wick-evidence-list__item--selected" : "",
                ]
                  .filter(Boolean)
                  .join(" ")}
                aria-current={selected ? "true" : undefined}
                onClick={() => onSelect(item.evidenceId)}
                data-testid={`evidence-list-item-${item.evidenceId}`}
              >
                <span className="wick-evidence-list__item-title">
                  {item.title}
                </span>
                <span className="wick-evidence-list__item-meta">
                  <StatusBadge
                    status={item.statusPresentation.status}
                    label={item.status}
                  />
                  <span className="wick-evidence-muted">
                    {item.evidenceClassLabel} · {item.release}
                  </span>
                  <span
                    className="wick-evidence-muted wick-evidence-list__item-standing"
                    data-testid={`evidence-standing-${item.evidenceId}`}
                  >
                    {item.catalogStandingLabel}
                  </span>
                </span>
                <span
                  className="wick-evidence-list__item-provenance wick-evidence-muted"
                  data-testid={`evidence-provenance-${item.evidenceId}`}
                >
                  {item.dataOriginLabel} · {item.scientificStageLabel} ·{" "}
                  {item.stalenessLabel}
                </span>
                <span className="wick-evidence-list__item-summary">
                  {item.summary}
                </span>
              </button>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
