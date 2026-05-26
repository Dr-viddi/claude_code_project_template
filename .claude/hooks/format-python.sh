#!/usr/bin/env bash
# PostToolUse hook for Edit/Write. Formats Python files after Claude modifies them.
# Best-effort: failure to format does not block the tool call.

set -uo pipefail

INPUT="$(cat)"
FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')"

if [[ -z "$FILE" || ! -f "$FILE" ]]; then
  exit 0
fi

case "$FILE" in
  *.py)
    if command -v ruff >/dev/null 2>&1; then
      ruff check --fix --quiet "$FILE" || true
    fi
    if command -v black >/dev/null 2>&1; then
      black --quiet "$FILE" || true
    fi
    ;;
esac

exit 0
