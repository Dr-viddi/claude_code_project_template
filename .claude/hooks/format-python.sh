#!/usr/bin/env bash
# PostToolUse hook for Edit/Write. Auto-formats Python files Claude just touched so
# the diff stays clean. Best-effort: a formatter failure never blocks the tool call.
set -uo pipefail

INPUT="$(cat)"

if command -v jq >/dev/null 2>&1; then
  FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')"
else
  exit 0
fi

[ -z "$FILE" ] || [ ! -f "$FILE" ] && exit 0

case "$FILE" in
  *.py)
    command -v ruff  >/dev/null 2>&1 && ruff check --fix --quiet "$FILE" || true
    command -v black >/dev/null 2>&1 && black --quiet "$FILE"            || true
    ;;
esac

exit 0
