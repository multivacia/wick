/**
 * Stable operational reason codes (technical). User-facing text is separate.
 */

export const REASON_CODES = [
  "WINDOW_DAYS_INSUFFICIENT",
  "HOST_DISCOVERY_DEFERRED",
  "SCHEDULER_NOT_REGISTERED",
  "SCHEDULER_BLOCKED",
  "ACTIVATION_NOT_AUTHORIZED",
  "DATA_UNAVAILABLE",
  "LAST_RUN_FAILED",
  "EVIDENCE_MISSING",
  "UNKNOWN_STATE",
] as const;

export type ReasonCode = (typeof REASON_CODES)[number];

const REASON_PLAIN_LANGUAGE: Record<ReasonCode, string> = {
  WINDOW_DAYS_INSUFFICIENT:
    "A janela futura observada ainda é insuficiente para prontidão.",
  HOST_DISCOVERY_DEFERRED: "A descoberta de host permanece adiada.",
  SCHEDULER_NOT_REGISTERED: "O agendador ainda não está registrado.",
  SCHEDULER_BLOCKED: "A ativação do agendador permanece bloqueada.",
  ACTIVATION_NOT_AUTHORIZED:
    "Não há autorização separada para ativar o agendador.",
  DATA_UNAVAILABLE: "Dados operacionais necessários não estão disponíveis.",
  LAST_RUN_FAILED: "A última execução registrada falhou.",
  EVIDENCE_MISSING: "Evidência técnica não foi fornecida.",
  UNKNOWN_STATE: "O estado operacional não pôde ser determinado.",
};

export function explainReasonCode(code: ReasonCode): string {
  return REASON_PLAIN_LANGUAGE[code];
}
