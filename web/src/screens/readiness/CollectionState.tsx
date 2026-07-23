import { Link } from "react-router-dom";
import { Card } from "../../components/primitives";
import type { ReadinessViewModel } from "../../viewmodels";

export type CollectionStateProps = {
  readiness: ReadinessViewModel;
};

/**
 * Collection-health metrics are NOT on ReadinessViewModel.
 * Disclose absence and point to Dados Coletados for illustrative quality detail.
 * Does not fabricate health metrics or imply scientific/readiness changes via nav.
 */
export function CollectionState({ readiness }: CollectionStateProps) {
  const waitingWindow =
    readiness.nextSafeAction.code === "wait_for_sufficient_future_window";

  return (
    <Card className="wick-readiness-card" data-testid="readiness-collection-state">
      <h2 className="wick-readiness-card-title">Estado da coleta</h2>
      <p
        className="wick-readiness-primary"
        data-testid="readiness-collection-message"
      >
        {waitingWindow
          ? "A próxima ação segura indica aguardar janela futura suficiente — a coleta futura ainda precisa avançar para a prontidão. Detalhes de saúde da coleta não fazem parte deste ViewModel."
          : "Estado detalhado de saúde da coleta não é fornecido pelo ViewModel de prontidão."}
      </p>
      <p className="wick-readiness-muted" data-testid="readiness-collection-scope">
        Fora de escopo nesta tela: completeness, gaps, duplicates, cutoff e
        contagens de série. Qualidade e cobertura ilustrativas dos dados
        coletados estão em{" "}
        <Link
          to="/future-collection/collected-data"
          data-testid="readiness-link-collected-data"
        >
          Dados Coletados
        </Link>
        , não na Visão Geral. Navegar até lá não altera prontidão, status
        científico, coleta, validação nem ativação operacional.
        DATA_QUALITY ≠ SCIENTIFIC_APPROVAL. COLLECTION_HEALTHY ≠
        VALIDATION_READY. COLLECTION_IN_PROGRESS ≠ READY.
      </p>
    </Card>
  );
}
