import { Link } from "react-router-dom";
import { Card } from "../../components/primitives";
import { RelatedEvidenceLinks } from "../shared/RelatedEvidenceLinks";

export type CrossNavLinksProps = {
  relatedEvidence: readonly { evidenceId: string; label: string }[];
};

/**
 * Approved internal cross-navigation only:
 * /future-collection/runs, /future-collection/readiness,
 * /governance/evidence?evidenceId=<sanitized>
 */
export function CrossNavLinks({ relatedEvidence }: CrossNavLinksProps) {
  return (
    <Card className="wick-collected-data-card" data-testid="collected-data-cross-nav">
      <h2 className="wick-collected-data-card-title">Navegação relacionada</h2>
      <ul className="wick-collected-data-cross-nav-list">
        <li>
          <Link to="/future-collection/runs" data-testid="collected-data-link-runs">
            Execuções da coleta
          </Link>
        </li>
        <li>
          <Link
            to="/future-collection/readiness"
            data-testid="collected-data-link-readiness"
          >
            Prontidão
          </Link>
        </li>
      </ul>
      <RelatedEvidenceLinks items={relatedEvidence} title="Evidências relacionadas" />
      <p className="wick-collected-data-muted">
        Apenas links internos aprovados. Sem downloads, URLs externas ou abertura de
        arquivos-fonte.
      </p>
    </Card>
  );
}
