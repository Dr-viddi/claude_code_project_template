#!/usr/bin/env bash
# .claude/hooks/validate-bash.sh
#
# Purpose
#   PreToolUse hook for the Bash tool. Receives a JSON payload on stdin
#   describing the bash command Claude Code is about to run, and decides whether
#   to let it through. Exit 0 = allow; exit non-zero = block (stderr is shown
#   to the model). Wired in .claude/settings.json.
#
# When you want a file like this
#   Any project where Claude Code might run destructive shell commands. That's
#   most of them.
#
# Why it matters
#   - Hooks are DETERMINISTIC. Unlike LLM-side rules ("don't run rm -rf"),
#     hooks can't be hallucinated past. The shell exit code is the contract.
#   - One file blocks the categories of damage that get junior incident reviews
#     started: rm -rf /, force push, hard reset, curl|sh, hook bypass.
#
# What goes in it
#   - jq extraction of `.tool_input.command` from the stdin JSON.
#   - A `deny` helper that prints a short reason and exits non-zero.
#   - A list of patterns to reject. Suggested baseline:
#       * rm -rf / and rm -rf /*
#       * git push --force / -f
#       * git reset --hard
#       * piping curl/wget into sh or bash
#       * chmod 777
#       * --no-verify (hook bypass)
#   - Exit 0 at the bottom so anything not denied is allowed.
#
# Example (commented; uncomment + edit; remember to chmod +x)
#
# set -euo pipefail
# INPUT="$(cat)"
# CMD="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty')"
# [ -z "$CMD" ] && exit 0
# deny() { echo "Blocked: $1" >&2; exit 2; }
# case "$CMD" in
#   *"rm -rf /"*)                          deny "rm -rf on root" ;;
#   *"git push --force"*|*"git push -f "*) deny "force push" ;;
#   *"git reset --hard"*)                  deny "destructive reset" ;;
#   *"curl "*"| sh"*|*"curl "*"| bash"*)   deny "piping curl into a shell" ;;
#   *"chmod 777"*)                         deny "world-writable permissions" ;;
#   *"--no-verify"*)                       deny "bypassing git hooks" ;;
# esac
# exit 0
