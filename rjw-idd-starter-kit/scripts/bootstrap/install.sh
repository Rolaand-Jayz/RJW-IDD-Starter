#!/usr/bin/env bash
# Bootstrap installer that captures telemetry consent before instrumentation runs.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"

DECISION="${RJW_CONSENT_DECISION:-}"
OPERATOR="${RJW_OPERATOR:-}"
REASON="${RJW_CONSENT_REASON:-bootstrap-install}"
STORE="${RJW_CONSENT_STORE:-${ROOT_DIR}/../artifacts/telemetry/consent.json}"
FORCE_FLAG="${RJW_CONSENT_FORCE:-}"

CMD=("${PYTHON_BIN}" -m tools.telemetry.install_prompt --store "${STORE}" --reason "${REASON}")

if [[ -n "${OPERATOR}" ]]; then
  CMD+=(--operator "${OPERATOR}")
fi

if [[ -n "${FORCE_FLAG}" ]]; then
  CMD+=(--force)
fi

if [[ -n "${DECISION}" ]]; then
  if [[ -z "${OPERATOR}" ]]; then
    echo "RJW_OPERATOR must be provided when RJW_CONSENT_DECISION is set" >&2
    exit 2
  fi
  CMD+=(--decision "${DECISION}")
fi

PYTHONPATH="${ROOT_DIR}/.." "${CMD[@]}"
