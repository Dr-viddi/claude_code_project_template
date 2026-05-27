#!/usr/bin/env bash
# .claude/hooks/validate-bash.sh
#
# Intention:
#   PreToolUse hook for the Bash tool. Receives a JSON payload on stdin describing
#   the bash command Claude is about to run, and decides whether to let it through.
#   Exit 0 = allow; exit non-zero = block (and stderr is shown to the model).
#
# What this script should contain:
#   - `jq` extraction of `.tool_input.command` from the stdin JSON.
#   - A `deny` helper that prints a short reason and exits non-zero.
#   - A list of patterns to reject. Suggested starting set:
#       * `rm -rf /` and `rm -rf /*`
#       * `git push --force` / `git push -f`
#       * `git reset --hard`
#       * piping curl/wget into `sh` or `bash`
#       * `chmod 777`
#       * `--no-verify` (hook bypass)
#   - Exit 0 at the bottom so anything not denied is allowed.
#
# Example (commented; remove the leading '#' to activate):
#
# set -euo pipefail
# INPUT="$(cat)"
# CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"
# [[ -z "$CMD" ]] && exit 0
# deny() { echo "Blocked: $1" >&2; exit 1; }
# case "$CMD" in
#   *"rm -rf /"*)           deny "rm -rf on root" ;;
#   *"git push --force"*)   deny "force push" ;;
#   *"--no-verify"*)        deny "hook bypass" ;;
# esac
# exit 0
