#!/usr/bin/env bash
# .claude/hooks/format-python.sh
#
# Purpose
#   PostToolUse hook for the Edit / Write tools. Auto-formats Python files Claude
#   just touched so the diff stays clean and consistent.
#   Best-effort: formatter failure should never block the tool call.
#
# When you want a file like this
#   Any project with a Python formatter. Removes "did Claude reformat
#   correctly?" review noise from PRs.
#
# Why it matters
#   - Catches the small "the formatter would have fixed that" diffs at the
#     moment of writing, not at PR review time.
#   - Best-effort: a missing formatter doesn't stop work; it just logs and moves on.
#
# What goes in it
#   - jq extraction of `.tool_input.file_path` from stdin JSON.
#   - Early exit when path is empty or doesn't exist.
#   - For `*.py`: run ruff --fix then black, each guarded by `command -v` so
#     missing tools degrade gracefully.
#   - Always `exit 0`.
#
# Example (commented; uncomment + edit; remember to chmod +x)
#
# set -uo pipefail
# INPUT="$(cat)"
# FILE="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // empty')"
# [ -z "$FILE" ] || [ ! -f "$FILE" ] && exit 0
# case "$FILE" in
#   *.py)
#     command -v ruff  >/dev/null && ruff check --fix --quiet "$FILE" || true
#     command -v black >/dev/null && black --quiet "$FILE"            || true
#     ;;
# esac
# exit 0
