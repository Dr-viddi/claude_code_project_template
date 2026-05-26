#!/usr/bin/env bash
# PreToolUse hook for Bash. Blocks dangerous patterns before they execute.
# Exit 0 = allow, exit 1 = block (and stderr is shown to the model).

set -euo pipefail

# stdin is a JSON payload from Claude Code. We pull the command out with jq.
INPUT="$(cat)"
CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"

if [[ -z "$CMD" ]]; then
  exit 0
fi

deny() {
  echo "Blocked by validate-bash.sh: $1" >&2
  exit 1
}

# Patterns we never want to see in this repo.
case "$CMD" in
  *"rm -rf /"*|*"rm -rf /*"*)            deny "rm -rf on root" ;;
  *"git push --force"*|*"git push -f "*) deny "force push - rerun with explicit user approval" ;;
  *"git reset --hard"*)                  deny "destructive reset - confirm with user first" ;;
  *"curl "*"| sh"*|*"curl "*"| bash"*)   deny "piping curl into a shell" ;;
  *"chmod 777"*)                         deny "world-writable permissions" ;;
  *"--no-verify"*)                       deny "bypassing git hooks" ;;
esac

exit 0
