/**
 * UX-R1 I6K — Host e Automação screen data assembly.
 * Fixture-backed only. No network / filesystem / operational sources.
 */

import {
  buildFixtureViewModels,
  type FixtureMetadata,
  type FixtureScenarioId,
  type FixtureViewModels,
} from "../../fixtures";
import type { HostSchedulerViewModel } from "../../viewmodels";

export const HOST_SCHEDULER_FIXTURE_ID =
  "current_project_state_illustrative" as const;

export const SYNTHETIC_EVIDENCE_DISCLAIMER =
  "Não representa evidência operacional real";

export const HOST_SCHEDULER_SYNTHETIC_ACTIVATION_DISCLAIMER =
  "Dados sintéticos ilustrativos — não comprovam descoberta de host, instalação nem ativação do agendador.";

/** Official UX-B4 operational debt wording (detail-safe short form). */
export const OPERATIONAL_DEBT_OFFICIAL_WORDING =
  "Débito técnico-operacional aceito e registrado. O projeto segue nas frentes não dependentes, sem considerar a ativação concluída.";

/** Detail-page variant from UX-R1 operational language guide §7. */
export const OPERATIONAL_DEBT_DETAIL_WORDING =
  "Há um débito técnico-operacional aceito e registrado: HOST_DISCOVERY=DEFERRED. O agendamento automático permanece BLOCKED. As frentes não dependentes podem avançar; a ativação não está concluída.";

export const VM_FIELD_ABSENT_DISCLOSURE =
  "Campo ausente do HostSchedulerViewModel — permanece indisponível (não inventado).";

export type HostSchedulerScreenData = {
  fixtureId: FixtureScenarioId;
  metadata: FixtureMetadata;
  hostScheduler: HostSchedulerViewModel;
  nowIso: string;
};

/**
 * Product route always uses HOST_SCHEDULER_FIXTURE_ID.
 * Tests may pass another catalog id to cover required scenarios.
 */
export function loadHostSchedulerScreenData(
  fixtureId: FixtureScenarioId = HOST_SCHEDULER_FIXTURE_ID,
): HostSchedulerScreenData {
  const packed: FixtureViewModels = buildFixtureViewModels(fixtureId);
  return {
    fixtureId,
    metadata: packed.metadata,
    hostScheduler: packed.hostScheduler,
    nowIso: packed.nowIso,
  };
}
