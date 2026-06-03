# agent/prompts/system.py
#
# Purpose
#   The agent's base system prompts - role, persona, hard rules, tool-use policy,
#   refusal policy. Versioned and immutable: changing a prompt means adding a new
#   version, never mutating an existing one, so evals can compare versions.
#
# When you want a file like this
#   Any agent (or LLM-using service) with more than a one-off prompt. The minute
#   you have two prompts you also have prompt versioning - whether you wanted to
#   or not.
#
# Why it matters
#   - Immutable versions + a registry let you A/B test new prompts behind a flag.
#   - The golden-set eval can score answers from each version side-by-side,
#     turning "this prompt is better" into a number.
#   - Co-locating system prompts here is the obvious place to enforce a
#     consistent voice / refusal policy across every intent.
#
# What goes in it
#   - A frozen `SystemPrompt` dataclass: `name`, `version`, `text`.
#   - One module-level constant per system prompt, named UPPER_SNAKE.
#   - A `get_system(name, version="latest")` accessor (or reuse the registry
#     pattern from templates.py).
#   - No I/O, no LLM calls - this file just declares strings.
#
# Example (commented)
#
#   @dataclass(frozen=True)
#   class SystemPrompt:
#       name: str
#       version: str
#       text: str
#
#   AGENT_BASE_V1 = SystemPrompt(
#       name="agent_base",
#       version="v1",
#       text=(
#           "You are a task-completing assistant. Use a tool only when it helps. "
#           "Never invent tool results. Refuse out-of-scope requests."
#       ),
#   )
