#!/usr/bin/env bash
# PreToolUse hook for the Bash tool. Reads the tool-call JSON on stdin and blocks
# dangerous commands before they run. Exit 0 = allow; exit non-zero = block (stderr
# is shown to the model). Wired in .claude/settings.json.
set -euo pipefail

INPUT="$(cat)"

if command -v jq >/dev/null 2>&1; then
  CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"
else
  # Fallback if jq is missing: scan the raw payload.
  CMD="$INPUT"
fi

[ -z "$CMD" ] && exit 0

deny() { echo "Blocked by validate-bash.sh: $1" >&2; exit 2; }

case "$CMD" in
  *"rm -rf /"*)                         deny "rm -rf on root" ;;
  *"git push --force"*|*"git push -f "*) deny "force push - rerun only with explicit approval" ;;
  *"git reset --hard"*)                 deny "destructive reset - confirm first" ;;
  *"curl "*"| sh"*|*"curl "*"| bash"*)  deny "piping curl into a shell" ;;
  *"chmod 777"*)                        deny "world-writable permissions" ;;
  *"--no-verify"*)                      deny "bypassing git hooks" ;;
esac

exit 0
