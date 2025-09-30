#!/usr/bin/env bash
# Reset sandboxed agent session: revoke temp credentials, tear down namespace, capture audit log.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

TOKEN_ROOT="${RJW_SANDBOX_TOKEN_DIR:-}"
NETNS_PATH="${RJW_SANDBOX_NETNS_PATH:-}"
SESSION_ID="${RJW_SANDBOX_SESSION_ID:-}"
AUDIT_LOG="${RJW_SANDBOX_AUDIT_LOG:-${ROOT_DIR}/../logs/security/sandbox-reset.log}"

if [[ -z "${SESSION_ID}" ]]; then
  echo "RJW_SANDBOX_SESSION_ID is required" >&2
  exit 2
fi

if [[ -z "${TOKEN_ROOT}" ]]; then
  echo "RJW_SANDBOX_TOKEN_DIR is required" >&2
  exit 2
fi

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

revoke_tokens() {
  if [[ ! -d "${TOKEN_ROOT}" ]]; then
    echo "Token directory '${TOKEN_ROOT}' missing" >&2
    return 1
  fi

  local revoked=0
  while IFS= read -r -d '' file; do
    : >"${file}" && rm -f "${file}"
    revoked=$((revoked + 1))
  done < <(find "${TOKEN_ROOT}" -type f -print0)

  rm -rf "${TOKEN_ROOT}"
  echo "revoked=${revoked}"
}

teardown_namespace() {
  if [[ -z "${NETNS_PATH}" ]]; then
    echo "skip_netns"
    return 0
  fi

  if [[ -e "${NETNS_PATH}" ]]; then
    rm -f "${NETNS_PATH}"
    echo "netns_removed"
  else
    echo "netns_missing"
  fi
}

log_audit() {
  local status="$1"
  local detail="$2"
  mkdir -p "$(dirname "${AUDIT_LOG}")"
  {
    printf "%s session=%s status=%s detail=%s evidence=%s\n" \
      "$(timestamp)" \
      "${SESSION_ID}" \
      "${status}" \
      "${detail}" \
      "<evidence-ids>"
  } >>"${AUDIT_LOG}"
}

main() {
  revoke_output="$(revoke_tokens)" || {
    log_audit "failure" "token_revoke"
    echo "Failed to revoke tokens" >&2
    exit 1
  }

  netns_output="$(teardown_namespace)"

  log_audit "success" "${revoke_output};${netns_output}"
  printf "Sandbox reset complete for session %s\n" "${SESSION_ID}"
}

main "$@"
