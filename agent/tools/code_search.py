# agent/tools/code_search.py
#
# Purpose
#   Repository code search tool, typically backed by ripgrep locally and/or an
#   MCP server for remote repos. Useful for developer-assistant agents.
#
# When you want a file like this
#   Any agent that answers "where is X defined?" / "find all references to Y" /
#   "show me the call sites of Z" - PR review bots, doc generators, refactor
#   assistants.
#
# Why it matters
#   - Local ripgrep gives sub-second results without an LLM call - cheap context.
#   - A path-traversal guard is critical: without one, an LLM-supplied pattern
#     could read files outside the repo. This is a common AI-tool CVE class.
#   - Falling back to a pure-Python search when ripgrep is missing keeps the
#     tool portable (e.g. container without rg installed).
#
# What goes in it
#   - A `CodeSearchTool` class with:
#       * `name = "code_search"` and a `description`.
#       * Constructor taking the repo root path or an MCP client handle.
#       * Async `__call__(pattern, k=10)` returning matches
#         (`{file, line, snippet}`).
#   - Path-traversal guard: refuse paths/patterns that escape the configured root.
#   - Bounded result count.
#
# Example (commented)
#
#   class CodeSearchTool:
#       name = "code_search"
#       description = "Search source code for symbols, references, or text patterns."
#       def __init__(self, repo_root: str): ...
#       async def __call__(self, pattern: str, k: int = 10) -> list[dict]: ...
