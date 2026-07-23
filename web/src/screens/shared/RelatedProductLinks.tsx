import { Link } from "react-router-dom";
import "./related-links.css";

export type RelatedProductLinkItem = {
  /** Internal app path only (no external URLs). */
  to: string;
  label: string;
  testId: string;
};

export type RelatedProductLinksProps = {
  items: readonly RelatedProductLinkItem[];
  title?: string;
  testId?: string;
  disclaimer?: string;
};

/**
 * Thin internal product cross-navigation list.
 * Uses react-router-dom Link only (no raw anchors, no external hrefs).
 */
export function RelatedProductLinks({
  items,
  title = "Navegação relacionada",
  testId = "related-product-links",
  disclaimer = "Apenas rotas internas aprovadas. Navegar não altera prontidão, status científico, coleta, validação nem ativação operacional.",
}: RelatedProductLinksProps) {
  if (items.length === 0) return null;

  return (
    <div className="wick-related-product" data-testid={testId}>
      <p className="wick-related-product__title">{title}</p>
      <ul className="wick-related-product__list">
        {items.map(({ to, label, testId: itemTestId }) => (
          <li key={to}>
            <Link to={to} data-testid={itemTestId}>
              {label}
            </Link>
          </li>
        ))}
      </ul>
      {disclaimer ? (
        <p className="wick-related-product__disclaimer">{disclaimer}</p>
      ) : null}
    </div>
  );
}
