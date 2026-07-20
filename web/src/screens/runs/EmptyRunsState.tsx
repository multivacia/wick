import { Section } from "../../components/primitives";

export type EmptyRunsStateProps = {
  technicalCode: string | null;
  plainLanguage: string;
};

/**
 * Empty / no-runs presentation — never fault semantics.
 */
export function EmptyRunsState({
  technicalCode,
  plainLanguage,
}: EmptyRunsStateProps) {
  return (
    <Section title="Estado vazio" data-testid="runs-empty-state">
      <p className="wick-runs-primary">Ainda não há execuções registradas.</p>
      <p className="wick-runs-technical">{plainLanguage}</p>
      {technicalCode ? (
        <p className="wick-runs-technical">
          Código: <code>{technicalCode}</code>
        </p>
      ) : null}
      <p className="wick-runs-muted">
        Lista vazia não é falha confirmada (EMPTY ≠ FAULT).
      </p>
    </Section>
  );
}
