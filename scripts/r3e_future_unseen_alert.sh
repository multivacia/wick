#!/usr/bin/env bash
# Email alert adapter for collector exit codes / readiness transitions.
# Does NOT run validate. Does NOT log secret values.
# EMAIL_TRANSPORT_STATUS may remain PENDING_CONFIGURATION until SMTP/mail is set.
set -euo pipefail

ALERT_EMAIL="${ALERT_EMAIL:-}"
EMAIL_TRANSPORT="${EMAIL_TRANSPORT:-mail}"
SUBJECT_PREFIX="${ALERT_SUBJECT_PREFIX:-[wick-r3e-collector]}"
EXIT_CODE="${1:-}"
STATUS_TEXT="${2:-UNKNOWN}"
DETAIL="${3:-}"

log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >&2; }

should_alert() {
  case "${STATUS_TEXT}" in
    FAILED|BLOCKED|READY_TRANSITION|SKIPPED_LOCKED_REPEATED) return 0 ;;
    *) return 1 ;;
  esac
}

if [[ -z "${EXIT_CODE}" ]]; then
  log "USAGE: $0 <exit_code> <STATUS> [detail]"
  exit 2
fi

if ! should_alert; then
  log "NO_ALERT status=${STATUS_TEXT} exit=${EXIT_CODE}"
  exit 0
fi

if [[ -z "${ALERT_EMAIL}" ]]; then
  log "EMAIL_TRANSPORT_STATUS=PENDING_CONFIGURATION reason=ALERT_EMAIL_unset status=${STATUS_TEXT}"
  exit 0
fi

BODY="host=$(hostname -f 2>/dev/null || hostname)
time_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)
exit_code=${EXIT_CODE}
status=${STATUS_TEXT}
detail=${DETAIL}
action=human_review_required
validate_authorized=false
"

SUBJECT="${SUBJECT_PREFIX} ${STATUS_TEXT} exit=${EXIT_CODE}"

case "${EMAIL_TRANSPORT}" in
  mail|sendmail)
    if command -v mail >/dev/null 2>&1; then
      printf '%s\n' "${BODY}" | mail -s "${SUBJECT}" "${ALERT_EMAIL}"
      log "ALERT_SENT transport=mail to=${ALERT_EMAIL} status=${STATUS_TEXT}"
      exit 0
    fi
    if [[ -x /usr/sbin/sendmail ]]; then
      {
        printf 'To: %s\n' "${ALERT_EMAIL}"
        printf 'Subject: %s\n' "${SUBJECT}"
        printf '\n'
        printf '%s\n' "${BODY}"
      } | /usr/sbin/sendmail -t
      log "ALERT_SENT transport=sendmail to=${ALERT_EMAIL} status=${STATUS_TEXT}"
      exit 0
    fi
    log "EMAIL_TRANSPORT_STATUS=PENDING_CONFIGURATION reason=mail_binary_missing"
    exit 0
    ;;
  smtp)
    log "EMAIL_TRANSPORT_STATUS=PENDING_CONFIGURATION reason=smtp_adapter_not_bundled_use_mail_or_external_relay"
    exit 0
    ;;
  *)
    log "EMAIL_TRANSPORT_STATUS=PENDING_CONFIGURATION reason=unknown_transport:${EMAIL_TRANSPORT}"
    exit 0
    ;;
esac
