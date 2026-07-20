/**
 * Synthetic fixture metadata — never treat as live/operational evidence.
 */

export const EXAMPLE_LABEL = "Dados ilustrativos";
export const TECHNICAL_LABEL = "Synthetic fixture";

export type FixtureMetadata = {
  fixtureId: string;
  fixtureLabel: string;
  fixturePurpose: string;
  synthetic: true;
  illustrative: true;
  notOperationalEvidence: true;
  exampleLabel: typeof EXAMPLE_LABEL;
  technicalLabel: typeof TECHNICAL_LABEL;
};

export function fixtureMetadata(
  fixtureId: string,
  fixtureLabel: string,
  fixturePurpose: string,
): FixtureMetadata {
  return {
    fixtureId,
    fixtureLabel,
    fixturePurpose,
    synthetic: true,
    illustrative: true,
    notOperationalEvidence: true,
    exampleLabel: EXAMPLE_LABEL,
    technicalLabel: TECHNICAL_LABEL,
  };
}
