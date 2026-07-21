import { Link } from "react-router-dom";
import { buildEvidenceExplorerHref } from "../../viewmodels";

export type RelatedEvidenceItem = {
  evidenceId: string;
  label: string;
};

export type RelatedEvidenceLinksProps = {
  /** Catalog evidence entries (ids must exist in the curated fixture). */
  items: readonly RelatedEvidenceItem[];
  title?: string;
};

/**
 * Internal deep-link list to Evidence Explorer entries.
 * Uses react-router-dom Link (no raw anchor, no external URLs).
 * Renders nothing if items is empty.
 */
export function RelatedEvidenceLinks({
  items,
  title = "Evidências relacionadas",
}: RelatedEvidenceLinksProps) {
  if (items.length === 0) return null;

  return (
    <div
      className="wick-related-evidence"
      data-testid="related-evidence-links"
    >
      <p className="wick-related-evidence__title">{title}</p>
      <ul className="wick-related-evidence__list">
        {items.map(({ evidenceId, label }) => (
          <li key={evidenceId}>
            <Link
              to={buildEvidenceExplorerHref(evidenceId)}
              data-testid={`related-evidence-link-${evidenceId}`}
            >
              {label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
