# agent/prompts/system.py
#
# Intention:
#   The agent's base system prompts - role, persona, hard rules, tool-use policy,
#   refusal policy. Versioned and immutable: changing a prompt means adding a new
#   version, never mutating an existing one, so evals can compare versions.
#
# What this file should contain:
#   - A frozen `SystemPrompt` dataclass: `name`, `version`, `text`.
#   - One module-level constant per system prompt, named UPPER_SNAKE.
#   - A small accessor (or reuse the registry pattern) to fetch the "latest" or a
#     pinned version at runtime.
#   - No I/O, no LLM calls - this file just declares strings.
#
# Example (commented):
#
#   @dataclass(frozen=True)
#   class SystemPrompt:
#       name: str
#       version: str
#       text: str
#
#   AGENT_BASE = SystemPrompt(
#       name="agent_base",
#       version="v1",
#       text=(
#           "You are a task-completing agent. Use tools when they help. "
#           "Never invent tool results. Refuse out-of-scope requests."
#       ),
#   )
