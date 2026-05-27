#!/usr/bin/env bash
# .claude/hooks/format-python.sh
#
# Intention:
#   PostToolUse hook for the Edit / Write tools. Auto-formats Python files after
#   Claude modifies them so the diff stays clean and consistent.
#   Best-effort: formatter failure should not block the tool call.
#
# What this script should contain:
#   - `jq` extraction of `.tool_input.file_path` from the stdin JSON.
#   - Early exit when the path is empty or doesn't exist.
#   - For `*.py`: run `ruff check --fix --quiet` then `black --quiet`,
#     each guarded by a `command -v` check so missing tools don't break it.
#   - Always `exit 0`.
#
# Example (commented; remove the leading '#' to activate):
#
# set -uo pipefail
# INPUT="$(cat)"
# FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')"
# [[ -z "$FILE" || ! -f "$FILE" ]] && exit 0
# case "$FILE" in
#   *.py)
#     command -v ruff  >/dev/null && ruff check --fix --quiet "$FILE" || true
#     command -v black >/dev/null && black --quiet "$FILE"            || true
#     ;;
# esac
# exit 0
