export type EvidenceSearchProps = {
  value: string;
  onChange: (value: string) => void;
};

export function EvidenceSearch({ value, onChange }: EvidenceSearchProps) {
  return (
    <div className="wick-evidence-search" data-testid="evidence-search">
      <label className="wick-evidence-field-label" htmlFor="evidence-search-input">
        Buscar evidências
      </label>
      <input
        id="evidence-search-input"
        type="search"
        className="wick-evidence-input"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Título, classe, release, status, resumo…"
        autoComplete="off"
        data-testid="evidence-search-input"
      />
    </div>
  );
}
