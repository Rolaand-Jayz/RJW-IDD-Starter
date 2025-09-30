#!/usr/bin/env bash
# CI guard ensuring code changes ship alongside tests per RJW-IDD policy.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
BASE_REF="${RJW_BASE_REF:-origin/main}"
HEAD_REF="${RJW_HEAD_REF:-HEAD}"

mapfile -t CHANGED_FILES < <(cd "${ROOT_DIR}" && git diff --name-only "${BASE_REF}" "${HEAD_REF}")

if [[ "${#CHANGED_FILES[@]}" -eq 0 ]]; then
  echo "red-green guard: no changes detected, skipping"
  exit 0
fi

"${PYTHON_BIN}" "${ROOT_DIR}/tools/testing/red_green_guard.py" --root "${ROOT_DIR}" --files "${CHANGED_FILES[@]}"

# Enforce Spec-Driven Development gate: ledgers, IDs, and change log references stay in sync.
"${PYTHON_BIN}" "${ROOT_DIR}/scripts/validate_ids.py"

# Decide whether evidence freshness needs validation and apply stricter recency controls.
NEEDS_EVIDENCE_CHECK=0
for path in "${CHANGED_FILES[@]}"; do
  case "${path}" in
    research/*|scripts/validate_evidence.py|tools/rjw_idd_evidence_harvester.py)
      NEEDS_EVIDENCE_CHECK=1
      break
      ;;
  esac
done

if [[ "${NEEDS_EVIDENCE_CHECK}" -eq 1 ]]; then
  "${PYTHON_BIN}" "${ROOT_DIR}/scripts/validate_evidence.py" \
    --input "${ROOT_DIR}/research/evidence_index.json" \
    --raw "${ROOT_DIR}/research/evidence_index_raw.json" \
    --cutoff-days 14 \
    --fail-on-warning
fi

# Enforce Living Documentation Driven Development by requiring a change-log entry and cleared doc gaps.
"${PYTHON_BIN}" "${ROOT_DIR}/tools/testing/change_log_guard.py" \
  --root "${ROOT_DIR}" \
  --files "${CHANGED_FILES[@]}"

"${PYTHON_BIN}" "${ROOT_DIR}/tools/testing/living_docs_guard.py" \
  --root "${ROOT_DIR}" \
  --files "${CHANGED_FILES[@]}" \
  --fail-on-placeholder

# Ensure specs, ledgers, and decision logs stay aligned with governed changes.
"${PYTHON_BIN}" "${ROOT_DIR}/tools/testing/governance_alignment_guard.py" \
  --root "${ROOT_DIR}" \
  --files "${CHANGED_FILES[@]}"
