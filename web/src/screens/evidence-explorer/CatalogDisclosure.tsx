import { Alert } from "../../components/primitives";

export type CatalogDisclosureProps = {
  disclosure: string;
};

export function CatalogDisclosure({ disclosure }: CatalogDisclosureProps) {
  return (
    <Alert
      tone="informational"
      title="Divulgação do catálogo"
      data-testid="evidence-catalog-disclosure"
    >
      <p>{disclosure}</p>
    </Alert>
  );
}
